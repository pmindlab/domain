from __future__ import annotations

import json
import math
import re
from pathlib import Path
from collections import Counter

VOWELS = set("aeiou")
NEGATIVE_ROOTS = {
    "toxin", "toxic", "virus", "cancer", "tumor", "tumour", "disease", "plague",
    "venom", "morb", "death", "dead", "kill", "fatal", "pest", "rot", "fungal",
    "rabies", "sepsis", "ulcer", "necros", "poison", "pathogen", "parasite",
}
DIFFICULT_PATTERNS = {
    "ph": 1.7, "ae": 1.3, "oe": 1.3, "th": 1.0, "rh": 1.4, "ps": 1.6,
    "pt": 1.4, "gn": 1.0, "sch": 2.0, "chth": 3.0, "y": 0.8, "qu": 0.8,
}
SCI_HEAVY = {
    "rhynchus": 5.0, "phorus": 2.8, "opsis": 2.0, "ptera": 1.5, "ichthys": 3.8,
    "gnathus": 4.0, "cerus": 1.3, "somus": 1.0,
}
STARTUPISH = {"neo": 1.4, "meta": 1.2, "tech": 4.0, "labs": 4.0, "ify": 2.0, "ly": 0.7}
VISUAL_NICHE_BONUS = {
    "jewel beetles": 9.0,
    "butterflies": 8.0,
    "moths": 7.0,
    "dragonflies": 8.0,
    "hummingbirds": 8.0,
    "tropical birds": 7.0,
    "nudibranchs": 9.0,
    "bioluminescent": 10.0,
    "lanternfish": 9.0,
    "ctenophores": 8.0,
    "corals": 7.0,
    "hydrozoa": 7.0,
    "marine": 7.0,
    "fireflies": 10.0,
}


def _ngrams(s: str, n: int = 2) -> Counter[str]:
    s = f"^{s.lower()}$"
    return Counter(s[i:i+n] for i in range(len(s)-n+1))


def _cosine(a: Counter[str], b: Counter[str]) -> float:
    keys = set(a) | set(b)
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


class PreferenceProfile:
    def __init__(self, likes: list[str], rejects: list[str]):
        self.likes = [x.lower() for x in likes]
        self.rejects = [x.lower() for x in rejects]
        self.like_grams = [_ngrams(x) for x in self.likes]
        self.reject_grams = [_ngrams(x) for x in self.rejects]

    @classmethod
    def from_file(cls, path: str | Path) -> "PreferenceProfile":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data.get("likes", []), data.get("rejects", []))

    def similarity_score(self, name: str) -> float:
        g = _ngrams(name)
        like = sum(_cosine(g, x) for x in self.like_grams) / max(1, len(self.like_grams))
        reject = sum(_cosine(g, x) for x in self.reject_grams) / max(1, len(self.reject_grams))
        raw = (like - 0.65 * reject)
        return max(0.0, min(10.0, 5.0 + raw * 18.0))


def _max_consonant_cluster(name: str) -> int:
    best = cur = 0
    for ch in name.lower():
        if ch.isalpha() and ch not in VOWELS:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def valid_candidate(name: str, min_len: int = 5, max_len: int = 9) -> bool:
    n = name.strip().lower()
    if not (min_len <= len(n) <= max_len):
        return False
    if not re.fullmatch(r"[a-z]+", n):
        return False
    if any(root in n for root in NEGATIVE_ROOTS):
        return False
    if len(set(n)) < 3:
        return False
    return True


def score_name(name: str, niche: str, profile: PreferenceProfile) -> tuple[float, dict[str, float], list[str]]:
    n = name.lower().strip()
    reasons: list[str] = []

    if 6 <= len(n) <= 8:
        length = 16.0
        reasons.append("idealna długość 6–8")
    elif len(n) in (5, 9):
        length = 11.5
    elif len(n) == 4:
        length = 8.0
    elif len(n) == 3:
        length = 5.0
    else:
        length = max(0.0, 12.0 - abs(7 - len(n)) * 3)

    vowel_ratio = sum(c in VOWELS for c in n) / len(n)
    cluster = _max_consonant_cluster(n)
    pronunciation = 18.0 - abs(vowel_ratio - 0.43) * 24.0 - max(0, cluster - 2) * 3.2
    pronunciation = max(2.0, min(18.0, pronunciation))
    if cluster <= 2:
        reasons.append("lekki rytm bez ciężkich zbitek")

    phone_penalty = 0.0
    for pat, p in DIFFICULT_PATTERNS.items():
        if pat in n:
            phone_penalty += p
    if re.search(r"[aeiou]{3}", n):
        phone_penalty += 2.2
    if "x" in n:
        phone_penalty += 0.35
    phone = max(3.0, 18.0 - phone_penalty)
    if phone >= 15:
        reasons.append("dobry phone test")

    visual = 7.0 + (1.0 if "x" in n else 0.0) + (0.5 if any(c in n for c in "lvtk") else 0.0)
    visual = min(10.0, visual)

    meaning = VISUAL_NICHE_BONUS.get(niche.lower(), 6.0)
    if meaning >= 8:
        reasons.append("mocny motyw wizualny ze źródła")

    brand = 18.0
    for suffix, penalty in SCI_HEAVY.items():
        if n.endswith(suffix):
            brand -= penalty
    for bit, penalty in STARTUPISH.items():
        if n.startswith(bit) or n.endswith(bit):
            brand -= penalty
    if n.count("i") + n.count("a") + n.count("o") >= 3:
        brand += 0.6
    brand = max(5.0, min(19.0, brand))

    preference = profile.similarity_score(n)
    if preference >= 6.2:
        reasons.append("zbliżone do profilu zaakceptowanych nazw")

    total = length + pronunciation + phone + visual + meaning + brand + preference
    total = round(max(0.0, min(100.0, total / 101.0 * 100.0)), 1)
    components = {
        "length": round(length, 1),
        "pronunciation": round(pronunciation, 1),
        "phone_test": round(phone, 1),
        "visual": round(visual, 1),
        "meaning": round(meaning, 1),
        "brand": round(brand, 1),
        "preference": round(preference, 1),
    }
    return total, components, reasons


def apply_collision_penalty(score: float, status: str) -> float:
    if status == "conflict":
        return max(0.0, round(score - 35.0, 1))
    if status == "review":
        return max(0.0, round(score - 10.0, 1))
    return score
