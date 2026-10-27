import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "data" / "ghosttrace.db"

def connect():
    DB.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def initialize():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filetype TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            risk TEXT NOT NULL,
            score INTEGER NOT NULL,
            findings TEXT NOT NULL,
            scanned_at TEXT NOT NULL DEFAULT (datetime('now'))
        )""")

def save_scan(filename, filetype, sha256, risk, score, findings):
    import json
    with connect() as con:
        con.execute("INSERT INTO scans(filename,filetype,sha256,risk,score,findings) VALUES(?,?,?,?,?,?)",
                    (filename,filetype,sha256,risk,score,json.dumps(findings)))

def get_scans():
    import pandas as pd
    with connect() as con:
        return pd.read_sql_query("SELECT * FROM scans ORDER BY id DESC", con)

def clear_scans():
    with connect() as con:
        con.execute("DELETE FROM scans")

def load_demo_scans():
    """Import 50 clearly synthetic demo records once, without overwriting user scans."""
    import csv
    source = DB.parent / "sample_scans_50.csv"
    with connect() as con:
        existing = con.execute("SELECT COUNT(*) FROM scans WHERE filename LIKE 'demo_evidence_%'").fetchone()[0]
        if existing:
            return 0
        with source.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        con.executemany(
            "INSERT INTO scans(filename,filetype,sha256,risk,score,findings,scanned_at) VALUES(?,?,?,?,?,?,?)",
            [(r["filename"],r["filetype"],r["sha256"],r["risk"],int(r["score"]),r["findings"],r["scanned_at"]) for r in rows]
        )
        return len(rows)
