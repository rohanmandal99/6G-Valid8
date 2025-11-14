# backend/app/db.py
import sqlite3
import json
from datetime import datetime

DB_PATH = "backend/data/valid8.db"

# Initialize tables
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        created_at TEXT,
        source_file TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        ts TEXT,
        component TEXT,
        event_type TEXT,
        msg TEXT,
        metrics_json TEXT,
        FOREIGN KEY(run_id) REFERENCES runs(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS procedures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        name TEXT,
        result_json TEXT,
        FOREIGN KEY(run_id) REFERENCES runs(id)
    )
    """)

    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB_PATH)
