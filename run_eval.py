import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from agent import resolve_ticket

with open("eval/scenarios.json") as f:
    scenarios = json.load(f)

results = []
for s in scenarios:
    r = resolve_ticket(s["input"])
    passed = r["resolution"] == s["expected_action"]
    results.append({"name": s["name"], "passed": passed, "expected": s["expected_action"], "got": r["resolution"]})

for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"[{status}] {r['name']} (expected={r['expected']}, got={r['got']})")

pass_rate = sum(r["passed"] for r in results) / len(results)
print(f"\nOverall pass rate: {pass_rate*100:.0f}%")