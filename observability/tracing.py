"""One trace schema for every framework (Lesson 43 demo).

Runs, steps, tool calls, tokens and cost in a single record you own;
secrets are redacted before storage. Stdlib only.
"""
import re
SECRET = re.compile(r"(sk-[A-Za-z0-9]+|password=\S+)")
def redact(text):
    return SECRET.sub("[REDACTED]", text)
class Trace:
    def __init__(self, run_id, workflow):
        self.run_id, self.workflow, self.steps = run_id, workflow, []
    def step(self, name, tokens, cost, note=""):
        self.steps.append({"step": name, "tokens": tokens, "cost": cost, "note": redact(note)})
    @property
    def total_tokens(self): return sum(s["tokens"] for s in self.steps)
    @property
    def total_cost(self): return round(sum(s["cost"] for s in self.steps), 4)
def main():
    t = Trace("run-118", "incident-triage")
    t.step("retrieve", 820, 0.0041, "queries ran with key sk-abc123")
    t.step("reason", 1240, 0.0062)
    t.step("tool:lookup_order", 210, 0.0011)
    print("trace: run-118 incident-triage")
    for s in t.steps: print(f"  {s}")
    print(f"total tokens: {t.total_tokens}")
    print(f"total cost: ${t.total_cost}")
    print("secrets in stored trace: 0 (redacted before storage)")
    print("tracing demo complete")
if __name__ == "__main__":
    main()
