# Mianem

**Mianem v1.5.0** is a local PMindLab naming research engine and interactive naming workshop for finding brandable names with an actually available `.com`.

It searches real biological taxa and curated real-language words, ranks them for brand quality, checks `.com` availability, screens likely brand collisions, and lets a human develop a promising root into a semantically coherent two-word name.

## Product rules

- prefer real words / real taxa over artificial startup blends,
- focus on short, pronounceable, memorable candidates,
- no aftermarket, auctions, brokers, redemption or merely expiring domains,
- Dropped results are shown only after the domain is actually available again,
- two-word construction is curated semantically rather than brute-forcing random pairs,
- negative meanings are blocked before a two-word domain check,
- brand screening is triage, not legal trademark clearance.

## Current search sources

### Biology
Mianem includes a growing catalog of biological areas such as butterflies, dragonflies, hummingbirds, jewel beetles, fireflies, nudibranchs, ctenophores, corals and related groups. Taxonomy discovery uses GBIF.

### Languages
Curated real-word sources currently include English, Polish, Spanish, French, Latin and Mandarin Hanyu Pinyin. Words with diacritics keep their source spelling in metadata while the `.com` candidate uses an ASCII form.

## Mianem v1.5 — Naming Workshop

A one-word result is no longer the end of the process. Open **Warsztat** from any candidate or type a root manually.

The workshop shows:

- English and Polish meaning/context when the local semantic dictionary knows the root,
- tone and visual associations,
- a small curated set of words that fit **before** the root,
- a small curated set of words that fit **after** the root,
- semantic compatibility score and explanation,
- negative-root screening before any network request,
- live `.com` status after the human selects a pair,
- brand screening for an available pair.

Example path: `lark` → `dawn + lark` → `dawnlark.com` → live availability → brand screen.

The workshop deliberately keeps the human in the loop. It does not generate thousands of random combinations.

### Length controls
Search length is now entered directly as **Min / Max**, with an optional **Dokładnie** value that overrides the range.

## Run locally

### Windows

Double-click:

```text
run.bat
```

Mianem opens at:

```text
http://127.0.0.1:8787
```

### macOS / Linux

```bash
chmod +x run.sh
./run.sh
```

## Development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Run manually:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8787 --reload
```

CI also syntax-checks the modular v1.5 JavaScript with `node --check`.

## Optional environment variables

Copy `.env.example` to `.env` when needed.

- `GITHUB_TOKEN` — higher GitHub search limits.
- `BRAVE_SEARCH_API_KEY` — broader web/brand screening.
- `HTTP_TIMEOUT` — outbound request timeout.
- `MAX_CONCURRENCY` — outbound concurrency limit.

The application works without optional API keys. Without Brave, brand screening is narrower and GitHub-focused.

## Local data

User decisions and research history remain stored in the legacy-compatible local SQLite file `data/namelab.db`. Custom user-added niches are stored locally in `data/custom_niches.json`.

Both files are ignored by Git and are not part of the repository. The legacy filename is intentionally retained so the product rename does not discard existing local history.

## Design

- light background: `#FAFAF7`
- text: black
- PMind: `#26588C`
- Lab: `#16325C`
- monospace typography
- persistent light/dark mode
- PMindLab header uses the supplied SVG asset in `app/static/logo.svg`

## Repository workflow

Canonical repository: `pmindlab/mianem`.

AI/developer agents should read `AGENTS.md`, `PROJECT_STATE.md`, and `CURRENT_TASK.md` before substantial changes.
