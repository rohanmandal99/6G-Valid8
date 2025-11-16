# backend/app/llm_client.py
import asyncio
from typing import Optional
import httpx

OLLAMA_URL = "http://localhost:11434"   # default local Ollama serve URL
MODEL_NAME = "llama3.2:3b"

async def query_llama(prompt: str,
                      model: str = MODEL_NAME,
                      max_tokens: int = 512,
                      timeout: int = 120) -> str:
    """
    Send prompt to local Ollama server and return generated text.
    Uses /api/generate (non-streaming simple approach).
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        r.raise_for_status()
        data = r.json()
        # docs differ — but typical responses include 'text' or structured tokens.
        # adapt based on what your ollama version returns.
        # Try a few fallbacks:
        if isinstance(data, dict):
            if "text" in data:
                return data["text"]
            if "output" in data:
                return data["output"]
            # some versions return choices
            if "choices" in data and len(data["choices"]) > 0:
                c = data["choices"][0]
                return c.get("text") or c.get("message") or str(c)
        return str(data)

# For synchronous wrapper
# def query_llama_sync(prompt, **kwargs):
#     return asyncio.run(query_llama(prompt, **kwargs))