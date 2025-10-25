from fastapi import FastAPI
from app.log_parser import parse_log_file

app = FastAPI(title="6G-Valid8 Backend")

@app.get("/")
def read_root():
    return {"message": "6G-Valid8 backend is alive!"}

@app.get("/parse-log")
def parse_log():
    log_path = "backend/sample_logs/simple_rach_log.txt"
    result = parse_log_file(log_path)
    return result
