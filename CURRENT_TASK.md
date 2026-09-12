# Current Task

TASK_ID: mianem-v1-7-construction-families-2026-09-12

Status: implementation complete on feature branch; pending CI/review/merge.

## Trigger
Owner approved a Workshop model where Mianem must actively curate two-word constructions instead of exposing equivalent-looking word combinations and forcing the user to guess which ones make linguistic sense.

## Product decisions
- Construction families are explicit product concepts: context-semantic, brand frame, relation/preposition, action/product, contact, possessive and descriptor.
- Recommendation strength is decided before `.com` availability.
- Strong recommended directions are visually distinguished from good alternatives.
- Experimental / weak constructions are not promoted on the main Workshop surfaces.
- Every curated construction has an EN and PL interpretation of the whole name, not just translations of the component words.
- Fixed grammatical constructions keep their valid direction (`By Lark`, not an automatic `Lark By`).
- Workshop targets 6–8 strong free `.com` directions from a deeper semantic/construction pool; if the pool cannot supply six without lowering quality, the UI says so explicitly.
- Taken domains stay hidden by default and may only be revealed as inspiration.
- Brand screening remains deferred until the user chooses a free construction.

## Implementation
- Expanded `app/workshop_v16.py` into the v1.7 curator layer with construction-family metadata, context-specific scores, recommendation tiers and bilingual whole-name meanings.
- Added context-semantic directions such as Signal / Pulse / Flow / Core / Loop for software/product and Frame / Form / Mark for creative/photography contexts.
- Increased Workshop semantic depth to up to 32 candidates per side.
- Reworked Workshop frontend to build an overall strong available shortlist plus grouped Construction Families.
- Added a bilingual selected-construction panel with EN / PL whole-name meaning, tone and recommendation status.
- Added quality-floor messaging when fewer than 6 strong free directions survive.
- Updated visible product version to Mianem v1.7.
- Added v1.7 contract tests and product spec.

## QA required before merge
- `pytest -q`
- `node --check app/static/workshop-v16.js`
- full repository CI
- responsive visual review of Workshop at desktop and narrow/mobile widths

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Negative constructions are rejected before availability checks. Recommendation quality must not be driven by domain availability.
