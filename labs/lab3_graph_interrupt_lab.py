"""Hands-On Lab 3 — the human approval gate (graphcore interrupts).

Session arc: build a refund pipeline whose LAST action issues money —
and money never moves on a model's say-so. The run executes retrieve
and reason, reaches the interrupt, and STOPS: a pending-approval file
is the only thing on disk. The terminal then waits — counted aloud —
until a second shell approves (in a real deployment: a human in a UI;
here: the operator, in a second command). The run resumes, verifies
the approval is on record, and only then issues the refund. The trace
and the audit lines are the proof. A second, short run is DENIED, and
the pipeline refuses to pay. The gate is a state the run waits in —
not a comment, not a hope.
    python -m labs.lab3_graph_interrupt_lab
"""
import json
import os
import subprocess
import sys
import time

from labs.shellkit import title_card, step, say, finish

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDING = os.path.join(REPO_ROOT, "labs", ".lab3-pending.json")
LAB = 3
STEPS = 6


def worker():
    """The pipeline process. Run 1: pauses at the interrupt.
    Run 2 (after a decision file appears): verifies and acts."""
    if not os.path.exists(PENDING):
        print("  pipeline: retrieve -> reason -> INTERRUPT")
        print("  node retrieve: evidence = policy 30-day window; "
              "order #1042 delivered 12 days ago")
        print("  node reason: draft = eligible (inside the window)")
        req = {"action": "issue_refund", "order": "#1042",
               "amount": "$49.00", "draft": "eligible",
               "status": "awaiting-approval"}
        with open(PENDING, "w") as f:
            json.dump(req, f, indent=1)
        print("  INTERRUPT: refund request written to "
              "labs/.lab3-pending.json")
        print("  the run ends here — no approval, no payment")
        return 0
    req = json.load(open(PENDING))
    status = req.get("status")
    print(f"  pipeline resumed: approval record found, "
          f"status = {status}")
    if status == "approved":
        print(f"  audit: approved_by = {req['approved_by']}")
        print("  node verify: approval precedes action — order ok")
        print(f"  node act: REFUND {req['amount']} issued for order "
              f"{req['order']}")
        print("  trace: retrieve -> reason -> interrupt -> "
              "approve -> verify -> act")
    else:
        print("  node verify: NO approval on record — action refused")
        print("  node act: nothing issued; the request dies at the gate")
        print("  trace: retrieve -> reason -> interrupt -> DENIED -> stop")
    os.remove(PENDING)
    return 0


def sh(cmd, pause=0.5):
    print(f"$ {cmd}")
    time.sleep(pause)
    proc = subprocess.run(cmd, shell=True, cwd=REPO_ROOT, text=True)
    time.sleep(0.4)
    return proc.returncode


def run_worker():
    return subprocess.run(
        [sys.executable, "-c",
         "from labs.lab3_graph_interrupt_lab import worker; worker()"],
        cwd=REPO_ROOT, text=True).returncode


def takeaway():
    print()
    print("=" * 68)
    print("KEY TAKEAWAY — the gate is a state, not a comment")
    print("  irreversible actions pause the run; approval is data on disk")
    print("  verification reads the record BEFORE the action node runs")
    print("  denied is a first-class outcome: nothing issues, all is traced")
    print("=" * 68)
    time.sleep(1.0)


def main():
    if os.path.exists(PENDING):
        os.remove(PENDING)
    title_card(LAB, "The Human Approval Gate", "graphcore interrupts",
               "10")

    step(1, STEPS, "the pipeline: a refund is money, money needs a human")
    say("retrieve -> reason -> INTERRUPT -> verify -> act")
    say("the interrupt sits between deciding and paying — on purpose")

    step(2, STEPS, "run it — the pipeline stops itself")
    run_worker()
    say("the process has EXITED; the decision has not been made")

    step(3, STEPS, "inspect the pending request")
    sh(f"cat {os.path.relpath(PENDING, REPO_ROOT)}")
    say("action, order, amount, draft — everything a human needs")
    say("status: awaiting-approval. nothing has been paid")

    step(4, STEPS, "the run waits in the gate (the operator decides)")
    for i in range(1, 6):
        print(f"  ... gate holding, no payment issued ({i}/5)")
        time.sleep(1.0)
    say("in production this wait is minutes or hours — the run")
    say("does not care; its state is the file, not the process")

    step(5, STEPS, "approve from a second shell, then resume")
    sh("python3 -c \"import json; p = 'labs/.lab3-pending.json'\n"
       "d = json.load(open(p))\n"
       "d['status'] = 'approved'; d['approved_by'] = 'naveen (operator)'\n"
       "json.dump(d, open(p, 'w'), indent=1)\n"
       "print('decision recorded:', d['status'], 'by', d['approved_by'])\"")
    run_worker()
    say("the refund issued only AFTER the approval was read back")

    step(6, STEPS, "the denial path — same gate, opposite answer")
    run_worker()
    sh("python3 -c \"import json; p = 'labs/.lab3-pending.json'\n"
       "d = json.load(open(p))\n"
       "d['status'] = 'denied'; d['approved_by'] = 'naveen (operator)'\n"
       "json.dump(d, open(p, 'w'), indent=1)\n"
       "print('decision recorded:', d['status'])\"")
    run_worker()
    say("denied: the pipeline refused to pay, and the trace says why")
    takeaway()
    finish(LAB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
