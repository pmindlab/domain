from __future__ import annotations

import importlib.util
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "packaging" / "windows" / "launcher_windows.py"
SPEC = importlib.util.spec_from_file_location("mianem_windows_launcher", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
portable_launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(portable_launcher)


def test_portable_runtime_uses_bundled_defaults_and_local_mutable_state(tmp_path, monkeypatch):
    defaults = ROOT / "data"
    state = tmp_path / "state"

    for key in (
        "NAMELAB_DB",
        "NAMELAB_CUSTOM_NICHES",
        "NAMELAB_PROFILE",
        "NAMELAB_NICHES",
        "MIANEM_STATE_DIR",
    ):
        monkeypatch.delenv(key, raising=False)

    result = portable_launcher.configure_runtime(defaults_dir=defaults, state_dir=state)

    assert result["state_dir"] == state
    assert state.is_dir()
    assert os.environ["NAMELAB_DB"] == str(state / "namelab.db")
    assert os.environ["NAMELAB_CUSTOM_NICHES"] == str(state / "custom_niches.json")
    assert os.environ["NAMELAB_PROFILE"] == str(defaults / "profile.json")
    assert os.environ["NAMELAB_NICHES"] == str(defaults / "niches.json")


def test_portable_runtime_requires_all_seed_files(tmp_path, monkeypatch):
    defaults = tmp_path / "defaults"
    defaults.mkdir()
    (defaults / "profile.json").write_text("{}", encoding="utf-8")

    for key in (
        "NAMELAB_DB",
        "NAMELAB_CUSTOM_NICHES",
        "NAMELAB_PROFILE",
        "NAMELAB_NICHES",
    ):
        monkeypatch.delenv(key, raising=False)

    try:
        portable_launcher.configure_runtime(defaults_dir=defaults, state_dir=tmp_path / "state")
    except RuntimeError as exc:
        text = str(exc)
        assert "niches.json" in text
        assert "language_words.json" in text
        assert "seed_taxa.json" in text
    else:
        raise AssertionError("Expected missing portable seed data to block startup")
