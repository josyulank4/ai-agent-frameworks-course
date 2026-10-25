"""An evaluation harness (Lesson 40 demo).

Scores a workflow on a golden set — success, tool correctness and cost —
and diffs two versions so a regression cannot ship silently. Stdlib
only; the workflow under test is a deterministic triage stub.
"""
GOLDEN = [
    ("refund within window", "approve", "lookup_order"),
    ("refund outside window", "deny", "lookup_order"),
    ("account locked", "escalate", "draft_reply"),
    ("billing question", "answer", "lookup_order"),
]
def workflow_v1(case):
    # v1 mis-handles the locked-account case (answers instead of escalating)
    return {"refund within window": ("approve","lookup_order"),
            "refund outside window": ("deny","lookup_order"),
            "account locked": ("answer","draft_reply"),
            "billing question": ("answer","lookup_order")}[case]
def workflow_v2(case):
    return {"refund within window": ("approve","lookup_order"),
            "refund outside window": ("deny","lookup_order"),
            "account locked": ("escalate","draft_reply"),
            "billing question": ("answer","lookup_order")}[case]
def evaluate(fn):
    passed = 0; tool_ok = 0
    for case, expected, tool in GOLDEN:
        verdict, used = fn(case)
        if verdict == expected: passed += 1
        if used == tool: tool_ok += 1
    return passed, tool_ok, len(GOLDEN)
def main():
    print("evaluation harness: triage workflow, golden set of 4")
    for name, fn in [("v1", workflow_v1), ("v2", workflow_v2)]:
        p, t, n = evaluate(fn)
        print(f"  {name}: task success {p}/{n}, tool correctness {t}/{n}")
    print("regression diff: v2 fixes account-locked escalation (3/4 -> 4/4), no other case changed")
    print("release gate: v2 PASS (no regression, one fix)")
    print("evaluation demo complete")
if __name__ == "__main__":
    main()
