# Project State

Mianem v1.4.1 is the current baseline. The product was renamed from NameLab on 2026-09-12; repository name remains `pmindlab/domain`.

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

## Product direction
The next major iteration turns Mianem from a result generator into an interactive naming workshop:
- free min/max/custom length controls,
- stronger semantic curation than the current rule-based scorer,
- a root-word workbench with English and Polish meaning preview,
- intelligent prefix/suffix suggestions around a chosen root such as `lark`,
- two-word `.com` construction based on semantic compatibility rather than brute-force pairing,
- negative/slang/medical/sexual/brand collision screening before domain checks,
- human-in-the-loop exploration that returns a small number of high-quality directions instead of hundreds of records.

## Architecture
- Backend: FastAPI / Python.
- Frontend: vanilla HTML/CSS/JS.
- Local state: SQLite (ignored by Git).
- CI: pytest on GitHub Actions.

## Compatibility
Existing local state remains in `data/namelab.db` for now so the product rename does not lose user history. Internal legacy identifiers can be migrated separately with an explicit data-migration plan.

## Invariants
No aftermarket, auction, broker, or merely expiring domains may be presented as available. Brand screening is research triage rather than legal trademark clearance.
