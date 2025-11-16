from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from fastapi import UploadFile, BackgroundTasks
from ..models import Run, Event, Procedure
from ..ai import generate_run_summary_async
import asyncio

router = APIRouter()

@router.get("/runs/{run_id}")
async def get_run(run_id: int, session: Session = Depends(get_session)):
    run = session.get(Run, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    events = session.exec(select(Event).where(Event.run_id == run_id)).all()
    procedures = session.exec(select(Procedure).where(Procedure.run_id == run_id)).all()
    
    ai_summary = await generate_run_summary_async(run, events, procedures)
    return {"run": run, "ai_summary": ai_summary}


@router.post("/upload_log")
async def upload_log(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    try:
        content = (await file.read()).decode("utf-8")
        # Create a Run entry
        new_run = Run(name=file.filename)
        session.add(new_run)
        session.commit()
        session.refresh(new_run)

        # Example parser (replace with real log parsing)
        # Each line: COMPONENT|TYPE|MSG
        events_to_add: List[Event] = []
        procedures_to_add: List[Procedure] = []

        for line in content.splitlines():
            parts = line.split("|")
            if len(parts) == 3:
                component, event_type, msg = parts
                events_to_add.append(Event(
                    run_id=new_run.id,
                    component=component,
                    event_type=event_type,
                    msg=msg,
                    metrics_json={}
                ))
            elif len(parts) == 2:
                # Example procedure line: NAME|STEP
                name, step = parts
                procedures_to_add.append(Procedure(
                    run_id=new_run.id,
                    name=name
                ))

        session.add_all(events_to_add)
        session.add_all(procedures_to_add)
        session.commit()

        return {"run_id": new_run.id, "status": "uploaded"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))