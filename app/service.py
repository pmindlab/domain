from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path

from .config import settings
from .db import Store
from .models import Candidate
from .niche_catalog import NicheCatalog, NicheDefinition
from .scoring import PreferenceProfile, apply_collision_penalty, score_name, valid_candidate
from .providers import GBIFProvider, VerisignRdapProvider, BrandScreenProvider, TaxonHit, LanguageProvider, LanguageHit


class NameLabService:
    def __init__(self):
        self.store = Store(settings.db_path)
        self.base_profile = PreferenceProfile.from_file(settings.profile_path)
        self.profile = self.base_profile
        self.gbif = GBIFProvider(settings.http_timeout)
        self.domain = VerisignRdapProvider(settings.http_timeout, settings.max_concurrency)
        self.brand = BrandScreenProvider(settings.github_token, settings.brave_key, settings.http_timeout)
        self.seed_path = Path(settings.profile_path).parent / "seed_taxa.json"
        self.catalog = NicheCatalog(settings.niches_path, settings.custom_niches_path)
        self.language = LanguageProvider(Path(settings.profile_path).parent / "language_words.json")

    def list_niches(self) -> list[dict]:
        stats = self.store.niche_stats()
        out: list[dict] = []
        for niche in self.catalog.list():
            row = niche.to_dict()
            row["stats"] = stats.get(niche.key)
            out.append(row)
        return out

    def list_languages(self) -> list[dict]:
        return self.language.list_languages()

    async def add_custom_niche(self, taxon: str, label: str, group: str = "Custom") -> dict:
        taxon = taxon.strip()
        label = label.strip() or taxon
        if not taxon:
            raise ValueError("Podaj nazwę taksonu, np. Alcedinidae")
        match = await self.gbif.match_taxon(taxon)
        if not match.get("key"):
            raise ValueError(f"GBIF nie rozpoznał taksonu: {taxon}")
        canonical = str(match.get("canonical_name") or taxon)
        niche = self.catalog.add_custom(
            taxon=canonical,
            label=label,
            group=group or "Custom",
            description=f"Custom GBIF area · {match.get('rank') or 'taxon'}",
        )
        result = niche.to_dict()
        result["match"] = match
        return result

    def remove_custom_niche(self, key: str) -> bool:
        niche = self.catalog.get(key)
        if not niche or not niche.custom:
            return False
        removed = self.catalog.remove_custom(key)
        if removed:
            self.store.delete_niche_stats(key)
        return removed

    def _load_seed(self, selected_keys: list[str]) -> list[TaxonHit]:
        if not self.seed_path.exists():
            return []
        data = json.loads(self.seed_path.read_text(encoding="utf-8"))
        out: list[TaxonHit] = []
        for key in selected_keys:
            niche_def = self.catalog.get(key)
            label = niche_def.label if niche_def else key
            for name in data.get(key, []):
                out.append(TaxonHit(name=name, niche=label, key=None, source="seed"))
        return out

    async def discover(self, selected_keys: list[str], per_niche: int, language_keys: list[str] | None = None) -> tuple[list[TaxonHit | LanguageHit], list[str]]:
        warnings: list[str] = []
        tasks: list[tuple[str, asyncio.Task]] = []
        valid_defs: list[NicheDefinition] = []
        for key in selected_keys:
            niche = self.catalog.get(key)
            if not niche:
                warnings.append(f"Nieznana nisza: {key}")
                continue
            valid_defs.append(niche)
            tasks.append((key, asyncio.create_task(
                self.gbif.genera_for_niche(niche.taxon, niche.label, per_niche)
            )))

        hits: list[TaxonHit] = []
        for key, task in tasks:
            try:
                hits.extend(await task)
            except Exception as exc:
                warnings.append(f"GBIF {key}: {type(exc).__name__}; użyto seed fallback, jeśli istnieje")

        hits.extend(self._load_seed([n.key for n in valid_defs]))
        language_hits, language_warnings = self.language.discover(language_keys or [], per_niche)
        hits.extend(language_hits)
        warnings.extend(language_warnings)
        dedup: dict[str, TaxonHit | LanguageHit] = {}
        for h in hits:
            dedup.setdefault(h.name.lower(), h)
        return list(dedup.values()), warnings

    def _refresh_profile(self) -> None:
        base = json.loads(Path(settings.profile_path).read_text(encoding="utf-8"))
        likes = list(base.get("likes", []))
        rejects = list(base.get("rejects", []))
        likes.extend([x.get("name", "") for x in self.store.list("shortlist")])
        likes.extend([x.get("name", "") for x in self.store.list("radar")])
        rejects.extend([x.get("name", "") for x in self.store.list("reject")])
        self.profile = PreferenceProfile([x for x in likes if x], [x for x in rejects if x])

    def _known_names(self) -> set[str]:
        base_data = json.loads(Path(settings.profile_path).read_text(encoding="utf-8"))
        known = {x.lower() for x in (base_data.get("likes", []) + base_data.get("rejects", []))}
        known.update(x.get("name", "").lower() for x in self.store.list("all"))
        known.discard("")
        return known

    async def _screen_available(self, candidates: list[Candidate], brand_checks: int) -> list[Candidate]:
        candidates.sort(key=lambda c: c.score, reverse=True)
        for c in candidates[:max(0, brand_checks)]:
            br = await self.brand.screen(c.name)
            c.brand_status = br.status
            c.github_hits = br.github_hits
            c.web_hits = br.web_hits
            c.score = apply_collision_penalty(c.score, br.status)
            c.reasons.extend(br.notes)
        for c in candidates[max(0, brand_checks):]:
            c.brand_status = "unchecked"
        candidates.sort(key=lambda c: c.score, reverse=True)
        self.store.upsert_many(candidates)
        return candidates

    async def run_search(
        self,
        selected_keys: list[str],
        min_len: int = 5,
        max_len: int = 9,
        per_niche: int = 120,
        domain_checks: int = 50,
        brand_checks: int = 12,
        min_score: float = 55.0,
        language_keys: list[str] | None = None,
    ) -> dict:
        self._refresh_profile()
        discovered, warnings = await self.discover(selected_keys, per_niche, language_keys or [])
        known_names = self._known_names()
        known_skipped = 0

        scored: list[Candidate] = []
        for hit in discovered:
            name = hit.name.strip().lower()
            if name in known_names:
                known_skipped += 1
                continue
            if not valid_candidate(name, min_len, max_len):
                continue
            score, components, reasons = score_name(name, hit.niche, self.profile)
            if isinstance(hit, LanguageHit):
                detail = f"real word · {hit.niche}"
                if hit.meaning:
                    detail += f" · {hit.meaning}"
                reasons.insert(0, detail)
                if hit.key:
                    reasons.insert(1, f"original spelling: {hit.key}")
            if score < min_score:
                continue
            scored.append(Candidate(
                name=name.capitalize(), domain=f"{name}.com", niche=hit.niche,
                source=hit.source, taxon_key=hit.key, score=score,
                components=components, reasons=reasons,
                acquisition_mode="available_now",
            ))

        scored.sort(key=lambda c: c.score, reverse=True)
        to_check = scored[:max(1, domain_checks)]
        domain_results = await self.domain.check_many([c.domain for c in to_check])
        for c in to_check:
            dr = domain_results.get(c.domain.lower())
            c.domain_status = dr.status if dr else "unknown"

        available = [c for c in to_check if c.domain_status == "available"]
        available = await self._screen_available(available, brand_checks)
        return {
            "candidates": [self._with_links(c) for c in available],
            "stats": {
                "discovered": len(discovered),
                "after_brand_filter": len(scored),
                "domain_checked": len(to_check),
                "available": len(available),
                "brand_checked": min(len(available), max(0, brand_checks)),
                "known_skipped": known_skipped,
            },
            "warnings": warnings,
            "availability_note": "Tylko .com dostępne teraz. Domeny z aktywnym rekordem RDAP (aukcja, broker, wygasająca/pending-delete, aftermarket) są odrzucane.",
        }

    async def explore_niches(
        self,
        exclude_keys: list[str] | None = None,
        max_areas: int = 8,
        per_niche: int = 60,
        checks_per_area: int = 12,
        min_score: float = 62.0,
        min_len: int = 5,
        max_len: int = 9,
    ) -> dict:
        self._refresh_profile()
        exclude = set(exclude_keys or [])
        stats = self.store.niche_stats()
        areas = [n for n in self.catalog.list() if n.key not in exclude]
        if not areas:
            return {"areas": [], "note": "Brak nowych obszarów do eksploracji."}

        def explore_order(n: NicheDefinition):
            s = stats.get(n.key) or {}
            return (int(s.get("run_count", 0)), str(s.get("updated_at") or ""), n.group, n.label)

        buckets: dict[str, list[NicheDefinition]] = {}
        for area in sorted(areas, key=explore_order):
            buckets.setdefault(area.group, []).append(area)
        chosen: list[NicheDefinition] = []
        group_names = sorted(buckets)
        target = max(1, max_areas)
        while len(chosen) < target and any(buckets.values()):
            for group in group_names:
                if buckets[group] and len(chosen) < target:
                    chosen.append(buckets[group].pop(0))
        areas = chosen
        known = self._known_names()
        semaphore = asyncio.Semaphore(4)

        async def discover_one(area: NicheDefinition) -> tuple[NicheDefinition, list[TaxonHit], str | None]:
            async with semaphore:
                try:
                    hits = await self.gbif.genera_for_niche(area.taxon, area.label, per_niche)
                    return area, hits, None
                except Exception as exc:
                    return area, [], f"{type(exc).__name__}: {exc}"

        discovered_sets = await asyncio.gather(*(discover_one(a) for a in areas))
        area_candidates: dict[str, list[Candidate]] = {}
        meta: dict[str, dict] = {}
        all_domains: list[str] = []

        for area, hits, error in discovered_sets:
            unique: dict[str, TaxonHit] = {}
            for hit in hits:
                unique.setdefault(hit.name.lower(), hit)
            new_hits = [h for h in unique.values() if h.name.lower() not in known]
            strong: list[Candidate] = []
            for hit in new_hits:
                name = hit.name.strip().lower()
                if not valid_candidate(name, min_len, max_len):
                    continue
                score, components, reasons = score_name(name, area.label, self.profile)
                if score < min_score:
                    continue
                strong.append(Candidate(
                    name=name.capitalize(), domain=f"{name}.com", niche=area.label,
                    source="explore", taxon_key=hit.key, score=score,
                    components=components, reasons=reasons,
                    acquisition_mode="available_now",
                ))
            strong.sort(key=lambda c: c.score, reverse=True)
            checked = strong[:max(1, checks_per_area)]
            area_candidates[area.key] = checked
            all_domains.extend(c.domain for c in checked)
            meta[area.key] = {
                "area": area,
                "error": error,
                "discovered": len(new_hits),
                "strong": len(strong),
            }

        domain_results = await self.domain.check_many(all_domains) if all_domains else {}
        results: list[dict] = []
        for area in areas:
            candidates = area_candidates.get(area.key, [])
            for c in candidates:
                dr = domain_results.get(c.domain.lower())
                c.domain_status = dr.status if dr else "unknown"
            available = [c for c in candidates if c.domain_status == "available"]
            available.sort(key=lambda c: c.score, reverse=True)
            discovered_count = int(meta[area.key]["discovered"])
            strong_count = int(meta[area.key]["strong"])
            checked_count = len(candidates)
            available_count = len(available)
            strong_rate = round((strong_count / discovered_count * 100), 1) if discovered_count else 0.0
            available_rate = round((available_count / checked_count * 100), 1) if checked_count else 0.0
            row = {
                "key": area.key,
                "taxon": area.taxon,
                "label": area.label,
                "group": area.group,
                "custom": area.custom,
                "description": area.description,
                "discovered": discovered_count,
                "strong": strong_count,
                "domain_checked": checked_count,
                "available": available_count,
                "strong_rate": strong_rate,
                "available_rate": available_rate,
                "top_names": [self._with_links(c) for c in available[:4]],
                "error": meta[area.key]["error"],
            }
            self.store.upsert_niche_stats(row)
            results.append(row)

        results.sort(key=lambda r: (r["available"], r["available_rate"], r["strong_rate"]), reverse=True)
        return {
            "areas": results,
            "note": "Explore mierzy scoring + live .com. Nie wykonuje jeszcze pełnego brand screeningu; ten następuje w zwykłym wyszukiwaniu.",
        }

    @staticmethod
    def _extract_dropped_names(raw_text: str) -> list[str]:
        raw = raw_text.lower()
        domains = re.findall(r"(?<![a-z0-9-])([a-z0-9-]+\.com)(?![a-z0-9.-])", raw)
        names: list[str] = []
        if domains:
            names.extend(d[:-4] for d in domains)
        else:
            for token in re.split(r"[\s,;|]+", raw):
                token = token.strip().strip('"\'[](){}<>')
                if not token:
                    continue
                if "." in token:
                    if token.endswith(".com"):
                        token = token[:-4]
                    else:
                        continue
                names.append(token)
        clean: list[str] = []
        seen: set[str] = set()
        for name in names:
            if not re.fullmatch(r"[a-z]+", name):
                continue
            if name not in seen:
                clean.append(name)
                seen.add(name)
        return clean

    async def run_dropped_search(
        self,
        raw_text: str,
        min_len: int = 5,
        max_len: int = 9,
        brand_checks: int = 15,
        min_score: float = 50.0,
        max_checks: int = 250,
    ) -> dict:
        self._refresh_profile()
        parsed = self._extract_dropped_names(raw_text)[:max(1, max_checks)]
        known_names = self._known_names()
        scored: list[Candidate] = []
        known_skipped = 0
        for name in parsed:
            if name in known_names:
                known_skipped += 1
                continue
            if not valid_candidate(name, min_len, max_len):
                continue
            score, components, reasons = score_name(name, "expired/dropped .com", self.profile)
            if score < min_score:
                continue
            reasons.append("from expired/dropped list")
            scored.append(Candidate(
                name=name.capitalize(), domain=f"{name}.com", niche="expired/dropped .com",
                source="dropped_list", score=score, components=components, reasons=reasons,
                acquisition_mode="dropped_available",
            ))

        scored.sort(key=lambda c: c.score, reverse=True)
        domain_results = await self.domain.check_many([c.domain for c in scored]) if scored else {}
        for c in scored:
            dr = domain_results.get(c.domain.lower())
            c.domain_status = dr.status if dr else "unknown"

        released = [c for c in scored if c.domain_status == "available"]
        released = await self._screen_available(released, brand_checks)
        return {
            "candidates": [self._with_links(c) for c in released],
            "stats": {
                "discovered": len(parsed),
                "after_brand_filter": len(scored),
                "domain_checked": len(scored),
                "available": len(released),
                "brand_checked": min(len(released), max(0, brand_checks)),
                "known_skipped": known_skipped,
            },
            "warnings": [],
            "availability_note": "Lista może zawierać expired/pending-delete/aukcje, ale NameLab pokazuje wyłącznie pozycje, które po live RDAP są już naprawdę wolne do rejestracji.",
        }

    def _with_links(self, c: Candidate) -> dict:
        d = c.to_dict()
        d["screen_links"] = self.brand.search_links(c.name)
        return d

    async def check_name(self, name: str, niche: str = "manual") -> dict:
        clean = "".join(ch for ch in name.lower().strip() if ch.isalpha())
        if not valid_candidate(clean, 3, 15):
            raise ValueError("Nazwa musi być jednym słowem, 3–15 liter A–Z")
        self._refresh_profile()
        score, components, reasons = score_name(clean, niche, self.profile)
        c = Candidate(
            name=clean.capitalize(), domain=f"{clean}.com", niche=niche, source="manual",
            score=score, components=components, reasons=reasons, acquisition_mode="manual",
        )
        dr = (await self.domain.check_many([c.domain])).get(c.domain)
        c.domain_status = dr.status if dr else "unknown"
        if c.domain_status == "available":
            br = await self.brand.screen(c.name)
            c.brand_status = br.status
            c.github_hits = br.github_hits
            c.web_hits = br.web_hits
            c.score = apply_collision_penalty(c.score, br.status)
            c.reasons.extend(br.notes)
            self.store.upsert_many([c])
        return self._with_links(c)

    def update_decision(self, name: str, decision: str, note: str = "") -> dict | None:
        if decision not in {"new", "shortlist", "radar", "reject"}:
            raise ValueError("Invalid decision")
        self.store.set_decision(name, decision, note)
        return self.store.get(name)

    def list_saved(self, decision: str | None = None) -> list[dict]:
        return self.store.list(decision)
