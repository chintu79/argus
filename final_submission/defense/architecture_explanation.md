# Architecture Explanation

## Level 1: Executive (60–90 seconds)

BCADE-AI is a research prototype that evaluates AI agent security under constrained budgets. The system uses an adaptive candidate selector to choose which evaluation scenarios to test, state-based branching to reuse execution state across related tests, and a structured pipeline to detect, validate, and classify failures into families. The goal is to maximize the number of validated failures discovered within a fixed evaluation budget, while providing auditable evidence for each discovery.

## Level 2: Technical

### Core Components

```
candidate
  ↓
selector
  ↓
agent
  ↓
environment
  ↓
trajectory
  ↓
state
  ↓
branch
  ↓
invariant
  ↓
failure
  ↓
family
  ↓
validation
  ↓
metrics
```

### Component Details

- **Candidate**: An evaluation scenario defined by a prompt, tool configuration, and initial state. Candidates are generated from the invariant violation space and ranked by the adaptive selector.

- **Selector**: An adaptive candidate selection mechanism that ranks candidates based on multiple criteria: failure probability (estimated from previous runs), coverage (diversity of explored space), novelty (potential new failure modes), and cost (budget tokens consumed). The selector uses an epsilon-greedy strategy balancing exploration and exploitation.

- **Agent**: A mock AI agent that executes trajectories in the evaluation environment. The agent follows a prompt → tool → observation cycle, logging the complete trajectory for later analysis.

- **Environment**: A controlled evaluation environment that provides the context for agent execution. The environment is deterministic given a seed and supports state snapshotting and branching.

- **Trajectory**: A logged sequence of agent-environment interactions, from initial prompt through final observation. Trajectories are stored persistently and include prompts, tool calls, observations, state transitions, and budget consumption.

- **State**: The agent's execution state at a point in time, including internal memory, tool session state, and environment configuration. State is snapshotted for branching.

- **Branch**: An isolated execution branch created from a state snapshot. Branches share the parent's state up to the snapshot point but diverge thereafter. Branching cost is explicitly accounted for in the evaluation budget.

- **Invariant**: A deterministic check during trajectory execution that evaluates whether a security property holds. Examples include `prompt_injection_guard`, `tool_access_control`, and `state_persistence_integrity`. Invariants are checked after each tool call during trajectory execution.

- **Failure**: An observed invariant violation during trajectory execution. Failures are classified through the pipeline: candidate failure → independent reproduction → validated failure → failure family.

- **Family**: A group of failures sharing common mechanism characteristics. Families are assigned based on shared invariant violations, tool usage patterns, or state transition characteristics.

- **Validation**: The process of independently replaying a candidate failure to confirm it is consistent and not a stochastic artifact. Validated failures are the unit of measurement for discovery efficiency.

- **Metrics**: Computed evaluation metrics including FDE, CPF, TTFF, Rep_k, FRR, TSR, PTR, BTCR, and RTR. Metrics are derived from persisted run-level data and validated failures.

### Data Flow

1. Candidate selection → agent execution in environment
2. Trajectory logging with invariant checks during execution
3. Invariant violation → candidate failure recording
4. Candidate failure → independent replay → validation
5. Validated failure → family assignment
6. All data persisted to SQLite via SQLModel
7. Metrics computed from persisted data
8. Visualizations generated from metrics
9. Statistical analysis from hypothesis tests
10. Audit and validation of all above