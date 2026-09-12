# Mianem v1.6.7 — Workshop available-first UX

Decision: semantic quality is evaluated before domain availability, but the default Workshop result surface shows only combinations whose `.com` is currently available.

Rules:
- semantic ranking remains independent from availability,
- availability is checked automatically for the semantic candidate pool,
- taken domains are hidden by default from `Najlepsze podpowiedzi Mianem` and `Rozszerzenia marki`,
- the UI may disclose how many taken candidates were hidden and allow the user to reveal them,
- full brand screening remains deferred until the user selects an available combination,
- if no available candidate exists in the current semantic pool, say so explicitly rather than fabricating lower-quality combinations.
