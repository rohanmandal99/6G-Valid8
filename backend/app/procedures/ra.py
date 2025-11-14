# backend/app/procedures/ra.py - Random Access Procedure

import re

class RAProcedureParser:
    """
    Parse CBRA RA procedure:
    - Detect Msg1, Msg2, Msg3, Msg4
    - Track RNTI
    - Mark success/failure
    """

    RNTI_RE = re.compile(r"(C-RNTI|rnti)[^\dA-Fa-f]*([0-9A-Fa-f]{2,4})")

    def __init__(self):
        self.reset()

    def reset(self):
        self.active = False
        self.data = {
            "msg1": False,
            "msg2": False,
            "msg3": False,
            "msg4": False,
            "rnti": None,
            "errors": [],
            "messages": [],
        }

    # Incoming event = {ts, component, message, event_type, metrics}
    def consume(self, ev):
        msg = ev["message"]

        # Msg1: PRACH
        if ev["event_type"] == "prach":
            self.active = True
            self.data["msg1"] = True
            self.data["messages"].append(msg)

        # Msg2: RAR
        if "RAR" in msg or ev["event_type"] == "rar":
            if self.active:
                self.data["msg2"] = True
                self.data["messages"].append(msg)

        # Msg3: PUSCH
        if "Msg3" in msg:
            if self.active:
                self.data["msg3"] = True
                self.data["messages"].append(msg)

        # Msg4: contention resolution
        if "Contention Resolution" in msg or "msg4" in msg.lower():
            if self.active:
                self.data["msg4"] = True
                self.data["messages"].append(msg)
                self.active = False  # RA done

        # Extract RNTI
        m = self.RNTI_RE.search(msg)
        if m:
            self.data["rnti"] = m.group(2)

        # Errors
        if ev["event_type"] == "error":
            self.data["errors"].append(msg)

    def result(self):
        return self.data