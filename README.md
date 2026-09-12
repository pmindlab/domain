# NameLab

**NameLab v1.4.0** is a local PMindLab naming research engine for finding brandable names with an actually available `.com`.

It searches real biological taxa and curated real-language words, ranks them for brand quality, checks `.com` availability, screens likely brand collisions, and stores human decisions locally.

## Product rules

- one-word names,
- focus on short, pronounceable, memorable candidates,
- real words / real taxa preferred over artificial startup blends,
- no aftermarket, auctions, brokers, or merely expiring domains,
- Dropped results are shown only after the domain is actually available again,
- brand screening is triage, not legal trademark clearance.

## Current search sources

### Biology
NameLab includes a growing catalog of biological areas such as butterflies, dragonflies, hummingbirds, jewel beetles, fireflies, nudibranchs, ctenophores, corals and related groups. Taxonomy discovery uses GBIF.

### Languages
Curated real-word sources currently include:

- English
- Polish
- Spanish
- French
- Latin
- Mandarin (Hanyu Pinyin with source Chinese characters and meaning)

Words with diacritics keep their source spelling in metadata while the `.com` candidate uses an ASCII form.

## UX

The primary UI deliberately hides technical pipeline knobs. The user chooses:

- search areas,
- languages,
- Fast / Detailed / Deep mode,
- name length,
- grid or list view.

Advanced sample sizes, domain-check counts, brand-screening depth and score thresholds are controlled by the selected mode.

## Run locally

### Windows

Double-click:

```text
run.bat
```

NameLab opens at:

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

## Optional environment variables

Copy `.env.example` to `.env` when needed.

- `GITHUB_TOKEN` — higher GitHub search limits.
- `BRAVE_SEARCH_API_KEY` — broader web/brand screening.
- `HTTP_TIMEOUT` — outbound request timeout.
- `MAX_CONCURRENCY` — outbound concurrency limit.

The application works without optional API keys.

## Local data

User decisions and research history are stored in SQLite at `data/namelab.db`. Custom user-added niches are stored locally in `data/custom_niches.json`.

Both files are ignored by Git and are not part of the repository.

## Design

- light background: `#FAFAF7`
- text: black
- PMind: `#26588C`
- Lab: `#16325C`
- monospace typography
- persistent light/dark mode

## Repository workflow

AI/developer agents should read `AGENTS.md`, `.ai/PROJECT_STATE.md`, and `.ai/CURRENT_TASK.md` before substantial changes.
