# Data / Database Schema

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** DBS-01
**Document Type:** Data / Database Schema Specification
**Version:** 1.0
**Status:** Draft for Implementation

---

# 1. Purpose

This document defines the data model and database schema for the **Budget-Constrained Adaptive Security Evaluation of AI Agents** research platform.

The database must support the complete experimental lifecycle:

```text
Experiment
    ↓
Candidate Pool
    ↓
Scenario
    ↓
Agent Execution
    ↓
Trajectory
    ↓
Events / States
    ↓
Snapshots / Branches
    ↓
Invariant Evaluation
    ↓
Failure Candidate
    ↓
Validated Failure
    ↓
Failure Signature
    ↓
Failure Family
    ↓
Reproduction
    ↓
Metamorphic Testing
    ↓
Holdout Evaluation
    ↓
Metrics
```

The schema is designed around five principles:

1. **Raw execution evidence must be preserved.**
2. **Derived results must retain provenance.**
3. **Experiment configurations must be versioned.**
4. **Metrics must be recomputable from underlying records.**
5. **Development, validation, and holdout data must remain distinguishable.**

---

# 2. Storage Architecture

The initial implementation should use a hybrid storage architecture:

```text
SQLite
    +
JSONL
    +
Artifact Files
```

### SQLite

Used for:

* metadata,
* experiment records,
* scenarios,
* executions,
* states,
* events,
* invariant results,
* failures,
* families,
* validation results,
* metrics.

### JSONL

Used for:

* high-volume trajectory events,
* large tool responses,
* execution traces,
* model outputs,
* detailed state snapshots where appropriate.

### Artifact Files

Used for:

* configuration snapshots,
* experiment bundles,
* large serialized states,
* reports,
* plots,
* exported datasets.

---

# 3. Design Principle: Database as Evidence Ledger

The database should be treated as an **evidence ledger**, not merely an application database.

The system must preserve the relationship:

```text
"What happened?"
        ↓
"What was observed?"
        ↓
"What invariant was evaluated?"
        ↓
"Why was this considered a failure?"
        ↓
"How was it validated?"
        ↓
"Which family did it belong to?"
        ↓
"What experiment produced the result?"
```

Every derived research claim must be traceable backward to raw evidence.

---

# 4. Logical Data Layers

The schema is divided into six layers.

## Layer 1: Configuration

```text
experiments
agents
agent_configs
environments
environment_configs
tool_definitions
policy_definitions
invariants
```

## Layer 2: Scenario and Candidate Data

```text
scenario_pools
scenarios
scenario_versions
scenario_mutations
candidate_costs
```

## Layer 3: Execution Evidence

```text
experiment_runs
executions
trajectories
trajectory_events
states
snapshots
branches
```

## Layer 4: Evaluation

```text
invariant_evaluations
failure_candidates
validated_failures
failure_signatures
failure_families
failure_family_members
```

## Layer 5: Validation

```text
reproduction_attempts
metamorphic_transformations
metamorphic_tests
holdout_runs
```

## Layer 6: Measurement

```text
selection_decisions
cost_records
metric_definitions
run_metrics
aggregate_metrics
```

---

# 5. Identifier Strategy

All major entities require stable identifiers.

Recommended format:

```text
experiment_id
run_id
scenario_id
execution_id
trajectory_id
event_id
state_id
snapshot_id
branch_id
invariant_id
evaluation_id
failure_id
family_id
metric_id
```

Identifiers should be generated using UUIDv4 or another collision-resistant mechanism.

Example:

```text
execution_id:
exec_01J...
```

Human-readable prefixes are recommended.

---

# 6. Identifier Requirements

Identifiers must:

* be globally unique within the project,
* remain immutable,
* never be reused,
* survive database export/import,
* remain stable across analysis runs.

---

# 7. Versioning Strategy

Version the following independently:

```text
scenario_version
agent_config_version
environment_version
tool_registry_version
policy_version
invariant_version
trace_schema_version
detector_version
clustering_version
metric_version
experiment_config_version
```

A derived result must record the versions used to generate it.

---

# 8. Experiment Table

The `experiments` table represents a logical experimental study.

```sql
CREATE TABLE experiments (
    experiment_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    experiment_type TEXT NOT NULL,
    status TEXT NOT NULL,
    protocol_version TEXT NOT NULL,
    config_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### `experiment_type`

Examples:

```text
MAIN_DISCOVERY
ABLATION
REPRODUCTION
METAMORPHIC
HOLDOUT
EVALUATOR_VALIDATION
```

---

# 9. Experiment Run Table

A run is one independent statistical unit.

```sql
CREATE TABLE experiment_runs (
    run_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,

    method TEXT NOT NULL,
    seed INTEGER NOT NULL,

    agent_config_id TEXT NOT NULL,
    environment_config_id TEXT NOT NULL,
    scenario_pool_id TEXT NOT NULL,

    budget_allocated REAL NOT NULL,
    budget_actual REAL,

    started_at TEXT,
    completed_at TEXT,

    status TEXT NOT NULL,

    git_commit TEXT,
    container_version TEXT,

    FOREIGN KEY (experiment_id)
        REFERENCES experiments(experiment_id)
);
```

---

# 10. Run Status

Allowed values:

```text
CREATED
RUNNING
COMPLETED
PARTIAL
FAILED
INVALID
CANCELLED
```

---

# 11. Experiment Method

The `method` field identifies the evaluation strategy.

Initial values:

```text
RANDOM
UNIFORM
UCBV
COST_AWARE_UCBV
NOVELTY_AUGMENTED_UCBV
ADAPTIVE_BRANCHING
PROPOSED
```

The actual configuration must be stored separately.

---

# 12. Agent Table

```sql
CREATE TABLE agents (
    agent_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    adapter_type TEXT NOT NULL,
    model_provider TEXT,
    model_name TEXT,
    model_version TEXT,
    created_at TEXT NOT NULL
);
```

---

# 13. Agent Configuration Table

```sql
CREATE TABLE agent_configs (
    agent_config_id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    version TEXT NOT NULL,

    system_prompt_hash TEXT,
    generation_config_json TEXT,
    tool_config_json TEXT,
    memory_config_json TEXT,
    capability_config_json TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(agent_id, version),

    FOREIGN KEY (agent_id)
        REFERENCES agents(agent_id)
);
```

The actual system prompt may be stored as a protected artifact rather than directly in SQLite.

---

# 14. Agent Configuration Requirements

Record:

```text
model
model version
generation parameters
temperature
sampling configuration
context configuration
memory configuration
tool configuration
capabilities
policy constraints
```

This allows agent behavior to be reproduced as closely as possible.

---

# 15. Environment Table

```sql
CREATE TABLE environments (
    environment_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    environment_type TEXT NOT NULL,
    description TEXT,
    created_at TEXT NOT NULL
);
```

---

# 16. Environment Configuration

```sql
CREATE TABLE environment_configs (
    environment_config_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    version TEXT NOT NULL,

    database_config_json TEXT,
    policy_config_json TEXT,
    tool_config_json TEXT,
    fault_config_json TEXT,
    resource_limits_json TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(environment_id, version),

    FOREIGN KEY (environment_id)
        REFERENCES environments(environment_id)
);
```

---

# 17. Tool Definition Table

```sql
CREATE TABLE tool_definitions (
    tool_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,

    description TEXT,
    operation_type TEXT NOT NULL,

    input_schema_json TEXT,
    output_schema_json TEXT,

    trust_level TEXT,
    capability_required TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(name, version)
);
```

---

# 18. Tool Operation Types

Examples:

```text
READ
WRITE
NOTIFY
SEARCH
UPDATE
DELETE
EXTERNAL_REQUEST
```

The initial project may use:

```text
customer.lookup
account.lookup
transaction.lookup
ticket.search
ticket.update
notification.send
database.write
```

---

# 19. Scenario Pool Table

```sql
CREATE TABLE scenario_pools (
    scenario_pool_id TEXT PRIMARY KEY,

    name TEXT NOT NULL,
    version TEXT NOT NULL,

    split TEXT NOT NULL,

    generation_method TEXT,
    generation_config_json TEXT,

    candidate_count INTEGER,

    frozen INTEGER NOT NULL DEFAULT 0,

    created_at TEXT NOT NULL,

    UNIQUE(name, version)
);
```

---

# 20. Scenario Split

Allowed values:

```text
DEVELOPMENT
VALIDATION
HOLDOUT
REFERENCE
```

Holdout scenarios must be explicitly marked.

---

# 21. Scenario Table

```sql
CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,

    scenario_pool_id TEXT NOT NULL,

    scenario_key TEXT NOT NULL,
    current_version TEXT NOT NULL,

    category TEXT NOT NULL,
    subcategory TEXT,

    difficulty INTEGER,
    risk_level TEXT,

    description TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(
        scenario_pool_id,
        scenario_key
    ),

    FOREIGN KEY (scenario_pool_id)
        REFERENCES scenario_pools(scenario_pool_id)
);
```

---

# 22. Scenario Version Table

```sql
CREATE TABLE scenario_versions (
    scenario_version_id TEXT PRIMARY KEY,

    scenario_id TEXT NOT NULL,
    version TEXT NOT NULL,

    task_definition_json TEXT,
    initial_state_json TEXT,
    preconditions_json TEXT,
    goal_definition_json TEXT,

    attack_objective_json TEXT,
    perturbation_json TEXT,

    expected_invariants_json TEXT,

    estimated_cost REAL,

    created_at TEXT NOT NULL,

    UNIQUE(scenario_id, version),

    FOREIGN KEY (scenario_id)
        REFERENCES scenarios(scenario_id)
);
```

---

# 23. Scenario Categories

Initial values:

```text
BENIGN
AUTHORIZATION
TOOL_SECURITY
PROMPT_INJECTION
DATA_EXPOSURE
STATE_MANIPULATION
SEQUENCE_ATTACK
FAULT_TOLERANCE
ROBUSTNESS
RESOURCE_ABUSE
RECOVERY
BRANCH_ATTACK
METAMORPHIC
HOLDOUT_VARIANT
```

---

# 24. Scenario Mutation Table

```sql
CREATE TABLE scenario_mutations (
    mutation_id TEXT PRIMARY KEY,

    parent_scenario_version_id TEXT NOT NULL,

    mutation_operator TEXT NOT NULL,
    mutation_parameters_json TEXT,

    resulting_scenario_version_id TEXT,

    created_at TEXT NOT NULL
);
```

This preserves scenario lineage.

---

# 25. Candidate Table

A candidate is an executable evaluation opportunity.

```sql
CREATE TABLE candidates (
    candidate_id TEXT PRIMARY KEY,

    scenario_version_id TEXT NOT NULL,

    candidate_type TEXT NOT NULL,

    novelty_features_json TEXT,
    branch_features_json TEXT,
    estimated_cost REAL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (scenario_version_id)
        REFERENCES scenario_versions(scenario_version_id)
);
```

---

# 26. Candidate vs Scenario

These must remain separate.

### Scenario

Defines what should be tested.

### Candidate

Defines a particular executable evaluation opportunity.

For example:

```text
Scenario:
Unauthorized transaction access

Candidate 1:
customer=A, transaction=B

Candidate 2:
customer=C, transaction=D

Candidate 3:
cross-account variation
```

---

# 27. Execution Table

Each candidate execution receives a unique execution record.

```sql
CREATE TABLE executions (
    execution_id TEXT PRIMARY KEY,

    run_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,

    execution_mode TEXT NOT NULL,

    parent_execution_id TEXT,
    parent_snapshot_id TEXT,
    branch_id TEXT,

    seed INTEGER,

    started_at TEXT,
    completed_at TEXT,

    status TEXT NOT NULL,

    termination_reason TEXT,

    trace_schema_version TEXT NOT NULL,

    FOREIGN KEY (run_id)
        REFERENCES experiment_runs(run_id),

    FOREIGN KEY (candidate_id)
        REFERENCES candidates(candidate_id)
);
```

---

# 28. Execution Modes

Initial values:

```text
NORMAL
BRANCH
REPLAY
METAMORPHIC_BASE
METAMORPHIC_TRANSFORMED
HOLDOUT
REFERENCE
```

---

# 29. Execution Status

```text
RUNNING
COMPLETED
TIMEOUT
FAILED
INVALID
CANCELLED
```

---

# 30. Trajectory Table

```sql
CREATE TABLE trajectories (
    trajectory_id TEXT PRIMARY KEY,

    execution_id TEXT NOT NULL,

    sequence_start INTEGER,
    sequence_end INTEGER,

    event_count INTEGER,
    state_count INTEGER,

    completeness_status TEXT,

    trajectory_hash TEXT,

    created_at TEXT NOT NULL,

    FOREIGN KEY (execution_id)
        REFERENCES executions(execution_id)
);
```

---

# 31. Trajectory Completeness

Allowed values:

```text
COMPLETE
PARTIAL
CORRUPTED
UNKNOWN
```

A partial trajectory must not automatically produce a PASS result for absence-based invariants.

---

# 32. Event Table

The event table stores the chronological execution trace.

```sql
CREATE TABLE trajectory_events (
    event_id TEXT PRIMARY KEY,

    trajectory_id TEXT NOT NULL,

    sequence_number INTEGER NOT NULL,

    event_type TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    state_id TEXT,

    actor TEXT,

    tool_id TEXT,

    policy_decision_id TEXT,

    payload_json TEXT,

    payload_hash TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(
        trajectory_id,
        sequence_number
    ),

    FOREIGN KEY (trajectory_id)
        REFERENCES trajectories(trajectory_id)
);
```

---

# 33. Event Types

Initial event types:

```text
EXECUTION_START
AGENT_OUTPUT
TOOL_REQUEST
TOOL_RESPONSE
POLICY_DECISION
STATE_TRANSITION
FAULT_INJECTION
SNAPSHOT_CREATED
SNAPSHOT_RESTORED
BRANCH_CREATED
INVARIANT_EVALUATION
COST_RECORDED
EXECUTION_TERMINATION
ERROR
```

---

# 34. Event Payload

`payload_json` stores structured event-specific data.

Example:

```json
{
  "tool": "transaction.lookup",
  "arguments": {
    "transaction_id": "txn_123"
  }
}
```

Sensitive identifiers should be normalized or protected where required.

---

# 35. Event Immutability

Once a trajectory is finalized:

```text
trajectory_events
```

must be append-only or immutable.

Corrections should create:

```text
correction_record
```

rather than silently modifying historical evidence.

---

# 36. State Table

```sql
CREATE TABLE states (
    state_id TEXT PRIMARY KEY,

    execution_id TEXT NOT NULL,
    trajectory_id TEXT,

    sequence_number INTEGER NOT NULL,

    state_type TEXT NOT NULL,

    canonical_state_json TEXT,
    state_artifact_uri TEXT,

    state_hash TEXT,

    created_at TEXT NOT NULL,

    FOREIGN KEY (execution_id)
        REFERENCES executions(execution_id)
);
```

---

# 37. State Types

Examples:

```text
INITIAL
INTERMEDIATE
POST_TOOL
POST_POLICY
PRE_FAULT
POST_FAULT
TERMINAL
RESTORED
BRANCH_INITIAL
```

---

# 38. State Representation

The controlled environment state should represent:

$$
S=
\{
identity\_state,
authorization\_state,
data\_state,
tool\_state,
service\_state,
policy\_state,
task\_state,
fault\_state,
resource\_state
\}
$$

Not every component needs to be persisted for every state if the environment can deterministically reconstruct it.

---

# 39. State Hash

Every canonical state should have:

```text
state_hash
```

computed from a canonical serialized representation.

This enables:

* equality checks,
* snapshot verification,
* branch comparison,
* reproducibility checks.

---

# 40. Snapshot Table

```sql
CREATE TABLE snapshots (
    snapshot_id TEXT PRIMARY KEY,

    execution_id TEXT NOT NULL,
    trajectory_id TEXT NOT NULL,
    state_id TEXT NOT NULL,

    parent_snapshot_id TEXT,

    snapshot_type TEXT NOT NULL,

    state_hash TEXT NOT NULL,
    artifact_uri TEXT,

    snapshot_cost REAL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (execution_id)
        REFERENCES executions(execution_id),

    FOREIGN KEY (trajectory_id)
        REFERENCES trajectories(trajectory_id),

    FOREIGN KEY (state_id)
        REFERENCES states(state_id)
);
```

---

# 41. Snapshot Types

```text
AUTOMATIC
MANUAL
BRANCH_POINT
REPLAY
CHECKPOINT
```

---

# 42. Branch Table

```sql
CREATE TABLE branches (
    branch_id TEXT PRIMARY KEY,

    run_id TEXT NOT NULL,

    parent_execution_id TEXT NOT NULL,
    parent_snapshot_id TEXT NOT NULL,

    branch_depth INTEGER NOT NULL,

    branch_index INTEGER NOT NULL,

    execution_id TEXT,

    branch_reason TEXT,

    restore_cost REAL,
    execution_cost REAL,
    analysis_cost REAL,

    status TEXT NOT NULL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (run_id)
        REFERENCES experiment_runs(run_id)
);
```

---

# 43. Branch Status

```text
CREATED
RESTORED
RUNNING
COMPLETED
FAILED
INVALID
CANCELLED
```

---

# 44. Invariant Table

```sql
CREATE TABLE invariants (
    invariant_id TEXT PRIMARY KEY,

    version TEXT NOT NULL,

    name TEXT NOT NULL,
    description TEXT,

    category TEXT NOT NULL,
    subcategory TEXT,

    severity TEXT,

    status TEXT NOT NULL,

    scope_json TEXT,
    preconditions_json TEXT,
    predicate_json TEXT,
    evidence_requirements_json TEXT,

    detector_version TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(invariant_id, version)
);
```

---

# 45. Invariant Status

```text
DRAFT
ACTIVE
DEPRECATED
INVALID
```

Only `ACTIVE` invariants may be used in primary experiments.

---

# 46. Scenario-Invariant Mapping

```sql
CREATE TABLE scenario_invariants (
    scenario_version_id TEXT NOT NULL,
    invariant_id TEXT NOT NULL,
    invariant_version TEXT NOT NULL,

    required INTEGER NOT NULL DEFAULT 1,

    PRIMARY KEY (
        scenario_version_id,
        invariant_id,
        invariant_version
    )
);
```

This explicitly records which invariants apply to each scenario.

---

# 47. Invariant Evaluation Table

```sql
CREATE TABLE invariant_evaluations (
    evaluation_id TEXT PRIMARY KEY,

    execution_id TEXT NOT NULL,
    trajectory_id TEXT NOT NULL,

    invariant_id TEXT NOT NULL,
    invariant_version TEXT NOT NULL,

    result TEXT NOT NULL,

    evidence_complete INTEGER NOT NULL,

    explanation TEXT,

    detector_version TEXT,

    evaluation_cost REAL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (execution_id)
        REFERENCES executions(execution_id),

    FOREIGN KEY (trajectory_id)
        REFERENCES trajectories(trajectory_id),

    FOREIGN KEY (invariant_id, invariant_version)
        REFERENCES invariants(invariant_id, version)
);
```

---

# 48. Invariant Results

Allowed values:

```text
PASS
FAIL
INCONCLUSIVE
ERROR
NOT_APPLICABLE
```

---

# 49. Evaluation Evidence Table

Evidence should be normalized rather than embedded entirely inside the evaluation record.

```sql
CREATE TABLE evaluation_evidence (
    evidence_id TEXT PRIMARY KEY,

    evaluation_id TEXT NOT NULL,

    evidence_type TEXT NOT NULL,

    event_id TEXT,
    state_id TEXT,
    snapshot_id TEXT,
    policy_decision_id TEXT,

    relevance TEXT,

    created_at TEXT NOT NULL,

    FOREIGN KEY (evaluation_id)
        REFERENCES invariant_evaluations(evaluation_id)
);
```

---

# 50. Evidence Types

```text
EVENT
STATE
POLICY_DECISION
TOOL_REQUEST
TOOL_RESPONSE
STATE_TRANSITION
FAULT
RESOURCE_ACCESS
RESOURCE_MUTATION
```

---

# 51. Failure Candidate Table

```sql
CREATE TABLE failure_candidates (
    candidate_failure_id TEXT PRIMARY KEY,

    evaluation_id TEXT NOT NULL,

    execution_id TEXT NOT NULL,
    trajectory_id TEXT NOT NULL,

    invariant_id TEXT NOT NULL,
    invariant_version TEXT NOT NULL,

    detector_version TEXT NOT NULL,

    status TEXT NOT NULL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (evaluation_id)
        REFERENCES invariant_evaluations(evaluation_id)
);
```

---

# 52. Failure Candidate Status

```text
DETECTED
UNDER_VALIDATION
VALIDATED
REJECTED
INCONCLUSIVE
```

---

# 53. Validated Failure Table

```sql
CREATE TABLE validated_failures (
    failure_id TEXT PRIMARY KEY,

    candidate_failure_id TEXT NOT NULL,

    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL,

    scenario_id TEXT NOT NULL,
    scenario_version TEXT NOT NULL,

    execution_id TEXT NOT NULL,
    trajectory_id TEXT NOT NULL,
    branch_id TEXT,

    invariant_id TEXT NOT NULL,
    invariant_version TEXT NOT NULL,

    responsibility TEXT NOT NULL,

    validation_status TEXT NOT NULL,

    classification_json TEXT,

    severity TEXT,

    detector_version TEXT,
    validator_version TEXT,

    created_at TEXT NOT NULL,

    FOREIGN KEY (candidate_failure_id)
        REFERENCES failure_candidates(candidate_failure_id)
);
```

---

# 54. Failure Responsibility

Allowed values:

```text
AGENT
ENVIRONMENT
TOOL
POLICY_ENGINE
EVALUATOR
INFRASTRUCTURE
SCENARIO
UNKNOWN
```

---

# 55. Validation Status

```text
VALIDATED
REJECTED
INCONCLUSIVE
```

Only `VALIDATED` records enter the primary failure-discovery metrics.

---

# 56. Failure Signature Table

```sql
CREATE TABLE failure_signatures (
    signature_id TEXT PRIMARY KEY,

    failure_id TEXT NOT NULL,

    invariant_id TEXT NOT NULL,
    category TEXT,
    failure_type TEXT,
    mechanism TEXT,

    tool_path TEXT,
    resource_type TEXT,
    state_transition_type TEXT,
    policy_context TEXT,
    attack_surface TEXT,

    canonical_signature_json TEXT NOT NULL,

    exact_fingerprint TEXT NOT NULL,

    signature_version TEXT NOT NULL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (failure_id)
        REFERENCES validated_failures(failure_id)
);
```

---

# 57. Signature Canonicalization

Canonical signatures must remove execution-specific information such as:

```text
execution UUID
event UUID
temporary resource ID
timestamp
random trace identifier
```

while preserving mechanism-relevant distinctions.

---

# 58. Failure Family Table

```sql
CREATE TABLE failure_families (
    family_id TEXT PRIMARY KEY,

    experiment_id TEXT NOT NULL,

    family_name TEXT,

    family_description TEXT,

    clustering_version TEXT NOT NULL,

    clustering_method TEXT NOT NULL,

    family_fingerprint TEXT,

    created_at TEXT NOT NULL
);
```

---

# 59. Failure Family Membership

```sql
CREATE TABLE failure_family_members (
    family_id TEXT NOT NULL,
    failure_id TEXT NOT NULL,

    membership_score REAL,
    membership_type TEXT NOT NULL,

    assigned_by TEXT NOT NULL,

    created_at TEXT NOT NULL,

    PRIMARY KEY (
        family_id,
        failure_id
    ),

    FOREIGN KEY (family_id)
        REFERENCES failure_families(family_id),

    FOREIGN KEY (failure_id)
        REFERENCES validated_failures(failure_id)
);
```

---

# 60. Membership Types

```text
EXACT
STRUCTURED_SIMILARITY
MANUAL_REVIEW
OUTLIER
```

---

# 61. Clustering Rule

The database must preserve:

```text
clustering_method
clustering_version
parameters
```

The clustering implementation must be reproducible from the stored configuration.

---

# 62. Reproduction Attempt Table

```sql
CREATE TABLE reproduction_attempts (
    reproduction_id TEXT PRIMARY KEY,

    failure_id TEXT NOT NULL,

    attempt_number INTEGER NOT NULL,

    execution_id TEXT,

    reproduction_mode TEXT NOT NULL,

    seed INTEGER,

    outcome TEXT NOT NULL,

    mechanism_match INTEGER,

    evidence_match INTEGER,

    divergence_type TEXT,

    cost REAL,

    created_at TEXT NOT NULL,

    FOREIGN KEY (failure_id)
        REFERENCES validated_failures(failure_id)
);
```

---

# 63. Reproduction Modes

```text
EXACT_REPLAY
CONTROLLED_REPLAY
INDEPENDENT_SEED
STATE_REPLAY
BRANCH_REPLAY
```

---

# 64. Reproduction Outcomes

```text
REPRODUCED
NOT_REPRODUCED
PARTIAL
INCONCLUSIVE
INVALID
ERROR
```

---

# 65. Metamorphic Transformation Table

```sql
CREATE TABLE metamorphic_transformations (
    transformation_id TEXT PRIMARY KEY,

    name TEXT NOT NULL,
    version TEXT NOT NULL,

    category TEXT NOT NULL,

    definition_json TEXT NOT NULL,
    rationale TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(name, version)
);
```

---

# 66. Transformation Categories

```text
SEMANTIC_PRESERVING
IDENTIFIER_PRESERVING
FORMAT_ONLY
CONTEXT_IRRELEVANT
SEQUENCE_EQUIVALENT
AUTHORIZATION_EQUIVALENT
DATA_EQUIVALENT
TOOL_EQUIVALENT
```

---

# 67. Metamorphic Test Table

```sql
CREATE TABLE metamorphic_tests (
    metamorphic_test_id TEXT PRIMARY KEY,

    failure_id TEXT,
    base_execution_id TEXT NOT NULL,
    transformed_execution_id TEXT NOT NULL,

    transformation_id TEXT NOT NULL,
    transformation_version TEXT NOT NULL,

    relation_type TEXT NOT NULL,

    expected_relation_json TEXT NOT NULL,

    result TEXT NOT NULL,

    comparison_json TEXT,

    cost REAL,

    created_at TEXT NOT NULL
);
```

---

# 68. Metamorphic Results

```text
PASS
VIOLATION
INCONCLUSIVE
INVALID
ERROR
```

---

# 69. Holdout Run Table

```sql
CREATE TABLE holdout_runs (
    holdout_run_id TEXT PRIMARY KEY,

    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL,

    scenario_id TEXT NOT NULL,
    scenario_version TEXT NOT NULL,

    development_family_id TEXT,

    execution_id TEXT,

    matched_mechanism INTEGER,

    result TEXT NOT NULL,

    created_at TEXT NOT NULL
);
```

---

# 70. Holdout Isolation

Holdout records must be clearly marked and must not influence adaptive selection during development.

The database should enforce this through experiment-stage metadata where possible.

---

# 71. Selection Decision Table

Every adaptive selection decision should be stored.

```sql
CREATE TABLE selection_decisions (
    selection_id TEXT PRIMARY KEY,

    run_id TEXT NOT NULL,

    decision_number INTEGER NOT NULL,

    candidate_id TEXT NOT NULL,

    selected INTEGER NOT NULL,

    remaining_budget REAL,

    estimated_cost REAL,

    reward_mean REAL,
    reward_variance REAL,

    ucb_score REAL,
    novelty_score REAL,
    branch_score REAL,
    severity_score REAL,
    cost_penalty REAL,

    final_score REAL,

    selection_algorithm TEXT,
    algorithm_version TEXT,

    created_at TEXT NOT NULL
);
```

---

# 72. Selection Decision Purpose

This table allows the experiment to answer:

> Why was candidate \(c\) selected at time \(t\)?

without requiring private model reasoning.

---

# 73. Cost Record Table

```sql
CREATE TABLE cost_records (
    cost_id TEXT PRIMARY KEY,

    run_id TEXT NOT NULL,
    execution_id TEXT,

    cost_type TEXT NOT NULL,

    quantity REAL NOT NULL,
    unit TEXT NOT NULL,

    monetary_cost REAL,

    source TEXT,

    created_at TEXT NOT NULL
);
```

---

# 74. Cost Types

```text
GENERATION
MODEL_CALL
TOKEN
EXECUTION
BRANCH
SNAPSHOT
RESTORE
ANALYSIS
VERIFICATION
SELECTION
REPRODUCTION
METAMORPHIC
HOLDOUT
INFRASTRUCTURE
```

---

# 75. Cost Aggregation

The total experiment cost is:

$$
C_{total}
=
C_{generation}
+
C_{execution}
+
C_{branch}
+
C_{snapshot}
+
C_{restore}
+
C_{analysis}
+
C_{verification}
$$

Additional costs such as selection, reproduction, metamorphic testing, and holdout evaluation should be included when they belong to the declared experiment budget.

---

# 76. Budget Table

```sql
CREATE TABLE budgets (
    budget_id TEXT PRIMARY KEY,

    run_id TEXT NOT NULL,

    budget_type TEXT NOT NULL,

    allocated REAL NOT NULL,
    consumed REAL DEFAULT 0,
    reserved REAL DEFAULT 0,

    unit TEXT NOT NULL,

    created_at TEXT NOT NULL
);
```

---

# 77. Budget Types

```text
DISCOVERY
FULL_EVALUATION
MODEL
COMPUTE
MONETARY
COMPOSITE
```

---

# 78. Metric Definition Table

```sql
CREATE TABLE metric_definitions (
    metric_id TEXT PRIMARY KEY,

    name TEXT NOT NULL,
    version TEXT NOT NULL,

    category TEXT NOT NULL,

    numerator_definition TEXT,
    denominator_definition TEXT,

    population TEXT,
    aggregation_method TEXT,

    direction TEXT,

    formula TEXT,

    created_at TEXT NOT NULL,

    UNIQUE(metric_id, version)
);
```

---

# 79. Run Metrics Table

```sql
CREATE TABLE run_metrics (
    metric_record_id TEXT PRIMARY KEY,

    metric_id TEXT NOT NULL,
    metric_version TEXT NOT NULL,

    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL,

    value REAL,
    numerator REAL,
    denominator REAL,

    unit TEXT,

    aggregation_method TEXT,

    created_at TEXT NOT NULL
);
```

---

# 80. Aggregate Metrics Table

```sql
CREATE TABLE aggregate_metrics (
    aggregate_id TEXT PRIMARY KEY,

    metric_id TEXT NOT NULL,
    metric_version TEXT NOT NULL,

    experiment_id TEXT NOT NULL,
    method TEXT NOT NULL,

    sample_count INTEGER NOT NULL,

    mean REAL,
    median REAL,
    stddev REAL,
    q1 REAL,
    q3 REAL,

    ci_lower REAL,
    ci_upper REAL,

    effect_size REAL,

    created_at TEXT NOT NULL
);
```

---

# 81. Metric Aggregation Boundary

Metrics must be calculated:

```text
raw records
   ↓
per-run metrics
   ↓
aggregate metrics
```

Do not directly aggregate raw events into final research statistics unless the metric definition explicitly requires it.

---

# 82. Error / Infrastructure Table

Evaluation infrastructure failures should be separately recorded.

```sql
CREATE TABLE system_errors (
    error_id TEXT PRIMARY KEY,

    run_id TEXT,
    execution_id TEXT,

    component TEXT NOT NULL,
    error_type TEXT NOT NULL,

    message TEXT,
    stacktrace_artifact_uri TEXT,

    recoverable INTEGER,
    recovered INTEGER,

    created_at TEXT NOT NULL
);
```

---

# 83. Component Values

Examples:

```text
AGENT
TOOL_GATEWAY
POLICY_ENGINE
ENVIRONMENT
TRACE_COLLECTOR
SNAPSHOT_MANAGER
BRANCH_MANAGER
INVARIANT_ENGINE
FAILURE_VALIDATOR
CLUSTERING
METRICS
EXPERIMENT_CONTROLLER
```

---

# 84. Artifact Table

Large files should be referenced rather than embedded into SQLite.

```sql
CREATE TABLE artifacts (
    artifact_id TEXT PRIMARY KEY,

    artifact_type TEXT NOT NULL,

    uri TEXT NOT NULL,

    content_hash TEXT NOT NULL,

    size_bytes INTEGER,

    media_type TEXT,

    created_at TEXT NOT NULL
);
```

---

# 85. Artifact Types

```text
TRACE
STATE
SNAPSHOT
CONFIG
MODEL_OUTPUT
REPORT
PLOT
DATASET
LOG
EXPERIMENT_BUNDLE
```

---

# 86. Configuration Artifact

Each experiment should preserve an immutable configuration artifact:

```yaml
experiment:
  method:
  seed:
  budget:
  agent_config:
  environment_config:
  scenario_pool:
  invariant_set:
  clustering:
  reproduction:
  metamorphic:
  holdout:
  metrics:
```

---

# 87. Foreign-Key Relationship Overview

The central relationship graph is:

```text
experiments
    │
    └── experiment_runs
             │
             ├── selection_decisions
             ├── budgets
             ├── cost_records
             └── executions
                    │
                    ├── trajectories
                    │       │
                    │       ├── trajectory_events
                    │       └── states
                    │
                    ├── snapshots
                    └── branches
```

Scenario side:

```text
scenario_pools
    ↓
scenarios
    ↓
scenario_versions
    ↓
candidates
    ↓
executions
```

Evaluation side:

```text
executions
    ↓
invariant_evaluations
    ↓
failure_candidates
    ↓
validated_failures
    ↓
failure_signatures
    ↓
failure_families
```

Validation side:

```text
validated_failures
    ├── reproduction_attempts
    └── metamorphic_tests

development families
    ↓
holdout_runs
```

Measurement side:

```text
experiments
    ↓
run_metrics
    ↓
aggregate_metrics
```

---

# 88. Simplified ER Diagram

```text
┌──────────────┐
│ experiments  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ experiment_  │
│ runs         │
└──────┬───────┘
       │
       ▼
┌──────────────┐       ┌──────────────┐
│ executions   │◄──────│ candidates   │
└──────┬───────┘       └──────┬───────┘
       │                      │
       ▼                      ▼
┌──────────────┐       ┌──────────────┐
│ trajectories │       │ scenarios    │
└──────┬───────┘       └──────────────┘
       │
       ├───────────────┐
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│ events       │ │ states       │
└──────┬───────┘ └──────┬───────┘
       │                │
       └───────┬────────┘
               ▼
      ┌────────────────────┐
      │ invariant_evaluate │
      └──────────┬─────────┘
                 ▼
      ┌────────────────────┐
      │ failure_candidates │
      └──────────┬─────────┘
                 ▼
      ┌────────────────────┐
      │ validated_failures │
      └──────────┬─────────┘
                 ▼
      ┌────────────────────┐
      │ failure_signatures │
      └──────────┬─────────┘
                 ▼
      ┌────────────────────┐
      │ failure_families   │
      └────────────────────┘
```

---

# 89. Data Lifecycle

Every execution follows:

```text
CREATED
   ↓
RUNNING
   ↓
TRACE_FINALIZED
   ↓
INVARIANTS_EVALUATED
   ↓
FAILURES_VALIDATED
   ↓
CLUSTERED
   ↓
VALIDATED
   ↓
ARCHIVED
```

The exact state machine may be simplified in implementation.

---

# 90. Immutable Data

The following should be treated as immutable after finalization:

```text
scenario version
candidate definition
trajectory event
original state
snapshot
original invariant result
original failure candidate
original validated failure
reproduction attempt
metamorphic test
holdout result
```

Corrections should create new records or revisions.

---

# 91. Derived Data

The following are derived:

```text
failure signatures
failure families
run metrics
aggregate metrics
discovery curves
statistical summaries
dashboard views
```

Derived data must always be reproducible from stored inputs.

---

# 92. Raw vs Derived Boundary

### Raw

```text
agent output
tool request
tool response
policy decision
state
fault
cost event
trajectory event
```

### Derived

```text
invariant result
failure classification
failure signature
cluster
metric
statistical result
```

This distinction must be preserved.

---

# 93. Data Provenance

Every derived object should record enough information to identify:

```text
source execution
source trace
source invariant
source configuration
source software version
```

---

# 94. Provenance Example

A failure record should allow:

```text
failure_id
    ↓
candidate_failure_id
    ↓
invariant_evaluation_id
    ↓
trajectory_id
    ↓
execution_id
    ↓
scenario_version_id
    ↓
candidate_id
    ↓
experiment_run_id
    ↓
experiment_id
```

---

# 95. Trace Hashing

Each finalized trajectory should have a deterministic hash.

Example:

$$
H_{\tau}
=
SHA256(
canonicalize(\tau)
)
$$

This helps detect accidental trace modification.

---

# 96. State Hashing

Similarly:

$$
H_s =
SHA256(
canonicalize(s)
)
$$

State hashes support snapshot integrity and branch comparison.

---

# 97. Snapshot Integrity

On restore:

```text
snapshot.state_hash
        ==
restored_state.state_hash
```

must hold for an exact restoration.

If not:

```text
snapshot restoration failure
```

must be recorded.

---

# 98. Data Normalization Strategy

The schema uses a mixed approach.

Normalize:

```text
experiments
runs
agents
scenarios
executions
events
states
failures
families
metrics
```

Use JSON for highly variable structures:

```text
tool arguments
tool responses
scenario configuration
policy configuration
state substructures
selection features
metric metadata
```

---

# 99. Why Not Fully Normalize Everything?

AI-agent trajectories contain heterogeneous payloads.

Forcing every possible tool response and state field into relational columns would produce a database schema approximately the size of a small bureaucracy.

Use structured JSON where the schema is intentionally extensible.

---

# 100. JSON Schema Validation

All JSON columns should have application-level schemas.

Recommended:

```text
Pydantic models
JSON Schema
```

Every major JSON payload type should have a version.

---

# 101. Trace JSONL Format

Example:

```json
{"event_id":"evt_001","sequence":1,"event_type":"EXECUTION_START","timestamp":"..."}
{"event_id":"evt_002","sequence":2,"event_type":"AGENT_OUTPUT","timestamp":"..."}
{"event_id":"evt_003","sequence":3,"event_type":"TOOL_REQUEST","timestamp":"..."}
{"event_id":"evt_004","sequence":4,"event_type":"POLICY_DECISION","timestamp":"..."}
{"event_id":"evt_005","sequence":5,"event_type":"TOOL_RESPONSE","timestamp":"..."}
```

---

# 102. Database Indexes

Recommended indexes:

```sql
CREATE INDEX idx_runs_experiment
ON experiment_runs(experiment_id);

CREATE INDEX idx_executions_run
ON executions(run_id);

CREATE INDEX idx_executions_candidate
ON executions(candidate_id);

CREATE INDEX idx_events_trajectory
ON trajectory_events(trajectory_id);

CREATE INDEX idx_events_type
ON trajectory_events(event_type);

CREATE INDEX idx_states_execution
ON states(execution_id);

CREATE INDEX idx_invariant_eval_execution
ON invariant_evaluations(execution_id);

CREATE INDEX idx_failures_run
ON validated_failures(run_id);

CREATE INDEX idx_failures_invariant
ON validated_failures(invariant_id);

CREATE INDEX idx_signatures_fingerprint
ON failure_signatures(exact_fingerprint);

CREATE INDEX idx_family_members_family
ON failure_family_members(family_id);

CREATE INDEX idx_family_members_failure
ON failure_family_members(failure_id);

CREATE INDEX idx_metrics_run
ON run_metrics(run_id);

CREATE INDEX idx_metrics_experiment
ON run_metrics(experiment_id);
```

---

# 103. Performance Strategy

High-volume tables:

```text
trajectory_events
states
cost_records
selection_decisions
```

may become large.

Use:

* batch inserts,
* WAL mode,
* prepared statements,
* JSONL streaming,
* periodic commits,
* artifact storage for large payloads.

---

# 104. SQLite Configuration

Recommended:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

For final archival databases, stricter durability settings may be appropriate.

---

# 105. Transaction Boundaries

Execution finalization should be transactional.

Example:

```text
BEGIN
    finalize trajectory
    write invariant results
    write failure candidates
    write costs
COMMIT
```

A partially committed execution should be clearly marked.

---

# 106. Concurrency

Multiple executions may run concurrently.

Avoid:

* shared mutable state,
* shared database transaction conflicts,
* branch-state contamination.

Use unique execution IDs and isolated environment instances.

---

# 107. Branch Isolation in Storage

Every branch must have:

```text
branch_id
parent_execution_id
parent_snapshot_id
execution_id
```

This permits complete lineage reconstruction.

---

# 108. Execution Lineage

The following must be reconstructible:

```text
root execution
   ↓
snapshot
   ↓
branch
   ↓
child execution
   ↓
child snapshot
   ↓
grandchild branch
```

---

# 109. Parent-Child Constraint

A branch execution must reference:

```text
valid parent snapshot
```

and the snapshot must belong to:

```text
parent execution
```

This should be checked by application-level validation.

---

# 110. Failure Lineage

A failure must retain:

```text
scenario
execution
trajectory
branch
invariant
evidence
```

No failure should exist as an orphaned row.

---

# 111. Family Lineage

A family must retain:

```text
clustering version
clustering method
member failures
membership scores
assignment source
```

---

# 112. Reproduction Lineage

A reproduction attempt must point to:

```text
original failure
new execution
new trajectory
new evidence
```

The original failure must remain immutable.

---

# 113. Metamorphic Lineage

A metamorphic test must point to:

```text
base execution
transformed execution
transformation
relation
comparison result
```

---

# 114. Holdout Lineage

A holdout result must record:

```text
holdout scenario
holdout execution
development family if matched
matching method
holdout experiment
```

---

# 115. Data Split Protection

The schema should include explicit split metadata.

Example:

```text
split = DEVELOPMENT
split = VALIDATION
split = HOLDOUT
```

Application logic must prevent accidental holdout leakage.

---

# 116. Security and Privacy

Even in a simulated environment, the schema should assume that logs may contain sensitive data.

Apply:

```text
data minimization
field masking
synthetic identifiers
access control
artifact encryption where required
```

---

# 117. Sensitive Field Handling

Potential sensitive fields:

```text
customer identifiers
account identifiers
transaction details
authentication tokens
tool credentials
model prompts
environment secrets
```

Use synthetic values in the research environment wherever possible.

---

# 118. Hashing Sensitive Values

Where exact values are unnecessary:

$$
H(x)=SHA256(x)
$$

can be stored instead.

However, security-relevant distinctions must not be destroyed by over-aggressive normalization.

---

# 119. Retention

Research artifacts should be retained for the duration of the project and according to the project's institutional requirements.

At minimum retain:

```text
raw traces
configurations
failure records
metrics
experiment artifacts
code version
```

---

# 120. Export Format

The database should support export to:

```text
CSV
JSON
JSONL
Parquet
SQLite
```

For large trajectory datasets, JSONL or Parquet is preferred.

---

# 121. Reproducibility Bundle

A final experiment should be exportable as:

```text
experiment_bundle/
├── config/
├── scenarios/
├── candidates/
├── traces/
├── states/
├── snapshots/
├── failures/
├── families/
├── validation/
├── metrics/
├── reports/
└── manifest.json
```

---

# 122. Manifest

The bundle manifest should contain:

```json
{
  "experiment_id": "...",
  "run_ids": [],
  "code_version": "...",
  "database_schema_version": "1.0",
  "trace_schema_version": "1.0",
  "metric_version": "1.0",
  "created_at": "...",
  "artifacts": []
}
```

---

# 123. Database Schema Versioning

Maintain:

```text
schema_version
```

separately from application version.

Migration scripts should be stored in:

```text
migrations/
```

---

# 124. Migration Rules

Never silently modify production research tables.

Each schema change should create:

```text
migration_001.sql
migration_002.sql
...
```

Historical databases should remain migratable.

---

# 125. Recommended Repository Structure

```text
src/
└── agent_eval/
    └── storage/
        ├── __init__.py
        ├── database.py
        ├── models.py
        ├── repositories/
        │   ├── experiments.py
        │   ├── scenarios.py
        │   ├── executions.py
        │   ├── traces.py
        │   ├── states.py
        │   ├── failures.py
        │   ├── families.py
        │   ├── validation.py
        │   └── metrics.py
        └── migrations/
```

---

# 126. ORM Recommendation

An ORM may be used for metadata and relational records.

Recommended options:

```text
SQLAlchemy
SQLModel
```

However, large trajectory payloads should still be handled carefully rather than blindly loading entire traces into ORM objects.

---

# 127. Pydantic Models

Use Pydantic for:

```text
scenario
candidate
event
state
invariant
invariant result
failure
family
reproduction
metamorphic test
metric
```

This creates a stable application-level schema above SQLite.

---

# 128. Repository Interface

Example:

```python
class ExecutionRepository:

    def create(self, execution):
        ...

    def get(self, execution_id):
        ...

    def finalize(self, execution_id):
        ...

    def list_by_run(self, run_id):
        ...
```

---

# 129. Failure Repository

```python
class FailureRepository:

    def create_candidate(self, candidate):
        ...

    def validate(self, failure_id):
        ...

    def get(self, failure_id):
        ...

    def list_by_run(self, run_id):
        ...

    def list_validated(self, experiment_id):
        ...
```

---

# 130. Metric Repository

```python
class MetricRepository:

    def write_run_metric(self, metric):
        ...

    def aggregate(self, experiment_id):
        ...

    def get_primary_metrics(self, experiment_id):
        ...
```

---

# 131. Data Integrity Constraints

The system must enforce:

```text
No execution without valid run.
No execution without valid candidate.
No trajectory without execution.
No event without trajectory.
No invariant evaluation without execution.
No failure candidate without failed invariant.
No validated failure without candidate.
No family membership without failure.
No reproduction without original failure.
No metamorphic test without base/transformed executions.
No run metric without run.
```

---

# 132. Required Referential Integrity

Foreign keys should be enabled:

```sql
PRAGMA foreign_keys = ON;
```

Application logic should additionally validate semantic relationships not expressible through simple foreign keys.

---

# 133. Orphan Detection

Periodic integrity checks should identify:

```text
orphan executions
orphan events
orphan states
orphan failures
orphan family memberships
orphan metrics
```

---

# 134. Database Integrity Checks

Run:

```sql
PRAGMA integrity_check;
```

before final experiment archival.

---

# 135. Research Query Examples

## Total Validated Failures

```sql
SELECT COUNT(*)
FROM validated_failures
WHERE validation_status = 'VALIDATED';
```

---

# 136. Failure Families by Method

```sql
SELECT
    r.method,
    COUNT(DISTINCT ffm.family_id) AS families
FROM experiment_runs r
JOIN validated_failures f
    ON f.run_id = r.run_id
JOIN failure_family_members ffm
    ON ffm.failure_id = f.failure_id
GROUP BY r.method;
```

---

# 137. Cost per Family

Conceptually:

```sql
SELECT
    run_id,
    SUM(cost) / NULLIF(family_count, 0)
FROM ...
```

The implementation should use a controlled metric view rather than ad-hoc dashboard calculations.

---

# 138. Discovery Curve Query

For each run, calculate cumulative family count by execution/budget position.

Required data:

```text
run_id
execution order
cumulative cost
family discovery event
```

---

# 139. Reproduction Rate Query

```sql
SELECT
    COUNT(*) FILTER (
        WHERE outcome = 'REPRODUCED'
    ) * 1.0
    /
    NULLIF(
        COUNT(*) FILTER (
            WHERE outcome NOT IN (
                'INVALID',
                'ERROR'
            )
        ),
        0
    )
FROM reproduction_attempts;
```

---

# 140. Metamorphic Consistency Query

```sql
SELECT
    SUM(
        CASE WHEN result = 'PASS'
             THEN 1 ELSE 0 END
    ) * 1.0
    /
    NULLIF(
        SUM(
            CASE WHEN result NOT IN (
                'INVALID',
                'ERROR'
            )
            THEN 1 ELSE 0 END
        ),
        0
    )
FROM metamorphic_tests;
```

---

# 141. Holdout Generalization Query

The exact query depends on the frozen matching definition.

The database must preserve enough fields to distinguish:

```text
development family
holdout mechanism
matching evidence
matching method
```

---

# 142. Database Views

Recommended views:

```text
v_validated_failures
v_failure_families
v_execution_costs
v_run_metrics
v_discovery_curve
v_reproduction_summary
v_metamorphic_summary
v_holdout_summary
v_evaluator_reliability
```

---

# 143. Validated Failure View

Conceptually:

```sql
CREATE VIEW v_validated_failures AS
SELECT *
FROM validated_failures
WHERE validation_status = 'VALIDATED';
```

---

# 144. Execution Cost View

Aggregate all cost records by execution:

```sql
CREATE VIEW v_execution_costs AS
SELECT
    execution_id,
    SUM(
        COALESCE(monetary_cost, 0)
    ) AS monetary_cost,
    SUM(quantity) AS total_quantity
FROM cost_records
GROUP BY execution_id;
```

The actual implementation should preserve units rather than blindly summing incompatible quantities.

---

# 145. Data Quality Checks

Before final analysis:

```text
[ ] No orphaned records
[ ] No duplicate IDs
[ ] No invalid foreign keys
[ ] No impossible metric ranges
[ ] No negative costs
[ ] No duplicate event sequence numbers
[ ] No missing experiment seeds
[ ] No missing method labels
[ ] No unversioned invariants
[ ] No unversioned clustering
[ ] No holdout leakage
```

---

# 146. Metric Range Checks

For rate metrics:

$$
0 \le metric \le 1
$$

For counts:

$$
metric \ge 0
$$

For costs:

$$
cost \ge 0
$$

---

# 147. Family Consistency Checks

Expected:

$$
N_{families}
\le
N_{fingerprints}
\le
N_{validated\ failures}
$$

Violations should trigger a data-integrity error.

---

# 148. Discovery Monotonicity

For cumulative family discovery:

$$
F(t+1)\ge F(t)
$$

If not, the metric-generation pipeline is invalid.

---

# 149. Cost Consistency

Every execution should satisfy:

$$
C_{execution}
=
\sum C_{recorded\ components}
$$

within the explicitly defined accounting tolerance.

---

# 150. Budget Consistency

For each run:

$$
C_{actual}
\le
C_{allocated}
+
AllowedOvershoot
$$

If the budget is exceeded, the run must record:

```text
budget_overshoot
```

rather than silently changing the denominator.

---

# 151. Selection Consistency

Every selected candidate should have:

```text
selection_decision
execution
cost record
```

A selected candidate without an execution record requires an explicit reason such as:

```text
budget rejection
execution error
controller failure
```

---

# 152. Failure Consistency

Every validated failure must have:

```text
failed invariant evaluation
valid evidence
scenario
execution
trajectory
validation result
```

---

# 153. Reproduction Consistency

Every `REPRODUCED` result must reference:

```text
original failure
independent execution
new evidence
```

---

# 154. Metamorphic Consistency

Every valid metamorphic test must reference:

```text
base execution
transformed execution
transformation
relation
result
```

---

# 155. Holdout Integrity

A holdout result must not reference:

```text
future development selection state
post-hoc selector updates
holdout-informed clustering parameters
```

The experiment manifest should record when holdout access occurred.

---

# 156. Data Security Boundary

The database contains:

```text
agent outputs
tool interactions
environment state
failure evidence
potentially sensitive synthetic data
```

Therefore:

```text
database access
artifact access
dashboard access
experiment-control access
```

should be separate permissions where practical.

---

# 157. Recommended Initial SQLite Database

The first prototype does not need every table described above.

Minimum implementation:

```text
experiments
experiment_runs
agents
agent_configs
environment_configs
scenario_pools
scenarios
scenario_versions
candidates
executions
trajectories
trajectory_events
states
snapshots
branches
invariants
scenario_invariants
invariant_evaluations
evaluation_evidence
failure_candidates
validated_failures
failure_signatures
failure_families
failure_family_members
reproduction_attempts
metamorphic_tests
holdout_runs
selection_decisions
cost_records
metric_definitions
run_metrics
aggregate_metrics
artifacts
system_errors
```

---

# 158. Minimum Viable Database

For the first working prototype, the minimum critical tables are:

```text
experiments
experiment_runs
scenario_versions
candidates
executions
trajectories
trajectory_events
states
invariants
invariant_evaluations
validated_failures
failure_signatures
failure_families
selection_decisions
cost_records
run_metrics
```

Add reproduction, metamorphic, and holdout tables before the final research experiment.

---

# 159. Recommended Data Flow

```text
Candidate
    ↓
Execution
    ↓
Trajectory
    ├── Events
    └── States
          ↓
       Snapshot
          ↓
       Branch
          ↓
   Invariant Evaluation
          ↓
   Failure Candidate
          ↓
   Validated Failure
          ↓
   Failure Signature
          ↓
    Failure Family
          ↓
 ┌────────┼──────────┐
 ↓        ↓          ↓
Replay  Metamorphic Holdout
 ↓        ↓          ↓
 └────────┴──────────┘
          ↓
       Metrics
```

---

# 160. Recommended Implementation Order

Implement storage in this order:

## Phase 1: Core Experiment

```text
experiments
experiment_runs
agents
agent_configs
environment_configs
```

## Phase 2: Scenarios

```text
scenario_pools
scenarios
scenario_versions
candidates
```

## Phase 3: Execution

```text
executions
trajectories
trajectory_events
states
```

## Phase 4: State Branching

```text
snapshots
branches
```

## Phase 5: Evaluation

```text
invariants
scenario_invariants
invariant_evaluations
evaluation_evidence
```

## Phase 6: Failures

```text
failure_candidates
validated_failures
failure_signatures
failure_families
failure_family_members
```

## Phase 7: Validation

```text
reproduction_attempts
metamorphic_transformations
metamorphic_tests
holdout_runs
```

## Phase 8: Measurement

```text
selection_decisions
cost_records
metric_definitions
run_metrics
aggregate_metrics
```

---

# 161. Definition of Done

The database subsystem is complete when:

* [ ] Every experiment has a unique ID.
* [ ] Every run has a unique seed.
* [ ] Agent configuration is versioned.
* [ ] Environment configuration is versioned.
* [ ] Scenario pools are versioned and frozen.
* [ ] Candidates reference scenario versions.
* [ ] Executions reference candidates and runs.
* [ ] Trajectories reference executions.
* [ ] Events preserve chronological order.
* [ ] States are versioned through execution lineage.
* [ ] Snapshots preserve state hashes.
* [ ] Branches preserve parent lineage.
* [ ] Invariants are versioned.
* [ ] Scenario-invariant mappings are stored.
* [ ] Invariant evaluations retain evidence.
* [ ] Failure candidates reference failed evaluations.
* [ ] Validated failures retain provenance.
* [ ] Failure signatures are canonicalized.
* [ ] Failure families preserve clustering version.
* [ ] Reproduction attempts reference original failures.
* [ ] Metamorphic tests reference base and transformed executions.
* [ ] Holdout records are isolated.
* [ ] Selection decisions are logged.
* [ ] Costs are recorded by category.
* [ ] Metrics are stored per run.
* [ ] Aggregate metrics retain statistical metadata.
* [ ] Large artifacts are content-hashed.
* [ ] Database migrations are versioned.
* [ ] Foreign-key integrity is enforced.
* [ ] Data-quality checks are automated.
* [ ] Experiment bundles can be exported.
* [ ] Raw evidence remains recoverable.
* [ ] Derived results are recomputable.

---

# 162. Final Data Architecture

The complete storage model is:

$$
\boxed{
Configuration
\rightarrow
Scenario
\rightarrow
Candidate
\rightarrow
Execution
\rightarrow
Trajectory
\rightarrow
State/Event
\rightarrow
Invariant
\rightarrow
Failure
\rightarrow
Family
\rightarrow
Validation
\rightarrow
Metrics
}
$$

The most important architectural rule is:

$$
\boxed{
Raw\ Evidence
\neq
Derived\ Interpretation
}
$$

Raw observations such as:

```text
tool request
tool response
policy decision
state transition
fault
agent output
```

must remain available independently of:

```text
failure classification
failure family
reproduction status
generalization
metric
```

This allows the research results to be recomputed when an invariant, clustering algorithm, or metric definition changes.

The database therefore acts as the project's **reproducible evidence layer**, not merely as storage for whatever numbers happened to make it onto the dashboard.
