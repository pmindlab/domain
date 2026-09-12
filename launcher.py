from __future__ import annotations

import os
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = ROOT / ".env"

if ENV.exists():
    for raw in ENV.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def open_browser() -> None:
    time.sleep(1.1)
    webbrowser.open("http://127.0.0.1:8787")


if __name__ == "__main__":
    import uvicorn
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8787, reload=False)
