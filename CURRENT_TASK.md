# Current Task

TASK_ID: mianem-v1-7-construction-families-2026-09-12

Status: MERGED TO `main`.

## Completion
- PR: #13 — `Mianem v1.7 — construction families, strong recommendations and bilingual meanings`
- Merge commit: `b1087057e2dd9580aac54b9a537b6bfb030df322`
- PR CI: success
- Post-merge `main` CI: success

## Product decisions now canonical
- Construction families are explicit Workshop concepts: context-semantic, brand frame, relation/preposition, action/product, contact, possessive and descriptor.
- Recommendation strength is decided before `.com` availability.
- Strong recommended directions are visually distinguished from good alternatives.
- Experimental / weak constructions are not promoted on the main Workshop surfaces.
- Every curated construction has an EN and PL interpretation of the whole name, not just translations of component words.
- Fixed grammatical constructions keep their valid direction (`By Lark`, not an automatic `Lark By`).
- Workshop targets 6–8 strong free `.com` directions from a deeper semantic/construction pool; if the pool cannot supply six without lowering quality, the UI says so explicitly.
- Taken domains stay hidden by default and may only be revealed as inspiration.
- Brand screening remains deferred until the user chooses a free construction.

## Implemented in v1.7
- Curator layer in `app/workshop_v16.py` with construction-family metadata, context-specific scores, recommendation tiers and bilingual whole-name meanings.
- Context-semantic directions such as Signal / Pulse / Flow / Core / Loop for software/product and Frame / Form / Mark for creative/photography contexts.
- Workshop semantic depth up to 32 candidates per side.
- Overall strong available shortlist plus grouped Construction Families.
- Bilingual selected-construction panel with EN / PL whole-name meaning, tone, recommendation status and semantic alert.
- Quality-floor messaging when fewer than 6 strong free directions survive.
- Visible product version updated to Mianem v1.7.
- v1.7 contract tests and product spec added.

## Next validation
Human Owner visual/interaction review in the local app, especially:
- whether the 6–8 shortlist is useful rather than noisy,
- whether Construction Families are understandable without naming/grammar expertise,
- whether `recommended` emphasis is strong enough but not visually heavy,
- whether the EN/PL whole-name panel is clear in light and dark modes,
- responsive behavior on narrow and short-height layouts.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Negative constructions are rejected before availability checks. Recommendation quality must not be driven by domain availability.
