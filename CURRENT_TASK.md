# Current Task

TASK_ID: mianem-v1-5-interactive-workshop-2026-09-12

Status: implementation complete on feature branch; pending PR CI/review/merge.

## Implemented
- Bumped product/API/package to Mianem v1.5.0.
- Replaced fixed length presets at runtime with Min / Max / optional exact length controls.
- Added working `app/workshop.py` semantic workshop engine.
- Added `/api/workshop` for bilingual root context + curated before/after suggestions.
- Added `/api/workshop/check` for pair analysis → live `.com` → brand screen.
- Added negative-root screening before network/domain checks.
- Added a human-in-the-loop workshop modal available from result cards and manual roots.
- Added custom partner entry: user can test a word before or after the root.
- Renamed Explore CTA to `Sprawdź inne obszary` so it no longer implies discovery beyond the static catalog.
- Replaced `app/static/logo.svg` with the exact SVG attachment supplied by the user for v1.5.
- Updated provider/launcher product identity from NameLab to Mianem.
- Added workshop tests and frontend JS syntax checks to CI.
- Updated README and project state.

## Known scope / follow-up
1. Expand bilingual root dictionary and semantic partner graph substantially.
2. Add a stronger semantic curator stage for one-word results; current one-word ranking still relies primarily on the existing rule-based scorer.
3. Add genuine new-area discovery outside the current taxonomy catalog.
4. Consider persistent workshop history/workbench once interaction patterns are validated.
5. Migrate legacy `namelab.db` only through an explicit data migration so user history is preserved.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Two-word negative constructions are rejected before availability checks.
