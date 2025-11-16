import asyncio
import json
from typing import Optional
import httpx

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2:3b"

def parse_ollama_stream(raw_text: str) -> str:
    """
    Ollama /api/generate returns **multiple JSON objects**, one per token.
    This function extracts all `response` fields and concatenates them.
    """
    output = []
    for line in raw_text.splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if "response" in obj:
                output.append(obj["response"])
        except json.JSONDecodeError:
            # ignore malformed lines
            continue
    return "".join(output)

async def query_llama(prompt: str,
                      model: str = MODEL_NAME,
                      max_tokens: int = 512,
                      timeout: int = 120) -> str:
    """
    Send prompt to local Ollama server and return the full generated text.
    IMPORTANT: Ollama returns streaming JSON → must manually parse.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        r.raise_for_status()

        raw_text = r.text  # streaming JSON, not a single JSON object
        cleaned = parse_ollama_stream(raw_text)
        return cleaned