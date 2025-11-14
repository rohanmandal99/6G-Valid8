# backend/app/api_runs.py
from fastapi import APIRouter, UploadFile, BackgroundTasks
from ..log_parser import parse_log_data
from ..db import get_db
import json
import time
import tempfile
import os

router = APIRouter()

def process_log_file(file_path: str, file_name: str):
    """
    Background task: parse log file and insert into DB.
    """
    # Read file line by line to reduce memory usage
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        log_data = f.read()  # For MVP, still read full file. Can switch to streaming parsing later.

    parsed = parse_log_data(log_data)
    events = parsed["events"]
    procedures = parsed["procedures"]

    conn = get_db()
    cur = conn.cursor()

    # Create run entry
    cur.execute(
        "INSERT INTO runs (name, created_at, source_file) VALUES (?, ?, ?)",
        (file_name, time.strftime("%Y-%m-%d %H:%M:%S"), file_name)
    )
    run_id = cur.lastrowid

    # Batch insert events
    event_rows = [
        (run_id, e["ts"], e["component"], e["event_type"], e["message"], json.dumps(e["metrics"]))
        for e in events
    ]
    cur.executemany(
        "INSERT INTO events (run_id, ts, component, event_type, msg, metrics_json) VALUES (?, ?, ?, ?, ?, ?)",
        event_rows
    )

    # Insert procedures
    proc_rows = [
        (run_id, pname, json.dumps(pdata)) for pname, pdata in procedures.items()
    ]
    cur.executemany(
        "INSERT INTO procedures (run_id, name, result_json) VALUES (?, ?, ?)",
        proc_rows
    )

    conn.commit()
    conn.close()

    # Optional: remove temp file after processing
    os.remove(file_path)

@router.post("/upload_log")
async def upload_log(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Upload a log file.
    Parsing & DB insertion is done in the background for large files.
    Returns a run_id immediately.
    """
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
        while chunk := await file.read(1024*1024):  # 1 MB chunks
            tmp.write(chunk)
        tmp_path = tmp.name

    # Schedule background processing
    background_tasks.add_task(process_log_file, tmp_path, file.filename)

    # Immediate response
    return {
        "status": "processing",
        "message": "Log is being parsed in background",
        "file_name": file.filename
    }
