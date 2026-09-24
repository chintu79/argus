# Trajectory / Trace Schema

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** TTS-01
**Document Type:** Trajectory / Trace Schema Specification
**Version:** 1.0
**Status:** Draft for Implementation

**Related Documents:**

* Project Specification
* Research Questions & Success Criteria
* System Architecture
* Agent / Environment Specification
* Test Scenario & Attack Specification
* Adaptive Test Selection Specification
* State Snapshot & Branching Specification
* Invariant & Failure Detection Specification
* Failure Classification & Clustering Specification
* Reproducibility & Metamorphic Testing Specification
* Hidden Holdout & Generalization Specification
* Evaluation Metrics Specification

---

# 1. Purpose

This document defines the canonical representation of an AI-agent execution trajectory and its underlying event trace.

The trace is the primary experimental record used to reconstruct:

* what the agent was asked to do,
* what the agent attempted,
* which tools it requested,
* which tool calls were allowed or denied,
* what the environment returned,
* how the environment changed,
* which states were reached,
* where security-relevant states occurred,
* which snapshots were created,
* which branches originated from those states,
* which invariants were evaluated,
* which failures were detected,
* how much evaluation budget was consumed.

The trace must contain **observed execution evidence**, not inferred or fabricated descriptions of what the model may have internally reasoned.

---

# 2. Core Principle

The canonical execution representation is:

$$
\tau =
\{e_0,e_1,e_2,\ldots,e_n\}
$$

where each `e_i` is an immutable execution event.

A trajectory is therefore an ordered event sequence:

```text
Experiment
   ↓
Scenario
   ↓
Execution
   ↓
Event 0
   ↓
Event 1
   ↓
Event 2
   ↓
...
   ↓
Event n
```

State representations are derived from relevant events and state checkpoints.

---

# 3. Why the Trace Is Central

The same trace must support multiple downstream systems.

```text
                    TRAJECTORY / TRACE
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   State Analysis      Failure Engine     Cost Engine
        │                  │                  │
        ▼                  ▼                  ▼
    Snapshots          Failures/Families    Metrics
        │
        ▼
     Branching
```

The trace therefore acts as the **source of execution evidence** for the evaluation platform.

---

# 4. Design Goals

The trace schema shall provide:

1. deterministic event ordering,
2. complete execution provenance,
3. explicit agent actions,
4. explicit tool interactions,
5. explicit policy decisions,
6. explicit environment transitions,
7. state references and hashes,
8. perturbation records,
9. snapshot references,
10. branch lineage,
11. invariant evaluation references,
12. failure evidence,
13. cost measurements,
14. reproducibility metadata,
15. experiment configuration references,
16. privacy-aware data handling,
17. versioning,
18. efficient querying,
19. machine-readable storage,
20. human-readable debugging.

---

# 5. Trace Design Boundary

The trace records **observable and instrumented execution behavior**.

It must not claim to contain:

* private chain-of-thought,
* hidden model activations,
* undisclosed internal reasoning,
* proprietary model internals,
* unavailable model state.

Instead, the trace may contain:

```text
agent output
tool request
tool response
policy decision
environment state change
execution decision
termination decision
```

---

# 6. Terminology

| Term             | Definition                                               |
| ---------------- | -------------------------------------------------------- |
| Experiment       | A controlled evaluation study                            |
| Scenario         | A defined evaluation case                                |
| Execution        | One run of an agent against one scenario                 |
| Trajectory       | Ordered representation of one execution                  |
| Trace            | Event-level record underlying a trajectory               |
| Event            | Atomic recorded execution occurrence                     |
| State            | Relevant observable execution/environment configuration  |
| State Checkpoint | Recorded representation or hash of state at an event     |
| Action           | Observable operation initiated by the agent or evaluator |
| Observation      | Information returned to the agent or evaluator           |
| Tool Call        | Agent request to invoke a tool                           |
| Tool Result      | Result returned by the tool                              |
| Policy Decision  | Allow/deny/review/error decision                         |
| Perturbation     | Controlled change introduced by the evaluator            |
| Snapshot         | Persisted branchable state                               |
| Branch           | Execution continuation from a snapshot                   |
| Invariant Result | Evaluation of a required property                        |
| Failure Evidence | Observable evidence supporting a detected failure        |

---

# 7. Hierarchical Data Model

The system shall organize data as:

```text
Experiment
 ├── Scenario
 │    ├── Execution
 │    │    ├── Trajectory
 │    │    │    ├── Event
 │    │    │    ├── Event
 │    │    │    └── ...
 │    │    ├── Snapshot
 │    │    └── Branch
 │    └── ...
 └── ...
```

---

# 8. Identity Model

Every major object requires a stable identifier.

Required identifiers:

```text
experiment_id
scenario_id
execution_id
trajectory_id
event_id
snapshot_id
branch_id
perturbation_id
invariant_id
failure_id
```

Identifiers must be unique within the experiment system.

---

# 9. Execution Identity

An execution represents one concrete run.

Example:

```yaml
execution_id: EXEC-00124
scenario_id: S14
experiment_id: EXP-003
execution_index: 17
```

The same scenario may therefore have multiple executions.

---

# 10. Scenario Identity vs Execution Identity

These must remain separate.

```text
Scenario S14
   ├── Execution E01
   ├── Execution E02
   ├── Execution E03
   └── Execution E04
```

A scenario describes what is being tested.

An execution describes what happened in one run.

---

# 11. Trajectory Identity

Each execution has one primary trajectory.

```yaml
trajectory_id: TRAJ-00124
execution_id: EXEC-00124
```

If execution is branched, each branch execution shall have its own trajectory.

---

# 12. Event Identity

Each event requires:

```yaml
event_id:
execution_id:
trajectory_id:
sequence_number:
event_type:
timestamp:
```

`sequence_number` is the canonical ordering mechanism within a trajectory.

---

# 13. Event Ordering

Events must be ordered by a monotonically increasing sequence number.

Example:

```text
0  TASK_STARTED
1  AGENT_STEP_STARTED
2  AGENT_OUTPUT
3  TOOL_REQUEST
4  POLICY_DECISION
5  TOOL_RESPONSE
6  STATE_TRANSITION
7  AGENT_STEP_COMPLETED
8  TASK_COMPLETED
```

Timestamps are useful but must not be the sole ordering mechanism.

---

# 14. Event Timestamp

Each event should record:

```text
timestamp
monotonic_time
```

where available.

Wall-clock timestamps support human debugging.

Monotonic time supports latency measurement without clock-adjustment problems.

---

# 15. Event Types

The initial event taxonomy shall include:

```text
EXPERIMENT_STARTED
EXPERIMENT_ENDED

SCENARIO_STARTED
SCENARIO_ENDED

EXECUTION_STARTED
EXECUTION_ENDED

TASK_STARTED
TASK_COMPLETED

AGENT_STEP_STARTED
AGENT_OUTPUT
AGENT_ACTION
AGENT_STEP_COMPLETED

TOOL_REQUEST
TOOL_ARGUMENTS
POLICY_DECISION
TOOL_EXECUTION_STARTED
TOOL_RESPONSE
TOOL_EXECUTION_COMPLETED

STATE_OBSERVED
STATE_TRANSITION
STATE_CHECKPOINT

PERTURBATION_REQUESTED
PERTURBATION_APPLIED

SNAPSHOT_REQUESTED
SNAPSHOT_CREATED
SNAPSHOT_VALIDATED
SNAPSHOT_RESTORED

BRANCH_CREATED
BRANCH_STARTED
BRANCH_ENDED

INVARIANT_EVALUATED
FAILURE_DETECTED

BUDGET_RESERVED
COST_RECORDED

ERROR
WARNING

EXECUTION_TERMINATED
```

Not every execution will contain every event type.

---

# 16. Event Categories

For easier querying, event types should also belong to categories.

```text
LIFECYCLE
AGENT
TOOL
POLICY
STATE
PERTURBATION
SNAPSHOT
BRANCH
EVALUATION
FAILURE
COST
ERROR
```

---

# 17. Base Event Schema

Canonical event structure:

```yaml
event:
  event_id:
  experiment_id:
  scenario_id:
  execution_id:
  trajectory_id:

  sequence_number:
  event_type:
  event_category:

  timestamp:
  monotonic_time:

  actor:
  source:

  state_before:
  state_after:

  payload:

  cost:
  metadata:
```

---

# 18. Event Actor

The `actor` field identifies who caused or generated the event.

Allowed values:

```text
AGENT
USER_SIMULATOR
TOOL
POLICY_ENGINE
ENVIRONMENT
EVALUATOR
SNAPSHOT_MANAGER
BRANCH_MANAGER
INVARIANT_ENGINE
SYSTEM
```

---

# 19. Event Source

The `source` identifies the component that emitted the event.

Example:

```yaml
source:
  component: tool_gateway
  version: "0.1.0"
```

This helps diagnose evaluator-side failures.

---

# 20. State References

Events should reference relevant state without unnecessarily duplicating the entire state.

Example:

```yaml
state_before:
  state_id: STATE-101
  state_hash: "..."

state_after:
  state_id: STATE-102
  state_hash: "..."
```

Full state should only be embedded when required.

---

# 21. State Checkpoint

A checkpoint represents a logically meaningful state.

Example:

```yaml
state_checkpoint:
  state_id: STATE-102
  state_hash: "sha256..."
  step_index: 5
```

The state itself is maintained by the State Manager.

---

# 22. Event Payload

The payload contains event-specific data.

Example for a tool request:

```yaml
payload:
  tool_name: transaction_lookup
  request_id: TOOLREQ-0042
  arguments:
    account_id: ACC-001
```

Sensitive fields must be redacted or represented using controlled references.

---

# 23. Trace-Level Metadata

A trajectory shall contain metadata describing the execution environment.

```yaml
metadata:
  agent_version:
  model_provider:
  model_name:
  model_version:
  environment_version:
  policy_version:
  tool_registry_version:
  scenario_version:
  trace_schema_version:
```

---

# 24. Agent Configuration Metadata

The trace should record the configuration necessary to identify the evaluated agent.

Example:

```yaml
agent:
  agent_id:
  adapter_version:
  model:
    provider:
    name:
    version:
  generation:
    temperature:
    max_tokens:
  system_instruction_hash:
```

Actual system instructions need not be duplicated in every event.

---

# 25. Configuration References

Large or sensitive configuration should be referenced by ID or hash.

Example:

```yaml
configuration:
  agent_config_id: AGCFG-003
  environment_config_id: ENVCFG-002
  policy_config_id: POLCFG-001
```

This avoids excessive trace duplication.

---

# 26. Task Start Event

Example:

```yaml
event_type: TASK_STARTED

payload:
  task_id: TASK-014
  task_type: support_ticket
  input_hash: "..."
  task_metadata:
    difficulty: 3
```

Sensitive task content should follow the project's data-handling policy.

---

# 27. Agent Step Event

An agent step represents one observable decision/execution cycle.

Example:

```yaml
event_type: AGENT_STEP_STARTED

payload:
  step_index: 4
  context_reference: CTX-004
```

---

# 28. Agent Output Event

The trace may record the model's externally visible output.

```yaml
event_type: AGENT_OUTPUT

payload:
  output_id: OUT-004
  content_reference: CONTENT-004
  output_type: text
```

Where possible, large outputs should be stored separately and referenced.

---

# 29. Agent Action Event

If the agent produces a structured action:

```yaml
event_type: AGENT_ACTION

payload:
  action_type: TOOL_CALL
  target: transaction_lookup
  action_id: ACT-004
```

---

# 30. Tool Request Event

A tool request records what the agent attempted to invoke.

```yaml
event_type: TOOL_REQUEST

payload:
  request_id: TOOLREQ-004
  tool_name: transaction_lookup
  arguments:
    account_id: ACC-001
```

---

# 31. Tool Argument Handling

Arguments must be traceable but sensitive values should be protected.

Possible representation:

```yaml
arguments:
  account_id:
    value_reference: SECRET-001
    hash: "..."
```

or, for safe simulated values:

```yaml
arguments:
  account_id: ACC-001
```

---

# 32. Policy Decision Event

Every policy-controlled tool invocation should produce a policy event.

```yaml
event_type: POLICY_DECISION

payload:
  request_id: TOOLREQ-004
  decision: ALLOW
  policy_rule_id: POL-007
  reason_code: AUTHORIZED_RESOURCE
```

The reason should represent the observable policy decision, not hidden model reasoning.

---

# 33. Policy Decision Values

Allowed initial values:

```text
ALLOW
DENY
REVIEW
ERROR
```

---

# 34. Tool Execution Event

```yaml
event_type: TOOL_EXECUTION_STARTED

payload:
  request_id: TOOLREQ-004
  tool_name: transaction_lookup
```

---

# 35. Tool Response Event

```yaml
event_type: TOOL_RESPONSE

payload:
  request_id: TOOLREQ-004
  response_id: RESP-004
  status: SUCCESS
  content_reference: CONTENT-005
```

---

# 36. Tool Response Status

Recommended values:

```text
SUCCESS
DENIED
TIMEOUT
MALFORMED
ERROR
UNAVAILABLE
PARTIAL
```

---

# 37. Environment State Transition

Every meaningful environment mutation should generate a state transition event.

```yaml
event_type: STATE_TRANSITION

payload:
  transition_id: TRANS-004
  component: database
  operation: UPDATE
  affected_resource_type: ticket
  affected_resource_id: TICKET-014
```

---

# 38. State Transition Evidence

Where safe and appropriate:

```yaml
payload:
  before_hash:
  after_hash:
  changed_fields:
```

Sensitive values should not be logged unnecessarily.

---

# 39. State Observation Event

An observation event records relevant state without necessarily changing it.

```yaml
event_type: STATE_OBSERVED

payload:
  state_id: STATE-004
  state_hash: "..."
  observed_components:
    - authorization
    - task
    - tool_state
```

---

# 40. State Checkpoint Event

When a state is considered important enough to preserve:

```yaml
event_type: STATE_CHECKPOINT

payload:
  state_id: STATE-004
  state_hash: "..."
  checkpoint_reason:
    - authorization_change
    - sensitive_resource_access
```

This event can trigger the Snapshot Manager.

---

# 41. Interesting-State Metadata

When the Interesting-State Detector identifies a relevant state:

```yaml
payload:
  interesting: true
  rules_triggered:
    - IS-001
    - IS-004
  interestingness_score: 0.82
  snapshot_eligible: true
```

If a score is not implemented, it must not be fabricated.

---

# 42. Perturbation Request

```yaml
event_type: PERTURBATION_REQUESTED

payload:
  perturbation_id: P-042
  type: TOOL_RESPONSE
  target: transaction_lookup
  source: evaluator
```

---

# 43. Perturbation Applied

```yaml
event_type: PERTURBATION_APPLIED

payload:
  perturbation_id: P-042
  type: TOOL_RESPONSE
  target: transaction_lookup
  modification:
    mode: malformed_response
  original_state_hash: "..."
  resulting_state_hash: "..."
```

---

# 44. Snapshot Requested

```yaml
event_type: SNAPSHOT_REQUESTED

payload:
  snapshot_reason:
    - interesting_state
  state_id: STATE-004
```

---

# 45. Snapshot Created

```yaml
event_type: SNAPSHOT_CREATED

payload:
  snapshot_id: SNAP-004
  state_id: STATE-004
  state_hash: "..."
  size_bytes: 18342
```

---

# 46. Snapshot Validation

```yaml
event_type: SNAPSHOT_VALIDATED

payload:
  snapshot_id: SNAP-004
  status: VALID
  validation_checks:
    integrity: PASS
    schema: PASS
    compatibility: PASS
```

---

# 47. Snapshot Restore

```yaml
event_type: SNAPSHOT_RESTORED

payload:
  snapshot_id: SNAP-004
  branch_id: BR-004
  restored_state_hash: "..."
  expected_state_hash: "..."
  status: SUCCESS
```

---

# 48. Branch Creation

```yaml
event_type: BRANCH_CREATED

payload:
  branch_id: BR-004
  parent_snapshot_id: SNAP-004
  perturbation_id: P-042
  branch_depth: 1
```

---

# 49. Branch Start

```yaml
event_type: BRANCH_STARTED

payload:
  branch_id: BR-004
  parent_snapshot_id: SNAP-004
  execution_mode: BRANCH
```

---

# 50. Branch End

```yaml
event_type: BRANCH_ENDED

payload:
  branch_id: BR-004
  outcome: FAIL
  termination_reason: INVARIANT_VIOLATION
```

---

# 51. Invariant Evaluation Event

```yaml
event_type: INVARIANT_EVALUATED

payload:
  invariant_id: I-004
  result: FAIL
  evaluator_version: "0.1.0"
  evidence_reference: EVID-004
```

---

# 52. Invariant Result Values

Initial values:

```text
PASS
FAIL
INCONCLUSIVE
NOT_APPLICABLE
ERROR
```

---

# 53. Failure Detection Event

```yaml
event_type: FAILURE_DETECTED

payload:
  failure_id: FAIL-004
  failure_type: SECURITY
  invariant_id: I-004
  evidence_reference: EVID-004
  severity: HIGH
```

Severity must be determined according to the project's defined severity rules and must not be arbitrarily assigned.

---

# 54. Failure Evidence

Evidence should reference actual trace observations.

Example:

```yaml
evidence:
  evidence_id: EVID-004

  event_ids:
    - EVT-021
    - EVT-022
    - EVT-025

  state_ids:
    - STATE-004
    - STATE-005

  expected_property:
    invariant_id: I-004

  observed_property:
    description: unauthorized resource was returned

  evidence_hash: "..."
```

---

# 55. Cost Event

Every measurable resource-consuming operation should be traceable.

```yaml
event_type: COST_RECORDED

payload:
  cost_type: MODEL_CALL
  quantity: 1
  unit: call
  component: agent
```

---

# 56. Cost Types

Initial cost categories:

```text
MODEL_CALL
INPUT_TOKENS
OUTPUT_TOKENS
TOOL_CALL
EXECUTION_TIME
WALL_CLOCK_TIME
SNAPSHOT
RESTORE
BRANCH
ANALYSIS
VERIFICATION
```

---

# 57. Budget Reservation

Adaptive selection may reserve budget before execution.

```yaml
event_type: BUDGET_RESERVED

payload:
  reservation_id: RES-004
  estimated_cost:
  budget_type:
  amount:
```

The reservation should be linked to the execution or branch.

---

# 58. Error Event

Errors must be recorded as structured events.

```yaml
event_type: ERROR

payload:
  error_code:
  component:
  severity:
  message_reference:
  recoverable:
```

Sensitive stack traces should be stored separately when necessary.

---

# 59. Warning Event

Warnings should not be silently converted into failures.

```yaml
event_type: WARNING

payload:
  warning_code:
  component:
  description:
```

---

# 60. Execution Termination

Every execution should end with an explicit termination event.

```yaml
event_type: EXECUTION_TERMINATED

payload:
  termination_reason:
  final_status:
  final_state_id:
  final_state_hash:
```

---

# 61. Termination Reasons

Initial values:

```text
TASK_COMPLETED
AGENT_TERMINATED
MAX_STEPS
TIMEOUT
BUDGET_EXHAUSTED
FAILURE_TERMINAL
ENVIRONMENT_ERROR
EVALUATOR_ERROR
CANCELLED
```

---

# 62. Execution Status

Allowed values:

```text
RUNNING
COMPLETED
FAILED
INCONCLUSIVE
INVALID
ERROR
CANCELLED
```

A security failure does not necessarily mean the execution infrastructure itself failed.

---

# 63. Complete Execution Record

A complete execution record should look conceptually like:

```yaml
execution:
  execution_id: EXEC-001

  experiment_id: EXP-001
  scenario_id: S14
  trajectory_id: TRAJ-001

  status: COMPLETED

  configuration:
    agent_config_id: AGCFG-001
    environment_config_id: ENVCFG-001
    policy_config_id: POLCFG-001

  randomization:
    seed: 4821

  start:
    timestamp:
    monotonic_time:

  end:
    timestamp:
    monotonic_time:

  event_count: 31

  final_state:
    state_id:
    state_hash:

  cost:
    total:
    model_calls:
    tool_calls:
    execution_time:

  termination:
    reason: TASK_COMPLETED
```

---

# 64. Complete Trajectory Record

```yaml
trajectory:
  trajectory_id: TRAJ-001
  execution_id: EXEC-001

  schema_version: "1.0"

  events:
    - event_001
    - event_002
    - event_003

  state_checkpoints:
    - STATE-001
    - STATE-002

  snapshots:
    - SNAP-001

  branches:
    - BR-001

  invariant_results:
    - INVRES-001

  failures:
    - FAIL-001
```

---

# 65. Canonical JSONL Representation

The recommended initial storage format is JSON Lines.

Each line represents one immutable event.

Example:

```json
{"event_id":"EVT-001","execution_id":"EXEC-001","trajectory_id":"TRAJ-001","sequence_number":0,"event_type":"EXECUTION_STARTED","event_category":"LIFECYCLE"}
{"event_id":"EVT-002","execution_id":"EXEC-001","trajectory_id":"TRAJ-001","sequence_number":1,"event_type":"TASK_STARTED","event_category":"LIFECYCLE"}
{"event_id":"EVT-003","execution_id":"EXEC-001","trajectory_id":"TRAJ-001","sequence_number":2,"event_type":"AGENT_OUTPUT","event_category":"AGENT"}
```

The production storage layer may additionally index these records in SQLite.

---

# 66. Why JSONL

JSONL is recommended initially because it provides:

* append-only logging,
* simple debugging,
* easy replay,
* streaming,
* compatibility with Python,
* straightforward experiment archival,
* simple conversion to pandas,
* easy integration with SQLite.

---

# 67. SQLite Index

SQLite may maintain queryable metadata:

```text
experiments
scenarios
executions
trajectories
events
states
snapshots
branches
perturbations
invariant_results
failures
cost_records
```

Large event payloads may remain in JSONL or object storage.

---

# 68. Event Immutability

After an event is committed, it should not be modified.

Corrections should be represented by new events or metadata.

Example:

```text
Original Event
      ↓
Correction Event
```

This preserves experimental provenance.

---

# 69. Event Hashing

For high-integrity experiments, events may have hashes:

$$
H_i = Hash(
H_{i-1}
\Vert
CanonicalEvent_i
)
$$

This creates a hash chain.

It can detect accidental modification or deletion.

---

# 70. Trace Integrity

Optional trace-level integrity structure:

```yaml
trace_integrity:
  first_event_hash:
  final_event_hash:
  event_count:
  hash_algorithm:
```

The initial prototype may implement event hashing after basic logging works.

---

# 71. State-to-Event Relationship

State changes must be reconstructable from events.

Conceptually:

$$
S_{t+1}
=
Transition(S_t,e_t)
$$

The evaluator should be able to determine which event caused a relevant state transition.

---

# 72. State Reconstruction

A replay engine may reconstruct state:

```text
Initial State
     ↓
Event 1
     ↓
State 1
     ↓
Event 2
     ↓
State 2
     ↓
...
```

This should be tested against recorded checkpoints.

---

# 73. State Checkpoint Validation

For checkpoints:

```text
Reconstructed State Hash
          =
Recorded State Hash
```

If not:

```text
TRACE_RECONSTRUCTION_MISMATCH
```

This is an evaluator integrity problem and must not automatically become an agent failure.

---

# 74. Tool Call Correlation

Tool-related events must share a request identifier.

```text
TOOL_REQUEST
     │
     ├── request_id = R1
     │
     ▼
POLICY_DECISION
     │
     ├── request_id = R1
     │
     ▼
TOOL_EXECUTION
     │
     ├── request_id = R1
     │
     ▼
TOOL_RESPONSE
     │
     └── request_id = R1
```

This allows complete tool-call reconstruction.

---

# 75. Agent Step Correlation

Agent events should include:

```text
step_index
```

Example:

```text
Step 4
 ├── AGENT_STEP_STARTED
 ├── AGENT_OUTPUT
 ├── TOOL_REQUEST
 ├── POLICY_DECISION
 ├── TOOL_RESPONSE
 └── AGENT_STEP_COMPLETED
```

---

# 76. Branch Correlation

All branch events must include:

```yaml
branch_id:
parent_snapshot_id:
```

where applicable.

This makes branch-specific trace extraction possible.

---

# 77. Perturbation Correlation

All perturbation-related events must include:

```yaml
perturbation_id:
```

This allows the evaluator to reconstruct exactly what was changed.

---

# 78. Failure Correlation

A failure must reference:

```text
failure_id
invariant_id
event_ids
state_ids
execution_id
trajectory_id
branch_id
```

where applicable.

---

# 79. Trace-to-Failure Evidence Chain

The evidence chain should be:

```text
Scenario
   ↓
Execution
   ↓
Trajectory
   ↓
Event(s)
   ↓
State(s)
   ↓
Invariant Evaluation
   ↓
Failure
   ↓
Failure Family
```

This is the required evidence hierarchy.

---

# 80. No Direct Failure Without Evidence

A failure record must not exist solely because a classifier predicted one.

A valid failure requires observable evidence.

Therefore:

```text
Classifier Prediction
       ≠
Validated Failure
```

The classifier can assist analysis, but evidence must originate from the trace and invariant engine.

---

# 81. Failure Family Link

After failure clustering:

```yaml
failure:
  failure_id: FAIL-004
  family_id: FAMILY-007
```

The trace itself should retain the individual evidence.

---

# 82. Reproducibility Metadata

Every execution must record enough metadata for replay.

Minimum:

```yaml
reproducibility:
  random_seed:
  scenario_version:
  agent_config_id:
  environment_config_id:
  policy_config_id:
  tool_registry_version:
  invariant_version:
  trace_schema_version:
```

---

# 83. Randomness

Randomness should be separated where possible:

```text
scenario_seed
agent_seed
environment_seed
perturbation_seed
execution_seed
```

If the underlying model does not expose deterministic generation, this limitation must be recorded.

---

# 84. Model Reproducibility

The trace should record:

```yaml
model:
  provider:
  model_name:
  model_version:
  generation_parameters:
```

If a provider does not expose a stable model version, the trace should explicitly record that limitation.

---

# 85. Tool Reproducibility

Tool behavior should be reproducible through controlled mocks where possible.

Record:

```yaml
tool:
  tool_name:
  tool_version:
  mock_version:
  response_fixture_id:
```

---

# 86. Environment Reproducibility

Record:

```yaml
environment:
  environment_version:
  state_schema_version:
  initial_state_hash:
  final_state_hash:
```

---

# 87. Trace Sampling

The research system should not silently sample away security-relevant events.

If sampling is used for performance:

```text
sampling_policy
sampling_rate
sampled_event_types
```

must be recorded.

For initial experiments, full event logging is recommended.

---

# 88. Trace Granularity

The system should distinguish:

### Execution-level

One execution.

### Step-level

One agent decision cycle.

### Event-level

One atomic observable event.

### State-level

One relevant state representation.

This prevents the trace from becoming either an unreadable firehose or a useless summary.

---

# 89. Trace Payload Size

Large content should not be duplicated across every event.

Use:

```text
content_reference
content_hash
content_store
```

where appropriate.

Example:

```yaml
content:
  reference: CONTENT-1004
  hash: "..."
  size_bytes: 18291
```

---

# 90. Sensitive Data

The trace may contain:

* user-like identifiers,
* simulated customer data,
* account information,
* transaction information,
* authorization information.

The initial environment should use synthetic data.

Sensitive real-world information must not be introduced merely because the schema technically permits it.

---

# 91. Redaction

The trace layer should support:

```text
PLAINTEXT
HASHED
REDACTED
REFERENCE
```

for sensitive values.

The chosen representation must be deterministic where replay requires it.

---

# 92. Trace Access Control

The trace should be accessible only to authorized experiment components and researchers.

The evaluated agent must not have unrestricted access to:

```text
raw traces
future events
failure labels
hidden holdout traces
adaptive selection statistics
```

---

# 93. Information Boundary

The trace must not leak future evaluation information into the agent or selector.

For example:

```text
Future Failure Label
       ✕
Agent Context
```

and:

```text
Hidden Holdout Outcome
       ✕
Adaptive Selector
```

until the appropriate evaluation phase.

---

# 94. Adaptive Selector Trace Access

The adaptive selector may consume permitted historical information such as:

```text
past reward
candidate statistics
validated failure history
cost history
state coverage
branch yield
```

It must not access future outcomes.

---

# 95. Trace Versioning

The schema shall use semantic versioning or an equivalent explicit version system.

Example:

```text
trace_schema_version = 1.0
```

Breaking changes require a major version increment.

---

# 96. Backward Compatibility

Readers should explicitly declare which trace versions they support.

Unsupported versions should produce a clear compatibility error.

The system should not silently interpret an incompatible trace.

---

# 97. Event Validation

Every event should pass schema validation before persistence.

Validation checks include:

```text
required fields
valid event type
valid actor
valid identifiers
valid sequence number
valid payload schema
valid references
```

---

# 98. Trace Validation

At trajectory completion:

```text
event_count
sequence continuity
execution identity
trajectory identity
tool correlation
branch correlation
state references
termination event
```

must be validated.

---

# 99. Sequence Validation

For events:

```text
0
1
2
3
...
n
```

the system must detect:

```text
duplicate sequence numbers
missing sequence numbers
out-of-order events
```

unless explicit asynchronous semantics are supported.

---

# 100. Asynchronous Events

If parallel tool calls or asynchronous events are introduced, the schema should retain:

```yaml
sequence_number:
parent_event_id:
logical_timestamp:
```

A partial-order representation may be needed.

The initial implementation should prefer sequential execution for easier reproducibility.

---

# 101. Trace Completion Criteria

A trajectory is complete when:

1. execution has a terminal status,
2. a termination event exists,
3. final state is recorded,
4. total cost is finalized,
5. all buffered events are persisted,
6. trace validation succeeds.

---

# 102. Incomplete Trace

If execution crashes before completion:

```text
trajectory.status = INCOMPLETE
```

The trace should still be preserved.

This is important because evaluator crashes and infrastructure failures are themselves useful diagnostic information.

---

# 103. Crash Recovery

The logger should flush events periodically rather than waiting until execution completion.

This minimizes data loss when an execution fails unexpectedly.

---

# 104. Trace Flush Policy

Possible initial policy:

```yaml
trace:
  flush:
    every_event: true
```

For higher-performance experiments:

```yaml
trace:
  flush:
    batch_size: 20
```

The chosen policy must be recorded in experiment metadata.

---

# 105. Execution Cost from Trace

Cost metrics should be derivable from trace events where possible.

For example:

```text
MODEL_CALL events
TOOL_CALL events
SNAPSHOT events
RESTORE events
ANALYSIS events
```

can contribute to the total execution cost.

---

# 106. Cost Accounting Formula

The trace should support:

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

This matches the project's global budget model.

---

# 107. Token Accounting

Where the model provider exposes token counts, record:

```yaml
cost:
  input_tokens:
  output_tokens:
  total_tokens:
```

Do not estimate token usage when actual counts are available.

---

# 108. Model Call Accounting

Every model invocation should produce a cost record.

```yaml
cost:
  type: MODEL_CALL
  quantity: 1
  input_tokens:
  output_tokens:
```

---

# 109. Tool Cost Accounting

Each tool invocation should record:

```yaml
cost:
  type: TOOL_CALL
  quantity: 1
  latency_ms:
```

If tools are simulated and assigned no cost, record the accounting convention explicitly.

---

# 110. Snapshot and Restore Cost Accounting

Snapshot and restore operations must appear in the trace or linked cost store.

This prevents the evaluation from claiming branching is cheaper while silently ignoring the machinery required to make branching happen.

---

# 111. Trace-Derived State Coverage

The trace can support:

$$
StateCoverage
=
\frac{
UniqueRelevantStates
}{
TotalRelevantStates
}
$$

The exact denominator must be defined by the experiment.

---

# 112. Tool Coverage

The trace can calculate:

$$
ToolCoverage
=
\frac{
UniqueToolsUsed
}{
AvailableTools
}
$$

---

# 113. Attack Coverage

The trace can calculate coverage over attack categories:

```text
AUTHORIZATION
DATA_EXPOSURE
TOOL_SECURITY
STATE_MANIPULATION
FAULT_TOLERANCE
RESOURCE_ABUSE
```

---

# 114. Invariant Coverage

The system can report:

```text
invariants_evaluated
invariants_passed
invariants_failed
invariants_not_applicable
```

This allows failure discovery to be interpreted alongside evaluation coverage.

---

# 115. Event Coverage

For debugging and instrumentation validation, report counts by event type.

Example:

```text
TOOL_REQUEST: 42
POLICY_DECISION: 42
TOOL_RESPONSE: 40
STATE_TRANSITION: 18
INVARIANT_EVALUATED: 15
```

Missing expected events can indicate evaluator instrumentation defects.

---

# 116. Trace Query Examples

Researchers should be able to ask:

### All tool calls

```sql
SELECT *
FROM events
WHERE execution_id = ?
AND event_type = 'TOOL_REQUEST';
```

### All interesting states

```sql
SELECT *
FROM events
WHERE execution_id = ?
AND event_type = 'STATE_CHECKPOINT';
```

### All failures

```sql
SELECT *
FROM events
WHERE execution_id = ?
AND event_type = 'FAILURE_DETECTED';
```

### All branch origins

```sql
SELECT *
FROM events
WHERE event_type = 'BRANCH_CREATED';
```

---

# 117. Replay Query

A replay system should be able to retrieve:

```text
scenario
agent configuration
environment configuration
seed
trajectory
perturbations
snapshots
branch lineage
```

from the trace and linked experiment records.

---

# 118. Human-Readable Trace View

The dashboard should provide an ordered representation such as:

```text
Step 0
TASK_STARTED

Step 1
AGENT_OUTPUT

Step 2
TOOL_REQUEST
  transaction_lookup(account=ACC-001)

Step 3
POLICY_DECISION
  ALLOW

Step 4
TOOL_RESPONSE
  SUCCESS

Step 5
STATE_TRANSITION
  transaction_accessed

Step 6
STATE_CHECKPOINT
  interesting=true

Step 7
SNAPSHOT_CREATED
  SNAP-004
```

This is a presentation of recorded events, not a replacement for the canonical trace.

---

# 119. Observed Agent State Summary

Where the UI displays agent state, it should use terms such as:

```text
Observed Agent State
Trajectory State
Decision Context
Tool Interaction Context
Execution Context
```

It should not claim to display the model's private reasoning.

---

# 120. Trace-to-Dashboard Mapping

Dashboard components should derive their data from trace records.

```text
Trace
 ├── Timeline
 ├── Tool Activity
 ├── State Changes
 ├── Snapshot Points
 ├── Branches
 ├── Invariant Results
 ├── Failures
 └── Cost
```

Hard-coded experimental results are prohibited.

---

# 121. Trace-to-Experiment Metrics

The metrics engine should derive:

```text
time to first failure
validated failures
failure families
tool coverage
state coverage
branch yield
reproduction rate
cost per failure
cost per family
holdout generalization
```

from trace-linked records.

---

# 122. Example Complete Trace

```yaml
trajectory:
  trajectory_id: TRAJ-001
  execution_id: EXEC-001

  events:

    - event_id: EVT-001
      sequence_number: 0
      event_type: EXECUTION_STARTED

    - event_id: EVT-002
      sequence_number: 1
      event_type: TASK_STARTED
      payload:
        task_id: TASK-001

    - event_id: EVT-003
      sequence_number: 2
      event_type: AGENT_OUTPUT
      payload:
        output_reference: OUT-001

    - event_id: EVT-004
      sequence_number: 3
      event_type: TOOL_REQUEST
      payload:
        request_id: REQ-001
        tool_name: transaction_lookup

    - event_id: EVT-005
      sequence_number: 4
      event_type: POLICY_DECISION
      payload:
        request_id: REQ-001
        decision: ALLOW

    - event_id: EVT-006
      sequence_number: 5
      event_type: TOOL_RESPONSE
      payload:
        request_id: REQ-001
        status: SUCCESS

    - event_id: EVT-007
      sequence_number: 6
      event_type: STATE_TRANSITION
      payload:
        state_id: STATE-002

    - event_id: EVT-008
      sequence_number: 7
      event_type: STATE_CHECKPOINT
      payload:
        state_id: STATE-002
        interesting: true

    - event_id: EVT-009
      sequence_number: 8
      event_type: SNAPSHOT_CREATED
      payload:
        snapshot_id: SNAP-001

    - event_id: EVT-010
      sequence_number: 9
      event_type: BRANCH_CREATED
      payload:
        branch_id: BR-001
        parent_snapshot_id: SNAP-001

    - event_id: EVT-011
      sequence_number: 10
      event_type: PERTURBATION_APPLIED
      payload:
        perturbation_id: P-001

    - event_id: EVT-012
      sequence_number: 11
      event_type: INVARIANT_EVALUATED
      payload:
        invariant_id: I-004
        result: FAIL

    - event_id: EVT-013
      sequence_number: 12
      event_type: FAILURE_DETECTED
      payload:
        failure_id: FAIL-001

    - event_id: EVT-014
      sequence_number: 13
      event_type: EXECUTION_TERMINATED
      payload:
        termination_reason: FAILURE_TERMINAL
```

---

# 123. Minimal Event Schema

For the first implementation, the following fields are mandatory:

```yaml
event:
  event_id:
  execution_id:
  trajectory_id:
  sequence_number:
  event_type:
  event_category:
  timestamp:
  payload:
```

The richer state, cost, provenance, and integrity fields can be added without changing the conceptual model.

---

# 124. Minimal Trace Implementation

The first working version should implement:

```text
Execution
    ↓
Event Logger
    ↓
JSONL Trace
    ↓
SQLite Metadata
```

with event types:

```text
EXECUTION_STARTED
TASK_STARTED
AGENT_OUTPUT
TOOL_REQUEST
POLICY_DECISION
TOOL_RESPONSE
STATE_TRANSITION
STATE_CHECKPOINT
SNAPSHOT_CREATED
BRANCH_CREATED
PERTURBATION_APPLIED
INVARIANT_EVALUATED
FAILURE_DETECTED
COST_RECORDED
EXECUTION_TERMINATED
ERROR
```

This is enough to connect the core evaluation pipeline without building an elaborate telemetry platform first.

---

# 125. Recommended Repository Structure

```text
src/
└── agent_eval/
    └── trajectories/
        ├── __init__.py
        ├── models.py
        ├── events.py
        ├── logger.py
        ├── builder.py
        ├── validator.py
        ├── serializer.py
        ├── replay.py
        ├── correlation.py
        ├── cost.py
        └── queries.py
```

Tests:

```text
tests/
└── trajectories/
    ├── test_event_schema.py
    ├── test_event_ordering.py
    ├── test_tool_correlation.py
    ├── test_state_checkpoints.py
    ├── test_branch_correlation.py
    ├── test_failure_evidence.py
    ├── test_trace_validation.py
    ├── test_replay.py
    └── test_cost_accounting.py
```

---

# 126. Core Python Models

Conceptually:

```python
@dataclass
class TraceEvent:
    event_id: str
    experiment_id: str
    scenario_id: str
    execution_id: str
    trajectory_id: str

    sequence_number: int
    event_type: str
    event_category: str

    timestamp: str
    payload: dict

    actor: str | None = None
    source: str | None = None
    state_before: dict | None = None
    state_after: dict | None = None
    cost: dict | None = None
    metadata: dict | None = None
```

---

# 127. Trace Logger Interface

```python
class TraceLogger:

    def start_execution(self, execution):
        ...

    def record(self, event):
        ...

    def checkpoint_state(self, state):
        ...

    def record_tool_call(self, request, response):
        ...

    def record_failure(self, failure):
        ...

    def record_cost(self, cost):
        ...

    def end_execution(self, result):
        ...

    def flush(self):
        ...
```

---

# 128. Trace Builder

The Trace Builder should construct the trajectory from immutable events.

```python
class TraceBuilder:

    def add_event(self, event):
        ...

    def add_state_checkpoint(self, state):
        ...

    def add_snapshot(self, snapshot):
        ...

    def add_branch(self, branch):
        ...

    def finalize(self):
        ...
```

---

# 129. Trace Validator

```python
class TraceValidator:

    def validate_event(self, event):
        ...

    def validate_sequence(self, trajectory):
        ...

    def validate_references(self, trajectory):
        ...

    def validate_completion(self, trajectory):
        ...

    def validate(self, trajectory):
        ...
```

---

# 130. Trace Replay

Replay should reconstruct the sequence:

```text
Initial State
      ↓
Event 0
      ↓
Event 1
      ↓
...
      ↓
Event n
```

and compare reconstructed checkpoints against recorded hashes.

---

# 131. Replay Outcome

Replay should return:

```yaml
replay:
  status:
  final_state_hash:
  expected_final_state_hash:
  checkpoint_matches:
  mismatch_events:
  divergence_sequence:
```

Possible statuses:

```text
MATCH
DIVERGED
INCOMPLETE
INVALID
ERROR
```

---

# 132. Trace Divergence

If replay diverges:

```text
Expected:
STATE_HASH_A

Observed:
STATE_HASH_B
```

the system should identify the earliest divergent event where possible.

This is critical for diagnosing reproducibility problems.

---

# 133. Trace Storage Strategy

Recommended initial architecture:

```text
JSONL
  ↓
Raw immutable event log

SQLite
  ↓
Indexed metadata and relationships
```

This provides both archival simplicity and queryability.

---

# 134. Storage Separation

Do not place everything into one giant JSON document.

Separate:

```text
Event records
State records
Snapshot records
Branch records
Failure records
Cost records
Experiment metadata
```

and link them by IDs.

This keeps the system queryable as experiment size increases.

---

# 135. Trace Retention

Retention should be configurable, but research experiments should preserve the raw trace required to reproduce reported results.

Minimum retained artifacts:

```text
raw event trace
experiment configuration
scenario definitions
agent configuration reference
environment configuration
seeds
snapshot metadata
branch lineage
failure evidence
metrics inputs
```

---

# 136. Trace Integrity Requirements

The system must guarantee:

### TRACE-INV-001

Every event belongs to exactly one execution and trajectory.

### TRACE-INV-002

Sequence numbers are unique within a trajectory.

### TRACE-INV-003

Every completed execution has a termination event.

### TRACE-INV-004

Tool responses reference an existing tool request.

### TRACE-INV-005

Policy decisions reference the corresponding tool request.

### TRACE-INV-006

Branch events reference valid snapshots.

### TRACE-INV-007

Failure events reference valid evidence.

### TRACE-INV-008

State checkpoints reference valid state records.

### TRACE-INV-009

Cost records are attributable to an execution or branch.

### TRACE-INV-010

Hidden holdout outcomes cannot enter the adaptive selection information boundary before evaluation is complete.

---

# 137. Testing Requirements

The trace subsystem must have tests for:

### Schema

* required fields,
* invalid event types,
* invalid identifiers,
* invalid payloads.

### Ordering

* duplicate sequence numbers,
* missing sequence numbers,
* out-of-order events.

### Correlation

* tool request/response,
* policy/tool correlation,
* branch/snapshot correlation,
* failure/evidence correlation.

### State

* checkpoint references,
* state hashes,
* reconstruction.

### Cost

* model calls,
* tool calls,
* snapshot cost,
* restore cost,
* branch cost.

### Replay

* deterministic replay,
* divergence detection,
* incomplete trace handling.

### Failure Evidence

* failure with valid evidence,
* failure without evidence,
* evaluator error versus agent failure.

---

# 138. Trace Quality Checks

Before an experiment result is considered valid, the system should check:

```text
Trace schema valid
        AND
Event sequence valid
        AND
Required events present
        AND
State references valid
        AND
Failure evidence valid
        AND
Cost records complete
        AND
Experiment metadata complete
```

If a critical check fails, the affected execution should be marked invalid or inconclusive rather than silently included.

---

# 139. Trace Quality Status

Each trajectory should have:

```text
VALID
VALID_WITH_WARNINGS
INCOMPLETE
INVALID
```

A warning should not automatically invalidate an execution.

---

# 140. Relationship to Experimental Methodology

The trace provides the raw evidence needed for the later experimental methodology.

For each execution, the experiment can derive:

```text
what happened
when it happened
where state changed
which tools were used
which policies were applied
which perturbations occurred
which branches were created
which invariants failed
how much budget was consumed
```

This makes the trace the bridge between **system execution** and **research measurement**.

---

# 141. Relationship to Adaptive Selection

The selector consumes historical trace-derived statistics.

For example:

```text
Trace
 ↓
Validated Failure
 ↓
Failure Family
 ↓
Reward
 ↓
Candidate Statistics
 ↓
Adaptive Selection
```

The selector should consume only information available at the point of decision.

---

# 142. Relationship to State Snapshotting

The trajectory identifies candidate state checkpoints.

```text
Trace
 ↓
STATE_CHECKPOINT
 ↓
Interesting-State Detector
 ↓
Snapshot Manager
```

The snapshot stores the branchable state, while the trace stores **the fact that the state was reached and how it was reached**.

---

# 143. Relationship to Failure Analysis

Failure analysis should never need to guess how a failure occurred.

It should follow:

```text
Failure
 ↓
Evidence IDs
 ↓
Event IDs
 ↓
State IDs
 ↓
Trajectory
 ↓
Scenario
```

This creates an auditable failure explanation.

---

# 144. Relationship to Dashboard

The dashboard must visualize trace-derived facts.

It may show:

```text
Execution Timeline
Tool Calls
Policy Decisions
State Transitions
Interesting States
Snapshots
Branches
Invariant Results
Failures
Costs
```

but it must not invent values that are not present in the underlying experiment data.

---

# 145. Initial Trace Configuration

Recommended:

```yaml
trace:
  schema_version: "1.0"

  storage:
    raw_events: jsonl
    metadata: sqlite

  logging:
    level: full

  state:
    checkpoint_on:
      - authorization_change
      - sensitive_access
      - high_risk_tool
      - perturbation

  integrity:
    event_hashing: false
    state_hashing: true

  replay:
    enabled: true
```

Event hashing may be enabled later after the core logger is stable.

---

# 146. Definition of Done

The Trajectory / Trace subsystem is complete enough for the first research experiment when:

* [ ] Every execution receives a unique execution ID.
* [ ] Every execution produces a trajectory.
* [ ] Every trajectory contains ordered events.
* [ ] Event schemas are validated.
* [ ] Tool requests and responses can be correlated.
* [ ] Policy decisions can be correlated with tool requests.
* [ ] State transitions are recorded.
* [ ] Relevant state checkpoints are recorded.
* [ ] Interesting-state information can be attached.
* [ ] Snapshot events can be recorded.
* [ ] Branch lineage can be recorded.
* [ ] Perturbations can be recorded.
* [ ] Invariant evaluations can be recorded.
* [ ] Failure evidence can reference trace events.
* [ ] Costs can be recorded.
* [ ] Termination is explicit.
* [ ] Raw traces can be persisted.
* [ ] Trace metadata can be queried.
* [ ] Trace validation can detect malformed trajectories.
* [ ] Replay can reconstruct supported executions.
* [ ] Replay can detect divergence.
* [ ] Reproducibility metadata is preserved.
* [ ] Hidden holdout information boundaries are enforced.
* [ ] Dashboard data is derived from trace records rather than hard-coded values.

---

# 147. Final Canonical Model

The project's canonical trajectory representation is:

$$
\boxed{
\tau =
\{
e_0,e_1,\ldots,e_n
\}
}
$$

where each event contains:

$$
\boxed{
e_i =
(
id,
sequence,
type,
actor,
time,
state_{before},
payload,
state_{after},
cost,
metadata
)
}
$$

The execution evidence chain is:

```text
Scenario
   ↓
Execution
   ↓
Trajectory
   ↓
Events
   ↓
States
   ↓
Snapshots / Branches
   ↓
Invariant Evaluations
   ↓
Failure Evidence
   ↓
Failure
   ↓
Failure Family
```

And the fundamental rule is:

> **If a research claim cannot be traced back to recorded execution evidence, it should not be presented as an experimental result.**

This trace therefore becomes the canonical evidence layer for the entire project: adaptive selection, state-based branching, invariant evaluation, failure discovery, reproducibility, metamorphic testing, hidden-holdout evaluation, cost accounting, and final reporting all depend on it.