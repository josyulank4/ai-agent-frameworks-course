"""Framework selection scorer (Lesson 4 demo).

Scores candidate frameworks against weighted production criteria, with
veto conditions that a high average can never outvote. Stdlib only.
"""
CRITERIA = [
    ("control", "Explicit control flow", 5),
    ("state", "Durable state and resume", 5),
    ("hitl", "Human approval support", 4),
    ("observability", "Tracing you own", 4),
    ("tools", "Tool and MCP integration", 3),
    ("cost", "Cost controls", 3),
    ("exit", "Low exit cost", 2),
]
# scores are 0..5 per criterion, from the course's two-week spike evidence
CANDIDATES = {
    "langgraph": {"control":5,"state":5,"hitl":5,"observability":4,"tools":5,"cost":4,"exit":3},
    "crewai": {"control":3,"state":3,"hitl":3,"observability":3,"tools":4,"cost":3,"exit":4},
    "autogen": {"control":2,"state":2,"hitl":4,"observability":3,"tools":4,"cost":2,"exit":4},
}
VETOES = {"state": 3, "control": 3}  # a regulated workflow must resume and must be explicit

def score(name, scores):
    total = sum(scores[k]*w for k,_,w in CRITERIA)
    possible = sum(5*w for _,_,w in CRITERIA)
    vetoed = [k for k,minv in VETOES.items() if scores[k] < minv]
    return {"framework": name, "weighted": total, "possible": possible,
            "pct": round(100*total/possible,1), "vetoed_by": vetoed}

def decide(candidates=CANDIDATES):
    results = [score(n,s) for n,s in candidates.items()]
    eligible = [r for r in results if not r["vetoed_by"]]
    winner = max(eligible, key=lambda r: r["weighted"]) if eligible else None
    return results, winner

def main():
    results, winner = decide()
    print("framework selection: incident-triage workflow (regulated, resumable)")
    for r in results:
        line = f"{r['framework']}: {r['weighted']}/{r['possible']} ({r['pct']}%)"
        if r["vetoed_by"]:
            line += f" VETOED by {','.join(r['vetoed_by'])}"
        print(line)
    print(f"decision: {winner['framework']} — highest weighted score among non-vetoed candidates")
    print("selection demo complete")

if __name__ == "__main__":
    main()
