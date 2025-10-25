import re

# Define regex patterns for key events
PATTERNS = {
    "sync_start": re.compile(r"Starting sync detection", re.IGNORECASE),
    "sync_success": re.compile(r"Initial sync successful", re.IGNORECASE),
    "rrc_connected": re.compile(r"RRC_CONNECTED", re.IGNORECASE),
    "rach_start": re.compile(r"CBRA procedure", re.IGNORECASE),
    "rach_success": re.compile(r"RA procedure succeeded", re.IGNORECASE),
    "sib1_decoded": re.compile(r"SIB1 decoded", re.IGNORECASE),
}

def parse_log_file(file_path: str) -> dict:
    """
    Reads an OAI log file and extracts key events into a structured summary.
    Returns a dictionary containing events and counts.
    """
    summary = {key: 0 for key in PATTERNS.keys()}
    total_lines = 0

    with open(file_path, "r") as f:
        for line in f:
            total_lines += 1
            for key, pattern in PATTERNS.items():
                if pattern.search(line):
                    summary[key] += 1

    summary["total_lines"] = total_lines
    return summary
