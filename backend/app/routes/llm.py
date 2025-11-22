# backend/app/routes/llm.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.llm_client import analyze_events_llm

router = APIRouter(prefix="/llm")

class LLMPayload(BaseModel):
    events: list  # The parsed log JSON from frontend

@router.post("/analyze")
async def analyze(payload: LLMPayload):
    result = await analyze_events_llm(payload.dict())
    return {"summary": result}