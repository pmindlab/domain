# Current Task

TASK_ID: mianem-v1-7-1-workshop-depth-single-scroll-2026-09-12

Status: implementation complete on fix branch; pending CI/review/merge.

## Trigger
Human Owner visual QA of Mianem v1.7 found two concrete regressions:
- `Lark` in the `software` context still collapsed to one strong free result after availability filtering (`17` strong candidates were taken and only `Clear Lark` survived), despite the intended 6–8 shortlist target;
- opening the Workshop showed two vertical scroll surfaces: the Workshop content scroll plus the still-scrollable page behind the modal.

## Fix
- Added a second, still-curated software/product semantic pool with concrete whole-name EN/PL meanings and recommendation scores determined before `.com` availability.
- Added strong/good directions such as Agent, Query, Logic, Sync, Code, Data, Bridge, Beacon, Scope, Stack, Relay, Mesh, Grid, Stream, Layer, Engine, Pilot, Lens, Trace, Route, Scan and further technical/product directions.
- The added pool is automatically included in the existing live `.com` availability pass; taken domains remain hidden by default and cannot promote weaker names.
- Every added direction preserves the v1.7 whole-name meaning contract: EN, PL, tone, semantic class and recommendation tier.
- Added a v1.7.1 modal patch: the dialog itself no longer scrolls, the Workshop shell owns the single internal scrollbar, and background document scrolling is locked while the modal is open.
- Added regression tests and CI syntax coverage for the v1.7.1 frontend patch.

## QA required before merge
- `pytest -q`
- JavaScript syntax checks including `app/static/workshop-v171.js`
- full PR CI
- local Human Owner check with `Lark` / `software`: shortlist depth and exactly one visible Workshop scroll surface

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Negative constructions are rejected before availability checks. Recommendation quality remains independent from `.com` availability; deeper search expands only with curated, meaningful constructions.
