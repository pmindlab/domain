# Current Task

TASK_ID: mianem-v1-6-semantic-workshop-2026-09-12

Status: implementation on feature branch; pending PR CI/review/merge.

## Implemented
- Bumped product/API/package to Mianem v1.6.0.
- Added a semantic curation layer above the v1.5 workshop engine.
- Unknown scientific/taxonomic roots no longer pretend to have an English translation; the UI explains that they are scientific/coined roots.
- Added explicit semantic classes: natural / brandable / abstract / brand-form.
- Abstract combinations receive a visible warning instead of a misleading high score with no explanation.
- Added a ranked `Najlepsze podpowiedzi Mianem` stage before the longer before/after lists.
- Added brand-form extensions such as `The`, `One`, `New`, plus context-sensitive `Studio`, `Lab`, `Works`, `House`, `Co`, and software/product forms such as `Get`, `Use`, `App`, `AI`.
- Added lightweight `.com` availability precheck for only the short semantic shortlist; full brand screening still runs after the human selects a combination.
- Added a primary Workshop entry on the main search console for a user-supplied root.
- Main Workshop can search only before, only after, or both sides of the root.
- Added optional naming context: neutral brand / software-AI / creative studio / photography / product / service.
- Added v1.6 API and frontend tests plus JS syntax checks in CI.

## Product workflow
root → meaning/context → best semantic combinations → brand-form extensions → live `.com` precheck → human choice → full `.com` + brand screen.

## Follow-up
1. Replace local semantic heuristics with a stronger semantic curator for top-N candidates while keeping deterministic filters and explanations.
2. Expand bilingual lexical/taxonomic descriptions and partner graph.
3. Add genuine new-area discovery outside the current taxonomy catalog.
4. Add persistent workshop history/workbench after interaction patterns stabilize.
5. Migrate legacy `namelab.db` only through an explicit data migration so user history is preserved.

## Product invariant
Available `.com` only. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domains may be presented as available. Negative constructions are rejected before availability checks.
