# Current Task

TASK_ID: mianem-v1-7-2-selected-direction-switch-2026-09-12

Status: implementation on fix branch; pending CI/review/Human Owner QA.

## Trigger
Human Owner QA of Mianem v1.7.1 confirmed that:
- the deeper Workshop pool now reaches the intended 6–8 strong available `.com` directions for `Lark` / `software` after a clean backend restart;
- the Workshop now has one visible vertical scroll surface;
- the selected-construction panel correctly shows whole-name EN/PL meaning, recommendation tier, semantic class and tone.

The remaining interaction gap is direction control after selecting a member. Example: after choosing `Lark Echo`, the visible `przed rdzeniem` / `po rdzeniu` buttons still belong only to the separate custom-member field, so the user cannot clearly switch the selected member between `Echo Lark` and `Lark Echo` from the selected-construction panel.

## Fix
- Add an explicit `UKŁAD NAZWY` control inside the selected-construction panel.
- For semantic/custom members, expose both `before` and `after` arrangements and re-run the existing analysis/live check when the user changes arrangement.
- Each arrangement is evaluated independently; reversing a member does not inherit the original recommendation and may receive a weaker/abstract warning.
- Preserve fixed grammar for curated construction families such as `By Lark`, `With Lark`, `Get Lark`, possessives and canonical descriptors: do not automatically create reversed nonsense such as `Lark By`.
- Keep the custom-member `przed rdzeniem` / `po rdzeniu` controls for entering a new manual member; the new switch applies specifically to the currently selected construction.
- Add PMindLab-token styling, regression coverage and JavaScript syntax coverage.

## QA required before merge
- `pytest -q`
- JavaScript syntax checks including `app/static/workshop-v172.js`
- full PR CI
- Human Owner local check:
  - select a semantic member such as `Light` / `Echo` and confirm the selected-construction panel lets the user switch both arrangements;
  - confirm the meaning/recommendation is recalculated after switching;
  - select a fixed grammatical construction such as `By Lark` and confirm the UI explains the fixed natural order instead of offering `Lark By`;
  - confirm the v1.7.1 6–8 shortlist and single-scroll fixes remain intact.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Recommendation quality remains independent from `.com` availability. Direction switching is a user-controlled linguistic evaluation, not an instruction to recommend both orders equally.
