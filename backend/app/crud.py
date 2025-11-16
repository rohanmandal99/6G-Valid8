# backend/app/crud.py - This layer isolates DB logic, so FastAPI routes stay clean
from datetime import datetime
from sqlmodel import Session, select
from .models import Run, Event
import sqlite3
from .db import get_db
import json

def create_run(session: Session, name: str, source_file: str) -> Run:
    run = Run(
        name=name,
        created_at=datetime.utcnow(),
        source_file=source_file
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def add_event(session: Session, run_id: int, event_dict: dict) -> Event:
    ev = Event(run_id=run_id, **event_dict)
    session.add(ev)
    session.commit()
    session.refresh(ev)
    return ev


def list_runs(session: Session):
    return session.exec(select(Run)).all()


def list_events(session: Session, run_id: int):
    return session.exec(select(Event).where(Event.run_id == run_id)).all()


def store_run_summary(run_id: int, summary_text: str, metadata: dict = None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO run_summaries (run_id, summary_json, created_at)
        VALUES (?, ?, ?)
    """, (run_id, json.dumps({"summary": summary_text, "meta": metadata or {}}), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()