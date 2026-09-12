# Project State

Mianem v1.7.3 is the active baseline on `main`. Canonical repository: `pmindlab/mianem`.

## Product
- Local FastAPI web app for naming research and an interactive naming workshop.
- Sources: GBIF taxonomy plus curated real-word language datasets.
- Languages: English, Polish, Spanish, French, Latin, Mandarin pinyin.
- Live `.com` triage via Verisign RDAP.
- Brand screening via GitHub and optional Brave Search.
- Search modes: Fast, Detailed, Deep.
- Name length supports range and exact-length modes.
- Grid/list result views and persistent light/dark theme.
- Saved decisions: shortlist, radar, reject.
- Dropped/expired mode only returns domains that are actually available now.
- Shared UI authority: `pmindlab/pmindlab/design-system/PMINDLAB_PRODUCT_UI_V1.md`.

## Naming Workshop v1.7.3
The Workshop is a curator, not a blind word-combination generator.

Canonical flow:

`root -> context -> semantic direction / construction family -> linguistic + brand fit -> recommendation tier -> live .com -> user choice -> full brand screening`

Current verified behavior includes:
- whole-name EN + PL interpretation,
- recommendation tiers before domain availability,
- curated construction families with natural grammatical direction,
- a deeper curated software/product pool targeting 6–8 strong available `.com` directions without lowering quality,
- one Workshop scroll surface,
- selected semantic members can be switched between before/after order when both orders are meaningful,
- fixed grammatical constructions such as `By Lark` remain fixed,
- contextual `← Wróć do wyników` navigation from Workshop back to the originating result list and scroll position.

## Recommendation contract
- `recommended` — strong context fit and concrete whole-name meaning.
- `good` — valid alternative, weaker than the recommended direction.
- `experimental` — more brand-dependent / weaker and not promoted on primary Workshop surfaces.

A free `.com` cannot promote a weak construction. Taken candidates are hidden by default and can only be shown as inspiration.

## Explore
The current Explore function rotates through under-tested areas from the existing catalog. Genuine discovery of new taxonomy groups outside the catalog remains future work.

## Architecture
- Backend: FastAPI / Python.
- Base Workshop engine: `app/workshop.py`.
- v1.7 curator layer: `app/workshop_v16.py` plus incremental frontend modules.
- Frontend: vanilla HTML/CSS/JS.
- Local development state: SQLite in `data/namelab.db` (ignored by Git).
- CI: pytest plus JavaScript syntax checks.

## Windows portable packaging
A Windows 10/11 x64 portable build is being added on `build/windows-portable-v1-2026-09-12`.

Packaging contract:
- self-contained `Mianem.exe` built with PyInstaller on GitHub Actions `windows-latest`,
- no Python installation or administrator rights required for the recipient,
- browser UI still served only on `127.0.0.1`,
- packaged default datasets are read-only inside the executable bundle,
- mutable user state is stored under `%LOCALAPPDATA%\PMindLab\Mianem`,
- `.env`, SQLite history, custom niches and API secrets are never bundled,
- final delivery is a ZIP plus SHA-256 file,
- packaged executable must pass a frozen-app smoke test before artifact upload.

## Compatibility
The normal source/development launcher keeps legacy-compatible local state in `data/namelab.db`. Legacy localStorage values are read as fallback and new values are saved under `mianem-*` keys.

## Current QA state
PRs #15–#18 and their post-merge `main` workflows passed automated CI. Human QA confirmed the deeper Workshop pool, single-scroll behavior and selected-direction control. Windows portable packaging is the current active task.

## Invariants
No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Brand screening is research triage rather than legal trademark clearance. Negative two-word constructions must be blocked before a domain availability request. Recommendation quality remains independent from `.com` availability.
