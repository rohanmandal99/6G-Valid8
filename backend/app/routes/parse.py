from fastapi import APIRouter, UploadFile, File
from backend.app.log_parser import parse_log_data

router = APIRouter(prefix="/parse")

@router.post("/logfile")
async def parse_log_file(file: UploadFile = File(...)):
    content = (await file.read()).decode(errors="ignore")

    result = parse_log_data(content)  # Your parser returns JSON/dict

    return {"filename": file.filename, "parsed": result}