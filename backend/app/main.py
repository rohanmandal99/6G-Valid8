from fastapi import FastAPI
from .db import init_db
from .routes import runs

app = FastAPI(title="Valid8 Backend")

# Create tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Include routes
app.include_router(runs.router)