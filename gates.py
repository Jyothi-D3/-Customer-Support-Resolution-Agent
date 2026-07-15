LEGAL_KEYWORDS = ["sue", "lawsuit", "legal action", "attorney", "chargeback", "regulator", "complaint"]
CLOSURE_KEYWORDS = ["close my account", "delete my account", "deactivate my account"]

REFUND_THRESHOLD = 50.00
GOODWILL_CAP = 10.00


def needs_human_gate(ticket_text: str, refund_amount: float = 0.0) -> dict:
    """Deterministic rule-based gate — never trust the LLM alone for this."""
    text_lower = ticket_text.lower()

    if any(k in text_lower for k in LEGAL_KEYWORDS):
        return {"gate": True, "reason": "legal_language_detected"}

    if any(k in text_lower for k in CLOSURE_KEYWORDS):
        return {"gate": True, "reason": "account_closure_request"}

    if refund_amount > REFUND_THRESHOLD:
        return {"gate": True, "reason": f"refund_amount_exceeds_threshold_${REFUND_THRESHOLD}"}

    return {"gate": False, "reason": None}


def detect_injection(ticket_text: str) -> bool:
    """Very simple heuristic — flag attempts to override policy via ticket text."""
    suspicious = ["ignore policy", "ignore the policy", "ignore previous instructions", "disregard policy"]
    return any(s in ticket_text.lower() for s in suspicious)