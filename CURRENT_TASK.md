# Current Task

TASK_ID: mianem-v1-6-1-ui-regressions-2026-09-12

Status: implementation complete on fix branch; pending PR CI/review/merge.

## Scope
- Fix clipped search-area chips in the Areas dialog at desktop and short-height layouts.
- Fix Workshop flow so a user selecting a semantic partner such as `light` can explicitly choose `Light Lark` vs `Lark Light` before the full live `.com` + brand check when both directions are active.
- Make PMindLab Product UI v1 the canonical UI-rule source for future Mianem UI work.

## Implemented
- Added `ui-regression-v161.css` with non-shrinking content rows, internal dialog scrolling, dynamic viewport height and mobile/short-height handling.
- Added `workshop-direction-v161.js`: top semantic suggestions now pause at a human direction choice when both sides are enabled; brand-form extensions keep their fixed grammatical direction.
- Added direction-choice styles and CI JS syntax coverage.
- Added static regression tests for dialog layout, direction choice and UI-rule authority.
- Updated `AGENTS.md` to point to `pmindlab/pmindlab/design-system/PMINDLAB_PRODUCT_UI_V1.md` and its responsive workflow.

## UI audit finding
Mianem v1.6 is not yet fully PMindLab Product UI v1 compliant. The existing app still uses several legacy visual tokens and global monospace styling. Full visual standardisation is deliberately not mixed into this regression fix; it should be a separate UI adoption task with responsive/static review across the required test matrix.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Negative constructions are rejected before availability checks.
