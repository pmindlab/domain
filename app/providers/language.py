from __future__ import annotations

import json
import random
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LanguageHit:
    name: str
    niche: str
    key: str | None = None
    source: str = "language"
    meaning: str = ""


class LanguageProvider:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _data(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    @staticmethod
    def _ascii(text: str) -> str:
        special = str.maketrans({"ł":"l","Ł":"L","đ":"d","Đ":"D","ø":"o","Ø":"O","æ":"ae","Æ":"AE","œ":"oe","Œ":"OE"})
        normalized = unicodedata.normalize("NFKD", text.translate(special))
        return "".join(ch for ch in normalized if not unicodedata.combining(ch) and ord(ch) < 128).lower()

    def list_languages(self) -> list[dict]:
        return [
            {
                "key": key,
                "label": item.get("label", key),
                "description": item.get("description", ""),
                "count": len(item.get("words", [])),
            }
            for key, item in self._data().items()
        ]

    def discover(self, selected_keys: list[str], per_language: int = 120) -> tuple[list[LanguageHit], list[str]]:
        data = self._data()
        hits: list[LanguageHit] = []
        warnings: list[str] = []
        for key in selected_keys:
            item = data.get(key)
            if not item:
                warnings.append(f"Nieznany język: {key}")
                continue
            label = str(item.get("label") or key)
            words = list(item.get("words", []))
            rng = random.Random(f"namelab:{key}:{len(words)}")
            rng.shuffle(words)
            for entry in words[:max(1, per_language)]:
                original = str(entry.get("word") or "").strip()
                ascii_name = str(entry.get("ascii") or self._ascii(original)).strip().lower()
                meaning = str(entry.get("meaning") or "").strip()
                if not ascii_name:
                    continue
                meta = original if original.lower() != ascii_name else None
                hits.append(LanguageHit(
                    name=ascii_name,
                    niche=label,
                    key=meta,
                    source=f"language:{key}",
                    meaning=meaning,
                ))
        dedup: dict[str, LanguageHit] = {}
        for hit in hits:
            dedup.setdefault(hit.name.lower(), hit)
        return list(dedup.values()), warnings
