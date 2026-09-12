from app.service import NameLabService


def test_extract_dropped_domains_only():
    raw = "Dixeia.com, HELLO.NET\nLampetis.com; bad-name.com\nPanacra.COM"
    got = NameLabService._extract_dropped_names(raw)
    assert got == ["dixeia", "lampetis", "panacra"]


def test_extract_bare_names_when_no_domains():
    raw = "Dixeia\nLampetis, Panacra | bad-name"
    got = NameLabService._extract_dropped_names(raw)
    assert got == ["dixeia", "lampetis", "panacra"]
