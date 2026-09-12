# Project State

Mianem v1.5.0 is the active development baseline on `feature/mianem-v1-5-workshop-2026-09-12`. Canonical repository: `pmindlab/mianem`.

## Product
- Local FastAPI web app for naming research and an interactive naming workshop.
- Sources: GBIF taxonomy plus curated real-word language datasets.
- Languages: English, Polish, Spanish, French, Latin, Mandarin pinyin.
- Live `.com` triage via Verisign RDAP.
- Brand screening via GitHub and optional Brave Search.
- Search modes: Fast, Detailed, Deep.
- Name length uses direct Min / Max plus optional exact length.
- Grid/list result views and persistent light/dark theme.
- Saved decisions: shortlist, radar, reject.
- Dropped/expired mode only returns domains that are actually available now.

## v1.5 Naming Workshop
- Every search candidate can be opened as a root word in the workshop.
- The workshop shows EN/PL meaning/context when covered by the local semantic dictionary.
- Curated suggestions are separated into words fitting before and after the root.
- A human selects the direction; the app does not brute-force thousands of random pairs.
- Pair analysis checks semantic overlap, boundary readability, total length and negative roots before the network check.
- A selected pair is checked live for `.com` availability.
- Available pairs can then receive the existing brand screen.
- Manual roots and manual partner words are supported.

## Semantic scope
v1.5 introduces a real working semantic workshop, but it is currently a curated local engine rather than an LLM. Known roots such as `lark`, `bird`, `light`, `grain` and `page` have richer bilingual context; unknown roots retain source context and can still be developed with tagged suggestions. Expansion of the semantic dictionary and an intelligent curator layer remain future quality work.

## Explore
The current Explore function rotates through under-tested areas from the existing catalog. It is intentionally labelled `Sprawdź inne obszary`; genuine discovery of new taxonomy groups outside the catalog remains future work.

## Architecture
- Backend: FastAPI / Python.
- Workshop engine: `app/workshop.py`.
- Frontend: vanilla HTML/CSS/JS; v1.5 frontend is split into small sequential modules loaded by `app/static/app.js`.
- Local state: SQLite (ignored by Git).
- CI: pytest plus JavaScript syntax checks.

## Compatibility
Existing local state remains in `data/namelab.db` for now so the product rename does not lose user history. Legacy localStorage values are read as fallback and new values are saved under `mianem-*` keys.

## Invariants
No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Brand screening is research triage rather than legal trademark clearance. Negative two-word constructions must be blocked before a domain availability request.
