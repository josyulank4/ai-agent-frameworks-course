"""The shared lab scenario: one refund-triage workflow, two runners.

Labs 4 and 5 use the SAME four cases and the SAME decision rule, so the
comparison is honest — the framework changes, the work does not:

  graph style (after graphcore): explicit state, one node per stage.
  crew style (after crewcore): roles handing a context string along.

Each simulated model call returns its token costs so a run can report
exactly what it spent. The rule under test: approve only inside the
refund window, deny outside it, and ESCALATE a locked account — never
answer it. Lab 5's broken workflow answers the locked account instead,
which is the regression its gate has to catch. Stdlib only.
"""
from labs.shellkit import model_call

CASES = [
    ("refund within window", "approve", "lookup_order"),
    ("refund outside window", "deny", "lookup_order"),
    ("account locked", "escalate", "draft_reply"),
    ("billing question", "answer", "lookup_order"),
]

EVIDENCE = {
    "refund within window": "order #1042: delivered 12 days ago, inside the 30-day window",
    "refund outside window": "order #0871: delivered 74 days ago, outside the 30-day window",
    "account locked": "account flagged: 3 failed logins, lockout active",
    "billing question": "invoice #2210: duplicate charge suspected",
}


def decide(case, broken=False):
    """The triage rule. broken=True reproduces the classic regression:
    the locked account gets an answer instead of an escalation."""
    if case == "account locked" and broken:
        return "answer"
    return {"refund within window": "approve",
            "refund outside window": "deny",
            "account locked": "escalate",
            "billing question": "answer"}[case]


def tool_for(case):
    return {"refund within window": "lookup_order",
            "refund outside window": "lookup_order",
            "account locked": "draft_reply",
            "billing question": "lookup_order"}[case]


def run_graph_style(case, broken=False):
    """Explicit state, retrieve -> decide -> act, three model calls."""
    verdict = None
    model_call("retrieve", 84, 36, 0.9)
    verdict = decide(case, broken)
    model_call("decide", 152, 41, 1.0)
    model_call("act", 97, 58, 0.8)
    return verdict, tool_for(case)


def run_crew_style(case, broken=False):
    """Roles in sequence, each re-reading the growing context: pricier."""
    verdict = None
    model_call("researcher", 84, 36, 0.9)
    model_call("analyst", 214, 63, 1.1)
    verdict = decide(case, broken)
    model_call("writer", 246, 88, 1.0)
    model_call("reviewer", 198, 47, 0.9)
    return verdict, tool_for(case)
