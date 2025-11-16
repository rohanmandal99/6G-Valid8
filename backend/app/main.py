from backend.app.db import init_db
from backend.app.routes import runs
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI(title="6G-Valid8 Backend")

# Serve frontend static files
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def home():
    return {"status": "6G-Valid8 Backend Running"}

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(runs.router)