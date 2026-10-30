# AI Agent Frameworks — Course Code

Companion code for **AI Agent Frameworks: LangGraph, CrewAI, AutoGen**
(Udemy Course 5) by Naveen Kumar Josyula.

Every demo is small, self-contained, and runs **offline with no API
keys**: Python standard library only. The demos implement framework
mechanics transparently — a graph engine, a crew runner, a group-chat
engine, a tool server, tracing and an evaluation harness — so students
see exactly what LangGraph, CrewAI and AutoGen do, then map each piece
to the real library.

## Requirements

- Python 3.11+
- No third-party packages (`requirements.txt` is intentionally empty)

## How to run each demo

Run from the repo root:

| Area | Command | What it shows |
|---|---|---|
| Selection | `python -m frameworkselect.selection` | Weighted framework scoring with veto conditions and a defended decision |
| Graph core | `python -m graphcore.graph_engine` | Nodes, conditional edges, checkpointing, loop guard and a full trace |
| Crew core | `python -m crewcore.crew_runner` | Roles, task contracts, sequential and hierarchical processes, task ledger |
| Conversation | `python -m conversation.group_chat` | Speaker selection, message budget and explicit termination |
| Portability | `python -m portability.portability` | One triage workflow as a graph and as a crew — same inputs, scored outputs |
| Tools / MCP | `python -m toolsmith.tool_server` | One registry, schema validation, destructive-tool gating, audit log |
| Memory | `python -m memory.memory_store` | Namespaced memory with provenance and quarantine |
| Observability | `python -m observability.tracing` | One trace schema, cost attribution, secrets redacted before storage |
| Evaluation | `python -m evaluation.harness` | Golden-set scoring and a v1→v2 regression diff with a release gate |
| Reliability | `python -m reliability.reliability` | Retries, circuit breaker and run budgets |
| Readiness | `python -m readiness.readiness` | Capstone readiness review: GO / NO-GO with named blockers |

## Hands-On Labs

The course's hands-on lab section: full working sessions built on the
packages above — real runs, real failures, real fixes. Each lab is
checksummed by a pair of git tags: check out `lab-N-start` for the
state before the lab's code, `lab-N-finish` for the state the video
ends in, and run the driver to reproduce the session.

| Lab | Command | What happens |
|---|---|---|
| 1 · Selection | `python -m labs.lab1_selection_lab` | Score a real framework choice: a careless edit crashes the run, a hand-typed loop crashes it again, vetoes are proven to disqualify |
| 2 · Graph resume | `python -m labs.lab2_graph_resume_lab` | Kill a graph run with SIGKILL mid-flight; resume from the persisted checkpoint; prove the final state identical |
| 3 · Approval gate | `python -m labs.lab3_graph_interrupt_lab` | A refund pipeline stops at a human interrupt; approval on disk releases the payment; denial refuses it |
| 4 · Showdown | `python -m labs.lab4_showdown_lab` | One triage workflow as a graph and as a crew: same verdicts, token and time bills compared, failure behavior contrasted |
| 5 · Regression gate | `python -m labs.lab5_eval_gate_lab` | Break the evaluation harness with a one-word edit; watch validate.py go red; fix; gate a second workflow by the same rule |
| 6 · Readiness | `python -m labs.lab6_readiness_lab` | The readiness review re-run with receipts from Labs 1–5; NO-GO with two honest blockers, flags never flipped |

## Validation

`python validate.py` runs every demo end to end as a subprocess, checks
the expected output markers, and adds direct assertions per module.
It exits non-zero if anything fails.
