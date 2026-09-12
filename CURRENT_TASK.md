# Current Task

TASK_ID: mianem-product-rename-and-workshop-direction-2026-09-12

Status: rename implemented on feature branch; pending CI and merge.

## Completed in this task
- Renamed visible product identity from NameLab to Mianem.
- Bumped product version to v1.4.1.
- Updated FastAPI metadata, health response and CSV export filename.
- Preserved legacy local data identifiers so existing SQLite history is not lost.
- Captured the next product direction: interactive naming workshop rather than bulk-result generator.

## Next product work — v1.5
1. Replace length presets with clear min/max plus optional exact/custom length.
2. Improve one-word quality with semantic curation beyond the current rule-based scorer.
3. Add a root-word workshop: choose a result such as `lark`, see EN/PL meaning and associations, then explore compatible words before and after it.
4. Add two-word `.com` mode using semantic compatibility, natural-language quality, phone test and negative-meaning screening before domain checks.
5. Make discovery genuinely expand beyond the existing static niche catalog.
6. Keep human choice central: suggest a small set of directions rather than returning hundreds of combinations.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available.
