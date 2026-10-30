"""Hands-On Lab 1 — score a real framework choice, with vetoes.

Session arc (every command below runs for real, in this order):
  1. read the frameworkselect scorer and its evidence table,
  2. run it once with a careless edit in place — it crashes,
  3. fix the syntax, run again — it crashes differently (my bug),
  4. apply the candidate scores through the scorer's own functions,
  5. prove a veto beats a higher average,
  6. the verdict, defended line by line.

The typo and the loop bug are deliberate teaching failures, and they are
real: this driver types them, the interpreter rejects them, and the fix
is applied in the session. Run from the repo root:
    python -m labs.lab1_selection_lab
"""
import os
import subprocess
import sys
import time

from labs.shellkit import title_card, step, say, takeaway_card, finish

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEL = os.path.join(REPO_ROOT, "frameworkselect", "selection.py")
LAB = 1
STEPS = 6


def run(cmd, pause=0.5, shell=True):
    print(f"$ {cmd}")
    time.sleep(pause)
    proc = subprocess.run(cmd, shell=shell, cwd=REPO_ROOT, text=True)
    time.sleep(0.4)
    return proc.returncode


def type_cmd(typed, pause=0.5):
    """Type a command WITHOUT executing it (the mistake being shown)."""
    print(f"$ {typed}")
    time.sleep(pause)


def patch(old, new):
    src = open(SEL).read()
    assert old in src, f"patch target missing: {old}"
    open(SEL, "w").write(src.replace(old, new, 1))


def main():
    backup = open(SEL).read()
    try:
        title_card(LAB, "Score a Real Framework Choice",
                   "frameworkselect", "10")

        step(1, STEPS, "read the scorer before we run it")
        say("line 1 of 2")
        run("sed -n '6,26p' frameworkselect/selection.py")
        say("seven criteria, weighted; scores are 0..5")
        say("vetoes: state < 3 or control < 3 disqualifies outright")
        say("line 2 of 2")
        run("sed -n '27,48p' frameworkselect/selection.py")

        step(2, STEPS, "a careless edit is in place — watch the run")
        patch('"tools":5,', '"tools" 5,')
        say("the langgraph row lost a colon while tidying ("
            "git diff shows it)")
        run("git diff --stat")
        say("running the scorer now:")
        rc = run("python3 -m frameworkselect.selection")
        say(f"exit code {rc} — nothing scored; the file itself is broken")

        step(3, STEPS, "fix the syntax, run again")
        time.sleep(0.8)  # thinking pause: read the traceback first
        say("the traceback names the line; put the colon back")
        patch('"tools" 5,', '"tools": 5,')
        say("now score every candidate through the module's functions")
        type_cmd('python3 -c "from frameworkselect.selection import CANDIDATES, score"')
        type_cmd('[print(score(n, s)) for n, s in CANDIDATES]')
        say("wait — I typed that from memory; watch what it does")
        run('python3 -c "from frameworkselect.selection import CANDIDATES, score\n'
            '[print(score(n, s)) for n, s in CANDIDATES]"')
        say("an AttributeError, and it is mine: a dict iterates keys,")
        say("not pairs — the loop needs CANDIDATES.items()")
        say("correcting the loop, nothing else:")
        run('python3 -c "from frameworkselect.selection import CANDIDATES, score\n'
            '[print(score(n, s)) for n, s in CANDIDATES.items()]"')
        say("three scored rows — now we can read them")

        step(4, STEPS, "read the scores the way a reviewer would")
        say("langgraph 119/130 (91.5%): no vetoes")
        say("crewai 88/130 (67.7%): no vetoes, simply lighter")
        say("autogen 77/130 (59.2%) — and VETOED by state,control")
        say("its human-approval score of 4 cannot rescue it")

        step(5, STEPS, "prove the veto is doing real work")
        say("strip the vetoes out in memory and re-decide:")
        run('python3 -c "import frameworkselect.selection as fs\n'
            'fs.VETOES = {}\n'
            'results, winner = fs.decide()\n'
            'print(\'without vetoes the winner is:\', winner[\'framework\'])"')
        say("the winner does NOT change: langgraph also tops the average")
        say("so the veto is not what picks langgraph —")
        say("it is what removes autogen from the shortlist entirely:")
        run('python3 -c "from frameworkselect.selection import score, CANDIDATES\n'
            'r = score(\'autogen\', CANDIDATES[\'autogen\'])\n'
            'print(\'autogen weighted:\', r[\'weighted\'], \'vetoed_by:\', r[\'vetoed_by\'])"')
        say("even with the best pitch in the room, autogen is out —")
        say("a workflow that cannot resume is not a candidate")

        step(6, STEPS, "the module's own decision, end to end")
        run("python3 -m frameworkselect.selection")
        say("decision: langgraph — and every number above came from")
        say("the scorer's own arithmetic, not from this narration")

        takeaway_card("averages rank; vetoes disqualify",
                      ["  vetoes first: eligibility is binary, scores only rank the eligible",
                       "  defend a choice with the table, not with adjectives",
                       "  a crash in the session is data — read it, fix it, re-run"])
        finish(LAB)
        return 0
    finally:
        open(SEL, "w").write(backup)


if __name__ == "__main__":
    sys.exit(main())
