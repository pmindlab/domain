# NameLab — agent instructions

## Purpose
NameLab is a local naming research engine for finding brandable names with an actually available `.com`.

## Product invariants
1. Never present aftermarket, auction, broker, or merely expiring domains as available.
2. A normal search result qualifies only when the live domain check does not show an active `.com` registration record.
3. A Dropped result qualifies only after the domain has actually returned to availability.
4. Prefer real words, real taxa, and curated language terms over synthetic startup-style blends.
5. Keep the UI simple. Advanced pipeline parameters belong behind presets rather than on the primary screen.
6. Brand screening is risk triage, not legal trademark clearance.

## Development workflow
Before changing code, read:
- `PROJECT_STATE.md`
- `CURRENT_TASK.md`

For every change:
1. preserve the invariants above,
2. add or update tests,
3. run `pytest -q`,
4. update `CURRENT_TASK.md` when the work materially changes project state.

Do not commit local SQLite state, secrets, `.env`, or user-added custom niches.
