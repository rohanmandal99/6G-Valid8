from .models import Run, Event, Procedure
from .llm_client import query_llama
from typing import List, Dict
import asyncio

async def generate_run_summary_async(run: Run, events: List[Event], procedures: List[Procedure]) -> Dict:
    """
    Returns AI summary including structured info + LLM note (Ollama).
    """
    # Build structured summary
    component_summary = {}
    for event in events:
        if event.component not in component_summary:
            component_summary[event.component] = {}
        if event.event_type not in component_summary[event.component]:
            component_summary[event.component][event.event_type] = 0
        component_summary[event.component][event.event_type] += 1

    # Build payload for LLM
    run_payload = {
        "run": {
            "id": run.id,
            "name": run.name,
            "timestamp": str(run.timestamp),
            "events": [{"component": e.component, "type": e.event_type, "msg": e.msg} for e in events],
            "procedures": [{"name": p.name} for p in procedures],
        }
    }

    prompt = f"""
        You are an expert 5G/6G RAN analyst.  
        You read UE logs and produce human-quality engineering insights.

        Generate a **crisp technical summary** of this run with:
        1. High-level explanation
        2. Important events and what they mean
        3. Potential issues or anomalies
        4. Next steps the engineer should check
        5. A 1–sentence executive summary

        ### Run Info
        ID: {run.id}
        Name: {run.name}
        Timestamp: {run.timestamp}

        ### Events:
        {[ (e.component, e.event_type, e.msg) for e in events ]}

        ### Procedures:
        {[ (p.name, p.status) for p in procedures ]}

        Now produce a **professional, insightful, domain-aware** interpretation.
        Do NOT simply restate the events.  
        Infer what is happening (e.g., “UE started RACH but no PDCCH yet”, “SSB detected but no PRACH attempt”, etc.)

        Output format:

        **Executive Summary:** <one sentence>

        **Technical Breakdown:**
        - <insight 1>
        - <insight 2>
        - <insight 3>

        **Events Interpreted:**
        - <event → meaning>

        **Potential Issues:**
        - <issue or 'None detected'>

        **Next Steps:**
        - <engineer actions>
    """
    ai_note = await query_llama(prompt)
    
    return {
        "total_events": len(events),
        "total_procedures": len(procedures),
        "component_summary": component_summary,
        "example_ai_note": ai_note
    }