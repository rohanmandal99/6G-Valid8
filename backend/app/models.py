from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.types import JSON
from typing import Optional, List
from datetime import datetime

class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    events: List["Event"] = Relationship(back_populates="run")
    procedures: List["Procedure"] = Relationship(back_populates="run")  # <-- add this

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: int = Field(foreign_key="run.id")
    component: str
    event_type: str
    msg: str
    metrics_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    run: Optional[Run] = Relationship(back_populates="events")

class Procedure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: int = Field(foreign_key="run.id")
    name: str
    run: Optional[Run] = Relationship(back_populates="procedures")  # <-- matches Run.procedures
    