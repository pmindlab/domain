from __future__ import annotations

import asyncio
from dataclasses import dataclass
import httpx


@dataclass
class DomainResult:
    domain: str
    status: str  # available/taken/unknown
    detail: str = ""


class VerisignRdapProvider:
    BASE = "https://rdap.verisign.com/com/v1/domain"

    def __init__(self, timeout: float = 8.0, concurrency: int = 8):
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(concurrency)

    async def check_one(self, client: httpx.AsyncClient, domain: str) -> DomainResult:
        async with self.semaphore:
            try:
                r = await client.get(f"{self.BASE}/{domain.lower()}")
                if r.status_code == 200:
                    return DomainResult(domain, "taken", "RDAP record exists")
                if r.status_code == 404:
                    return DomainResult(domain, "available", "No .com RDAP record")
                if r.status_code in (429, 503):
                    return DomainResult(domain, "unknown", f"RDAP rate limited ({r.status_code})")
                return DomainResult(domain, "unknown", f"RDAP HTTP {r.status_code}")
            except Exception as exc:
                return DomainResult(domain, "unknown", f"RDAP error: {type(exc).__name__}")

    async def check_many(self, domains: list[str]) -> dict[str, DomainResult]:
        headers = {"User-Agent": "NameLab/1.4 domain availability research"}
        async with httpx.AsyncClient(timeout=self.timeout, headers=headers, follow_redirects=True) as client:
            results = await asyncio.gather(*(self.check_one(client, d) for d in domains))
        return {r.domain.lower(): r for r in results}
