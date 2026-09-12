from __future__ import annotations

import json
import os
import socket
import sys
import threading
import urllib.request
import webbrowser
from pathlib import Path

APP_NAME = "Mianem"
HOST = "127.0.0.1"
PORT_RANGE = range(8787, 8800)


def _is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def runtime_dir() -> Path:
    if _is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def bundle_root() -> Path:
    if _is_frozen():
        return Path(getattr(sys, "_MEIPASS")).resolve()
    return runtime_dir()


def default_state_dir() -> Path:
    override = os.getenv("MIANEM_STATE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "PMindLab" / APP_NAME
    return Path.home() / ".mianem"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def configure_runtime(*, defaults_dir: Path | None = None, state_dir: Path | None = None) -> dict[str, Path]:
    launch_dir = runtime_dir()
    load_env_file(launch_dir / ".env")

    defaults = defaults_dir or (bundle_root() / ("data_defaults" if _is_frozen() else "data"))
    state = state_dir or default_state_dir()
    state.mkdir(parents=True, exist_ok=True)

    required = ["profile.json", "niches.json", "language_words.json", "seed_taxa.json"]
    missing = [name for name in required if not (defaults / name).exists()]
    if missing:
        raise RuntimeError(f"Brak danych aplikacji: {', '.join(missing)}")

    os.environ.setdefault("NAMELAB_DB", str(state / "namelab.db"))
    os.environ.setdefault("NAMELAB_CUSTOM_NICHES", str(state / "custom_niches.json"))
    os.environ.setdefault("NAMELAB_PROFILE", str(defaults / "profile.json"))
    os.environ.setdefault("NAMELAB_NICHES", str(defaults / "niches.json"))

    return {"launch_dir": launch_dir, "defaults_dir": defaults, "state_dir": state}


def _health_url(port: int) -> str:
    return f"http://{HOST}:{port}/api/health"


def _app_url(port: int) -> str:
    return f"http://{HOST}:{port}"


def existing_mianem_port() -> int | None:
    for port in PORT_RANGE:
        try:
            with urllib.request.urlopen(_health_url(port), timeout=0.2) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if payload.get("ok") is True and payload.get("app") == APP_NAME:
                return port
        except Exception:
            continue
    return None


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((HOST, port))
        except OSError:
            return False
    return True


def choose_port() -> int:
    for port in PORT_RANGE:
        if port_is_free(port):
            return port
    raise RuntimeError("Nie znaleziono wolnego lokalnego portu 8787–8799.")


def native_error(message: str) -> None:
    if os.name == "nt":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(None, message, APP_NAME, 0x10)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


def smoke_test() -> int:
    configure_runtime()
    from app.main import service

    if not service.list_niches():
        raise RuntimeError("Portable smoke test: brak obszarów.")
    if not service.list_languages():
        raise RuntimeError("Portable smoke test: brak źródeł językowych.")
    return 0


def run_gui() -> int:
    paths = configure_runtime()

    existing = existing_mianem_port()
    if existing is not None:
        webbrowser.open(_app_url(existing))
        return 0

    port = choose_port()

    from app import __version__
    from app.main import app
    import tkinter as tk
    from tkinter import ttk
    import uvicorn

    config = uvicorn.Config(
        app,
        host=HOST,
        port=port,
        loop="asyncio",
        http="h11",
        ws="none",
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run, name="mianem-server", daemon=True)

    root = tk.Tk()
    root.title(f"Mianem {__version__}")
    root.geometry("430x210")
    root.resizable(False, False)

    outer = ttk.Frame(root, padding=22)
    outer.pack(fill="both", expand=True)

    ttk.Label(outer, text="Mianem", font=("Segoe UI", 20, "bold")).pack(anchor="w")
    status_text = tk.StringVar(value="Uruchamiam lokalną aplikację…")
    ttk.Label(outer, textvariable=status_text, font=("Segoe UI", 10)).pack(anchor="w", pady=(8, 3))
    ttk.Label(
        outer,
        text="Dane pozostają lokalnie na tym komputerze.\nDo wyszukiwania i live .com potrzebne jest połączenie z internetem.",
        justify="left",
        foreground="#555555",
    ).pack(anchor="w", pady=(0, 14))

    actions = ttk.Frame(outer)
    actions.pack(fill="x")
    open_button = ttk.Button(actions, text="Otwórz Mianem", state="disabled")
    open_button.pack(side="left")
    stop_button = ttk.Button(actions, text="Zakończ")
    stop_button.pack(side="right")

    url = _app_url(port)
    opened = False
    stopping = False

    def open_app() -> None:
        webbrowser.open(url)

    def poll_startup() -> None:
        nonlocal opened
        if server.started:
            status_text.set(f"Gotowe · {url}")
            open_button.configure(state="normal")
            if not opened:
                opened = True
                open_app()
            return
        if not server_thread.is_alive():
            status_text.set("Nie udało się uruchomić serwera Mianem.")
            native_error("Nie udało się uruchomić Mianem. Spróbuj ponownie lub uruchom na innym komputerze.")
            return
        root.after(120, poll_startup)

    def finish_close() -> None:
        if server_thread.is_alive():
            root.after(120, finish_close)
            return
        root.destroy()

    def stop() -> None:
        nonlocal stopping
        if stopping:
            return
        stopping = True
        status_text.set("Zamykam Mianem…")
        open_button.configure(state="disabled")
        stop_button.configure(state="disabled")
        server.should_exit = True
        root.after(120, finish_close)

    open_button.configure(command=open_app)
    stop_button.configure(command=stop)
    root.protocol("WM_DELETE_WINDOW", stop)

    server_thread.start()
    root.after(120, poll_startup)
    root.mainloop()
    return 0


def main() -> int:
    try:
        if "--smoke-test" in sys.argv:
            return smoke_test()
        return run_gui()
    except Exception as exc:
        native_error(f"Mianem nie może się uruchomić.\n\n{type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
