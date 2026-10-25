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
| Tools / MCP | `python -m toolsmith.tool_server` | One registry, schema validation, destructive-tool gating, audit log |
| Memory | `python -m memory.memory_store` | Namespaced memory with provenance and quarantine |
| Observability | `python -m observability.tracing` | One trace schema, cost attribution, secrets redacted before storage |
| Evaluation | `python -m evaluation.harness` | Golden-set scoring and a v1→v2 regression diff with a release gate |
| Reliability | `python -m reliability.reliability` | Retries, circuit breaker and run budgets |
| Readiness | `python -m readiness.readiness` | Capstone readiness review: GO / NO-GO with named blockers |

## Validation

`python validate.py` runs every demo end to end as a subprocess, checks
the expected output markers, and adds direct assertions per module.
It exits non-zero if anything fails.
