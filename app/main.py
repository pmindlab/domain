from __future__ import annotations

import csv
import io
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .service import NameLabService
from .workshop import analyze_pair, workshop

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Mianem", version="1.5.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
service = NameLabService()


class SearchRequest(BaseModel):
    niches: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    min_len: int = 3
    max_len: int = 9
    per_niche: int = 120
    domain_checks: int = 60
    brand_checks: int = 10
    min_score: float = 55.0


class ExploreRequest(BaseModel):
    exclude_keys: list[str] = Field(default_factory=list)
    max_areas: int = 8
    per_niche: int = 60
    checks_per_area: int = 12
    min_score: float = 62.0
    min_len: int = 5
    max_len: int = 9


class CustomNicheRequest(BaseModel):
    taxon: str
    label: str = ""
    group: str = "Custom"


class DroppedRequest(BaseModel):
    raw_text: str
    min_len: int = 3
    max_len: int = 9
    brand_checks: int = 15
    min_score: float = 50.0
    max_checks: int = 250


class CheckRequest(BaseModel):
    name: str
    niche: str = "manual"


class DecisionRequest(BaseModel):
    decision: str
    note: str = ""


class WorkshopRequest(BaseModel):
    root: str
    niche: str = ""
    limit: int = 8


class WorkshopCheckRequest(BaseModel):
    root: str
    partner: str
    position: str = "before"
    niche: str = ""
    brand_check: bool = True


@app.get("/", response_class=HTMLResponse)
async def index():
    return (ROOT / "templates" / "index.html").read_text(encoding="utf-8")


@app.get("/api/health")
async def health():
    niches = service.list_niches()
    return {
        "ok": True,
        "app": "Mianem",
        "version": "1.5.0",
        "niche_count": len(niches),
        "custom_niche_count": sum(1 for n in niches if n.get("custom")),
        "language_count": len(service.list_languages()),
        "workshop": True,
    }


@app.get("/api/languages")
async def languages():
    return {"languages": service.list_languages()}


@app.get("/api/niches")
async def niches():
    items = service.list_niches()
    return {
        "niches": items,
        "default_keys": [n["key"] for n in items if n.get("default")],
        "groups": sorted({n["group"] for n in items}),
    }


@app.post("/api/niches/custom")
async def add_custom_niche(req: CustomNicheRequest):
    try:
        return await service.add_custom_niche(req.taxon, req.label, req.group)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except Exception as exc:
        raise HTTPException(500, f"Custom niche failed: {type(exc).__name__}: {exc}")


@app.delete("/api/niches/custom/{key}")
async def remove_custom_niche(key: str):
    if not service.remove_custom_niche(key):
        raise HTTPException(404, "Custom niche not found")
    return {"ok": True, "key": key}


@app.post("/api/explore")
async def explore(req: ExploreRequest):
    if req.min_len > req.max_len:
        raise HTTPException(400, "min_len > max_len")
    try:
        return await service.explore_niches(
            exclude_keys=req.exclude_keys,
            max_areas=max(1, min(req.max_areas, 20)),
            per_niche=max(20, min(req.per_niche, 150)),
            checks_per_area=max(3, min(req.checks_per_area, 25)),
            min_score=req.min_score,
            min_len=req.min_len,
            max_len=req.max_len,
        )
    except Exception as exc:
        raise HTTPException(500, f"Explore failed: {type(exc).__name__}: {exc}")


@app.post("/api/search")
async def search(req: SearchRequest):
    if req.min_len > req.max_len:
        raise HTTPException(400, "min_len > max_len")
    if not req.niches and not req.languages:
        raise HTTPException(400, "Wybierz co najmniej jeden obszar lub język")
    try:
        return await service.run_search(
            req.niches, req.min_len, req.max_len, req.per_niche,
            req.domain_checks, req.brand_checks, req.min_score, req.languages,
        )
    except Exception as exc:
        raise HTTPException(500, f"Search failed: {type(exc).__name__}: {exc}")


@app.post("/api/dropped")
async def dropped(req: DroppedRequest):
    if req.min_len > req.max_len:
        raise HTTPException(400, "min_len > max_len")
    if not req.raw_text.strip():
        raise HTTPException(400, "Wklej listę domen/nazw")
    try:
        return await service.run_dropped_search(
            req.raw_text, req.min_len, req.max_len,
            req.brand_checks, req.min_score, req.max_checks,
        )
    except Exception as exc:
        raise HTTPException(500, f"Dropped search failed: {type(exc).__name__}: {exc}")


@app.post("/api/check")
async def check(req: CheckRequest):
    try:
        return await service.check_name(req.name, req.niche)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except Exception as exc:
        raise HTTPException(500, f"Check failed: {type(exc).__name__}: {exc}")


@app.post("/api/workshop")
async def naming_workshop(req: WorkshopRequest):
    try:
        return workshop(req.root, req.niche, max(4, min(req.limit, 12)))
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@app.post("/api/workshop/check")
async def workshop_check(req: WorkshopCheckRequest):
    if req.position not in {"before", "after"}:
        raise HTTPException(400, "position must be before or after")
    analysis = analyze_pair(req.root, req.partner, req.position, req.niche)
    if not analysis.get("ok"):
        return {**analysis, "domain_status": "blocked", "brand_status": "blocked"}
    domain = analysis["domain"]
    checked = await service.domain.check_many([domain])
    dr = checked.get(domain.lower())
    domain_status = dr.status if dr else "unknown"
    result = {**analysis, "domain_status": domain_status, "brand_status": "unchecked"}
    if domain_status == "available" and req.brand_check:
        br = await service.brand.screen(analysis["joined"])
        result.update({
            "brand_status": br.status,
            "github_hits": br.github_hits,
            "web_hits": br.web_hits,
            "brand_notes": br.notes,
        })
    return result


@app.post("/api/candidates/{name}/decision")
async def decision(name: str, req: DecisionRequest):
    try:
        result = service.update_decision(name, req.decision, req.note)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    if not result:
        raise HTTPException(404, "Candidate not found")
    return result


@app.get("/api/saved")
async def saved(decision: str = Query("all")):
    return {"candidates": service.list_saved(decision)}


@app.get("/api/export.csv")
async def export_csv(decision: str = Query("all")):
    rows = service.list_saved(decision)
    out = io.StringIO()
    fieldnames = ["name", "domain", "score", "niche", "domain_status", "acquisition_mode", "brand_status", "decision", "note"]
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row.get(k, "") for k in fieldnames})
    content = out.getvalue().encode("utf-8-sig")
    return StreamingResponse(
        io.BytesIO(content), media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=mianem-{decision}.csv"},
    )
