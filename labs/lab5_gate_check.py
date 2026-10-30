"""Lightweight Lab 5 gate check — the module validate.py runs.

The full Lab 5 driver (labs.lab5_eval_gate_lab) shells out to
validate.py itself; that confrontation is its showpiece. validate
must therefore NOT execute the full driver, or the two recurse
without bound. This module exercises the same rule directly and
fast: the shared triage scenario gated by its golden expectations —
the correct variant passes 4/4, the deliberately broken variant
(the one that answers the locked account) fails at 3/4.
    python -m labs.lab5_gate_check
"""
import sys

from labs.scenarios import CASES, decide


def main():
    ok = sum(1 for case, exp, _t in CASES if decide(case) == exp)
    bad = sum(1 for case, exp, _t in CASES if decide(case, broken=True) == exp)
    print(f"  correct workflow: {ok}/4 golden cases pass")
    print(f"  broken workflow (answers the lockout): {bad}/4 pass")
    assert ok == 4 and bad == 3, "gate check: unexpected pass counts"
    print("  the broken variant FAILS the gate on exactly one case")
    print("lab 5 gate check complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
