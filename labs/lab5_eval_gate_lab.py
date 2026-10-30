"""Hands-On Lab 5 — the regression gate: break it, watch it get caught.

Session arc: the course's evaluation harness passes v2 clean (4/4).
Then I make the classic careless edit — rename a golden-set key in the
harness's own v2 table — and the gate goes RED with the failure named,
case and all. I try to talk my way past it ('the change is trivial')
and the gate is unimpressed. One-line fix, gate runs GREEN, and the
lab closes with a second, independent method — the shared lab
scenario — being gated by the same rule: its deliberately broken
variant (answers the locked account) FAILS, the correct one passes.
A gate you have never seen fail is a gate you do not actually have.
    python -m labs.lab5_eval_gate_lab
"""
import os
import subprocess
import sys
import time

from labs.scenarios import CASES, decide
from labs.shellkit import (title_card, step, say, takeaway_card, finish)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARNESS = os.path.join(REPO_ROOT, "evaluation", "harness.py")
LAB = 5
STEPS = 6


def sh(cmd, pause=0.5):
    print(f"$ {cmd}")
    time.sleep(pause)
    proc = subprocess.run(cmd, shell=True, cwd=REPO_ROOT, text=True)
    time.sleep(0.4)
    return proc.returncode


def patch(old, new):
    src = open(HARNESS).read()
    assert old in src, f"patch target missing: {old}"
    open(HARNESS, "w").write(src.replace(old, new, 1))


def gate(expected, tool, fn):
    passed = 0
    for case, exp, _t in CASES:
        if fn(case) == exp:
            passed += 1
    return passed


def main():
    backup = open(HARNESS).read()
    try:
        title_card(LAB, "Break It. Watch the Gate Catch It.",
                   "evaluation", "11")

        step(1, STEPS, "the gate at rest: the course harness, green")
        sh("python3 -m evaluation.harness")
        say("v1 scores 3/4, v2 scores 4/4, release gate: v2 PASS")
        say("a gate is only worth having if you have seen it fail")

        step(2, STEPS, "the careless edit — a renamed golden-set key")
        say("someone 'tidies' the v2 table and renames a case key:")
        patch('"account locked": ("escalate","draft_reply"),\n'
              '            "billing question"',
              '"locked account": ("escalate","draft_reply"),\n'
              '            "billing question"')
        sh("git diff -U1 evaluation/harness.py")
        say("one word changed. it looks harmless. it is not:")

        step(3, STEPS, "run the harness — the gate goes red")
        rc = sh("python3 -m evaluation.harness")
        say(f"exit code {rc}: the workflow CRASHED on the renamed key")
        say("the golden case 'account locked' has no entry in v2 now —")
        say("in production this is the escalation that silently dies")

        step(4, STEPS, "'it's a trivial change' — the validate gate answers")
        rc = sh("python3 validate.py")
        say(f"validate exit code {rc}: OVERALL FAIL, and it names the")
        say("evaluation checks — the harness markers are gone and the")
        say("direct assertions fail. trivial changes do not get waived")

        step(5, STEPS, "fix the one line and re-run BOTH gates")
        patch('"locked account": ("escalate","draft_reply"),',
              '"account locked": ("escalate","draft_reply"),')
        sh("python3 -m evaluation.harness")
        rc = sh("python3 validate.py 2>&1 | tail -2")
        say("green again — because the behavior is back, not the excuse")

        step(6, STEPS, "the same rule, second method: the lab scenario")
        say("gate the shared triage scenario by its golden expectations:")
        ok = gate(None, None, lambda c: decide(c, broken=False))
        bad = gate(None, None, lambda c: decide(c, broken=True))
        print(f"  correct workflow: {ok}/4 golden cases pass")
        print(f"  broken workflow (answers the lockout): {bad}/4 pass")
        assert ok == 4 and bad == 3
        say("the broken variant FAILS the gate on exactly one case —")
        say("the locked account — the case that matters most")
        takeaway_card("a gate you have never seen fail is not a gate",
                      ["  golden sets are cheap; silent regressions are not",
                       "  gates do not grade intentions — 'trivial' still runs",
                       "  name the failing case in the output, every time"])
        finish(LAB)
        return 0
    finally:
        open(HARNESS, "w").write(backup)


if __name__ == "__main__":
    sys.exit(main())
