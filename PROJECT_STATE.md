# Project State

NameLab v1.4 is the current baseline.

## Product
- Local FastAPI web app for naming research.
- Sources: GBIF taxonomy plus curated real-word language datasets.
- Languages: English, Polish, Spanish, French, Latin, Mandarin pinyin.
- Live `.com` triage via Verisign RDAP.
- Brand screening via GitHub and optional Brave Search.
- Search modes: Fast, Detailed, Deep.
- Name-length presets include 3–9 letters.
- Grid/list result views and persistent light/dark theme.
- Saved decisions: shortlist, radar, reject.
- Dropped/expired mode only returns domains that are actually available now.

## Architecture
- Backend: FastAPI / Python.
- Frontend: vanilla HTML/CSS/JS.
- Local state: SQLite (ignored by Git).
- CI: pytest on GitHub Actions.

## Invariants
No aftermarket, auction, broker, or merely expiring domains may be presented as available. Brand screening is research triage rather than legal trademark clearance.
