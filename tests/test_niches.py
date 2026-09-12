import json
from pathlib import Path

from app.niche_catalog import NicheCatalog
from app.service import NameLabService


def test_builtin_catalog_is_broad():
    service = NameLabService()
    niches = service.list_niches()
    assert len(niches) >= 60
    groups = {n["group"] for n in niches}
    assert {"Insects", "Birds", "Marine", "Plants"}.issubset(groups)
    assert any(n["key"] == "jewel_beetles" and n["default"] for n in niches)


def test_custom_niche_roundtrip(tmp_path):
    builtin = tmp_path / "niches.json"
    custom = tmp_path / "custom.json"
    builtin.write_text(json.dumps([
        {"key":"birds","taxon":"Aves","label":"birds","group":"Birds","default":True}
    ]), encoding="utf-8")
    custom.write_text("[]", encoding="utf-8")
    catalog = NicheCatalog(builtin, custom)
    added = catalog.add_custom("Alcedinidae", "kingfishers", "Birds")
    assert added.key.startswith("custom_kingfishers")
    assert catalog.get(added.key).taxon == "Alcedinidae"
    assert catalog.remove_custom(added.key) is True
    assert catalog.get(added.key) is None
