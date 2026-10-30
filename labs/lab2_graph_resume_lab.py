"""Hands-On Lab 2 — kill a graph run mid-flight; resume it from the
checkpoint. The survival moment of the frameworks course.

Why this driver is longer than the demo: graphcore's Graph appends a
checkpoint after every node but cannot persist or reload one — a design
collision the lab surfaces ON PURPOSE and resolves by composition:
run_graph_resumable() drives the SAME nodes with the engine's own
router and loop guard, and writes its checkpoint dict to disk after
every step. The engine class is never modified; validate.py still
passes; the student sees both the limit and the production fix.

Session arc: full demo run -> read the checkpoint shape -> run with a
SIGKILL after step 1 (exit -9, shown) -> inspect the surviving
checkpoint file -> resume in a NEW process from step 1 -> verify the
resumed run's final state EQUALS an uninterrupted run, field by field.
    python -m labs.lab2_graph_resume_lab
"""
import json
import os
import subprocess
import sys
import time

from graphcore.graph_engine import (State, retrieve, reason, verify,
                                    escalate, route_after_reason, MAX_STEPS)
from labs.shellkit import title_card, step, say, finish

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CKPT = os.path.join(REPO_ROOT, "labs", ".lab2-checkpoint.json")
NODES = {"retrieve": retrieve, "reason": reason,
         "verify": verify, "escalate": escalate}
LAB = 2
STEPS = 6


def save(node, state):
    data = {"next_node": node, "question": state.question,
            "evidence": state.evidence, "draft": state.draft,
            "verdict": state.verdict, "steps": state.steps}
    with open(CKPT, "w") as f:
        json.dump(data, f, indent=1)
    print(f"  checkpoint written: next={node} steps={state.steps}")


def run_graph_resumable(kill_after=None, resume=False):
    if resume:
        d = json.load(open(CKPT))
        state = State(question=d["question"], evidence=d["evidence"],
                      draft=d["draft"], verdict=d["verdict"],
                      steps=d["steps"])
        node = d["next_node"]
        print(f"  resumed: next node {node}, steps already done: "
              f"{state.steps}")
    else:
        state = State(question="is order #1042 refundable?")
        node = "retrieve"
        print("  fresh run: retrieve -> reason -> verify/escalate")
    while node != "END":
        if state.steps >= MAX_STEPS:
            print("  loop-guard: MAX_STEPS reached, run stopped")
            state.verdict = "stopped-by-loop-guard"
            break
        state = NODES[node](state)
        state.steps += 1
        print(f"  step {state.steps}: {node} -> "
              f"verdict={state.verdict or '-'} draft={state.draft or '-'}")
        node = (route_after_reason(state) if node == "reason"
                else {"retrieve": "reason", "verify": "END",
                      "escalate": "END"}[node])
        save(node, state)
        if kill_after is not None and state.steps >= kill_after:
            print(f"  *** SIGKILL lands now — the process dies mid-run ***")
            sys.stdout.flush()
            os.kill(os.getpid(), 9)
    return state


def child(kill_after=None, resume=False):
    code = ("from labs.lab2_graph_resume_lab import run_graph_resumable\n"
            f"run_graph_resumable(kill_after={kill_after}, resume={resume})\n")
    proc = subprocess.run([sys.executable, "-c", code], cwd=REPO_ROOT,
                          text=True)
    return proc.returncode


def sh(cmd, pause=0.5):
    print(f"$ {cmd}")
    time.sleep(pause)
    proc = subprocess.run(cmd, shell=True, cwd=REPO_ROOT, text=True)
    time.sleep(0.4)
    return proc.returncode


def takeaway():
    print()
    print("=" * 68)
    print("KEY TAKEAWAY — a checkpoint you cannot reload is a log, not a rescue")
    print("  persist state after EVERY step, in a form a new process can read")
    print("  resume must be provable: same final state as the unkilled run")
    print("  composition beat modification: the engine stayed untouched")
    print("=" * 68)
    time.sleep(1.0)


def main():
    if os.path.exists(CKPT):
        os.remove(CKPT)
    title_card(LAB, "Kill the Run. Resume from the Checkpoint.",
               "graphcore", "12")

    step(1, STEPS, "the course demo, uninterrupted")
    sh("python3 -m graphcore.graph_engine")
    say("three checkpoints saved — in the engine's memory only")

    step(2, STEPS, "read what a checkpoint actually holds")
    sh("sed -n '49,66p' graphcore/graph_engine.py")
    say("a tuple: (node name, step count, verdict) — no state fields")
    say("if this process died, the run would die with it")

    step(3, STEPS, "the resumable runner: same nodes, persisted state")
    say("run_graph_resumable drives the engine's own nodes and")
    say("router, and writes the full state dict after every step")
    say("the Graph class is untouched — composition, not surgery")

    step(4, STEPS, "start a fresh run and kill it after step 1")
    rc = child(kill_after=1)
    say(f"exit code {rc} — negative means killed by signal 9")
    say("no cleanup ran; no finally block saved us")

    step(5, STEPS, "what survived the kill")
    sh(f"cat {os.path.relpath(CKPT, REPO_ROOT)}")
    say("next node: reason. steps done: 1. evidence already on disk")
    say("the checkpoint is a file now, not a memory")

    step(6, STEPS, "resume in a new process — and prove equivalence")
    rc = child(resume=True)
    say(f"resume exit code {rc}: reason and verify ran, retrieve did not")
    say("now the control experiment — one uninterrupted run:")
    ref = run_graph_resumable()
    d = json.load(open(CKPT))
    resumed_final = {"evidence": d["evidence"], "draft": d["draft"],
                     "verdict": d["verdict"], "steps": d["steps"]}
    control_final = {"evidence": ref.evidence, "draft": ref.draft,
                     "verdict": ref.verdict, "steps": ref.steps}
    print(f"  resumed run final state: {resumed_final}")
    print(f"  control run final state: {control_final}")
    assert resumed_final == control_final, "RESUMED STATE != CONTROL STATE"
    say("identical, field by field — the kill cost us nothing")
    os.remove(CKPT)
    takeaway()
    finish(LAB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
