# Current Task

TASK_ID: mianem-v1-6-2-product-ui-dark-theme-2026-09-12

Status: implementation complete on fix branch; pending PR CI/review/merge.

## Trigger
Owner review found that Mianem dark mode did not match PMindLab Product UI v1: the wordmark kept light-theme colours, the app still used legacy `#26588C`, dark surfaces were from the old palette, and contextual windows/buttons had weak hierarchy and readability.

## Implemented
- Added a local copy of canonical `PMindLab Product UI v1` tokens.
- Mapped legacy Mianem variables onto canonical background, surface, text, line, brand and action tokens.
- Separated brand/logo colour from action/button colour, especially in dark mode.
- Dark mode now uses canonical surfaces: `#101216`, `#171A1F`, `#1D2127`.
- PMind brand accent is `#3B72B5` on light and `#6A9DD8` on dark.
- Lab wordmark colour is `#16325C` on light and `#C3D9F0` on dark.
- Dark wordmark is generated from the canonical light SVG by colour substitution only, preserving identical geometry.
- Main UI typography moves to system sans; mono remains for domains, technical metadata and lab-style kickers.
- Context dialogs, workshop cards, inputs, secondary buttons, selected chips and semantic status pills receive clearer dark-mode borders/surfaces and canonical semantic colours.
- Added Product UI v1 contract tests and JS syntax coverage.

## Important distinction
`Lab = #C3D9F0` is a dark-wordmark colour, not a button fill. Dark primary actions use the separate canonical action token `#244E78` with white text.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Negative constructions are rejected before availability checks.
