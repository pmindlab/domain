# Mianem v1.5 — Naming Workshop

## Purpose
Turn a promising one-word result into an interactive naming session instead of dumping hundreds of generated combinations.

## Flow
1. Search returns a real-word/taxon candidate such as `lark`.
2. User opens **Warsztat**.
3. Mianem shows local EN/PL context plus tone and visual associations.
4. Mianem shows a small curated set of compatible terms before and after the root.
5. User chooses a direction or types a custom partner.
6. Pair is screened locally for negative roots, semantic compatibility, boundary readability and total length.
7. Only then is the combined `.com` checked live.
8. If available, the existing brand screen runs.

## v1.5 scope
The semantic workshop is a real local curated engine, not an LLM. It intentionally starts with a controlled partner graph and richer entries for selected roots. Unknown roots can still use source-context tags and custom partner checks.

The existing one-word candidate scorer remains primarily rule based in v1.5. A later curator stage can rank a smaller top-N set with deeper semantic reasoning without exposing thousands of low-quality candidates.

## Safety / quality invariants
- no random Cartesian-product generator,
- negative constructions are blocked before network checks,
- only live-available `.com` can be described as available,
- no aftermarket / auction / pending-delete results,
- brand screening remains triage, not trademark clearance.
