from app.db import Store
from app.models import Candidate

def test_decision_roundtrip(tmp_path):
    s = Store(tmp_path / "x.db")
    c = Candidate(name="Dixeia", domain="dixeia.com", niche="butterflies", score=88)
    s.upsert_many([c])
    s.set_decision("Dixeia", "shortlist", "nice")
    row = s.get("Dixeia")
    assert row["decision"] == "shortlist"
    assert row["note"] == "nice"
