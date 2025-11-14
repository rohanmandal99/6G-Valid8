from fastapi import APIRouter, UploadFile
from ..log_parser import parse_log_data  # Keep this, it's fine, just needs correct relative path
from ..db import get_db  # Same with this import
import json
import time

router = APIRouter()

@router.post("/upload_log")
async def upload_log(file: UploadFile):
    raw = await file.read()
    text = raw.decode("utf-8")

    # 1. Parse
    parsed = parse_log_data(text)
    events = parsed["events"]
    procedures = parsed["procedures"]

    conn = get_db()
    cur = conn.cursor()

    # 2. Create run entry
    cur.execute(
        "INSERT INTO runs (name, created_at, source_file) VALUES (?, ?, ?)",
        (file.filename, time.strftime("%Y-%m-%d %H:%M:%S"), file.filename)
    )
    run_id = cur.lastrowid

    # 3. Insert events
    for e in events:
        cur.execute("""
            INSERT INTO events (run_id, ts, component, event_type, msg, metrics_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            e["ts"],
            e["component"],
            e["event_type"],
            e["message"],
            json.dumps(e["metrics"])
        ))

    # 4. Insert procedures (RA, etc.)
    for pname, pdata in procedures.items():
        cur.execute("""
            INSERT INTO procedures (run_id, name, result_json)
            VALUES (?, ?, ?)
        """, (
            run_id,
            pname,
            json.dumps(pdata)
        ))

    conn.commit()
    conn.close()

    return {
        "status": "stored",
        "run_id": run_id,
        "events": len(events),
        "procedures": list(procedures.keys())
    }

# backend/app/api_runs.py

@router.get("/{run_id}")
async def get_run(run_id: int):
    conn = get_db()
    cur = conn.cursor()
    
    # Fetch the run details
    cur.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
    run = cur.fetchone()
    
    if not run:
        return {"error": "Run not found"}

    # Fetch events for the run
    cur.execute("SELECT * FROM events WHERE run_id = ?", (run_id,))
    events = cur.fetchall()

    # Fetch procedures for the run
    cur.execute("SELECT * FROM procedures WHERE run_id = ?", (run_id,))
    procedures = cur.fetchall()

    conn.close()

    # Return all the data for this run
    return {
        "run_id": run_id,
        "run_name": run[1],  # assuming name is at index 1
        "created_at": run[2],
        "events": events,
        "procedures": procedures
    }

