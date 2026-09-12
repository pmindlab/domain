from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import quote_plus
import httpx

TECH_WORDS = re.compile(r"\b(ai|artificial intelligence|software|developer|development|web|design|digital|code|coding|app|saas|cloud|tech|technology|github|api)\b", re.I)


@dataclass
class BrandResult:
    status: str = "clear"  # clear/review/conflict
    github_hits: list[dict] = field(default_factory=list)
    web_hits: list[dict] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class BrandScreenProvider:
    def __init__(self, github_token: str | None = None, brave_key: str | None = None, timeout: float = 8.0):
        self.github_token = github_token
        self.brave_key = brave_key
        self.timeout = timeout

    async def _github(self, client: httpx.AsyncClient, name: str) -> tuple[list[dict], bool]:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        hits: list[dict] = []
        strong = False

        try:
            r = await client.get(f"https://api.github.com/users/{name}", headers=headers)
            if r.status_code == 200:
                data = r.json()
                hits.append({"type": "account", "name": data.get("login", name), "url": data.get("html_url", ""), "text": data.get("bio") or ""})
        except Exception:
            pass

        try:
            r = await client.get("https://api.github.com/search/repositories", headers=headers, params={
                "q": f"{name} in:name",
                "per_page": 8,
            })
            if r.status_code == 200:
                for item in r.json().get("items", []):
                    repo_name = (item.get("name") or "").lower()
                    owner = ((item.get("owner") or {}).get("login") or "").lower()
                    desc = item.get("description") or ""
                    exact = repo_name == name.lower() or owner == name.lower()
                    if exact:
                        tech = bool(TECH_WORDS.search(desc))
                        strong = strong or tech
                        hits.append({
                            "type": "repo", "name": item.get("full_name", ""), "url": item.get("html_url", ""),
                            "text": desc, "tech": tech,
                        })
        except Exception:
            pass
        return hits, strong

    async def _brave(self, client: httpx.AsyncClient, name: str) -> tuple[list[dict], bool]:
        if not self.brave_key:
            return [], False
        q = f'"{name}" (software OR AI OR web OR design OR digital OR company OR GitHub)'
        headers = {"Accept": "application/json", "X-Subscription-Token": self.brave_key}
        try:
            r = await client.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params={"q": q, "count": 10})
            if r.status_code != 200:
                return [], False
            hits = []
            strong = False
            for item in (r.json().get("web") or {}).get("results", []):
                title = item.get("title") or ""
                desc = item.get("description") or ""
                url = item.get("url") or ""
                text = f"{title} {desc}"
                exact = name.lower() in text.lower() or name.lower() in url.lower()
                if exact:
                    tech = bool(TECH_WORDS.search(text))
                    strong = strong or tech
                    hits.append({"title": title, "url": url, "text": desc, "tech": tech})
            return hits, strong
        except Exception:
            return [], False

    async def screen(self, name: str) -> BrandResult:
        headers = {"User-Agent": "Mianem/1.5 brand screening"}
        async with httpx.AsyncClient(timeout=self.timeout, headers=headers, follow_redirects=True) as client:
            gh_hits, gh_strong = await self._github(client, name)
            web_hits, web_strong = await self._brave(client, name)

        result = BrandResult(github_hits=gh_hits, web_hits=web_hits)
        if gh_strong or web_strong:
            result.status = "conflict"
            result.notes.append("Exact-name technology signal found")
        elif gh_hits or web_hits:
            result.status = "review"
            result.notes.append("Exact-name use found; human review recommended")
        else:
            result.status = "clear"
            if not self.brave_key:
                result.notes.append("GitHub screened; full web screening unavailable without BRAVE_SEARCH_API_KEY")
        return result

    @staticmethod
    def search_links(name: str) -> dict[str, str]:
        q = quote_plus(f'"{name}" software AI web design company')
        return {
            "google": f"https://www.google.com/search?q={q}",
            "bing": f"https://www.bing.com/search?q={q}",
            "github": f"https://github.com/search?q={quote_plus(name)}&type=repositories",
        }
