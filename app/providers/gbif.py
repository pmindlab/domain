from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class TaxonHit:
    name: str
    niche: str
    key: str | None = None
    source: str = "gbif"


class GBIFProvider:
    BASE = "https://api.gbif.org/v1"

    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout

    async def _get(self, client: httpx.AsyncClient, path: str, params: dict[str, Any]) -> dict:
        r = await client.get(f"{self.BASE}{path}", params=params)
        r.raise_for_status()
        return r.json()

    async def match_taxon(self, taxon_name: str) -> dict:
        headers = {"User-Agent": "NameLab/1.4 taxonomy research"}
        async with httpx.AsyncClient(timeout=self.timeout, headers=headers, follow_redirects=True) as client:
            data = await self._get(client, "/species/match", {"name": taxon_name})
        key = data.get("usageKey") or data.get("nubKey") or data.get("key")
        return {
            "key": int(key) if key else None,
            "scientific_name": data.get("scientificName") or data.get("canonicalName") or taxon_name,
            "canonical_name": data.get("canonicalName") or taxon_name,
            "rank": data.get("rank"),
            "status": data.get("status"),
            "match_type": data.get("matchType"),
            "confidence": data.get("confidence"),
        }

    async def resolve_taxon(self, client: httpx.AsyncClient, taxon_name: str) -> int | None:
        data = await self._get(client, "/species/match", {"name": taxon_name})
        for key_name in ("usageKey", "nubKey", "key"):
            val = data.get(key_name)
            if val:
                try:
                    return int(val)
                except Exception:
                    pass
        return None

    async def genera_for_niche(self, taxon_name: str, label: str, limit: int = 120) -> list[TaxonHit]:
        headers = {"User-Agent": "NameLab/1.4 taxonomy research"}
        async with httpx.AsyncClient(timeout=self.timeout, headers=headers, follow_redirects=True) as client:
            key = await self.resolve_taxon(client, taxon_name)
            if not key:
                return []

            first = await self._get(client, "/species/search", {
                "highertaxon_key": key,
                "rank": "GENUS",
                "status": "ACCEPTED",
                "limit": min(100, max(20, limit)),
                "offset": 0,
            })
            results = list(first.get("results", []))
            count = int(first.get("count", len(results)) or len(results))

            page_size = min(100, max(20, limit))
            pages_needed = max(0, min(4, (limit + page_size - 1) // page_size - 1))
            if count > page_size and pages_needed:
                max_offset = max(0, count - page_size)
                offsets = set()
                rng = random.Random(f"{taxon_name}:{count}:{limit}")
                while len(offsets) < pages_needed:
                    offsets.add(rng.randint(0, max_offset))
                tasks = [
                    self._get(client, "/species/search", {
                        "highertaxon_key": key,
                        "rank": "GENUS",
                        "status": "ACCEPTED",
                        "limit": page_size,
                        "offset": off,
                    }) for off in offsets
                ]
                pages = await asyncio.gather(*tasks, return_exceptions=True)
                for page in pages:
                    if isinstance(page, dict):
                        results.extend(page.get("results", []))

        seen: set[str] = set()
        hits: list[TaxonHit] = []
        for item in results:
            raw = item.get("canonicalName") or item.get("scientificName") or ""
            genus = raw.split()[0].strip() if raw else ""
            if not genus or genus.lower() in seen:
                continue
            seen.add(genus.lower())
            hits.append(TaxonHit(name=genus, niche=label, key=str(item.get("key") or "") or None))
            if len(hits) >= limit:
                break
        return hits
