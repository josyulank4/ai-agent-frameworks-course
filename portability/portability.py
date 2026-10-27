"""One workflow, two frameworks (Lesson 26 demo).

The portability exercise: the same incident-triage workflow, fed the
same three input cases, built twice — once as a graph (nodes, a router,
checkpoints, a trace) on graphcore's engine, and once as a crew (roles,
task contracts, a ledger) in crewcore's style. One shared rubric scores
both runs, so the comparison is evidence, not opinion. Stdlib only;
both implementations are deterministic stubs — where control lives is
the subject of the lesson.
"""
from dataclasses import dataclass

from graphcore.graph_engine import Graph

CASES = [
    {"id": "INC-1", "summary": "checkout error rate doubled after deploy",
     "impact": 82, "revenue_path": True, "expected": "escalate"},
    {"id": "INC-2", "summary": "one user reports a slow dashboard",
     "impact": 12, "revenue_path": False, "expected": "queue"},
    {"id": "INC-3", "summary": "payment webhooks failing for some orders",
     "impact": 64, "revenue_path": True, "expected": "escalate"},
]
ESCALATE_IMPACT = 50

def triage_decision(case):
    """The one triage rule both implementations must honour."""
    if case["impact"] >= ESCALATE_IMPACT or case["revenue_path"]:
        return "escalate"
    return "queue"

@dataclass
class TriageState:
    case: dict = None
    draft: str = ""
    verdict: str = ""
    steps: int = 0

def _classify(state):
    state.draft = "high" if state.case["impact"] >= ESCALATE_IMPACT else "low"
    return state

def _route(state):
    return triage_decision(state.case)

def _escalate(state):
    state.verdict = "escalate"
    return state

def _queue(state):
    state.verdict = "queue"
    return state

def run_graph_triage(cases):
    decisions, total_steps = {}, 0
    for case in cases:
        g = Graph()
        g.add_node("classify", _classify)
        g.add_node("escalate", _escalate)
        g.add_node("queue", _queue)
        g.add_router("classify", _route)
        g.add_edge("escalate", "END"); g.add_edge("queue", "END")
        state = g.run(TriageState(case=case), "classify")
        decisions[case["id"]] = state.verdict
        total_steps += state.steps
    return decisions, total_steps

CREW_TASKS = [
    ("triager", "classify the incident", "severity class recorded"),
    ("responder", "apply the triage rule", "decision recorded"),
    ("reviewer", "check the decision against the rule", "decision verified"),
]

def run_crew_triage(cases):
    decisions, ledger = {}, []
    for case in cases:
        decision = ""
        for role, job, expected in CREW_TASKS:
            if role == "triager":
                output = f"{expected} [impact {case['impact']}]"
            elif role == "responder":
                decision = triage_decision(case)
                output = f"{expected} [{decision}]"
            else:
                output = f"{expected} [{decision} stands]"
            ledger.append((case["id"], role, job, output))
        decisions[case["id"]] = decision
    return decisions, ledger

def score(decisions, cases):
    return sum(1 for case in cases if decisions[case["id"]] == case["expected"])

def main():
    graph_decisions, graph_steps = run_graph_triage(CASES)
    crew_decisions, ledger = run_crew_triage(CASES)
    print("portability: incident triage, one workflow two frameworks")
    for case in CASES:
        print(f"  {case['id']}: graph={graph_decisions[case['id']]} "
              f"crew={crew_decisions[case['id']]} expected={case['expected']}")
    agree = sum(1 for case in CASES
                if graph_decisions[case["id"]] == crew_decisions[case["id"]])
    print(f"graph: {score(graph_decisions, CASES)}/{len(CASES)} decisions match expected ({graph_steps} node steps)")
    print(f"crew: {score(crew_decisions, CASES)}/{len(CASES)} decisions match expected ({len(ledger)} task executions)")
    print(f"agreement: graph and crew agree on {agree}/{len(CASES)} incidents")
    print("lesson: the workflow ports; what changes is where control lives — router vs roles")
    print("portability demo complete")

if __name__ == "__main__":
    main()
