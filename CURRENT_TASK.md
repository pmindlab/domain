# Current Task

TASK_ID: mianem-windows-portable-v1-2026-09-12

Status: implementation on build branch; pending Linux CI, Windows package build, packaged-executable smoke test and Human Owner handoff.

## Trigger
Human Owner requested a downloadable build that can be started on another Windows computer without installing Python, FastAPI or project dependencies.

## Scope
- Build a self-contained Windows 10/11 x64 `Mianem.exe` with PyInstaller.
- Keep the product local: bind only to `127.0.0.1` and open the browser automatically.
- Provide a small Windows launcher window with `Otwórz Mianem` and `Zakończ` so the local server can be stopped cleanly.
- Store mutable user state outside the executable under `%LOCALAPPDATA%\PMindLab\Mianem`.
- Bundle only canonical static/template/default-data files; do not bundle local SQLite state, custom niches, `.env`, API keys or other secrets.
- Support an optional `.env` placed next to `Mianem.exe` for the existing optional GitHub/Brave keys.
- If another Mianem instance is already running locally, open that instance instead of failing on port 8787.
- Fall back through local ports 8787–8799 if the preferred port is occupied by another process.

## Delivery contract
The downloadable artifact is a ZIP containing:
- `Mianem.exe`,
- `README-URUCHOM.txt`,
- `BUILD-INFO.txt`.

The ZIP must be built on GitHub Actions `windows-latest`, not cross-compiled on Linux. A SHA-256 sidecar must be produced.

## QA gates
- Existing repository `pytest -q` remains green.
- `tests/test_windows_portable.py` verifies separation of bundled defaults from mutable local state.
- PyInstaller build on `windows-latest` succeeds.
- The packaged `Mianem.exe --smoke-test` successfully imports the frozen application and loads niches/language sources.
- Build workflow uploads the final ZIP and SHA-256 file.

## Product invariants
Packaging must not change naming, scoring, `.com` availability, brand-screening or Workshop-curation rules. No aftermarket, auction, broker, redemption, pending-delete or merely expiring domain may be presented as available.
