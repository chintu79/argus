# Budget-Constrained Adaptive Security Evaluation of AI Agents

## README / Developer Setup Guide

**Project:** Budget-Constrained Adaptive Security Evaluation of AI Agents
**Document ID:** DEV-README-01
**Document Type:** README / Developer Setup Guide
**Status:** Research Prototype
**Version:** 1.0

---

# 1. Project Overview

This repository contains a research prototype for evaluating AI agents under a fixed and explicitly measured evaluation budget.

The project investigates whether **adaptive test selection combined with trajectory-aware state-based branching** can discover and validate AI-agent security and reliability failures more efficiently than non-adaptive evaluation strategies.

The evaluation pipeline is:

```text
Task / Scenario Generation
        ↓
Candidate Pool
        ↓
Adaptive Test Selection
        ↓
Agent Execution
        ↓
Trajectory Collection
        ↓
Interesting-State Detection
        ↓
State Snapshot
        ↓
Branch Generation
        ↓
Perturbation / Attack
        ↓
Invariant Evaluation
        ↓
Failure Detection
        ↓
Failure Classification
        ↓
Failure Clustering
        ↓
Reproducibility Testing
        ↓
Metamorphic Testing
        ↓
Hidden Holdout Evaluation
        ↓
Metrics / Statistics
        ↓
Experimental Report
```

The repository is designed as a **research platform**, not a production agent framework.

---

# 2. Core Research Question

The central research question is:

> Under a fixed and explicitly measured evaluation budget, does combining adaptive test selection with trajectory-aware state-based branching enable more efficient discovery and validation of AI-agent security and reliability failures, while producing failure families that reproduce and generalize to unseen scenarios?

The implementation must preserve the ability to answer this question experimentally.

---

# 3. Core Research Principle

The project follows:

```text
Raw Evidence
     ↓
Evaluation
     ↓
Validated Failure
     ↓
Failure Family
     ↓
Reproduction
     ↓
Metamorphic Validation
     ↓
Hidden-Holdout Generalization
     ↓
Research Metrics
```

Do not skip evidence layers merely because a dashboard would look cleaner.

---

# 4. Important Terminology

| Term              | Meaning                                                        |
| ----------------- | -------------------------------------------------------------- |
| Candidate         | A selectable evaluation scenario/configuration                 |
| Scenario          | A defined test situation or attack/fault condition             |
| Execution         | One actual run of an agent against a candidate                 |
| Trajectory        | Chronological execution record                                 |
| State             | Structured environment/execution state                         |
| Snapshot          | Persisted representation of controlled execution state         |
| Branch            | Isolated execution created from a snapshot                     |
| Invariant         | Executable property that should hold                           |
| Failure Candidate | Suspected failure supported by an observed violation           |
| Validated Failure | Failure satisfying the configured evidence criteria            |
| Failure Family    | Group of related validated failure occurrences                 |
| Reproduction      | Independent attempt to reproduce a validated failure           |
| Metamorphic Test  | Base/transformed execution pair evaluated through a relation   |
| Holdout           | Hidden evaluation population unavailable to adaptive selection |
| Budget            | Explicit resource allowance for evaluation                     |
| Discovery         | Finding previously unknown validated failure families          |
| Validation        | Additional evidence establishing the reliability of a finding  |

---

# 5. What This Repository Is

The repository implements:

* controlled AI-agent evaluation;
* scenario generation and mutation;
* adaptive candidate selection;
* agent execution;
* controlled tools and environment;
* trajectory collection;
* state analysis;
* state snapshots;
* isolated branching;
* invariant evaluation;
* failure detection;
* failure classification;
* failure clustering;
* reproduction;
* metamorphic testing;
* hidden holdout evaluation;
* budget accounting;
* experiment tracking;
* metrics;
* statistical analysis;
* reporting.

---

# 6. What This Repository Is Not

The project is not:

* a production autonomous-agent platform;
* a general-purpose LLM framework;
* a vulnerability scanner for arbitrary software;
* a replacement for human security review;
* an enterprise compliance certification system;
* an unrestricted agent sandbox;
* an implementation of LLM KV-cache branching.

The initial branching mechanism operates on **controlled execution/environment state**.

---

# 7. Technology Stack

Recommended implementation stack:

| Area                  | Technology             |
| --------------------- | ---------------------- |
| Language              | Python 3.11+           |
| API                   | FastAPI                |
| Data validation       | Pydantic v2            |
| ORM / DB              | SQLAlchemy or SQLModel |
| Database              | SQLite initially       |
| Raw traces            | JSONL                  |
| Numerical computing   | NumPy                  |
| Data analysis         | pandas                 |
| ML utilities          | scikit-learn           |
| Testing               | pytest                 |
| Containers            | Docker                 |
| Visualization         | Plotly                 |
| Configuration         | YAML + Pydantic        |
| Experiment tracking   | MLflow or equivalent   |
| Linting               | Ruff                   |
| Type checking         | mypy or pyright        |
| Dependency management | uv                     |
| CI                    | GitHub Actions         |

The implementation may substitute equivalent tools only when the change does not alter research semantics.

---

# 8. Prerequisites

Install:

* Python 3.11 or newer;
* Git;
* `uv`;
* Docker and Docker Compose if containerized execution is used.

Verify:

```bash
python --version
git --version
uv --version
docker --version
```

Expected Python version:

```text
Python 3.11+
```

---

# 9. Clone the Repository

```bash
git clone <repository-url>
cd agent-eval
```

Replace `<repository-url>` with the actual repository URL.

Do not invent a repository URL in project documentation until the repository has actually been published.

---

# 10. Recommended Repository Structure

```text
agent-eval/
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
│
├── configs/
│   ├── base.yaml
│   ├── development.yaml
│   ├── test.yaml
│   │
│   ├── agents/
│   │   ├── mock_agent.yaml
│   │   └── default_agent.yaml
│   │
│   ├── environments/
│   │   └── support_environment.yaml
│   │
│   ├── scenarios/
│   │   ├── seed.yaml
│   │   └── generation.yaml
│   │
│   ├── selectors/
│   │   ├── random.yaml
│   │   ├── uniform.yaml
│   │   ├── ucbv.yaml
│   │   └── proposed.yaml
│   │
│   ├── invariants/
│   │   └── default.yaml
│   │
│   ├── branching/
│   │   └── default.yaml
│   │
│   ├── validation/
│   │   ├── reproduction.yaml
│   │   └── metamorphic.yaml
│   │
│   ├── holdout/
│   │   └── default.yaml
│   │
│   ├── metrics/
│   │   └── default.yaml
│   │
│   ├── statistics/
│   │   └── default.yaml
│   │
│   └── experiments/
│       ├── baseline_random.yaml
│       ├── baseline_uniform.yaml
│       ├── baseline_ucbv.yaml
│       ├── adaptive_main.yaml
│       └── ablation_branching.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── scenarios/
│   └── holdout/
│
├── artifacts/
│   ├── experiments/
│   ├── validation/
│   ├── reports/
│   └── logs/
│
├── migrations/
│
├── notebooks/
│
├── scripts/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── property/
│   ├── regression/
│   ├── evaluator/
│   └── e2e/
│
└── src/
    └── agent_eval/
        ├── api/
        ├── cli/
        ├── config/
        ├── domain/
        ├── interfaces/
        ├── services/
        ├── agents/
        ├── environments/
        ├── tools/
        ├── scenarios/
        ├── selection/
        ├── execution/
        ├── trajectories/
        ├── states/
        ├── snapshots/
        ├── branching/
        ├── invariants/
        ├── failures/
        ├── clustering/
        ├── validation/
        ├── metamorphic/
        ├── holdout/
        ├── metrics/
        ├── experiments/
        ├── storage/
        ├── reporting/
        ├── tracking/
        └── utils/
```

---

# 11. Source Code Architecture

The source tree follows the research architecture.

```text
domain
  ↓
interfaces
  ↓
services
  ↓
execution components
  ↓
storage / reporting
```

The domain layer must remain independent of infrastructure frameworks wherever practical.

---

# 12. Domain Layer

Location:

```text
src/agent_eval/domain/
```

Contains core models such as:

```text
Experiment
ExperimentRun
Scenario
Candidate
Execution
Trajectory
TrajectoryEvent
State
Snapshot
Branch
Invariant
InvariantEvaluation
FailureCandidate
ValidatedFailure
FailureSignature
FailureFamily
ReproductionAttempt
MetamorphicTest
Metric
Budget
```

The domain layer should not directly depend on:

* FastAPI;
* SQLAlchemy;
* database sessions;
* HTTP request objects.

This keeps research semantics independent from infrastructure.

---

# 13. Interfaces Layer

Location:

```text
src/agent_eval/interfaces/
```

Use Python `Protocol` definitions for major abstractions.

Examples:

```python
class AgentAdapter(Protocol):
    ...

class EnvironmentInterface(Protocol):
    ...

class TestSelector(Protocol):
    ...

class SnapshotManager(Protocol):
    ...

class BranchManager(Protocol):
    ...

class InvariantEngine(Protocol):
    ...

class FailureDetector(Protocol):
    ...
```

Interfaces should define behavior, not infrastructure details.

---

# 14. Agent Module

Location:

```text
src/agent_eval/agents/
```

Responsibilities:

* agent adapter;
* mock agent;
* optional real-model adapter;
* generation configuration;
* capability metadata;
* reset semantics;
* execution metadata.

Initial development should use a deterministic or controlled mock agent.

Do not make an external LLM API a prerequisite for basic evaluator development.

---

# 15. Mock Agent

The mock agent is critical.

It should support deterministic behaviors such as:

```text
SAFE_AUTHORIZED_READ
UNSAFE_UNAUTHORIZED_READ
UNSAFE_WRITE
POLICY_BYPASS
SAFE_RECOVERY
UNSAFE_RECOVERY
RESOURCE_ABUSE
```

This makes evaluator validation independent of model stochasticity.

---

# 16. Environment Module

Location:

```text
src/agent_eval/environments/
```

Initial environment:

> Simulated enterprise-support environment.

It should contain:

* customer data;
* account data;
* transaction data;
* ticket data;
* authorization state;
* policy state;
* service state;
* resource state;
* fault state.

---

# 17. Tool Module

Location:

```text
src/agent_eval/tools/
```

Initial tools:

```text
customer.lookup
account.lookup
transaction.lookup
ticket.search
ticket.update
notification.send
database.write
```

Every tool should have:

```text
tool_id
version
input schema
output schema
required capabilities
policy requirements
cost model
side-effect description
```

---

# 18. Policy Engine

Policy enforcement should occur before tool execution.

Conceptually:

```text
Agent Tool Request
       ↓
Tool Gateway
       ↓
Capability Check
       ↓
Policy Engine
       ↓
ALLOW / DENY / REVIEW / ERROR
       ↓
Tool Execution
```

The policy result must be recorded in the trajectory.

---

# 19. Scenario Module

Location:

```text
src/agent_eval/scenarios/
```

Responsibilities:

* scenario models;
* scenario loading;
* scenario validation;
* seed scenarios;
* mutation operators;
* candidate generation;
* scenario versioning.

Initial scenario IDs:

```text
S01 Authorized Read
S02 Unauthorized Read
S03 Unauthorized Write
S04 Policy Bypass
S05 Tool Parameter Manipulation
S06 Tool Response Injection
S07 Sensitive Data Exposure
S08 Unsafe Multi-Step Sequence
S09 Malformed Tool Response
S10 Tool Timeout
S11 Service Unavailability
S12 Recovery Failure
S13 Cross-Tool Privilege Escalation
S14 State-Dependent Authorization
S15 Cross-Branch State Isolation
S16 Resource Abuse
S17 Metamorphic Consistency
S18 Hidden Holdout Variant
```

---

# 20. Candidate Model

A candidate is a selectable evaluation configuration derived from a scenario.

A candidate should contain:

```text
candidate_id
scenario_id
scenario_version
mutation
difficulty
risk_level
estimated_cost
expected_branchability
novelty_features
metadata
```

Candidate identity must remain stable during a frozen experiment.

---

# 21. Selection Module

Location:

```text
src/agent_eval/selection/
```

Implement selectors in this order:

```text
Random
   ↓
Uniform
   ↓
UCB-V
   ↓
Cost-Aware
   ↓
Novelty-Augmented
   ↓
Branch-Aware Proposed Method
```

Do not implement the final adaptive selector first.

That makes debugging needlessly miserable and makes it harder to determine which component caused an observed improvement.

---

# 22. Random Selector

Configuration:

```yaml
method: random
seed: 42
replacement: false
```

The selector must record:

```text
selected_candidate
selection_step
random_seed
available_candidates
estimated_cost
```

---

# 23. Uniform Selector

The uniform selector provides a non-adaptive baseline.

It should not use failure history to change future selection.

---

# 24. UCB-V Selector

The UCB-V selector uses:

```text
UCBV_i(t)
=
μ̂_i
+
sqrt((2 v̂_i ln(t)) / n_i)
+
(3 b ln(t)) / n_i
```

with:

```text
b = 1
```

for the binary reward configuration.

The implementation must maintain empirical variance.

If variance is not actually used, the method must not be labelled UCB-V.

---

# 25. Proposed Adaptive Selector

Initial conceptual score:

```text
A(c,t)
=
UCBV(c,t)
+
λN N(c)
+
λB B(c)
+
λS S(c)
-
λC C(c)
```

where:

* `N(c)` = novelty;
* `B(c)` = branch potential;
* `S(c)` = independently defined severity value, if enabled;
* `C(c)` = cost penalty.

All terms must be defined and versioned.

---

# 26. Selection Information Boundary

The selector may use:

```text
previous rewards
selection counts
empirical variance
observed costs
coverage information
validated failure history
novelty
branch potential
current budget
```

The selector must not use:

```text
future execution outcomes
holdout outcomes
future labels
post-hoc validation results
manually inserted future knowledge
private model reasoning
```

This boundary is essential for experimental validity.

---

# 27. Reward Definition

Initial reward:

```text
reward = 1
```

if the selected candidate produces a previously unseen **validated failure family**.

Otherwise:

```text
reward = 0
```

The reward should not be based merely on:

* raw failure occurrence;
* model output containing suspicious text;
* invariant suspicion without validation;
* a new execution of an existing failure family.

---

# 28. Execution Module

Location:

```text
src/agent_eval/execution/
```

Responsibilities:

* candidate execution;
* environment lifecycle;
* agent lifecycle;
* tool invocation;
* fault injection;
* timeout handling;
* cost tracking;
* termination;
* trace creation.

---

# 29. Execution Modes

The system should support:

```text
NORMAL
BRANCH
REPLAY
METAMORPHIC_BASE
METAMORPHIC_TRANSFORMED
HOLDOUT
```

Execution mode must be stored in every execution record.

---

# 30. Trajectory Module

Location:

```text
src/agent_eval/trajectories/
```

Trajectory structure:

```text
τ =
{s₀, a₀, o₀, s₁, a₁, o₁, ..., sₙ}
```

The trace should capture observable execution information.

Do not store or require private chain-of-thought.

Use:

```text
Observed Agent State Summary
```

or:

```text
Trajectory State and Decision Context
```

where appropriate.

---

# 31. Trace Events

Supported event types should include:

```text
AGENT_OUTPUT
TOOL_REQUEST
TOOL_RESPONSE
POLICY_DECISION
STATE_TRANSITION
FAULT_INJECTION
SNAPSHOT
BRANCH
INVARIANT_EVALUATION
TERMINATION
ERROR
COST
```

Every event should contain stable identifiers.

---

# 32. State Module

Location:

```text
src/agent_eval/states/
```

Environment state:

```text
S =
{
    identity_state,
    authorization_state,
    data_state,
    tool_state,
    service_state,
    policy_state,
    task_state,
    fault_state,
    resource_state
}
```

State should be serializable and hashable.

---

# 33. Interesting-State Detection

The state-analysis layer identifies points where branching may have useful evaluation value.

Possible signals:

```text
authorization transition
sensitive data exposure
privilege change
tool escalation
state mutation
policy decision
fault recovery
resource threshold
```

State detection must be based on observable execution evidence.

---

# 34. Snapshot Module

Location:

```text
src/agent_eval/snapshots/
```

Snapshots represent controlled execution/environment state.

They are **not** LLM KV-cache snapshots.

A snapshot should contain:

```text
snapshot_id
execution_id
state_id
environment_version
state_hash
serialized_state
parent_snapshot_id
creation_cost
```

---

# 35. Branching Module

Location:

```text
src/agent_eval/branching/
```

A branch is created from a valid snapshot.

```text
Parent Snapshot
      |
      +---- Branch A
      |
      +---- Branch B
      |
      +---- Branch C
```

Branches must be isolated.

A branch must not mutate the parent state.

---

# 36. Branch Perturbations

Initial perturbations can include:

```text
authorization change
tool response mutation
fault injection
state mutation
context mutation
policy boundary change
resource constraint
sequence modification
```

Every perturbation must have a machine-readable definition.

---

# 37. Invariant Module

Location:

```text
src/agent_eval/invariants/
```

Initial invariant set:

```text
I1 Authorization Integrity
I2 Unauthorized Data Access Prevention
I3 Unauthorized Write Prevention
I4 Policy Enforcement
I5 State Integrity
I6 Branch Isolation
I7 Safe Recovery
I8 Resource Constraint
```

Each invariant should define:

```text
invariant_id
version
description
preconditions
evaluation logic
evidence requirements
severity
```

---

# 38. Failure Module

Location:

```text
src/agent_eval/failures/
```

Failure lifecycle:

```text
Observed Execution
      ↓
Invariant Violation
      ↓
Failure Candidate
      ↓
Evidence Validation
      ↓
Validated Failure
```

A candidate is not automatically a validated failure.

---

# 39. Failure Classification

Initial categories:

```text
SECURITY
RELIABILITY
ROBUSTNESS
POLICY
AUTHORIZATION
DATA_EXPOSURE
STATE_INTEGRITY
RESOURCE
EVALUATOR
ENVIRONMENT
INFRASTRUCTURE
SCENARIO
```

The primary research failure population normally focuses on security, reliability, robustness, policy, authorization, data exposure, state integrity, and resource-related failures.

---

# 40. Failure Clustering

Location:

```text
src/agent_eval/clustering/
```

Clustering process:

```text
Validated Failure
      ↓
Canonical Signature
      ↓
Exact Fingerprint
      ↓
Structured Similarity
      ↓
Family Assignment
```

Do not treat clustering as proof of causal root cause.

A failure family represents observed similarity, not demonstrated causality.

---

# 41. Validation Module

Location:

```text
src/agent_eval/validation/
```

Responsibilities:

* reproduction;
* stability;
* evidence management;
* validation state;
* comparison.

Reproduction outcomes:

```text
REPRODUCED
NOT_REPRODUCED
PARTIAL
INCONCLUSIVE
INVALID
ERROR
```

---

# 42. Reproduction Modes

Initial modes:

```text
EXACT_REPLAY
CONTROLLED_REPLAY
INDEPENDENT_SEED
STATE_REPLAY
BRANCH_REPLAY
```

Recommended first implementation:

```text
new execution
+
fresh environment
+
fresh trace
+
independent seed
```

where stochastic execution is involved.

---

# 43. Metamorphic Module

Location:

```text
src/agent_eval/metamorphic/
```

Initial transformations:

```text
MT01 FORMAT_ONLY
MT02 SYNTHETIC_ID_RENAME
MT03 IRRELEVANT_CONTEXT
MT04 TASK_PARAPHRASE
```

The transformation must have a semantic rationale.

---

# 44. Metamorphic Pipeline

```text
Base Input
    ↓
Base Execution
    ↓
Base Result
    ↓
Transformation
    ↓
Transformed Input
    ↓
Transformed Execution
    ↓
Transformed Result
    ↓
Relation Evaluation
```

Possible relation types:

```text
EQUIVALENCE
INVARIANT_PRESERVATION
MONOTONICITY
NON_INTERFERENCE
PERMUTATION_INVARIANCE
IDEMPOTENCE
ROBUSTNESS
SECURITY_PROPERTY_PRESERVATION
```

---

# 45. Holdout Module

Location:

```text
src/agent_eval/holdout/
```

The holdout set must remain unavailable to:

* adaptive selector;
* candidate scoring;
* development-time clustering decisions;
* development-time tuning.

The holdout exists to measure generalization.

---

# 46. Metrics Module

Location:

```text
src/agent_eval/metrics/
```

Primary metrics include:

```text
Validated Failure Families
Family Discovery AUC
Cost Per New Family
Time / Cost to First Family
Reproduction Rate
Metamorphic Consistency
Holdout Generalization
```

Secondary evaluator-quality metrics should remain separate.

---

# 47. Budget Module

Budget accounting:

```text
C_total
=
C_generation
+
C_execution
+
C_branch
+
C_snapshot
+
C_restore
+
C_analysis
+
C_verification
```

The budget manager should support:

```text
reserve()
commit()
release()
remaining()
can_afford()
```

---

# 48. Storage Architecture

Initial storage:

```text
SQLite
+
JSONL
+
Artifact Files
```

SQLite stores structured relationships.

JSONL stores raw event streams and traces.

Artifact files store:

* reports;
* plots;
* experiment bundles;
* exported configurations;
* validation reports.

---

# 49. Database Initialization

Once database tooling is implemented:

```bash
uv run python -m agent_eval.cli db init
```

or the repository's equivalent CLI command.

Database commands should be documented in the final CLI implementation.

---

# 50. Configuration System

Configuration hierarchy:

```text
Global
  ↓
Environment
  ↓
Agent
  ↓
Scenario
  ↓
Selector
  ↓
Validation
  ↓
Experiment
  ↓
Run
  ↓
Immutable Manifest
```

Configuration precedence:

```text
Defaults
  ↓
Base YAML
  ↓
Component YAML
  ↓
Experiment YAML
  ↓
Environment Variables
  ↓
CLI Overrides
```

After an experiment starts, its resolved configuration must be treated as immutable.

---

# 51. Environment Configuration

Example:

```yaml
environment:
  name: support_simulator
  version: "1.0"

  tools:
    enabled:
      - customer.lookup
      - account.lookup
      - transaction.lookup
      - ticket.search
      - ticket.update
      - notification.send

  snapshots:
    enabled: true

  branching:
    enabled: true
```

The exact schema must follow the implemented Pydantic configuration models.

---

# 52. Agent Configuration

Example:

```yaml
agent:
  adapter: mock
  model: mock-agent-v1

  generation:
    temperature: 0.0
    max_tokens: 512

  determinism:
    enabled: true
    seed: 42

  reset:
    between_executions: true
```

Real model settings should be kept separate from mock-agent configuration.

---

# 53. Selector Configuration

Example:

```yaml
selector:
  method: ucbv

  initialization:
    strategy: one_sample_each

  reward:
    type: new_validated_failure_family

  ucbv:
    b: 1.0
```

For the proposed selector:

```yaml
selector:
  method: proposed_adaptive

  weights:
    novelty: 1.0
    branch_potential: 1.0
    severity: 0.0
    cost: 1.0
```

Weights shown here are configuration examples, not scientifically established constants.

---

# 54. Budget Configuration

Example:

```yaml
budget:
  unit: execution_units
  limit: 1000

  costs:
    generation: 1.0
    execution: 1.0
    snapshot: 0.2
    restore: 0.2
    branch: 1.0
    analysis: 0.1
    verification: 1.0
```

Actual values must be fixed before the relevant experiment.

---

# 55. Development Environment

Use a dedicated development configuration:

```text
configs/development.yaml
```

Recommended characteristics:

```text
small candidate pool
deterministic mock agent
small budget
verbose logging
local SQLite
fast test execution
```

Development configuration must not accidentally become the formal experimental configuration.

---

# 56. Test Environment

Use:

```text
configs/test.yaml
```

Characteristics:

```text
deterministic
isolated
small
synthetic
repeatable
```

Tests should not depend on external LLM APIs.

---

# 57. Environment Variables

Use `.env` only for local development secrets/configuration.

Example:

```text
DATABASE_URL=sqlite:///./data/agent_eval.db
LOG_LEVEL=INFO
```

Never commit:

```text
API keys
access tokens
passwords
private credentials
```

to Git.

Provide:

```text
.env.example
```

instead.

---

# 58. Dependency Installation

Recommended with `uv`:

```bash
uv sync
```

Run commands through:

```bash
uv run ...
```

This ensures the locked environment is used.

---

# 59. Virtual Environment

If using a conventional virtual environment instead:

```bash
python -m venv .venv
```

Activate it according to the operating system.

Then install the project dependencies from `pyproject.toml`.

The repository should standardize on one primary dependency workflow.

---

# 60. Development Installation

The package should be installed in editable mode through the chosen package manager.

With `uv`, the intended workflow is:

```bash
uv sync
```

Then verify:

```bash
uv run python -c "import agent_eval; print(agent_eval.__version__)"
```

---

# 61. Running Unit Tests

```bash
uv run pytest tests/unit
```

---

# 62. Running Integration Tests

```bash
uv run pytest tests/integration
```

---

# 63. Running Contract Tests

```bash
uv run pytest tests/contract
```

---

# 64. Running Evaluator Validation

```bash
uv run pytest tests/evaluator
```

This suite should contain:

* ground-truth scenarios;
* invariant validation;
* failure detection;
* reproduction;
* metamorphic validation;
* holdout isolation tests.

---

# 65. Running End-to-End Tests

```bash
uv run pytest tests/e2e
```

These tests should execute the complete pipeline using the mock agent.

---

# 66. Running the Complete Test Suite

```bash
uv run pytest
```

Before a formal research run:

```bash
uv run pytest
```

must pass.

---

# 67. Linting

Recommended:

```bash
uv run ruff check .
```

Formatting:

```bash
uv run ruff format .
```

---

# 68. Type Checking

If mypy is selected:

```bash
uv run mypy src
```

If pyright is selected:

```bash
uv run pyright
```

The project should standardize on one primary type checker.

---

# 69. Running the API

Once the FastAPI application is implemented:

```bash
uv run uvicorn agent_eval.api.main:app --reload
```

Development API:

```text
http://127.0.0.1:8000
```

The final repository should expose its OpenAPI documentation through the standard FastAPI endpoints.

---

# 70. Running a Development Experiment

A development experiment should use:

```text
mock agent
small candidate pool
small budget
deterministic seed
local environment
```

Example conceptual command:

```bash
uv run python -m agent_eval.cli experiment run \
  --config configs/experiments/baseline_random.yaml
```

The exact CLI command should match the implemented CLI.

---

# 71. Running the Main Adaptive Experiment

Conceptual command:

```bash
uv run python -m agent_eval.cli experiment run \
  --config configs/experiments/adaptive_main.yaml
```

Before executing, verify:

```text
candidate pool frozen
configuration hash generated
seed set fixed
budget fixed
holdout isolated
software version recorded
```

---

# 72. Running Baselines

Random:

```bash
... --config configs/experiments/baseline_random.yaml
```

Uniform:

```bash
... --config configs/experiments/baseline_uniform.yaml
```

UCB-V:

```bash
... --config configs/experiments/baseline_ucbv.yaml
```

Adaptive:

```bash
... --config configs/experiments/adaptive_main.yaml
```

The exact commands should be exposed through the CLI once implemented.

---

# 73. Recommended Development Sequence

Implementation order:

```text
1. Repository / Tooling
2. Domain Models
3. Database / Repositories
4. Controlled Environment
5. Mock Agent
6. Tool Gateway / Policy
7. Trajectory Logging
8. Invariant Engine
9. Failure Engine
10. Baseline Selectors
11. Budget Manager
12. Adaptive Feedback
13. State Detection
14. Snapshotting
15. Branching
16. Clustering
17. Reproduction
18. Metamorphic Testing
19. Hidden Holdout
20. Metrics
21. Statistics
22. Dashboard / Reporting
```

Do not invert this sequence by building the dashboard first.

The dashboard is the least interesting component and somehow humans always want to build it first.

---

# 74. Minimal Working Prototype

The first complete vertical slice should implement:

```text
Scenario
 ↓
Candidate
 ↓
Random Selector
 ↓
Mock Agent
 ↓
Controlled Environment
 ↓
Trajectory
 ↓
Invariant
 ↓
Failure
 ↓
SQLite
 ↓
Metric
```

This proves the core evaluator before adaptive complexity is introduced.

---

# 75. First Adaptive Prototype

Next implement:

```text
Candidate Pool
 ↓
Random
 ↓
Uniform
 ↓
UCB-V
 ↓
Proposed Adaptive
```

Compare the selectors using the same synthetic reward environment before connecting them to the complete evaluator.

---

# 76. First Branching Prototype

Implement:

```text
Execution
 ↓
Interesting State
 ↓
Snapshot
 ↓
Branch
 ↓
Perturbation
 ↓
Execution
 ↓
Invariant
```

Validate branch isolation before measuring research performance.

---

# 77. First Validation Prototype

Implement:

```text
Failure
 ↓
Independent Replay
 ↓
Reproduction Result
```

Then add:

```text
Metamorphic Test
```

Then:

```text
Hidden Holdout
```

---

# 78. Git Workflow

Recommended branches:

```text
main
develop
feature/*
experiment/*
fix/*
```

Research experiments should be tied to a specific Git commit.

For every formal experiment record:

```text
git_commit
git_branch
dirty_worktree
```

---

# 79. Commit Discipline

Research-critical changes should use descriptive commits.

Examples:

```text
feat(selector): implement empirical UCB-V
feat(branching): add isolated snapshot branches
fix(metrics): correct reproduction denominator
test(evaluator): add unauthorized-read ground truth
fix(holdout): block selector access to holdout results
```

---

# 80. Experiment Versioning

Each formal experiment must record:

```text
experiment_id
run_id
software_version
git_commit
configuration_hash
candidate_pool_hash
scenario_version
agent_version
environment_version
tool_registry_version
policy_version
invariant_version
selector_version
clustering_version
metric_version
seed
```

This makes the result reconstructable.

---

# 81. Experiment Artifacts

Each experiment should generate:

```text
artifacts/experiments/<experiment_id>/
├── manifest.yaml
├── resolved_config.yaml
├── config_hash.txt
├── seeds.yaml
├── software_versions.json
├── dependency_lock.txt
├── candidate_pool.json
├── invariant_registry.json
├── selector_config.json
├── validation_config.json
├── execution_summary.json
├── metrics.json
├── statistics.json
├── traces/
├── snapshots/
├── failures/
├── reports/
└── README.md
```

---

# 82. Immutable Experiment Manifest

The manifest is the authoritative description of a formal run.

Example:

```yaml
experiment_id: EXP-001

software:
  git_commit: "<commit>"
  python: "3.11"

configuration:
  hash: "<sha256>"

research:
  method: proposed_adaptive
  seed: 42

budget:
  unit: execution_units
  limit: 1000

candidate_pool:
  hash: "<sha256>"

holdout:
  enabled: true
  isolated: true
```

Values such as commit hashes should be generated automatically.

---

# 83. Logging

Recommended levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Use structured logging for experiment execution.

Every important event should include:

```text
experiment_id
run_id
execution_id
timestamp
component
event
```

---

# 84. Raw Data Preservation

Never overwrite raw traces.

Raw evidence should be immutable after an execution is finalized.

Derived data may be recomputed:

```text
trace
  ↓
failure detection
  ↓
classification
  ↓
clustering
  ↓
metrics
```

This allows evaluator logic to improve without rerunning expensive agent executions.

---

# 85. Data Directory Rules

```text
data/raw/
```

contains raw inputs.

```text
data/processed/
```

contains derived datasets.

```text
data/scenarios/
```

contains scenario definitions.

```text
data/holdout/
```

contains protected holdout data.

Holdout contents must not be casually committed to public repositories if their purpose is to remain hidden.

---

# 86. Artifact Directory Rules

Artifacts should be organized by experiment.

Do not place random output files directly into:

```text
artifacts/
```

Use:

```text
artifacts/experiments/<experiment_id>/
```

This prevents the repository from eventually becoming a digital junk drawer.

---

# 87. Notebook Rules

Notebooks belong in:

```text
notebooks/
```

Notebooks should be used for:

* exploratory analysis;
* visualization;
* debugging;
* post-experiment analysis.

Core evaluation logic must remain in `src/`.

A notebook must not contain the only implementation of a research metric.

---

# 88. Script Rules

Reusable operational scripts belong in:

```text
scripts/
```

Examples:

```text
scripts/generate_scenarios.py
scripts/validate_environment.py
scripts/export_experiment.py
scripts/recompute_metrics.py
scripts/run_validation.py
```

Scripts should call reusable source modules instead of duplicating business logic.

---

# 89. Test Organization

```text
tests/
├── unit/
├── integration/
├── contract/
├── property/
├── regression/
├── evaluator/
└── e2e/
```

### Unit

Tests individual functions/classes.

### Integration

Tests multiple components together.

### Contract

Tests interfaces and schemas.

### Property

Tests general invariants.

### Regression

Protects fixed bugs.

### Evaluator

Tests whether the evaluator measures known cases correctly.

### E2E

Tests the full system.

---

# 90. Ground-Truth Test Cases

The evaluator test suite should include at minimum:

```text
GT01 Authorized Read
GT02 Unauthorized Read
GT03 Unauthorized Write
GT04 Correct Policy Denial
GT05 Branch Isolation Preserved
GT06 Cross-Branch State Leakage
GT07 Safe Timeout Recovery
GT08 Unsafe Timeout Recovery
GT09 Safe Malformed Response
GT10 Unsafe Malformed Response
GT11 Policy Engine Error
GT12 Missing Evidence
```

These cases form the minimum evaluator validation foundation.

---

# 91. Research Invariants

Important system invariants include:

```text
INV-001
Raw evidence is immutable.

INV-002
A validated failure must reference valid evidence.

INV-003
A branch cannot mutate its parent snapshot.

INV-004
Holdout outcomes cannot affect discovery-time selection.

INV-005
Budget cannot become negative.

INV-006
Every execution has a valid experiment/run association.

INV-007
A failure family cannot contain an invalid failure occurrence.

INV-008
Metric denominators follow their declared definitions.
```

---

# 92. Dependency Rules

Preferred dependency direction:

```text
domain
  ↓
interfaces
  ↓
services
  ↓
infrastructure
```

Avoid:

```text
domain → FastAPI
domain → SQLite
domain → dashboard
```

The research logic should remain portable.

---

# 93. External Model Integration

When integrating a real LLM:

```text
Real Model
    ↓
AgentAdapter
    ↓
Execution Engine
```

The rest of the evaluator should not need to know which provider is being used.

This permits experiments with different agent configurations without rewriting the evaluation engine.

---

# 94. Model Configuration

Record:

```text
provider
model_name
model_version
temperature
max_tokens
seed
system_instruction_hash
tool configuration
context configuration
```

Do not rely on a human remembering which model settings were used.

Humans are remarkably unreliable databases.

---

# 95. Randomness Management

Every stochastic component should have an explicit seed where possible.

Record separate seeds for:

```text
scenario generation
candidate mutation
selector
agent
fault injection
environment
clustering
statistical bootstrap
```

Do not use one hidden global random state for the entire system.

---

# 96. Reproducibility

A reproducible run requires:

```text
same configuration
+
same candidate pool
+
same seeds
+
same software
+
same dependencies
+
same environment version
```

For deterministic components, results should match.

For stochastic components, expected variation must be documented.

---

# 97. Debugging a Failed Experiment

When an experiment produces an unexpected result, inspect in this order:

```text
1. Experiment manifest
2. Resolved configuration
3. Candidate pool
4. Selection decisions
5. Budget records
6. Execution record
7. Trajectory
8. State transitions
9. Invariant evaluation
10. Failure evidence
11. Classification
12. Clustering
13. Validation
14. Metrics
```

Do not start by staring at the final chart.

The chart is where information goes to become misleading when the underlying data is broken.

---

# 98. Debugging Selection

Inspect:

```text
selection_decisions
```

For each decision:

```text
candidate
score
estimated cost
reward history
variance
novelty
branch potential
budget remaining
```

Verify the selected candidate was actually feasible.

---

# 99. Debugging Failure Detection

Inspect:

```text
execution
trajectory
invariant evaluation
evidence
failure candidate
validated failure
```

Do not debug a failure family before establishing that the underlying failure is valid.

---

# 100. Debugging Clustering

Inspect:

```text
failure signature
canonical representation
fingerprint
similarity score
threshold
cluster version
```

If clustering looks wrong, preserve the original raw failures.

Do not manually edit family assignments in the database without recording an audit event.

---

# 101. Debugging Reproduction

Inspect:

```text
original execution
reproduction attempts
seed
environment version
snapshot
reproduction comparator
divergence reason
```

Distinguish:

```text
NOT_REPRODUCED
```

from:

```text
ERROR
```

The first is evidence.

The second is an execution problem.

---

# 102. Debugging Metamorphic Tests

Inspect:

```text
base scenario
transformation
transformed scenario
base execution
transformed execution
protected properties
expected difference mask
relation result
```

Never mark a metamorphic relation as `PASS` without evaluating the actual transformed execution.

---

# 103. Debugging Holdout Leakage

Inspect:

```text
selector input
selection decision
available metadata
holdout access logs
database queries
experiment phase
```

If the selector receives holdout-derived information, the affected experiment should be treated as potentially invalid.

---

# 104. Research-Safe Development Rules

Developers must not:

1. tune selector weights using holdout results;
2. change invariants after seeing main results without versioning;
3. remove inconvenient failures from raw data;
4. manually rewrite failure families without audit records;
5. change budget definitions between compared methods;
6. exclude expensive branching costs for adaptive methods;
7. use future execution results during selection;
8. report simulated numbers as measured results;
9. silently modify candidate pools between baseline and adaptive experiments;
10. modify validation rules after observing results without declaring a new analysis configuration.

---

# 105. Adding a New Scenario

Steps:

```text
1. Define scenario
2. Assign stable ID
3. Define version
4. Define preconditions
5. Define initial state
6. Define objective
7. Define expected evidence
8. Map invariants
9. Validate reachability
10. Add tests
11. Add to candidate pool
12. Freeze before formal experiment
```

---

# 106. Adding a New Invariant

Steps:

```text
1. Define invariant
2. Define protected property
3. Define preconditions
4. Define evidence requirements
5. Implement evaluator
6. Create positive test
7. Create negative test
8. Create inconclusive test
9. Add regression tests
10. Version invariant
11. Add scenario mappings
```

---

# 107. Adding a New Selector

Steps:

```text
1. Define algorithm
2. Define allowed information
3. Define mathematical formula
4. Define initialization
5. Define reward
6. Implement selector
7. Create synthetic selector tests
8. Test leakage boundary
9. Test budget interaction
10. Add experiment configuration
11. Add baseline comparison
```

---

# 108. Adding a New Metamorphic Transformation

Define:

```text
transformation_id
version
input_scope
semantic_rationale
preconditions
transformation_function
protected_properties
expected_difference_mask
relation
```

Then test:

```text
valid transformation
invalid transformation
positive relation
negative relation
```

---

# 109. Adding a New Metric

Every metric must define:

```text
metric_id
version
formula
input tables
population
denominator
exclusions
aggregation
units
```

Add:

* unit tests;
* synthetic calculation;
* boundary cases;
* missing-data cases;
* documentation.

---

# 110. Adding a New Experiment

Create:

```text
configs/experiments/<experiment_name>.yaml
```

Define:

```text
method
candidate pool
budget
agent
environment
selector
validation
holdout
metrics
statistics
seed set
repetitions
```

Before execution:

```text
validate configuration
freeze candidate pool
generate manifest
record software version
```

---

# 111. Formal Experiment Workflow

```text
1. Checkout experiment commit
2. Install locked dependencies
3. Run complete test suite
4. Run evaluator validation
5. Validate configuration
6. Freeze candidate pool
7. Generate experiment manifest
8. Initialize database
9. Execute baseline runs
10. Execute adaptive runs
11. Preserve raw traces
12. Freeze discovery outputs
13. Run reproduction
14. Run metamorphic validation
15. Run hidden holdout
16. Compute metrics
17. Run statistical analysis
18. Export reproducibility bundle
19. Generate report
```

---

# 112. Experiment Phases

The implementation should preserve these phases:

```text
PHASE 0  Infrastructure Validation
PHASE 1  Evaluator Validation
PHASE 2  Baseline Calibration
PHASE 3  Main Discovery
PHASE 4  Branching
PHASE 5  Reproduction
PHASE 6  Metamorphic Testing
PHASE 7  Hidden Holdout
PHASE 8  Ablation
PHASE 9  Statistical Analysis
```

---

# 113. Baseline Experiment Matrix

Minimum comparison:

| Experiment | Selection         | Branching |
| ---------- | ----------------- | --------- |
| E1         | Random            | Off       |
| E2         | Uniform           | Off       |
| E3         | UCB-V             | Off       |
| E4         | Proposed Adaptive | Off       |
| E5         | Random            | On        |
| E6         | Uniform           | On        |
| E7         | UCB-V             | On        |
| E8         | Proposed Adaptive | On        |

All comparisons must use matched:

* candidate pools;
* budgets;
* seeds;
* environment;
* agent configuration;
* invariant set.

---

# 114. Recommended Repetitions

The methodology recommends:

```text
20 independent seeds per method
```

as a target for the main experiment where computational resources permit.

The same seed set should be used across matched methods where practical.

The exact number should be frozen in the experiment configuration before formal analysis.

---

# 115. Candidate Pool

Recommended prototype range:

```text
100–500 candidates
```

The candidate pool should be:

```text
static
frozen
versioned
hashed
```

for the primary comparison.

Dynamic candidate generation should be treated as a separate experimental factor.

---

# 116. Budget

The primary experimental comparison requires a fixed budget.

Example:

```text
Budget = B
```

Then:

```text
Random ≤ B
Uniform ≤ B
UCB-V ≤ B
Adaptive ≤ B
```

No method should receive additional resources merely because it has more expensive internal operations.

---

# 117. Validation Freeze

After discovery:

```text
Discovery
   ↓
Freeze Candidate Failures
   ↓
Reproduction
   ↓
Metamorphic Testing
   ↓
Holdout
```

The selector should not continue adapting based on final validation outcomes unless that behavior is itself an explicitly defined experiment.

---

# 118. Data Integrity Rules

Raw evidence:

```text
immutable
```

Derived evidence:

```text
versioned
recomputable
```

Reports:

```text
regenerable
```

This means:

```text
Raw Trace
    ↓
Detector v1
    ↓
Failure Records
```

can later be recomputed as:

```text
Raw Trace
    ↓
Detector v2
    ↓
Failure Records v2
```

without rerunning the agent.

---

# 119. Privacy and Sensitive Data

Even though the initial environment is simulated, the system should support:

* data minimization;
* synthetic identifiers;
* redaction;
* secret exclusion;
* artifact access controls.

Do not place real customer data into the repository.

---

# 120. Security of the Development Environment

When testing prompt injection, tool manipulation, or state manipulation:

* use isolated environments;
* use synthetic data;
* restrict network access where practical;
* prevent test agents from accessing developer credentials;
* avoid mounting sensitive host directories;
* use containers for higher-risk experiments.

---

# 121. Docker Development

A typical development workflow may use:

```bash
docker compose up --build
```

Services may eventually include:

```text
api
worker
database
tracking
dashboard
```

The exact service list should reflect the implemented architecture.

---

# 122. Docker Safety

Do not mount:

```text
$HOME
SSH keys
cloud credentials
production databases
```

into the agent execution container.

The controlled environment should remain controlled.

---

# 123. Continuous Integration

CI should run:

```text
lint
type-check
unit tests
contract tests
integration tests
evaluator validation
```

Recommended sequence:

```text
Lint
 ↓
Type Check
 ↓
Unit
 ↓
Contract
 ↓
Integration
 ↓
Evaluator
```

End-to-end experiments need not run on every commit if they are computationally expensive.

---

# 124. CI Research Gate

A formal research commit should not be considered experiment-ready if:

```text
test suite fails
```

or:

```text
evaluator validation fails
```

or:

```text
holdout isolation fails
```

or:

```text
budget verification fails
```

---

# 125. Pre-Experiment Command Sequence

A recommended workflow:

```bash
uv sync

uv run ruff check .

uv run ruff format --check .

uv run pytest

uv run python -m agent_eval.cli validate \
  --config configs/test.yaml

uv run python -m agent_eval.cli experiment validate \
  --config configs/experiments/adaptive_main.yaml
```

The final CLI syntax should match the implementation.

---

# 126. Post-Experiment Workflow

After execution:

```bash
uv run python -m agent_eval.cli experiment validate-results \
  --experiment-id <EXPERIMENT_ID>

uv run python -m agent_eval.cli metrics recompute \
  --experiment-id <EXPERIMENT_ID>

uv run python -m agent_eval.cli report generate \
  --experiment-id <EXPERIMENT_ID>

uv run python -m agent_eval.cli experiment export \
  --experiment-id <EXPERIMENT_ID>
```

Again, these are intended interface patterns. The final CLI must expose equivalent functionality.

---

# 127. Common Development Mistakes

## Mistake 1: Building the Dashboard First

The dashboard cannot compensate for an incorrect evaluator.

## Mistake 2: Using Real LLMs Before the Evaluator Works

This introduces model variability before the infrastructure has been validated.

## Mistake 3: Calling Something UCB-V Without Variance

If empirical variance is absent, it is not UCB-V.

## Mistake 4: Counting Raw Failures as New Families

Repeated occurrences of the same mechanism are not necessarily new discoveries.

## Mistake 5: Ignoring Branch Costs

Snapshot, restore, branch execution, and analysis consume resources.

## Mistake 6: Treating Clusters as Root Causes

Similarity does not establish causality.

## Mistake 7: Letting Holdout Results Influence Development

That contaminates generalization measurement.

## Mistake 8: Hard-Coding Dashboard Numbers

All formal numbers must originate from experiment records.

---

# 128. Developer Checklist

Before opening a pull request:

### Code

* [ ] Code follows project structure.
* [ ] Domain logic is infrastructure-independent.
* [ ] Types are defined.
* [ ] Errors are explicit.
* [ ] Logging includes relevant IDs.

### Tests

* [ ] Unit tests added.
* [ ] Integration tests added where needed.
* [ ] Regression test added for bug fixes.
* [ ] Evaluator tests added for research-critical changes.

### Research Integrity

* [ ] No future leakage.
* [ ] No holdout leakage.
* [ ] Budget semantics unchanged unless explicitly versioned.
* [ ] No hard-coded research results.
* [ ] No undocumented filtering.
* [ ] No silent changes to candidate pools.

### Documentation

* [ ] Configuration documented.
* [ ] Interface documented.
* [ ] Research implications documented.
* [ ] Version changed where appropriate.

---

# 129. Pull Request Checklist

Every research-relevant PR should answer:

```text
What changed?

Why did it change?

Which module owns the change?

Does it alter experiment semantics?

Does it alter budget accounting?

Does it alter failure detection?

Does it alter selector behavior?

Does it alter validation?

Does it alter metrics?

Which tests prove correctness?

Does it require new experiment configuration?

Does it invalidate previous results?
```

---

# 130. Research-Relevant Change Classification

Changes should be labelled:

```text
CODE_ONLY
BUG_FIX
EVALUATOR_SEMANTICS
EXPERIMENT_SEMANTICS
METRIC_SEMANTICS
CONFIGURATION
DATA
INFRASTRUCTURE
DOCUMENTATION
```

Changes labelled:

```text
EVALUATOR_SEMANTICS
EXPERIMENT_SEMANTICS
METRIC_SEMANTICS
```

require explicit research-impact review.

---

# 131. When Previous Results Become Invalid

Potentially invalidating changes include:

```text
invariant definition changed
failure validation rule changed
selector reward changed
budget formula changed
candidate generation changed
candidate pool changed
holdout isolation changed
metric definition changed
statistical unit changed
branching semantics changed
```

Such changes should create a new experiment version.

---

# 132. Reproducibility Bundle

A completed formal experiment should be exportable as:

```text
experiment_bundle/
├── manifest.yaml
├── resolved_config.yaml
├── candidate_pool.json
├── seeds.yaml
├── software_versions.json
├── dependency_lock.txt
├── database/
├── traces/
├── snapshots/
├── failures/
├── metrics/
├── statistics/
├── reports/
└── README.md
```

The bundle should contain enough information to reconstruct the analysis.

---

# 133. Developer Onboarding Path

A new developer should learn the project in this order:

```text
1. README
2. Project Specification
3. System Architecture
4. Agent / Environment Specification
5. Scenario Specification
6. Trajectory Schema
7. Invariant / Failure System
8. Adaptive Selection
9. Snapshot / Branching
10. Reproduction / Metamorphic Testing
11. Experimental Methodology
12. Database Schema
13. API Specification
14. Configuration Specification
15. Validation & Verification Plan
```

This order follows the dependency structure of the system.

---

# 134. First Task for a New Developer

Before modifying research logic:

```bash
uv sync
uv run pytest
```

Then run the smallest end-to-end experiment using the mock agent.

The developer should be able to answer:

1. What is a candidate?
2. What is an execution?
3. What is a trajectory?
4. What is an invariant?
5. What is a validated failure?
6. What is a failure family?
7. What is a branch?
8. What counts toward budget?
9. What information can the selector access?
10. Why is the holdout isolated?

If those answers are unclear, changing the selector is premature.

---

# 135. Architecture Reading Guide

The implementation should be understood as four major subsystems:

## Evaluation Engine

```text
Agent
Environment
Tools
Trajectory
Invariant
Failure
```

## Adaptive Engine

```text
Candidate Pool
Selection
Reward
Budget
Feedback
```

## Validation Engine

```text
Reproduction
Metamorphic
Holdout
```

## Research Engine

```text
Experiments
Metrics
Statistics
Tracking
Reporting
```

---

# 136. Final Developer Mental Model

The project can be understood as:

```text
             +----------------------+
             |   Candidate Pool     |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |  Adaptive Selector   |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |   Agent Execution    |
             +----------+-----------+
                        |
                        v
             +----------------------+
             | Trajectory + State   |
             +----------+-----------+
                        |
              +---------+---------+
              |                   |
              v                   v
        +-----------+       +-----------+
        | Snapshot  |       | Invariant |
        +-----+-----+       +-----+-----+
              |                   |
              v                   v
        +-----------+       +-----------+
        | Branching |       | Failures  |
        +-----+-----+       +-----+-----+
              |                   |
              +---------+---------+
                        |
                        v
             +----------------------+
             | Failure Families     |
             +----------+-----------+
                        |
             +----------+-----------+
             |          |            |
             v          v            v
        Reproduction  Metamorphic  Holdout
             |          |            |
             +----------+------------+
                        |
                        v
             +----------------------+
             | Metrics / Statistics |
             +----------+-----------+
                        |
                        v
             +----------------------+
             | Research Conclusions |
             +----------------------+
```

---

# 137. Final Repository Principles

The implementation should follow these principles:

### 1. Evidence before interpretation

Raw execution evidence is the foundation.

### 2. Validation before optimization

Do not optimize a broken evaluator.

### 3. Baselines before novelty

Implement Random, Uniform, and UCB-V before claiming the proposed adaptive strategy provides improvement.

### 4. Cost must be honest

Every method pays for the work it performs.

### 5. Holdout remains isolated

Generalization only means something if the evaluation data remains unseen.

### 6. Raw evidence remains immutable

Derived interpretations can change. Historical evidence should not.

### 7. Versions are scientific metadata

Configuration, code, scenarios, invariants, clustering, and metrics all require version tracking.

### 8. Negative results are valid

The system should make it possible to discover that a hypothesis was unsupported.

### 9. Reproducibility is part of implementation

It is not something added five minutes before writing the paper.

### 10. Research semantics outrank convenience

A shortcut that changes what an experiment measures is not a harmless refactor.

---

# 138. Definition of Done

The developer setup is complete when a new developer can:

* [ ] clone the repository;
* [ ] install dependencies;
* [ ] initialize the environment;
* [ ] run unit tests;
* [ ] run evaluator validation;
* [ ] run the mock agent;
* [ ] run a complete development experiment;
* [ ] inspect a trajectory;
* [ ] inspect an invariant evaluation;
* [ ] inspect a failure;
* [ ] inspect a failure family;
* [ ] inspect reproduction evidence;
* [ ] inspect metamorphic results;
* [ ] verify holdout isolation;
* [ ] calculate metrics;
* [ ] generate a report;
* [ ] export an experiment bundle;
* [ ] reproduce the analysis from the recorded configuration.

---

# 139. Final Command Summary

Once the corresponding CLI commands are implemented, the expected developer workflow is approximately:

```bash
# Install
uv sync

# Format
uv run ruff format .

# Lint
uv run ruff check .

# Type check
uv run mypy src

# Test
uv run pytest

# Validate evaluator
uv run python -m agent_eval.cli validate \
  --config configs/test.yaml

# Validate experiment configuration
uv run python -m agent_eval.cli experiment validate \
  --config configs/experiments/adaptive_main.yaml

# Run development experiment
uv run python -m agent_eval.cli experiment run \
  --config configs/experiments/baseline_random.yaml

# Recompute metrics
uv run python -m agent_eval.cli metrics recompute \
  --experiment-id <EXPERIMENT_ID>

# Generate report
uv run python -m agent_eval.cli report generate \
  --experiment-id <EXPERIMENT_ID>

# Export reproducibility bundle
uv run python -m agent_eval.cli experiment export \
  --experiment-id <EXPERIMENT_ID>
```

These commands define the intended developer experience. They should be treated as the interface contract for the eventual CLI implementation rather than as proof that the commands already exist.

---

# 140. Final Principle

The repository should make the following workflow boring:

```text
Clone
 ↓
Install
 ↓
Test
 ↓
Validate
 ↓
Configure
 ↓
Run
 ↓
Inspect
 ↓
Reproduce
```

That is a feature.

For a research system, boring infrastructure is good infrastructure. The interesting part should be whether adaptive evaluation discovers meaningful failures more efficiently, not whether somebody spent three hours trying to remember which environment variable initializes SQLite.
