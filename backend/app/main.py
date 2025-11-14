from fastapi import FastAPI
from .db import init_db
from .routes import runs

app = FastAPI(title="6G-Valid8")

@app.get("/")
def read_root():
    return {"message": "Welcome to the 6G-Valid8 API"}


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(runs.router, prefix="/runs", tags=["runs"])

