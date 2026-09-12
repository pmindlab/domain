from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Optional


@dataclass
class Candidate:
    name: str
    domain: str
    niche: str
    source: str = "gbif"
    taxon_key: Optional[str] = None
    score: float = 0.0
    components: dict[str, float] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    domain_status: str = "unchecked"  # available/taken/unknown
    acquisition_mode: str = "available_now"  # available_now/dropped_available/manual
    brand_status: str = "unchecked"  # clear/review/conflict/unchecked
    github_hits: list[dict[str, Any]] = field(default_factory=list)
    web_hits: list[dict[str, Any]] = field(default_factory=list)
    decision: str = "new"  # new/shortlist/radar/reject
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
