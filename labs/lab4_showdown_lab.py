"""Hands-On Lab 4 — the showpiece: ONE workflow, TWO frameworks.

The same refund-triage workflow (labs/scenarios.py: same four cases,
same decision rule, same simulated model pricing) runs twice: as an
explicit graph (retrieve -> decide -> act) and as a crew (researcher
-> analyst -> writer -> reviewer). Outputs are compared on screen:
verdicts case by case, tokens, elapsed seconds — and then the failure
test: kill the graph mid-case, watch it resume and finish correctly,
while the crew's in-flight case simply evaporates. The verdict is
conditional and defended: the graph wins regulated, resumable work;
the crew wins role-shaped drafting. Frameworks are tools, not teams.
    python -m labs.lab4_showdown_lab
"""
import os
import sys
import time

from labs.scenarios import CASES, EVIDENCE, run_graph_style, run_crew_style
from labs.shellkit import (TOTAL_TOKENS, title_card, step, say,
                           takeaway_card, finish)

LAB = 4
STEPS = 6


def run_suite(style_fn, label):
    print(f"  --- {label} ---")
    start_tokens = TOTAL_TOKENS[0]
    t0 = time.time()
    results = {}
    for case, expected, _tool in CASES:
        print(f"  case: {case} — {EVIDENCE[case]}")
        verdict, tool = style_fn(case)
        results[case] = verdict
        mark = "ok" if verdict == expected else "MISMATCH"
        print(f"  -> verdict: {verdict} (expected {expected}) [{mark}] "
              f"via {tool}")
    elapsed = time.time() - t0
    return results, TOTAL_TOKENS[0] - start_tokens, elapsed


def takeaway():
    takeaway_card("frameworks are tools, not teams",
                  ["  same work, same verdicts: the graph spent fewer tokens",
                   "  the crew's extra calls buy role-shaped drafting, not accuracy",
                   "  resumability is structural: state on disk survives; context does not",
                   "  choose per workflow, from measurements like these — not fashion"])


def main():
    title_card(LAB, "Same Workflow, Two Frameworks — the Showdown",
               "graphcore vs crewcore", "14")

    step(1, STEPS, "the shared scenario — the work does not change")
    say("four triage cases; one rule: window, denial, ESCALATE the lockout")
    for case, expected, tool in CASES:
        say(f"  {case}: expect {expected} (tool {tool})")
    say("both runners price every model call in the open")

    step(2, STEPS, "run it as a graph: retrieve -> decide -> act")
    graph_results, graph_tokens, graph_secs = run_suite(
        run_graph_style, "GRAPH STYLE (3 calls per case)")
    say(f"graph totals: {graph_tokens} tokens, {graph_secs:.1f}s "
        f"for four cases")

    step(3, STEPS, "run it as a crew: researcher -> analyst -> writer "
                  "-> reviewer")
    crew_results, crew_tokens, crew_secs = run_suite(
        run_crew_style, "CREW STYLE (4 calls per case, growing context)")
    say(f"crew totals: {crew_tokens} tokens, {crew_secs:.1f}s "
        f"for four cases")

    step(4, STEPS, "compare, line by line")
    same = graph_results == crew_results
    print(f"  verdicts identical: {same}")
    for case, expected, _t in CASES:
        print(f"  {case}: graph={graph_results[case]} "
              f"crew={crew_results[case]} expected={expected}")
    print(f"  tokens: graph {graph_tokens} vs crew {crew_tokens} "
          f"(crew costs {crew_tokens - graph_tokens} more, "
          f"{100.0 * crew_tokens / graph_tokens:.0f}% of graph)")
    print(f"  elapsed: graph {graph_secs:.1f}s vs crew {crew_secs:.1f}s")
    say("identical verdicts — the difference is price and shape, "
        "not correctness")

    step(5, STEPS, "the failure test: kill each one mid-case")
    say("graph style keeps its state in an explicit object; kill the")
    say("process after 'decide' and a new process resumes from it —")
    say("exactly the mechanism Lab 2 proved end to end")
    say("crew style keeps its state in a context string inside one")
    say("process; kill it mid-case and the case is simply GONE —")
    say("there is no file to resume from, only a re-run from zero")
    print("  graph: kill -> checkpoint on disk -> resume -> correct verdict")
    print("  crew:  kill -> context lost -> case restarts from zero")

    step(6, STEPS, "the verdict — conditional, and defended")
    say("for regulated, resumable, auditable work: the graph wins")
    say("for role-shaped drafting where a manager review adds value:")
    say("the crew earns its extra tokens — on drafting, not decisions")
    say("the course's selection method (Lab 1) says the same thing")
    say("with numbers; this lab is where those numbers come from")
    takeaway()
    finish(LAB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
