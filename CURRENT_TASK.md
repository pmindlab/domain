# Current Task

TASK_ID: mianem-windows-portable-startup-remediation-2026-09-12

Status: root cause confirmed; corrected single-executable build pending final Windows CI and Human Owner retest.

## Trigger
The first Windows portable build passed CI and a narrow packaged `--smoke-test`, but on a second Windows computer the real launch failed and the launcher showed only the generic message `Mianem nie może się uruchomić`. The original QA gate did not exercise Uvicorn startup inside the windowed frozen executable.

## Confirmed root cause
The strengthened packaged-server test reproduced the failure on `windows-latest` and exposed the traceback:

`ValueError: Unable to configure formatter 'default'`

caused by Uvicorn's default logging formatter calling `.isatty()` on a `None` console stream in a PyInstaller `console=False` executable.

This was a launcher/runtime logging bug, not missing Python on the user's computer and not a reason to require installation or administrator access.

## Remediation
- Keep the simple PyInstaller single-executable portable package.
- Create Uvicorn with `log_config=None` so a windowed executable does not attempt to configure console-dependent formatters.
- Add a packaged `--server-smoke-test` that must start the local server and receive `ok=true`, `app=Mianem` from `/api/health` before the ZIP can be produced.
- Keep the existing frozen data-loading smoke test.
- Capture server-thread failures and write `%LOCALAPPDATA%\PMindLab\Mianem\startup-error.txt`.
- Show the real exception in the GUI failure dialog instead of the old generic re-extraction message.
- Preserve local-only binding to `127.0.0.1` and local mutable state under `%LOCALAPPDATA%\PMindLab\Mianem`.

## QA gates
- Existing repository CI remains green.
- Single-file PyInstaller build succeeds on `windows-latest`.
- `Mianem.exe --smoke-test` succeeds.
- `Mianem.exe --server-smoke-test` starts the packaged local server and reaches `/api/health` successfully.
- Final ZIP and SHA-256 are produced only after both packaged smoke tests pass.
- Human Owner re-tests the new ZIP on the same second Windows computer that exposed the original failure.

## Product invariants
Packaging only. Naming, scoring, `.com` availability, brand-screening and Workshop-curation behavior must not change. No local DB, custom niches, `.env`, API keys or other secrets may be bundled.
