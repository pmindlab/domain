# Current Task

TASK_ID: mianem-pmindlab-ui-v1-2026-09-12

Status: IN_PROGRESS

## Goal
Adopt the approved PMindLab Product UI v1 visual standard without changing Mianem search, workshop, domain-check, brand-screening or persistence behaviour.

## Baseline
- Branch created from `main` at `40346280c8c75a625d2cea249e6381b2023559d2`.
- Mianem v1.5 functional behaviour is the frozen baseline for this task.
- `app/static/logo.svg` already matches the exact Owner-supplied PMindLab SVG and must not be recreated or replaced.

## Authorized visual scope
- align shared light/dark neutral palette with PMindLab Product UI v1;
- use canonical PMind blue `#3B72B5` and navy `#16325C`;
- add the canonical dark wordmark variant with identical geometry;
- move general UI typography from global monospace to local/system sans;
- retain monospace only for technical data such as domains, source/provider metadata and machine-facing labels;
- align header proportions and parent-brand/product hierarchy;
- keep semantic success/warning/error colours distinct and compatible with the PMindLab palette;
- record `PMINDLAB_PRODUCT_UI_VERSION = 1` in the frontend layer.

## Explicit non-scope
- no workshop/search/scoring/provider changes;
- no domain-availability or brand-screening changes;
- no SQLite/data migration;
- no external font/CDN dependency;
- no deployment;
- no merge without a separate Owner decision.

## Acceptance
1. Existing Mianem behaviour remains unchanged.
2. Light background remains the approved warm `#FAFAF7` family.
3. Light wordmark remains the exact Owner asset.
4. Dark mode uses the matching canonical dark wordmark.
5. General UI uses sans; technical identifiers remain mono where useful.
6. Success/warning/error states remain semantically distinct and are not replaced by brand blue.
7. Existing tests and frontend syntax checks remain green.

## Exact next step
Implement the isolated visual layer, run the existing test/syntax suite, inspect the focused diff, then return for Owner visual review before any PR/merge.
