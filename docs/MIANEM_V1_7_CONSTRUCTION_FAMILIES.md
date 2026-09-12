# Mianem v1.7 — Construction Families

## Product decision

The Workshop is a curator, not a word-combination generator.

A user must not be asked to choose blindly between grammatically possible but semantically weak combinations. Every prominent suggestion is evaluated before domain availability and carries an explicit whole-name interpretation in English and Polish.

## Pipeline

`root -> context -> construction family / semantic direction -> linguistic + brand fit -> recommendation tier -> live .com -> user choice -> full brand screening`

Domain availability never creates a recommendation. A weak phrase does not become `recommended` because its `.com` is free.

## Recommendation tiers

- `recommended` — strong fit for the selected context, clear construction and concrete meaning.
- `good` — valid alternative with a useful meaning, but weaker than the recommended direction.
- `experimental` — understandable but weaker / more brand-dependent; hidden from the main surfaces by default.

## Construction families

- Context semantic directions — e.g. Signal / Pulse / Flow / Core / Frame / Form depending on context.
- Brand frame — The / One / New.
- Relation / preposition — By / With / From / For, context-gated.
- Action / product — Get / Use / Try / Ask / Join.
- Contact / communication — Hello / Hey.
- Possessive — My / Our / Your.
- Descriptor after root — Studio / Lab / Works / House / Co / App / AI.

Each construction has a fixed grammatical direction. For example, `By Lark` is a curated relation form; `Lark By` is not generated as an equivalent option.

## Whole-name meaning contract

Every curated construction must expose:

- full phrase,
- EN interpretation of the whole construction,
- PL interpretation of the whole construction,
- semantic / construction class,
- recommendation tier,
- tone,
- explicit warning when the direction is abstract or brand-dependent.

The meaning panel is shown when the user selects a construction, before treating the domain as a viable brand choice.

## Available-first with quality floor

The Workshop checks a deeper candidate pool and targets 6–8 strong available `.com` directions.

If fewer than six strong free directions exist, Mianem must say so. It must not lower the linguistic/semantic threshold or promote nonsense simply to fill the screen.

Taken domains may be revealed as inspiration but are hidden by default and never influence the recommendation tier.
