"""A transparent crew runner (Lesson 17 demo).

Implements CrewAI's organising ideas without magic: roles with goals,
tasks as contracts with expected outputs, sequential and hierarchical
processes, and a task ledger recording cost per successful outcome.
Stdlib only; agents are deterministic stubs.
"""
TASKS = [
    ("researcher", "gather evidence", "evidence pack: 3 sourced facts"),
    ("analyst", "assess options", "assessment: options scored"),
    ("writer", "draft the brief", "brief: decision-ready draft"),
]
def run_sequential():
    ledger = []
    context = "incident: checkout error rate doubled after deploy"
    for role, job, expected in TASKS:
        output = f"{expected} [from {role}, input: {context[:24]}...]"
        ledger.append((role, job, output))
        context = output
    return ledger
def run_hierarchical():
    plan = ["manager decomposes incident into 3 tasks", "delegates: researcher, analyst, writer", "manager reviews brief against contract"]
    return plan
def main():
    print("crew run: incident brief crew (sequential process)")
    ledger = run_sequential()
    for role, job, output in ledger:
        print(f"  task by {role}: {job} -> {output}")
    print(f"tasks completed: {len(ledger)}/3")
    print("hierarchical process plan:")
    for line in run_hierarchical(): print(f"  {line}")
    print("cost note: sequential = 3 model calls; consensual voting would cost 9 for the same brief")
    print("crew runner demo complete")
if __name__ == "__main__":
    main()
