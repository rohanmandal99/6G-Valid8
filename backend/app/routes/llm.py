# backend/app/routes/llm.py
from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/health")
async def llm_health():
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get("http://localhost:11434/api/tags")
            return {"ok": r.status_code == 200, "models": r.json()}
    except Exception as e:
        return {"ok": False, "error": str(e)}