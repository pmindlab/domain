# Project State

Mianem v1.7.0 is the active baseline on `main`. Canonical repository: `pmindlab/mianem`.

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

## Naming Workshop v1.7
The Workshop is a curator, not a blind word-combination generator.

Canonical flow:

`root -> context -> semantic direction / construction family -> linguistic + brand fit -> recommendation tier -> live .com -> user choice -> full brand screening`

### Construction families
- Context-semantic directions.
- Brand frame.
- Relation / preposition.
- Action / product.
- Contact / communication.
- Possessive.
- Descriptor after the root.

### Recommendation tiers
- `recommended` — strong context fit and concrete whole-name meaning.
- `good` — valid alternative, weaker than the recommended direction.
- `experimental` — more brand-dependent / weaker; not promoted on main Workshop surfaces.

Recommendation quality is determined before domain availability. A free `.com` cannot promote a weak construction.

### Whole-name meaning contract
Every curated construction exposes:
- full phrase,
- EN interpretation of the whole construction,
- PL interpretation of the whole construction,
- semantic/construction class,
- recommendation tier,
- tone,
- alert/explanation where appropriate.

The selected-construction panel presents this meaning before treating the domain as a viable brand choice.

### Available-first quality floor
- Workshop checks a deeper semantic/construction pool.
- Target is 6–8 strong available `.com` directions.
- Taken candidates are hidden by default and can be revealed only as inspiration.
- If fewer than six strong free directions survive, Mianem states that explicitly instead of lowering the linguistic/semantic quality threshold.
- Full brand screening is deferred until the user selects a free construction.

### Context examples
- Software/product can expand toward Signal, Pulse, Flow, Core, Loop, Get, Use, Try, Ask, With, App, AI, etc.
- Creative/photography can expand toward By, Studio, Works, House, Frame, Form, Mark, etc.
- Fixed grammatical constructions keep their natural direction (`By Lark`; no automatic `Lark By`).

## Semantic scope
v1.7 is a curated local semantic rules/knowledge layer, not an LLM. Known roots such as `lark`, `bird`, `light`, `grain` and `page` have richer bilingual context. Unknown roots retain source context and can still be developed with tagged suggestions. A future intelligent semantic curator may expand this layer, but current recommendations must remain explainable and testable.

## Explore
The current Explore function rotates through under-tested areas from the existing catalog. Genuine discovery of new taxonomy groups outside the catalog remains future work.

## Architecture
- Backend: FastAPI / Python.
- Base Workshop engine: `app/workshop.py`.
- v1.7 curator layer: `app/workshop_v16.py` (legacy filename retained for compatibility).
- Frontend: vanilla HTML/CSS/JS, with Workshop logic in `app/static/workshop-v16.js` and supporting modules loaded by `app/static/app.js`.
- Local state: SQLite (ignored by Git).
- CI: pytest plus JavaScript syntax checks.

## Compatibility
Existing local state remains in `data/namelab.db` for now so the product rename does not lose user history. Legacy localStorage values are read as fallback and new values are saved under `mianem-*` keys.

## Current QA state
PR #13 and the post-merge `main` workflow both passed automated CI. Human visual/interaction QA remains the next step for the v1.7 Workshop, especially family hierarchy, recommendation emphasis, EN/PL meaning presentation, dark/light readability and responsive behavior.

## Invariants
No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Brand screening is research triage rather than legal trademark clearance. Negative two-word constructions must be blocked before a domain availability request. Recommendation quality must remain independent from `.com` availability.
