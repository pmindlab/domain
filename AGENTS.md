# Mianem — agent instructions

## Purpose
Mianem is a local naming research engine and naming workshop for finding brandable names with an actually available `.com`.

## Product invariants
1. Never present aftermarket, auction, broker, or merely expiring domains as available.
2. A normal search result qualifies only when the live domain check does not show an active `.com` registration record.
3. A Dropped result qualifies only after the domain has actually returned to availability.
4. Prefer real words, real taxa, and curated language terms over synthetic startup-style blends.
5. Keep the UI simple. Advanced pipeline parameters belong behind presets rather than on the primary screen.
6. Brand screening is risk triage, not legal trademark clearance.
7. Two-word naming must use semantic compatibility and negative-meaning screening; never brute-force meaningless word pairs.

## UI authority
The canonical source of shared PMindLab product-interface rules is:

`pmindlab/pmindlab/design-system/PMINDLAB_PRODUCT_UI_V1.md`

The standard was introduced on `feature/pmindlab-product-ui-v1-2026-09-12`; use the canonical PMindLab repository copy and follow newer versions only when the Human Owner adopts them.

For materially changed UI use:

`CURRENT REALITY -> USER TASK -> INFORMATION ARCHITECTURE -> RESPONSIVE CONTRACT -> RESPONSIVE STATIC -> INTERACTION -> TEST MATRIX -> FREEZE`

Responsive behavior is correctness, not later polish. Review at minimum 320–480, 481–767, 768–1023, 1024–1439 and 1440+ widths, plus short-height/mobile-landscape when relevant. Do not silently invent near-duplicate brand tokens or component rules; document deliberate product-specific divergence.

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
