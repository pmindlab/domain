# Current Task

TASK_ID: mianem-windows-portable-startup-remediation-2026-09-12

Status: remediation in progress after real-machine startup failure.

## Trigger
The first Windows portable build passed CI and a narrow packaged `--smoke-test`, but on a second Windows computer the real GUI launch failed and the launcher showed only the generic message `Mianem nie może się uruchomić`. The original QA gate therefore did not cover the actual user startup path.

## Remediation
- Replace the PyInstaller single-file runtime with a portable `onedir` package so startup does not depend on extracting the whole application to a temporary directory.
- Keep `Mianem.exe` plus its `_internal` runtime folder together inside the ZIP; no Python installation is required.
- Add a real packaged startup smoke test on `windows-latest`: launch the normal GUI executable and require the local `/api/health` endpoint to become ready before packaging.
- Keep the existing frozen data-loading smoke test.
- Preserve local-only binding to `127.0.0.1` and mutable state under `%LOCALAPPDATA%\PMindLab\Mianem`.

## QA gates
- Existing repository CI remains green.
- PyInstaller `onedir` build succeeds on `windows-latest`.
- `Mianem.exe --smoke-test` succeeds from the packaged folder.
- A normal packaged `Mianem.exe` process starts successfully and `/api/health` responds with `ok=true` and `app=Mianem`.
- Final ZIP is generated with SHA-256 and then re-tested by Human Owner on the second Windows computer.

## Product invariants
Packaging only. Naming, scoring, `.com` availability, brand-screening and Workshop-curation behavior must not change. No local DB, custom niches, `.env`, API keys or other secrets may be bundled.
