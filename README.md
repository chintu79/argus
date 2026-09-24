# Budget-Constrained Adaptive Security Evaluation of AI Agents

**Research prototype** investigating whether adaptive test selection combined with trajectory-aware state-based branching enables more efficient discovery and validation of AI-agent security and reliability failures under a fixed evaluation budget.

## Quick Start

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint check
uv run ruff check .

# Type check
uv run mypy src/

# Initialize database
uv run python -m agent_eval.cli db init
```

## Philosophy

This is a **scientific instrument**, not a dashboard. Every research claim must be traceable through the full chain:

```
Configuration  →  Experiment  →  Execution  →  Raw Evidence  →  Evaluation  →  Validated Result  →  Metric  →  Statistical Analysis
```

If the evidence does not exist, the result does not exist.

## Research Integrity

- Never fabricate experimental results
- Never claim an experiment was run when it was not
- Never tune on the hidden holdout
- Never silently change candidate pools, budgets, or invariant definitions
- Raw evidence is immutable; derived data may be recomputed
- Holdout outcomes must never affect discovery-time selection

## First Milestone

The initial vertical slice implements:

```
Scenario  →  Candidate  →  Random Selector  →  Mock Agent  →  Controlled Environment  →  Trajectory  →  Invariant  →  Failure  →  SQLite
```

Full experiment flow: S01-S04 scenarios with unauthorized read/write/policy bypass detection, trajectory logging, invariant evaluation, failure candidate pipeline, and SQLite storage.

## Development Phases

Follows a strict 24-phase implementation order. See `IMPLEMENTATION_PLAN.md` for the complete sequence. Do not invert the sequence by building the dashboard first.

## CLI Commands (planned)

```bash
agent-eval db init
agent-eval validate
agent-eval experiment validate --config <path>
agent-eval experiment run --config <path>
agent-eval experiment status --experiment-id <id>
agent-eval metrics recompute --experiment-id <id>
agent-eval report generate --experiment-id <id>
agent-eval experiment export --experiment-id <id>
```

See the implementation plan for the complete 24-phase sequence and CLI specification.