from __future__ import annotations

import re
from dataclasses import dataclass


NEGATIVE_PARTS = {
    "toxic", "toxin", "virus", "cancer", "tumor", "tumour", "disease", "plague",
    "venom", "morb", "death", "dead", "kill", "fatal", "pest", "rot", "rabies",
    "sepsis", "ulcer", "necros", "poison", "pathogen", "parasite", "hate", "nazi",
    "rape", "porn", "sex", "slut", "shit", "fuck", "crap", "sick", "dumb", "stupid",
    "fraud", "scam", "crime", "war", "bomb", "gun", "blood", "hell", "evil", "curse",
}

DIFFICULT_BOUNDARIES = {"aa", "ii", "uu", "yy", "jj", "qq"}


@dataclass(frozen=True)
class Term:
    word: str
    en: str
    pl: str
    tags: tuple[str, ...]
    role: str = "both"
    tone: str = "neutral"

    def as_dict(self) -> dict:
        return {
            "word": self.word,
            "en": self.en,
            "pl": self.pl,
            "tags": list(self.tags),
            "role": self.role,
            "tone": self.tone,
        }


ROOT_INFO: dict[str, dict] = {
    "lark": {
        "en": "a small songbird; informally, something done for fun or adventure",
        "pl": "skowronek; potocznie także zabawa, figiel lub spontaniczna przygoda",
        "tags": ["bird", "nature", "dawn", "sound", "movement", "light"],
        "tone": "lekki · naturalny · pozytywny · lekko playful",
        "visual": "ptak · świt · lot · śpiew",
    },
    "bird": {
        "en": "a feathered, winged animal",
        "pl": "ptak",
        "tags": ["bird", "nature", "movement", "sound", "light"],
        "tone": "naturalny · lekki · uniwersalny",
        "visual": "lot · pióro · niebo · śpiew",
    },
    "light": {
        "en": "visible illumination; also something not heavy",
        "pl": "światło; także lekki",
        "tags": ["light", "clarity", "design", "movement"],
        "tone": "jasny · czysty · nowoczesny",
        "visual": "promień · blask · kontrast",
    },
    "grain": {
        "en": "a seed or a fine texture/structure",
        "pl": "ziarno; także struktura lub ziarnistość",
        "tags": ["nature", "material", "texture", "craft"],
        "tone": "organiczny · rzemieślniczy · materialny",
        "visual": "ziarno · faktura · materiał",
    },
    "page": {
        "en": "one side of a sheet or a screen/document view",
        "pl": "strona kartki lub dokumentu; także strona internetowa",
        "tags": ["design", "editorial", "clarity", "digital"],
        "tone": "prosty · editorial · cyfrowy",
        "visual": "siatka · typografia · karta",
    },
    "wing": {
        "en": "an organ used for flight; figuratively a side or extension",
        "pl": "skrzydło",
        "tags": ["bird", "movement", "nature", "speed"],
        "tone": "dynamiczny · lekki",
        "visual": "lot · pióro · kierunek",
    },
    "dawn": {
        "en": "the first light of day",
        "pl": "świt",
        "tags": ["dawn", "light", "time", "nature"],
        "tone": "poetycki · świeży · jasny",
        "visual": "świt · horyzont · pierwsze światło",
    },
    "glow": {
        "en": "a steady soft light or radiance",
        "pl": "blask, poświata",
        "tags": ["light", "design", "energy"],
        "tone": "ciepły · świetlisty · nowoczesny",
        "visual": "poświata · światło",
    },
    "swift": {
        "en": "moving very fast; also a type of bird",
        "pl": "szybki; także jerzyk",
        "tags": ["speed", "bird", "movement"],
        "tone": "szybki · dynamiczny",
        "visual": "ruch · lot · kierunek",
    },
}


PARTNERS = [
    Term("dawn", "first light of day", "świt", ("dawn", "light", "time", "nature"), "before", "poetic"),
    Term("silver", "a bright metallic colour/material", "srebro, srebrny", ("color", "material", "light", "premium"), "before", "premium"),
    Term("north", "the northern direction", "północ, północny", ("direction", "nature", "place"), "before", "grounded"),
    Term("wild", "living or growing freely", "dziki, swobodny", ("nature", "freedom", "energy"), "before", "natural"),
    Term("blue", "the colour blue", "niebieski", ("color", "sky", "water", "calm"), "before", "calm"),
    Term("amber", "warm golden-orange colour/resin", "bursztyn, bursztynowy", ("color", "material", "warmth", "premium"), "before", "warm"),
    Term("bright", "full of light; vivid or intelligent", "jasny, świetlisty; bystry", ("light", "clarity", "energy"), "before", "positive"),
    Term("quiet", "making little or no noise", "cichy, spokojny", ("calm", "clarity", "nature"), "before", "calm"),
    Term("clear", "easy to see or understand", "czysty, klarowny", ("clarity", "light", "design"), "before", "clean"),
    Term("first", "coming before all others", "pierwszy", ("time", "dawn", "lead"), "before", "direct"),
    Term("open", "not closed; accessible", "otwarty", ("freedom", "clarity", "digital"), "before", "open"),
    Term("rare", "uncommon or unusual", "rzadki, wyjątkowy", ("premium", "nature", "discovery"), "before", "distinctive"),
    Term("velvet", "a soft fabric with a dense pile", "aksamit", ("material", "texture", "premium", "soft"), "before", "tactile"),
    Term("copper", "a reddish metallic element/material", "miedź, miedziany", ("material", "color", "warmth"), "before", "material"),
    Term("lucid", "clear and easy to understand; bright", "klarowny, przejrzysty", ("clarity", "light", "design"), "before", "clean"),
    Term("vivid", "producing strong, clear impressions", "żywy, wyrazisty", ("color", "energy", "design"), "before", "energetic"),
    Term("swift", "moving very fast", "szybki", ("speed", "movement", "bird"), "before", "dynamic"),
    Term("soft", "not hard or harsh", "miękki, łagodny", ("soft", "calm", "design"), "before", "soft"),
    Term("true", "in accordance with fact; genuine", "prawdziwy, autentyczny", ("clarity", "trust"), "before", "trust"),
    Term("pine", "an evergreen conifer tree", "sosna", ("nature", "forest", "material"), "before", "natural"),
    Term("moss", "a small green non-flowering plant", "mech", ("nature", "forest", "texture"), "before", "organic"),
    Term("reef", "a ridge of rock/coral in the sea", "rafa", ("nature", "water", "place"), "before", "natural"),
    Term("wing", "an organ used for flight", "skrzydło", ("bird", "movement", "speed", "nature"), "after", "dynamic"),
    Term("song", "a short musical composition or singing", "pieśń, śpiew", ("sound", "bird", "emotion"), "after", "expressive"),
    Term("light", "visible illumination", "światło", ("light", "clarity", "design"), "after", "bright"),
    Term("field", "an open area of land; also a domain of activity", "pole; także dziedzina", ("nature", "place", "work"), "after", "grounded"),
    Term("line", "a long narrow mark; a sequence or range", "linia", ("design", "clarity", "direction"), "after", "graphic"),
    Term("rise", "to move upward or begin to appear", "wznosić się, wzrost", ("movement", "dawn", "growth"), "after", "positive"),
    Term("path", "a route or way forward", "ścieżka, droga", ("direction", "movement", "discovery"), "after", "directional"),
    Term("mark", "a visible sign or distinctive symbol", "znak", ("design", "brand", "clarity"), "after", "graphic"),
    Term("form", "shape or structure", "forma, kształt", ("design", "structure", "material"), "after", "design"),
    Term("frame", "a surrounding structure or boundary", "rama", ("design", "structure", "editorial"), "after", "structured"),
    Term("craft", "skill in making things", "rzemiosło, kunszt", ("craft", "material", "work"), "after", "crafted"),
    Term("studio", "a place for creative work", "studio, pracownia", ("design", "work", "creative"), "after", "creative"),
    Term("works", "products or acts of making", "prace, wytwory", ("work", "craft", "creative"), "after", "crafted"),
    Term("space", "an area or room; also outer space", "przestrzeń", ("place", "design", "digital"), "after", "open"),
    Term("wave", "a moving ridge or oscillation", "fala", ("movement", "water", "energy"), "after", "dynamic"),
    Term("flow", "continuous movement", "przepływ", ("movement", "design", "work"), "after", "smooth"),
]

PARTNER_INDEX = {p.word: p for p in PARTNERS}

ROOT_OVERRIDES = {
    "lark": {
        "before": ["dawn", "silver", "north", "wild", "blue", "bright", "swift", "amber"],
        "after": ["wing", "song", "light", "field", "rise", "line", "path", "mark"],
    },
    "bird": {
        "before": ["dawn", "silver", "north", "wild", "blue", "bright", "amber", "swift"],
        "after": ["wing", "song", "light", "field", "path", "rise"],
    },
    "light": {
        "before": ["dawn", "silver", "clear", "soft", "bright", "blue"],
        "after": ["wave", "flow", "line", "field", "form", "works"],
    },
    "grain": {
        "before": ["silver", "wild", "amber", "true", "pine", "clear"],
        "after": ["craft", "works", "studio", "form", "field", "mark"],
    },
    "page": {
        "before": ["clear", "open", "first", "bright", "lucid", "true"],
        "after": ["works", "studio", "flow", "form", "frame", "space"],
    },
}

NICHE_TAGS = {
    "bird": {"bird", "nature", "movement", "sound", "sky"},
    "birds": {"bird", "nature", "movement", "sound", "sky"},
    "humming": {"bird", "nature", "movement", "color", "speed"},
    "butter": {"nature", "movement", "color", "light"},
    "moth": {"nature", "night", "light", "movement"},
    "dragon": {"nature", "movement", "water", "speed"},
    "beetle": {"nature", "material", "color", "texture"},
    "firefl": {"nature", "light", "night"},
    "marine": {"nature", "water", "movement", "color"},
    "coral": {"nature", "water", "color", "structure"},
    "plant": {"nature", "growth", "material"},
    "flower": {"nature", "color", "growth"},
}


def _clean_word(value: str) -> str:
    return re.sub(r"[^a-z]", "", (value or "").lower())


def infer_tags(root: str, niche: str = "") -> set[str]:
    r = _clean_word(root)
    if r in ROOT_INFO:
        tags = set(ROOT_INFO[r]["tags"])
    else:
        tags = set()
    low = f"{r} {niche}".lower()
    for key, values in NICHE_TAGS.items():
        if key in low:
            tags.update(values)
    if not tags:
        tags.update({"clarity", "design", "nature"})
    return tags


def root_info(root: str, niche: str = "") -> dict:
    r = _clean_word(root)
    base = ROOT_INFO.get(r)
    if base:
        return {"word": r, **base}
    tags = sorted(infer_tags(r, niche))
    return {
        "word": r,
        "en": f"No local dictionary entry yet. Source context: {niche or 'custom root'}.",
        "pl": f"Brak lokalnego tłumaczenia. Kontekst źródła: {niche or 'własny rdzeń'}.",
        "tags": tags,
        "tone": "do oceny w warsztacie",
        "visual": " · ".join(tags[:4]),
    }


def _boundary_penalty(left: str, right: str) -> tuple[int, list[str]]:
    penalty = 0
    reasons: list[str] = []
    if not left or not right:
        return 0, reasons
    boundary = left[-1] + right[0]
    if boundary in DIFFICULT_BOUNDARIES:
        penalty += 9
        reasons.append("trudne łączenie liter na granicy słów")
    if left[-1] == right[0]:
        penalty += 6
        reasons.append("powtórzona litera na granicy")
    if len(left) + len(right) > 14:
        penalty += min(14, (len(left) + len(right) - 14) * 2)
        reasons.append("dłuższa domena")
    return penalty, reasons


def _negative_hits(text: str) -> list[str]:
    low = text.lower()
    return sorted({x for x in NEGATIVE_PARTS if x in low})


def analyze_pair(root: str, partner: str, position: str = "before", niche: str = "") -> dict:
    root_clean = _clean_word(root)
    partner_clean = _clean_word(partner)
    if not root_clean or not partner_clean:
        return {"ok": False, "risk": "blocked", "score": 0, "reasons": ["nieprawidłowe słowo"]}
    left, right = (partner_clean, root_clean) if position == "before" else (root_clean, partner_clean)
    joined = left + right
    hits = _negative_hits(joined)
    if hits:
        return {
            "ok": False,
            "risk": "blocked",
            "score": 0,
            "domain": f"{joined}.com",
            "reasons": [f"negatywne znaczenie/rdzeń: {', '.join(hits)}"],
        }

    root_tags = infer_tags(root_clean, niche)
    partner_term = PARTNER_INDEX.get(partner_clean)
    partner_tags = set(partner_term.tags) if partner_term else set()
    overlap = root_tags & partner_tags
    score = 64 + min(24, len(overlap) * 7)
    reasons: list[str] = []
    if overlap:
        reasons.append("zgodność semantyczna: " + ", ".join(sorted(overlap)[:4]))
    else:
        score -= 14
        reasons.append("słabsza zgodność semantyczna")
    penalty, boundary_reasons = _boundary_penalty(left, right)
    score -= penalty
    reasons.extend(boundary_reasons)
    if 8 <= len(joined) <= 12:
        score += 5
        reasons.append("dobra długość dla dwuwyrazowej .com")
    elif len(joined) <= 7:
        score += 3
    risk = "low" if score >= 72 else "review"
    return {
        "ok": True,
        "risk": risk,
        "score": max(0, min(100, score)),
        "domain": f"{joined}.com",
        "joined": joined,
        "position": position,
        "reasons": reasons,
    }


def _term_score(root: str, term: Term, position: str, niche: str) -> int:
    root_tags = infer_tags(root, niche)
    score = 48
    overlap = root_tags & set(term.tags)
    score += min(35, len(overlap) * 10)
    if term.role == position:
        score += 10
    if term.role == "both":
        score += 5
    pair = analyze_pair(root, term.word, position, niche)
    score = int((score + pair.get("score", 0)) / 2)
    return max(0, min(100, score))


def _suggest_side(root: str, niche: str, position: str, limit: int) -> list[dict]:
    clean = _clean_word(root)
    override = ROOT_OVERRIDES.get(clean, {}).get(position, [])
    ordered: list[Term] = []
    seen: set[str] = set()
    for word in override:
        term = PARTNER_INDEX.get(word)
        if term and word != clean:
            ordered.append(term)
            seen.add(word)
    rest = [p for p in PARTNERS if p.word not in seen and p.word != clean and p.role in (position, "both")]
    rest.sort(key=lambda p: _term_score(clean, p, position, niche), reverse=True)
    ordered.extend(rest)
    out: list[dict] = []
    for term in ordered:
        analysis = analyze_pair(clean, term.word, position, niche)
        if not analysis.get("ok"):
            continue
        row = term.as_dict()
        row["score"] = _term_score(clean, term, position, niche)
        row["pair"] = analysis
        out.append(row)
        if len(out) >= limit:
            break
    return out


def workshop(root: str, niche: str = "", limit: int = 8) -> dict:
    clean = _clean_word(root)
    if len(clean) < 2:
        raise ValueError("Podaj rdzeń co najmniej 2-literowy")
    if _negative_hits(clean):
        raise ValueError("Rdzeń ma negatywne znaczenie i nie może być rozwijany")
    return {
        "root": root_info(clean, niche),
        "before": _suggest_side(clean, niche, "before", limit),
        "after": _suggest_side(clean, niche, "after", limit),
        "note": "Sugestie są kuratorowane semantycznie i filtrowane przed sprawdzaniem domeny. Człowiek wybiera kierunek; Mianem nie brute-force'uje tysięcy par.",
    }
