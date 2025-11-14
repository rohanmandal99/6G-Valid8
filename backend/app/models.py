# backend/app/models.py
from typing import Optional, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime
    source_file: str

    events: list["Event"] = Relationship(back_populates="run")


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: int = Field(foreign_key="run.id")
    ts: Optional[datetime] = None
    component: Optional[str] = None
    layer: Optional[str] = None
    msg: str
    metrics_json: Dict = Field(default_factory=dict)

    run: Run = Relationship(back_populates="events")