import json
import os
from datetime import datetime

AUDIT_PATH = os.path.join(os.path.dirname(__file__), "audit_log.json")


def log_trace(trace: dict):
    trace["timestamp"] = datetime.utcnow().isoformat()
    logs = []
    if os.path.exists(AUDIT_PATH):
        with open(AUDIT_PATH) as f:
            logs = json.load(f)
    logs.append(trace)
    with open(AUDIT_PATH, "w") as f:
        json.dump(logs, f, indent=2)