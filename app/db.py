from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable
from .models import Candidate

SCHEMA = """
CREATE TABLE IF NOT EXISTS candidates (
    name TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    niche TEXT,
    source TEXT,
    payload TEXT NOT NULL,
    decision TEXT NOT NULL DEFAULT 'new',
    note TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_candidates_decision ON candidates(decision);

CREATE TABLE IF NOT EXISTS niche_stats (
    niche_key TEXT PRIMARY KEY,
    taxon TEXT NOT NULL,
    label TEXT NOT NULL,
    niche_group TEXT NOT NULL,
    discovered INTEGER NOT NULL DEFAULT 0,
    strong INTEGER NOT NULL DEFAULT 0,
    domain_checked INTEGER NOT NULL DEFAULT 0,
    available INTEGER NOT NULL DEFAULT 0,
    strong_rate REAL NOT NULL DEFAULT 0,
    available_rate REAL NOT NULL DEFAULT 0,
    run_count INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class Store:
    def __init__(self, path: str | Path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as con:
            con.executescript(SCHEMA)

    def upsert_many(self, candidates: Iterable[Candidate]) -> None:
        with sqlite3.connect(self.path) as con:
            for c in candidates:
                previous = con.execute(
                    "SELECT decision, note FROM candidates WHERE name=?", (c.name.lower(),)
                ).fetchone()
                if previous:
                    c.decision, c.note = previous[0], previous[1]
                payload = json.dumps(c.to_dict(), ensure_ascii=False)
                con.execute(
                    """INSERT INTO candidates(name,domain,niche,source,payload,decision,note)
                       VALUES(?,?,?,?,?,?,?)
                       ON CONFLICT(name) DO UPDATE SET domain=excluded.domain,niche=excluded.niche,
                       source=excluded.source,payload=excluded.payload,decision=excluded.decision,
                       note=excluded.note,updated_at=CURRENT_TIMESTAMP""",
                    (c.name.lower(), c.domain, c.niche, c.source, payload, c.decision, c.note),
                )

    def set_decision(self, name: str, decision: str, note: str = "") -> None:
        with sqlite3.connect(self.path) as con:
            row = con.execute("SELECT payload FROM candidates WHERE name=?", (name.lower(),)).fetchone()
            if not row:
                return
            data = json.loads(row[0])
            data["decision"] = decision
            data["note"] = note
            con.execute(
                "UPDATE candidates SET decision=?, note=?, payload=?, updated_at=CURRENT_TIMESTAMP WHERE name=?",
                (decision, note, json.dumps(data, ensure_ascii=False), name.lower()),
            )

    def list(self, decision: str | None = None) -> list[dict]:
        with sqlite3.connect(self.path) as con:
            con.row_factory = sqlite3.Row
            if decision and decision != "all":
                rows = con.execute(
                    "SELECT payload,decision,note FROM candidates WHERE decision=? ORDER BY updated_at DESC",
                    (decision,),
                ).fetchall()
            else:
                rows = con.execute(
                    "SELECT payload,decision,note FROM candidates ORDER BY updated_at DESC"
                ).fetchall()
        out = []
        for row in rows:
            data = json.loads(row["payload"])
            for legacy in ("price_status", "price", "currency"):
                data.pop(legacy, None)
            data.setdefault("acquisition_mode", "available_now")
            data["decision"] = row["decision"]
            data["note"] = row["note"]
            out.append(data)
        return out

    def get(self, name: str) -> dict | None:
        with sqlite3.connect(self.path) as con:
            row = con.execute(
                "SELECT payload,decision,note FROM candidates WHERE name=?", (name.lower(),)
            ).fetchone()
        if not row:
            return None
        data = json.loads(row[0])
        for legacy in ("price_status", "price", "currency"):
            data.pop(legacy, None)
        data.setdefault("acquisition_mode", "available_now")
        data["decision"] = row[1]
        data["note"] = row[2]
        return data

    def upsert_niche_stats(self, stats: dict) -> None:
        with sqlite3.connect(self.path) as con:
            con.execute(
                """INSERT INTO niche_stats(
                    niche_key,taxon,label,niche_group,discovered,strong,domain_checked,available,
                    strong_rate,available_rate,run_count,updated_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP)
                ON CONFLICT(niche_key) DO UPDATE SET
                    taxon=excluded.taxon,label=excluded.label,niche_group=excluded.niche_group,
                    discovered=excluded.discovered,strong=excluded.strong,domain_checked=excluded.domain_checked,
                    available=excluded.available,strong_rate=excluded.strong_rate,available_rate=excluded.available_rate,
                    run_count=niche_stats.run_count+1,updated_at=CURRENT_TIMESTAMP""",
                (
                    stats["key"], stats["taxon"], stats["label"], stats["group"],
                    int(stats.get("discovered", 0)), int(stats.get("strong", 0)),
                    int(stats.get("domain_checked", 0)), int(stats.get("available", 0)),
                    float(stats.get("strong_rate", 0)), float(stats.get("available_rate", 0)),
                ),
            )

    def niche_stats(self) -> dict[str, dict]:
        with sqlite3.connect(self.path) as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT * FROM niche_stats").fetchall()
        return {row["niche_key"]: dict(row) for row in rows}

    def delete_niche_stats(self, key: str) -> None:
        with sqlite3.connect(self.path) as con:
            con.execute("DELETE FROM niche_stats WHERE niche_key=?", (key,))
