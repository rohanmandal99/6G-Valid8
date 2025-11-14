# backend/app/crud.py - This layer isolates DB logic, so FastAPI routes stay clean
from datetime import datetime
from sqlmodel import Session, select
from .models import Run, Event

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
