from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class NicheDefinition:
    key: str
    taxon: str
    label: str
    group: str
    default: bool = False
    description: str = ""
    custom: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class NicheCatalog:
    def __init__(self, builtin_path: str | Path, custom_path: str | Path):
        self.builtin_path = Path(builtin_path)
        self.custom_path = Path(custom_path)
        self.custom_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.custom_path.exists():
            self.custom_path.write_text("[]\n", encoding="utf-8")

    @staticmethod
    def _read(path: Path, custom: bool) -> list[NicheDefinition]:
        if not path.exists():
            return []
        raw = json.loads(path.read_text(encoding="utf-8"))
        out: list[NicheDefinition] = []
        for item in raw:
            out.append(NicheDefinition(
                key=str(item["key"]),
                taxon=str(item["taxon"]),
                label=str(item.get("label") or item["taxon"]),
                group=str(item.get("group") or ("Custom" if custom else "Other")),
                default=bool(item.get("default", False)),
                description=str(item.get("description") or ""),
                custom=custom,
            ))
        return out

    def list(self) -> list[NicheDefinition]:
        builtins = self._read(self.builtin_path, False)
        customs = self._read(self.custom_path, True)
        merged: dict[str, NicheDefinition] = {n.key: n for n in builtins}
        for n in customs:
            merged[n.key] = n
        return sorted(merged.values(), key=lambda n: (n.group.lower(), n.label.lower()))

    def get(self, key: str) -> NicheDefinition | None:
        for item in self.list():
            if item.key == key:
                return item
        return None

    def default_keys(self) -> list[str]:
        return [n.key for n in self.list() if n.default]

    @staticmethod
    def _slug(text: str) -> str:
        s = text.lower().strip()
        s = re.sub(r"[^a-z0-9]+", "_", s)
        s = re.sub(r"_+", "_", s).strip("_")
        return s or "custom"

    def add_custom(self, taxon: str, label: str, group: str = "Custom", description: str = "") -> NicheDefinition:
        existing = {n.key for n in self.list()}
        base = self._slug(label or taxon)
        key = f"custom_{base}"
        i = 2
        while key in existing:
            key = f"custom_{base}_{i}"
            i += 1
        niche = NicheDefinition(
            key=key,
            taxon=taxon.strip(),
            label=(label or taxon).strip(),
            group=(group or "Custom").strip(),
            description=description.strip(),
            custom=True,
        )
        current = [n.to_dict() for n in self._read(self.custom_path, True)]
        record = niche.to_dict()
        record.pop("custom", None)
        current.append(record)
        self._atomic_write(current)
        return niche

    def remove_custom(self, key: str) -> bool:
        current = self._read(self.custom_path, True)
        kept = [n for n in current if n.key != key]
        if len(kept) == len(current):
            return False
        records = []
        for niche in kept:
            rec = niche.to_dict()
            rec.pop("custom", None)
            records.append(rec)
        self._atomic_write(records)
        return True

    def _atomic_write(self, payload: list[dict]) -> None:
        tmp = self.custom_path.with_suffix(self.custom_path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.custom_path)
