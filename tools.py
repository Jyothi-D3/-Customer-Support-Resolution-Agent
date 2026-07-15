import json
import os

ORDERS_PATH = os.path.join(os.path.dirname(__file__), "orders.json")
TICKETS_PATH = os.path.join(os.path.dirname(__file__), "tickets.json")

GOODWILL_CAP = 10.00
REFUND_THRESHOLD = 50.00


def order_lookup(order_id: str) -> dict:
    with open(ORDERS_PATH) as f:
        orders = json.load(f)
    order = orders.get(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    return {"order_id": order_id, **order}


def apply_credit(order_id: str, amount: float) -> dict:
    """Gated tool: only succeeds within the goodwill cap."""
    if amount > GOODWILL_CAP:
        return {
            "status": "needs_approval",
            "reason": f"Amount ${amount} exceeds goodwill cap of ${GOODWILL_CAP}",
        }
    return {"status": "applied", "order_id": order_id, "amount": amount}


def create_ticket(payload: dict) -> dict:
    """Simulates escalation to a human agent."""
    tickets = []
    if os.path.exists(TICKETS_PATH):
        with open(TICKETS_PATH) as f:
            tickets = json.load(f)
    ticket_id = f"T{len(tickets) + 1:04d}"
    record = {"ticket_id": ticket_id, **payload}
    tickets.append(record)
    with open(TICKETS_PATH, "w") as f:
        json.dump(tickets, f, indent=2)
    return {"ticket_id": ticket_id, "status": "escalated"}