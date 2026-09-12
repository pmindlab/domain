from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

@dataclass(frozen=True)
class Settings:
    db_path: str = os.getenv("NAMELAB_DB", str(ROOT / "data" / "namelab.db"))
    profile_path: str = os.getenv("NAMELAB_PROFILE", str(ROOT / "data" / "profile.json"))
    niches_path: str = os.getenv("NAMELAB_NICHES", str(ROOT / "data" / "niches.json"))
    custom_niches_path: str = os.getenv("NAMELAB_CUSTOM_NICHES", str(ROOT / "data" / "custom_niches.json"))
    github_token: str | None = os.getenv("GITHUB_TOKEN") or None
    brave_key: str | None = os.getenv("BRAVE_SEARCH_API_KEY") or None
    http_timeout: float = float(os.getenv("HTTP_TIMEOUT", "8"))
    max_concurrency: int = int(os.getenv("MAX_CONCURRENCY", "8"))

settings = Settings()
