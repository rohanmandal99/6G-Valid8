from backend.app.db import init_db
from backend.app.routes import runs
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="6G-Valid8 Backend")


# Allow React dev server to access
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def home():
    return {"status": "6G-Valid8 Backend Running"}

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(runs.router)