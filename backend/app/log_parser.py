# backend/app/log_parser.py

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# ---------------------------------------------------------
# 1. Timestamp parsing
# ---------------------------------------------------------
TS_PATTERNS = [
    re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?)"),
    re.compile(r"^\[(?P<ts>\d+\.\d+)\]"),
]

# ---------------------------------------------------------
# 2. Component extraction
# ---------------------------------------------------------
COMP_RE = re.compile(r"^\s*\[?(?P<comp>[A-Z0-9_]{2,20})\]?\s*(?P<rest>.*)", re.IGNORECASE)

# ---------------------------------------------------------
# 3. Metric regexes
# ---------------------------------------------------------
RSRP_RE = re.compile(r"RSRP\s*[:=]?\s*([-+]?\d+)", re.IGNORECASE)
SNR_RE = re.compile(r"SNR\s*[:=]?\s*([-+]?\d+(\.\d+)?)", re.IGNORECASE)
EVM_RE = re.compile(r"EVM\s*[:=]?\s*([0-9]*\.?[0-9]+)", re.IGNORECASE)

# ---------------------------------------------------------
# 4. Event classifier (light)
# ---------------------------------------------------------
EVENT_PATTERNS = [
    ("sync", re.compile(r"Initial sync|pbch decoded|synchronized", re.IGNORECASE)),
    ("prach", re.compile(r"PRACH|preamble", re.IGNORECASE)),
    ("rar", re.compile(r"RAR|Random Access Response", re.IGNORECASE)),
    ("msg3", re.compile(r"Msg3|PUSCH.*Msg3", re.IGNORECASE)),
    ("msg4", re.compile(r"Contention Resolution", re.IGNORECASE)),
    ("rrc", re.compile(r"RRC", re.IGNORECASE)),
    ("error", re.compile(r"fail|error|crc does not match", re.IGNORECASE)),
]

# ---------------------------------------------------------
# 5. Procedure modules (import here)
# ---------------------------------------------------------
from .procedures.ra import RAProcedureParser  # NEW

# ---------------------------------------------------------
# Core parsing helpers
# ---------------------------------------------------------
def _extract_timestamp(line: str):
    for p in TS_PATTERNS:
        m = p.match(line)
        if m:
            return m.group("ts")
    return None

def _extract_component_and_msg(line: str):
    original = line.strip()
    for p in TS_PATTERNS:
        m = p.match(original)
        if m:
            original = original[m.end():].strip()
            break
    m = COMP_RE.match(original)
    if m:
        return m.group("comp").upper(), m.group("rest").strip()
    return None, original

def _extract_metrics(line: str) -> Dict[str, Any]:
    metrics = {}
    if (m := RSRP_RE.search(line)):
        metrics["rsrp"] = int(m.group(1))
    if (m := SNR_RE.search(line)):
        metrics["snr"] = float(m.group(1))
    if (m := EVM_RE.search(line)):
        metrics["evm"] = float(m.group(1))
    return metrics

def _classify_event_type(line: str):
    for et, patt in EVENT_PATTERNS:
        if patt.search(line):
            return et
    return "info"

# ---------------------------------------------------------
# 6. MAIN: Parse log into events & push to procedures
# ---------------------------------------------------------
def parse_log_data(log_data: str):
    events = []
    procedures = {
        "ra": RAProcedureParser(),
        # "rrc": RRCProcedureParser(),  # future
        # "ho": HOProcedureParser(),
        # etc...
    }

    for raw_line in log_data.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        ev = {
            "ts": _extract_timestamp(line),
            "component": _extract_component_and_msg(line)[0],
            "message": _extract_component_and_msg(line)[1],
            "metrics": _extract_metrics(line),
            "event_type": _classify_event_type(line),
        }
        events.append(ev)

        # Send event to each procedure module
        for p in procedures.values():
            p.consume(ev)

    # Collect procedure summaries
    procedure_results = {name: p.result() for name, p in procedures.items()}

    return {
        "events": events,
        "procedures": procedure_results,
    }