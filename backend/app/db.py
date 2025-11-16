from sqlmodel import SQLModel, create_engine, Session
import os

DB_FILE = "backend/app/data/valid8.db"
DB_URL = f"sqlite:///{DB_FILE}"

# Ensure the data directory exists
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# Create engine
engine = create_engine(DB_URL, echo=True)

def init_db():
    """Initialize the database and create tables."""
    from .models import Run, Event, Procedure
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI dependency for DB session."""
    with Session(engine) as session:
        yield session