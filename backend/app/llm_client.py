# backend/app/llm_client.py
import asyncio
import json
from typing import Any, Dict
import httpx

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2:3b"

def parse_ollama_stream(raw_text: str) -> str:
    output = []
    for line in raw_text.splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if "response" in obj:
                output.append(obj["response"])
        except json.JSONDecodeError:
            continue
    return "".join(output)

async def query_llama(prompt: str, model: str = MODEL_NAME, max_tokens: int = 512, timeout: int = 120) -> str:
    payload = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        r.raise_for_status()
        raw_text = r.text
        return parse_ollama_stream(raw_text)

async def analyze_events_llm(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    events = parsed_data.get("events", [])
    procedures = parsed_data.get("procedures", {})

    system_prompt = """
    You are a 5G/NR/6G telecom protocol and PHY expert. 
    You analyze modem logs, detect anomalies, correlate PHY/MAC/RRC layers,
    and generate engineering-quality debugging insights.

    You MUST return ONLY valid JSON following EXACTLY this structure:

    {
    "observations": [],
    "triage_suggestions": [],
    "anomalies": [],
    "recommendations": []
    }

    Rules:
    - Absolutely NO markdown, NO explanations, NO extra keys.
    - Output must be STRICT JSON only.
    - Observations must be engineering-significant, not just repetitions.
    - Anomalies highlight unexpected or suspicious behavior.
    - Triage suggestions must be actionable debugging steps.
    - Recommendations give high-level next steps.
    - Use only provided logs for reasoning.
    """

    user_prompt = f"""
    Analyze the following modem events and RA procedure.

    Events:
    {json.dumps(events, indent=2)}

    RA procedure:
    {json.dumps(procedures.get("ra", {}), indent=2)}

    Return ONLY the JSON using the required structure.
    """

    # Combine for Ollama
    prompt = f"SYSTEM:\n{system_prompt}\n\nUSER:\n{user_prompt}"

    llm_text = await query_llama(prompt)

    # --- Extract JSON from LLM output ---
    json_start = llm_text.find("{")
    json_end = llm_text.rfind("}")

    extracted = "{}"
    if json_start != -1 and json_end != -1:
        extracted = llm_text[json_start : json_end + 1]

    try:
        structured = json.loads(extracted)
    except Exception:
        structured = {}

    return {
        "observations": structured.get("observations") or [{"description": "No observations available"}],
        "triage_suggestions": structured.get("triage_suggestions") or [{"description": "No triage suggestions available"}],
        "anomalies": structured.get("anomalies") or [{"description": "No anomalies detected"}],
        "recommendations": structured.get("recommendations") or [{"description": "No recommendations available"}],
    }