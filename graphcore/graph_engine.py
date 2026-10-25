"""A transparent graph engine (Lesson 8 demo).

Implements the mechanics LangGraph industrialises: typed state, nodes,
conditional edges, a loop guard, checkpoints after every super-step and a
full execution trace. Stdlib only; the model is a deterministic stub so
the orchestration — the subject of the lesson — is what you see.
"""
from dataclasses import dataclass, field

MAX_STEPS = 12

@dataclass
class State:
    question: str = ""
    evidence: list = field(default_factory=list)
    draft: str = ""
    verdict: str = ""
    steps: int = 0

def retrieve(state):
    state.evidence = ["policy: refunds within 30 days", "order #1042: delivered 12 days ago"]
    return state

def reason(state):
    state.draft = "eligible" if len(state.evidence) >= 2 else "needs-evidence"
    return state

def verify(state):
    state.verdict = "approve" if state.draft == "eligible" else "escalate"
    return state

def escalate(state):
    state.verdict = "escalated-to-human"
    return state

def route_after_reason(state):
    return "verify" if state.draft == "eligible" else "escalate"

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.routers = {}
        self.checkpoints = []
        self.trace = []
    def add_node(self, name, fn): self.nodes[name] = fn
    def add_edge(self, a, b): self.edges[a] = b
    def add_router(self, a, fn): self.routers[a] = fn
    def run(self, state, start):
        node = start
        while node != "END":
            if state.steps >= MAX_STEPS:
                self.trace.append("loop-guard: MAX_STEPS reached, run stopped")
                state.verdict = "stopped-by-loop-guard"
                break
            state = self.nodes[node](state)
            state.steps += 1
            self.trace.append(f"step {state.steps}: {node} -> verdict={state.verdict or '-'} draft={state.draft or '-'}")
            self.checkpoints.append((node, state.steps, state.verdict))
            if node in self.routers:
                node = self.routers[node](state)
            else:
                node = self.edges.get(node, "END")
        return state

def build_research_graph():
    g = Graph()
    g.add_node("retrieve", retrieve); g.add_node("reason", reason)
    g.add_node("verify", verify); g.add_node("escalate", escalate)
    g.add_edge("retrieve", "reason"); g.add_router("reason", route_after_reason)
    g.add_edge("verify", "END"); g.add_edge("escalate", "END")
    return g

def main():
    g = build_research_graph()
    state = g.run(State(question="is order #1042 refundable?"), "retrieve")
    print("graph run: refund-research workflow")
    for line in g.trace: print(" ", line)
    print(f"checkpoints saved: {len(g.checkpoints)}")
    print(f"final verdict: {state.verdict}")
    print(f"steps used: {state.steps} (loop guard at {MAX_STEPS})")
    print("graph engine demo complete")

if __name__ == "__main__":
    main()
