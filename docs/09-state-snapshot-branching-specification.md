# State Snapshot & Branching Specification

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** SSB-01
**Document Type:** State Snapshot & Branching Specification
**Version:** 1.0
**Status:** Draft for Implementation
**Related Documents:**

* Project Specification
* Research Questions & Success Criteria
* System Architecture
* Agent / Environment Specification
* Test Scenario & Attack Specification
* Adaptive Test Selection Specification
* Invariant & Failure Detection Specification
* Reproducibility & Metamorphic Testing Specification
* Budget & Cost Model

---

# 1. Purpose

This document specifies the **state snapshot and execution branching subsystem** used by the Budget-Constrained Adaptive Security Evaluation of AI Agents platform.

The subsystem allows the evaluator to:

1. identify security- or reliability-relevant intermediate states,
2. capture those states as reproducible snapshots,
3. restore snapshots into isolated execution contexts,
4. apply controlled perturbations,
5. execute multiple alternative continuations,
6. compare branch outcomes,
7. detect failures,
8. measure whether branching actually reduces evaluation cost.

The central research motivation is:

> Instead of repeatedly executing an entire agent trajectory from the beginning for every variation, can reusable intermediate execution states enable more efficient exploration of alternative continuations under a fixed evaluation budget?

---

# 2. Scope

This specification covers:

* interesting-state detection,
* state representation,
* snapshot creation,
* snapshot serialization,
* snapshot integrity,
* snapshot storage,
* snapshot restoration,
* restore validation,
* branch creation,
* branch isolation,
* branch perturbations,
* branch execution,
* branch lineage,
* branch termination,
* branch cost accounting,
* branch validation,
* snapshot reproducibility,
* snapshot compatibility,
* branch failure handling.

It does **not** assume that an LLM's internal KV cache can be captured or restored.

---

# 3. Fundamental Design Boundary

The project uses:

> **State-Based Execution Branching**

The initial implementation snapshots **controlled execution and environment state**.

It does not claim to snapshot the complete internal state of the language model.

Therefore:

```text
Environment / Execution Snapshot
              ≠
        LLM KV-Cache Snapshot
```

A branch may require the agent to reconstruct its model context from the stored execution context.

If future work introduces KV-cache restoration, that shall be treated as a separate experimental capability.

---

# 4. Research Objective

The branching subsystem exists to evaluate:

### RQ2

> Does state-based branching reduce redundant execution cost compared with independent full executions when evaluating multiple continuations from a common intermediate state?

The experiment must measure:

```text
Independent Execution Cost
vs.
Snapshot + Restore + Branch Execution Cost
```

rather than assuming that branching is cheaper.

---

# 5. Core Concept

A normal execution is:

```text
S0
 ↓
A0
 ↓
S1
 ↓
A1
 ↓
S2
 ↓
A2
 ↓
S3
```

Suppose `S2` is interesting.

Without branching:

```text
Full Execution A:
S0 → S1 → S2 → A2a → ...

Full Execution B:
S0 → S1 → S2 → A2b → ...

Full Execution C:
S0 → S1 → S2 → A2c → ...
```

With state-based branching:

```text
             S0 → S1 → S2
                       │
                    Snapshot
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Branch A     Branch B     Branch C
          │            │            │
       A2a → ...    A2b → ...    A2c → ...
```

The common prefix is executed once.

---

# 6. Terminology

| Term                   | Definition                                                         |
| ---------------------- | ------------------------------------------------------------------ |
| Execution              | One complete agent-environment run                                 |
| Trajectory             | Ordered sequence of execution events/states                        |
| State                  | Relevant observable execution/environment configuration            |
| Interesting State      | State meeting configured branching criteria                        |
| Snapshot               | Serialized representation of a branchable state                    |
| Restore                | Reconstruction of a snapshot into an isolated execution            |
| Branch                 | An execution continuation originating from a snapshot              |
| Parent Execution       | Execution that produced the snapshot                               |
| Parent Snapshot        | Snapshot from which a branch originates                            |
| Perturbation           | Controlled modification applied to a branch                        |
| Branch Lineage         | Relationship between executions, snapshots, and branches           |
| Branch Isolation       | Guarantee that branches do not unintentionally share mutable state |
| Snapshot Compatibility | Ability to safely restore and continue from a snapshot             |

---

# 7. State Model

The evaluator models execution state as:

$$
S_t =
\{
I_t,
A_t,
D_t,
T_t,
P_t,
F_t,
Q_t,
R_t
\}
$$

where:

* `I_t` = identity state,
* `A_t` = authorization/capability state,
* `D_t` = data/environment state,
* `T_t` = tool/service state,
* `P_t` = policy state,
* `F_t` = fault state,
* `Q_t` = task/execution context,
* `R_t` = relevant randomness state.

Not every experiment needs every component.

---

# 8. State Ownership

Each state component must have an explicit owner.

Example:

```text
Identity State
    → Environment State Manager

Database State
    → Database Simulator

Policy State
    → Policy Engine

Tool State
    → Tool Gateway / Tool Registry

Fault State
    → Fault Injector

Task State
    → Execution Manager

Agent Context
    → Agent Adapter / Execution Manager
```

The Snapshot Manager gathers the required state from these owners.

---

# 9. Snapshot Authority

The **Snapshot Manager** is responsible for creating and restoring snapshots.

It must not independently invent state.

The authoritative state is maintained by the relevant state-owning components.

```text
State Owners
     │
     ▼
Snapshot Manager
     │
     ▼
Serialized Snapshot
```

---

# 10. State Categories

State shall be divided into:

### 10.1 Environment State

Examples:

```text
database contents
resource ownership
permissions
service state
tool state
fault state
```

### 10.2 Execution State

Examples:

```text
step index
task progress
execution mode
trajectory position
pending operation
```

### 10.3 Agent Context State

Examples:

```text
conversation context
task context
tool history
configured memory
```

### 10.4 Configuration State

Examples:

```text
policy version
tool registry version
environment version
scenario version
invariant version
```

Configuration state may be referenced by version rather than fully copied if immutable.

---

# 11. Snapshot Contents

A snapshot shall contain sufficient information to reconstruct a supported branchable state.

Minimum structure:

```yaml
snapshot:
  snapshot_id:
  parent_execution_id:
  parent_trajectory_id:
  source_step:
  environment_version:
  state_schema_version:

  identity_state:
  authorization_state:
  data_state:
  tool_state:
  service_state:
  policy_state:
  fault_state:
  task_state:

  agent_context:
  randomness_state:

  state_hash:
  metadata:
```

---

# 12. Snapshot Metadata

Every snapshot shall include:

```yaml
snapshot_id:
experiment_id:
execution_id:
trajectory_id:
scenario_id:
scenario_version:
step_index:
timestamp:
state_hash:
schema_version:
environment_version:
agent_version:
policy_version:
tool_registry_version:
```

---

# 13. Snapshot Identity

Each snapshot must have a globally unique identifier within the experiment system.

Example:

```text
snapshot_id = SNAP-EXP001-EXEC0042-S17
```

The exact identifier format is implementation-specific.

Uniqueness is mandatory.

---

# 14. Snapshot Versioning

Snapshots shall have a schema version.

Example:

```text
snapshot_schema_version = 1.0
```

Changes to snapshot structure must increment the schema version.

The restoration system must reject unsupported snapshot versions rather than silently interpreting them.

---

# 15. Snapshot State Hash

Every snapshot shall have an integrity hash.

Conceptually:

$$
H_S = Hash(Canonicalize(S))
$$

The canonicalization process must be deterministic.

The hash allows the system to verify that:

* the snapshot was not corrupted,
* restored state matches the captured state,
* branch initialization began from the expected state.

---

# 16. State Canonicalization

Before hashing:

1. normalize object ordering,
2. normalize supported serialization formats,
3. remove non-semantic metadata,
4. preserve semantically relevant values,
5. serialize deterministically,
6. calculate the hash.

Example:

```text
Equivalent state
      ↓
Same canonical representation
      ↓
Same state hash
```

---

# 17. Semantic vs Non-Semantic State

The snapshot system must distinguish state that affects evaluation semantics from metadata that does not.

Potentially non-semantic:

```text
logging timestamp
internal object memory address
temporary debug identifier
```

Potentially semantic:

```text
resource ownership
permissions
database contents
authentication state
tool state
task progress
fault configuration
```

The exact classification must be documented by the environment implementation.

---

# 18. Agent Context Snapshot

Where supported, the system may capture the agent's observable execution context.

Examples:

```text
task
conversation history
tool interaction history
configured memory
execution metadata
```

The snapshot does not imply preservation of the model's hidden internal activations.

---

# 19. Agent Context Restoration

When restoring a branch, the Agent Adapter shall reconstruct the supported agent context.

Possible approaches include:

```text
stored conversation context
+
stored task context
+
stored tool history
```

The exact reconstruction mechanism depends on the agent implementation.

---

# 20. Model-State Boundary

The initial system shall assume:

```text
Model Internal State
    = NOT SNAPSHOTTED
```

Therefore, branch continuation may require a fresh model invocation using reconstructed context.

This cost must be included in branch cost measurements.

---

# 21. Interesting State

An interesting state is an intermediate execution state that has sufficient potential value to justify snapshotting and possible branching.

A state may be interesting because it:

* reaches a security boundary,
* changes authorization,
* accesses sensitive data,
* invokes a high-risk tool,
* reaches a novel state,
* satisfies a branchability condition,
* precedes a potentially unsafe action,
* has historically produced useful branches.

---

# 22. Interesting-State Detection

The Interesting-State Detector shall evaluate states using configured criteria.

Conceptually:

```python
def is_interesting(state, context):
    ...
```

Output:

```text
INTERESTING
NOT_INTERESTING
INDETERMINATE
```

---

# 23. Initial Interesting-State Criteria

The initial implementation should consider a state interesting when one or more of the following is true:

```text
authorization state changed
sensitive resource accessed
high-risk tool became available
security-relevant permission changed
new state feature observed
agent approaches security boundary
branchable perturbation exists
configured invariant becomes relevant
```

---

# 24. Interestingness Score

The system may calculate:

$$
I(S)
=
w_1 SecurityRelevance
+
w_2 Novelty
+
w_3 BranchPotential
+
w_4 RiskRelevance
-
w_5 SnapshotCost
$$

The weights must be configured experimentally.

The first implementation may instead use deterministic threshold rules.

---

# 25. Rule-Based Interesting-State Detection

Recommended initial implementation:

```yaml
interesting_state_rules:

  - rule_id: IS-001
    condition:
      authorization_state_changed: true

  - rule_id: IS-002
    condition:
      sensitive_resource_accessed: true

  - rule_id: IS-003
    condition:
      high_risk_tool_called: true

  - rule_id: IS-004
    condition:
      branchable_perturbation_available: true
```

This is easier to validate than an opaque learned detector.

---

# 26. Snapshot Trigger

When a state satisfies the configured interestingness condition:

```text
Trajectory Event
      ↓
State Extraction
      ↓
Interesting-State Detector
      ↓
INTERESTING
      ↓
Snapshot Eligibility Check
      ↓
Snapshot Creation
```

---

# 27. Snapshot Eligibility

A state may be interesting but not snapshot-compatible.

Therefore:

```text
Interesting
    ≠
Snapshotable
```

The Snapshot Manager must perform an additional compatibility check.

---

# 28. Snapshot Compatibility

A state is snapshot-compatible only when:

1. required mutable state can be serialized,
2. dependent services can be reconstructed,
3. required tool state can be restored,
4. policy state can be restored,
5. task context can be reconstructed,
6. branch isolation is possible,
7. required random state is available or explicitly unnecessary.

---

# 29. Snapshot Eligibility Result

The compatibility check shall return:

```text
SNAPSHOTABLE
NON_SNAPSHOTABLE
UNKNOWN
```

Only `SNAPSHOTABLE` states should normally enter the branch candidate pool.

---

# 30. Snapshot Creation

Snapshot creation consists of:

```text
1. Freeze relevant state
2. Gather state components
3. Validate state
4. Canonicalize state
5. Calculate state hash
6. Serialize state
7. Persist snapshot
8. Verify persisted snapshot
9. Register snapshot metadata
10. Release execution
```

---

# 31. State Freeze

During snapshot creation, mutable state should be temporarily protected from concurrent modification.

The system must avoid:

```text
State captured:
A = 1

State changes:
A = 2

Snapshot contains:
A = 1
other dependent state = 2
```

Such inconsistent snapshots can invalidate branch results.

---

# 32. Snapshot Consistency

A snapshot is consistent when all captured state components represent the same logical execution point.

The system should record:

```text
source_step
state_hash
component_versions
capture_timestamp
```

---

# 33. Snapshot Serialization

The snapshot serializer converts state into a persistent representation.

The initial implementation may use:

```text
JSON
MessagePack
SQLite
binary serialization
```

The selected format must support:

* deterministic reconstruction,
* versioning,
* integrity validation,
* reasonable performance.

---

# 34. Snapshot Storage

The Snapshot Store shall contain:

```text
snapshot metadata
serialized state
state hash
schema version
lineage information
compatibility status
creation cost
restore statistics
```

The store must be isolated from the agent.

---

# 35. Snapshot Storage Example

```text
snapshots/
├── SNAP-001/
│   ├── metadata.json
│   ├── state.json
│   └── hash.txt
│
├── SNAP-002/
│   ├── metadata.json
│   ├── state.json
│   └── hash.txt
```

The physical representation may instead use SQLite or object storage.

---

# 36. Snapshot Compression

Compression may be used when snapshots are large.

Compression must not alter the canonical state representation.

Conceptually:

```text
State
 ↓
Canonicalize
 ↓
Hash
 ↓
Serialize
 ↓
Compress
 ↓
Store
```

The hash should represent the logical state rather than the compressed byte stream unless explicitly configured otherwise.

---

# 37. Snapshot Integrity Verification

After writing a snapshot:

1. read it back,
2. deserialize it,
3. canonicalize it,
4. recalculate the hash,
5. compare hashes.

Expected:

$$
H_{stored}=H_{reconstructed}
$$

If not:

```text
SNAPSHOT_CORRUPTED
```

---

# 38. Snapshot Restoration

Restoration shall follow:

```text
Snapshot
   ↓
Load
   ↓
Schema Validation
   ↓
Integrity Validation
   ↓
Create Isolated Environment
   ↓
Restore State
   ↓
Recalculate State Hash
   ↓
Compare With Snapshot
   ↓
Validate Dependencies
   ↓
Branch Ready
```

---

# 39. Restore Isolation

Restoration shall never modify the original execution state.

Conceptually:

```text
Original Execution
        │
     Snapshot
        │
 ┌──────┴──────┐
 ▼             ▼
Branch A     Branch B
```

The parent execution remains unchanged.

---

# 40. Copy-on-Write

The implementation may use copy-on-write state to reduce memory and storage cost.

Example:

```text
Parent Snapshot
      │
      ├── shared immutable state
      │
      ├── Branch A mutable state
      │
      └── Branch B mutable state
```

Any mutation must create an isolated copy of the affected mutable component.

---

# 41. Copy-on-Write Requirement

If copy-on-write is used:

* immutable data may be shared,
* mutable data must be isolated,
* writes must never propagate between branches,
* branch state must remain independently hashable.

---

# 42. Full Copy Alternative

The initial implementation may use full state copying.

Advantages:

* simpler,
* easier to reason about,
* easier to test.

Disadvantages:

* higher memory/storage cost,
* slower for large state.

For the research prototype, correctness should be prioritized over premature optimization.

---

# 43. Branch Definition

A branch shall contain:

```yaml
branch:
  branch_id:
  parent_snapshot_id:
  parent_execution_id:
  parent_step:
  branch_depth:
  perturbation:
  agent_context:
  environment_config:
  budget_reservation:
  status:
```

---

# 44. Branch Identity

Every branch shall have a unique ID.

Example:

```text
BR-EXP001-SNAP042-B003
```

The branch ID shall remain stable throughout the branch lifecycle.

---

# 45. Branch Lineage

The system must preserve:

```text
Experiment
    ↓
Scenario
    ↓
Execution
    ↓
Snapshot
    ↓
Branch
    ↓
Branch Execution
    ↓
Failure
```

This relationship is essential for analyzing the value of branching.

---

# 46. Branch Depth

The system shall record branch depth.

Initial branch:

```text
depth = 1
```

If nested branching is permitted:

```text
Branch A
   ↓
Snapshot A
   ↓
Branch A1
```

then:

```text
depth = 2
```

The initial implementation should preferably restrict nested branching unless explicitly required.

---

# 47. Branch Creation

A branch is created by:

```text
1. Selecting a valid snapshot
2. Defining a perturbation
3. Validating the perturbation
4. Checking budget
5. Creating branch metadata
6. Reserving resources
7. Restoring the snapshot
8. Applying the perturbation
9. Validating resulting state
10. Starting branch execution
```

---

# 48. Branch Perturbation

A perturbation is a controlled modification to the restored state or execution conditions.

Example:

```yaml
perturbation:
  perturbation_id: P-042
  type: TOOL_RESPONSE
  target: transaction_lookup
  trigger:
    next_call: true
  modification:
    response_type: malformed
```

---

# 49. Perturbation Categories

Supported categories should include:

```text
INPUT
IDENTITY
PERMISSION
STATE
TOOL_ARGUMENT
TOOL_RESPONSE
POLICY
FAULT
TIMING
```

---

# 50. Perturbation Validation

Before branch execution, the system shall verify:

```text
target exists
+
perturbation is supported
+
perturbation is applicable to state
+
perturbation does not violate branch isolation
+
perturbation is reproducible
```

---

# 51. Branch State Transition

A branch follows:

```text
Restored Snapshot
        ↓
Perturbation
        ↓
Perturbed State
        ↓
Agent Continuation
        ↓
Environment Transitions
        ↓
Final Branch State
```

The perturbation must be recorded as an explicit event.

---

# 52. Perturbation Event

Example:

```yaml
event_type: PERTURBATION_APPLIED

payload:
  perturbation_id:
  type:
  target:
  original_value_hash:
  modified_value_hash:
```

Sensitive values should be redacted where appropriate.

---

# 53. Agent Continuation

The agent must continue from the reconstructed execution context.

Possible implementation:

```text
Stored Context
      ↓
Agent Adapter
      ↓
New Model Invocation
      ↓
Tool Interaction
```

This is a continuation at the evaluation semantics level, not necessarily a continuation of the model's exact internal computational state.

---

# 54. Branch Execution Modes

Branches should identify their execution mode:

```text
BRANCH
REPLAY_BRANCH
METAMORPHIC_BRANCH
FAULT_BRANCH
SECURITY_BRANCH
```

The mode is metadata and does not itself determine outcome.

---

# 55. Branch Isolation Requirement

The most important branching invariant is:

> A mutation performed in Branch A must not unintentionally affect Branch B or the parent execution.

Formally:

$$
\Delta State_A
\not\Rightarrow
\Delta State_B
$$

unless explicit shared-state semantics are configured.

---

# 56. Branch Isolation Test

Given:

```text
Snapshot S
├── Branch A
└── Branch B
```

execute:

```text
Branch A:
resource.status = modified
```

Then verify:

```text
Branch B:
resource.status = original
```

and:

```text
Parent:
resource.status = original
```

---

# 57. Shared-State Exceptions

Some experiments may intentionally configure shared immutable state.

Shared state must be explicitly declared.

Example:

```yaml
shared_state:
  - tool_registry
  - immutable_policy_definition
```

Mutable security-relevant state should not be implicitly shared.

---

# 58. Branch State Hash

Every branch should maintain:

```text
initial_branch_state_hash
current_state_hash
final_state_hash
```

This enables branch comparison and integrity verification.

---

# 59. Branch State Difference

For each branch, the evaluator should record relevant differences:

```text
Parent State
      ↓
Perturbed State
      ↓
Final Branch State
```

Example:

```yaml
state_diff:
  - path: authorization.permissions
    before: customer_read
    after: customer_read + ticket_update
```

---

# 60. Branch Termination

A branch terminates when:

* task completes,
* failure is detected and configured as terminal,
* maximum steps are reached,
* timeout occurs,
* budget is exhausted,
* environment error occurs,
* agent terminates.

Termination reason must be recorded.

---

# 61. Branch Status

Supported statuses:

```text
CREATED
VALIDATING
RESTORING
READY
RUNNING
COMPLETED
FAILED
INVALID
CANCELLED
ERROR
```

---

# 62. Snapshot Status

Supported statuses:

```text
CREATED
VALIDATING
VALID
INVALID
CORRUPTED
RESTORE_TESTED
ARCHIVED
DELETED
```

A snapshot should not be used for branching unless it is `VALID`.

---

# 63. Snapshot Restore Status

A restore operation shall return:

```text
SUCCESS
INTEGRITY_FAILURE
SCHEMA_FAILURE
DEPENDENCY_FAILURE
ISOLATION_FAILURE
STATE_MISMATCH
RESOURCE_FAILURE
```

---

# 64. Branch Validation

After restoration and perturbation, the branch environment must be validated.

Checks include:

```text
state hash
required resources
identity consistency
permission consistency
tool availability
policy compatibility
task context
fault configuration
isolation
```

---

# 65. Branch Execution Evidence

Every branch shall produce:

```yaml
branch_result:
  branch_id:
  parent_snapshot_id:
  execution_id:
  perturbation_id:
  outcome:
  final_state_hash:
  invariant_results:
  failures:
  cost:
  termination_reason:
```

---

# 66. Branch Failure Classification

A branch can produce:

### Agent Failure

Observable agent behavior violates an invariant.

### Environment Failure

Environment implementation behaves incorrectly.

### Snapshot Failure

Restoration does not reconstruct the expected state.

### Isolation Failure

Branches unintentionally affect each other.

### Perturbation Failure

Configured perturbation was not applied correctly.

### Execution Error

The branch could not be validly executed.

These categories must not be collapsed into one generic failure.

---

# 67. Snapshot Failure

A snapshot failure occurs when:

```text
stored state
    ≠
restored state
```

or required dependencies cannot be reconstructed.

This is a problem with the evaluation mechanism, not automatically a discovered agent vulnerability.

---

# 68. Branch Isolation Failure

An isolation failure occurs when:

```text
Branch A changes X
        ↓
Branch B unexpectedly observes X
```

This invalidates the corresponding branch results.

---

# 69. Perturbation Failure

A perturbation failure occurs when:

```text
configured perturbation
        ≠
actual applied perturbation
```

The branch must not be used as valid experimental evidence unless the experiment explicitly defines another interpretation.

---

# 70. Branch Cost Model

Branching must include:

$$
C_{branch,total}
=
C_{snapshot}
+
C_{restore}
+
C_{perturbation}
+
C_{execution}
+
C_{analysis}
$$

If verification is included:

$$
C_{branch,total}
=
C_{snapshot}
+
C_{restore}
+
C_{perturbation}
+
C_{execution}
+
C_{analysis}
+
C_{verification}
$$

---

# 71. Independent Execution Cost

For `k` independent executions:

$$
C_{independent}
=
\sum_{i=1}^{k}
C_{full,i}
$$

Each execution includes the common prefix.

---

# 72. Branching Cost

For one parent execution and `k` branches:

$$
C_{branching}
=
C_{prefix}
+
C_{snapshot}
+
\sum_{i=1}^{k}
(
C_{restore,i}
+
C_{perturbation,i}
+
C_{continuation,i}
)
+
C_{analysis}
$$

---

# 73. Branching Savings

The observed savings are:

$$
Savings
=
C_{independent}
-
C_{branching}
$$

and:

$$
SavingsRate
=
\frac{
C_{independent}-C_{branching}
}{
C_{independent}
}
$$

A positive value must be measured, not assumed.

---

# 74. Branching Break-Even Point

Branching becomes beneficial when:

$$
C_{branching}
<
C_{independent}
$$

The experiment should determine the number of branches `k` at which this occurs.

This is particularly important because snapshot and restore overhead can make branching inefficient for very small branch counts.

---

# 75. Snapshot Overhead

The system shall record:

```text
snapshot creation time
snapshot serialization size
snapshot storage cost
snapshot restore time
```

This allows researchers to understand the real cost of state-based branching.

---

# 76. Snapshot Size

Record:

```text
raw_state_size
serialized_size
compressed_size
```

where applicable.

Snapshot size is an important engineering metric because it affects branching scalability.

---

# 77. Restore Performance

Record:

```text
restore_latency
state_validation_latency
dependency_reconstruction_latency
```

These should be separated where possible.

---

# 78. Branch Execution Performance

Record:

```text
branch_start_time
branch_end_time
branch_execution_latency
model_calls
tool_calls
tokens
```

where available.

---

# 79. Snapshot Reuse

A single snapshot may produce multiple branches.

Example:

```text
Snapshot S1
├── Branch B1
├── Branch B2
├── Branch B3
├── Branch B4
└── Branch B5
```

The system shall record:

```text
branches_created_from_snapshot
```

This allows analysis of snapshot reuse efficiency.

---

# 80. Snapshot Utility

A snapshot's utility may be measured as:

$$
Utility(S)
=
\frac{
UsefulBranches(S)
}{
SnapshotCost(S)
}
$$

where `UsefulBranches` could mean:

* validated failures,
* new failure families,
* meaningful state exploration.

The definition must be fixed per experiment.

---

# 81. Branch Yield

For snapshot `S`:

$$
BranchYield(S)
=
\frac{
ValidatedFailures
}{
BranchesExecuted
}
$$

Another useful measure:

$$
FamilyYield(S)
=
\frac{
NewFailureFamilies
}{
BranchesExecuted
}
$$

---

# 82. Branch Diversity

The system may measure how different branch outcomes are.

Possible dimensions:

```text
final state
tool sequence
invariant outcomes
failure signatures
```

Branch diversity can indicate whether a snapshot provides meaningful alternative exploration.

---

# 83. Branch Selection

Branches may initially be generated using a fixed set of perturbations.

Example:

```text
Snapshot S
├── malformed response
├── timeout
├── adversarial response
├── permission change
└── state mutation
```

Later, the Adaptive Test Selection subsystem may select among these branch candidates.

Branch selection should be separately configurable.

---

# 84. Branch Candidate Model

A branch candidate contains:

```yaml
branch_candidate:
  branch_candidate_id:
  parent_snapshot_id:
  perturbation_id:
  estimated_cost:
  novelty:
  historical_yield:
  branch_depth:
  applicable:
```

---

# 85. Branch Budget

The system shall support:

```text
max_branches_per_snapshot
max_branches_per_execution
max_branches_per_experiment
max_branch_depth
```

These limits prevent uncontrolled branching.

---

# 86. Branch Explosion

Without limits:

```text
1 Snapshot
   ↓
5 Branches
   ↓
25 Branches
   ↓
125 Branches
   ↓
...
```

The system must therefore explicitly bound branching.

Nested branching should be disabled by default.

---

# 87. Snapshot Selection

Not every interesting state should necessarily be snapshotted.

The evaluator may apply:

```text
interestingness
+
snapshot compatibility
+
snapshot cost
+
remaining budget
+
historical utility
```

before creating a snapshot.

---

# 88. Snapshot Deduplication

Equivalent snapshots may be deduplicated.

Two snapshots can be considered equivalent when:

```text
same canonical state
+
same relevant configuration
+
same required execution context
```

The system should calculate a snapshot equivalence key.

---

# 89. Snapshot Equivalence Key

Conceptually:

$$
K_S =
Hash(
CanonicalState
+
PolicyVersion
+
ToolRegistryVersion
+
ScenarioVersion
)
$$

Additional fields may be included when required.

---

# 90. Snapshot Deduplication Rule

If an equivalent valid snapshot already exists:

```text
New Snapshot Request
        ↓
Equivalent Snapshot Found
        ↓
Reuse Existing Snapshot
```

The system must preserve lineage showing that multiple executions reached an equivalent state.

---

# 91. Snapshot Provenance

Every snapshot must identify:

```text
source execution
source scenario
source trajectory
source step
state hash
configuration versions
```

This enables researchers to trace a branch back to the original trajectory.

---

# 92. Branch Provenance

Every branch must identify:

```text
parent snapshot
parent scenario
perturbation
branch configuration
execution configuration
```

---

# 93. Snapshot and Branch Lineage Example

```text
Scenario S14
     │
     ▼
Execution E21
     │
     ▼
State at Step 7
     │
     ▼
Snapshot SNAP-021
     │
 ┌───┼─────────┐
 ▼   ▼         ▼
B1   B2        B3
│    │         │
E22  E23       E24
│    │         │
F1   PASS      F2
```

This structure must be preserved in the experiment database.

---

# 94. Snapshot Security

Snapshots may contain sensitive evaluation state.

Therefore:

* the agent must not access them,
* branch isolation must be enforced,
* storage permissions must be restricted,
* snapshots should not contain unnecessary secrets,
* sensitive values should be encrypted or redacted where appropriate.

---

# 95. Snapshot Secret Handling

If an environment contains secrets required for simulation, the snapshot system should prefer:

```text
secret reference
```

over:

```text
plaintext secret
```

where technically possible.

Restoration should retrieve the same controlled secret through the experiment environment.

---

# 96. Snapshot Integrity and Tampering

The system should detect unexpected snapshot modification using:

```text
state hash
schema validation
metadata integrity
```

For stronger integrity guarantees, a cryptographic integrity mechanism may be used.

---

# 97. Branch Environment Security

A branch shall not gain capabilities simply because it was created from a privileged snapshot.

The branch inherits the explicitly defined state.

Any capability changes must be part of the perturbation and experiment configuration.

---

# 98. Branch Capability Rule

```text
Parent Capability State
        ↓
Snapshot
        ↓
Branch
        ↓
Capability state preserved
```

unless:

```text
Explicit Capability Perturbation
```

is applied.

---

# 99. Branch Policy Rule

The branch shall preserve the parent policy configuration unless a controlled policy perturbation is explicitly specified.

This prevents accidental policy drift between branches.

---

# 100. Branch Environment Version

The branch must use a compatible environment version.

A snapshot generated under:

```text
environment_version = 1.0
```

must not automatically be restored under:

```text
environment_version = 2.0
```

unless compatibility is explicitly declared.

---

# 101. Snapshot Migration

If snapshot migration is required:

```text
Snapshot v1
    ↓
Migration Function
    ↓
Snapshot v2
    ↓
Validation
```

Migration must be versioned and tested.

The initial prototype should avoid migration where possible.

---

# 102. Snapshot Failure Recovery

If snapshot creation fails:

```text
parent execution continues
```

unless snapshot creation was configured as a terminal dependency.

The failure shall be logged as:

```text
SNAPSHOT_CREATION_ERROR
```

and shall not be treated as an agent failure.

---

# 103. Restore Failure Recovery

If restoration fails:

```text
branch status = ERROR
```

The system shall not continue executing from an unvalidated partial state.

---

# 104. Branch Cleanup

After branch termination:

1. collect final evidence,
2. persist branch result,
3. release resources,
4. remove temporary state,
5. retain required provenance,
6. update cost statistics.

---

# 105. Snapshot Retention

Snapshot retention should be configurable.

Possible policies:

```text
KEEP_ALL
KEEP_VALID_ONLY
KEEP_FAILURE_RELATED
KEEP_EXPERIMENT_DURATION
ARCHIVE_AFTER_EXPERIMENT
```

The retention policy must not remove snapshots required for reproducibility before the experiment is finalized.

---

# 106. Branch Concurrency

Multiple branches may execute concurrently when:

* environments are isolated,
* resource limits permit,
* the experiment allows parallelism.

Parallel execution must not introduce shared-state contamination.

---

# 107. Concurrency Cost

Parallel branches may reduce wall-clock time without reducing total computational cost.

Therefore report separately:

```text
total compute/evaluation cost
```

and:

```text
wall-clock elapsed time
```

A faster wall-clock experiment is not automatically a cheaper experiment.

---

# 108. Branch Scheduler

The Branch Manager may schedule:

```text
queued
running
completed
failed
```

branches.

The scheduler shall respect:

```text
maximum concurrent branches
branch budget
global experiment budget
resource limits
```

---

# 109. Snapshot Creation During Branching

Branches may themselves reach interesting states.

If nested branching is disabled:

```text
interesting branch state
        ↓
record state
        ↓
do not create child branch
```

If nested branching is enabled experimentally:

```text
branch
  ↓
snapshot
  ↓
child branch
```

The lineage must clearly distinguish parent and child branches.

---

# 110. Initial Nested Branching Policy

Recommended:

```yaml
branching:
  nested_branches: false
```

This simplifies:

* cost accounting,
* lineage,
* experiment analysis,
* isolation verification.

Nested branching can be evaluated as future work.

---

# 111. Snapshot Decision Policy

The initial system should use:

```text
Rule-based Interesting State
+
Snapshot Compatibility Check
+
Budget Check
+
Maximum Snapshot Count
```

rather than a learned snapshot policy.

This provides a stable baseline for studying adaptive branching later.

---

# 112. Snapshot Thresholds

Configurable thresholds may include:

```yaml
snapshot:
  enabled: true
  max_snapshots_per_execution: 5
  max_snapshots_per_experiment: 500

  interestingness:
    sensitive_access: true
    authorization_change: true
    high_risk_tool: true
    novel_state: true
```

---

# 113. Branch Configuration Example

```yaml
branching:
  enabled: true

  max_branches_per_snapshot: 5
  max_branches_per_execution: 10
  max_branches_per_experiment: 500
  max_depth: 1

  isolation:
    mode: full_copy

  perturbations:
    enabled:
      - TOOL_RESPONSE
      - TOOL_TIMEOUT
      - PERMISSION
      - STATE
```

---

# 114. Snapshot Configuration Example

```yaml
snapshot:
  enabled: true

  serializer: json

  integrity:
    hash_algorithm: sha256

  storage:
    backend: sqlite

  compression:
    enabled: false

  retention:
    policy: keep_failure_related
```

The exact serialization and hashing technologies are implementation choices, but the behavior must remain deterministic and verifiable.

---

# 115. Snapshot Manager Interface

Conceptual interface:

```python
class SnapshotManager:

    def is_snapshotable(self, state):
        ...

    def create_snapshot(self, execution, state):
        ...

    def validate_snapshot(self, snapshot):
        ...

    def restore_snapshot(self, snapshot):
        ...

    def verify_restored_state(self, snapshot, restored_state):
        ...

    def get_snapshot(self, snapshot_id):
        ...
```

---

# 116. Branch Manager Interface

```python
class BranchManager:

    def create_branch(
        self,
        snapshot,
        perturbation,
        budget
    ):
        ...

    def validate_branch(self, branch):
        ...

    def execute_branch(self, branch):
        ...

    def terminate_branch(self, branch):
        ...

    def get_lineage(self, branch_id):
        ...
```

---

# 117. Interesting-State Detector Interface

```python
class InterestingStateDetector:

    def evaluate(self, state, context):
        ...

    def score(self, state, context):
        ...

    def explain(self, state, context):
        ...
```

The `explain()` output should describe observable state features and triggered rules, not hidden model reasoning.

---

# 118. Snapshot Serializer Interface

```python
class SnapshotSerializer:

    def serialize(self, state):
        ...

    def deserialize(self, payload):
        ...

    def canonicalize(self, state):
        ...

    def hash(self, state):
        ...
```

---

# 119. Branch Perturbation Interface

```python
class PerturbationEngine:

    def validate(self, perturbation, state):
        ...

    def apply(self, perturbation, state):
        ...

    def describe(self, perturbation):
        ...

    def reverse(self, perturbation, state):
        ...
```

A reverse operation is optional if the branch uses isolated copies.

---

# 120. Branch Cost Tracker

Conceptual interface:

```python
class BranchCostTracker:

    def record_snapshot(self, cost):
        ...

    def record_restore(self, cost):
        ...

    def record_perturbation(self, cost):
        ...

    def record_execution(self, cost):
        ...

    def record_analysis(self, cost):
        ...

    def total(self):
        ...
```

---

# 121. Snapshot Cost Record

```yaml
snapshot_cost:
  snapshot_id:
  serialization_time:
  state_size:
  storage_size:
  storage_latency:
  hashing_time:
  total_cost:
```

---

# 122. Restore Cost Record

```yaml
restore_cost:
  snapshot_id:
  branch_id:
  load_time:
  deserialize_time:
  reconstruction_time:
  validation_time:
  total_cost:
```

---

# 123. Branch Cost Record

```yaml
branch_cost:
  branch_id:
  snapshot_cost:
  restore_cost:
  perturbation_cost:
  execution_cost:
  analysis_cost:
  verification_cost:
  total_cost:
```

---

# 124. Snapshot Quality Metrics

The system should measure:

```text
snapshot_creation_success_rate
snapshot_restore_success_rate
snapshot_integrity_failure_rate
snapshot_size
snapshot_creation_latency
snapshot_restore_latency
```

---

# 125. Branch Quality Metrics

Measure:

```text
branch_execution_success_rate
branch_isolation_failure_rate
branch_yield
branch_family_yield
branch_cost
branch_diversity
```

---

# 126. Branching Efficiency Metrics

Primary:

$$
BranchingEfficiency
=
\frac{
ValidatedFailureFamilies
}{
BranchingCost
}
$$

Secondary:

$$
CostSavingsRate
=
\frac{
C_{independent}-C_{branching}
}{
C_{independent}
}
$$

These metrics must be computed from actual measured cost.

---

# 127. State Reuse Metrics

Measure:

```text
snapshots_created
snapshots_reused
branches_per_snapshot
average_prefix_length
average continuation length
```

These metrics help determine whether the system is actually reusing meaningful execution state.

---

# 128. Prefix Reuse Ratio

For a trajectory with:

```text
prefix_steps
total_steps
```

the system may report:

$$
PrefixReuseRatio
=
\frac{prefix\_steps}{total\_steps}
$$

For multiple branches, this can be analyzed alongside measured cost.

---

# 129. Branching Benefit by Branch Count

Experiments should compare:

```text
k = 1
k = 2
k = 3
k = 5
k = 10
```

where feasible.

This can reveal the point at which snapshot overhead is amortized.

---

# 130. Snapshot Utility Curve

A useful experiment is:

```text
Number of Branches
        vs
Total Cost
```

Compare:

```text
Independent execution
```

against:

```text
Snapshot + branching
```

The result determines whether the branching mechanism provides an actual budget advantage.

---

# 131. Snapshot Reproducibility Test

For a snapshot:

```text
Create Snapshot S
      ↓
Restore S
      ↓
Hash Restored State
```

Expected:

$$
H_{restored}=H_{snapshot}
$$

for deterministic snapshot-compatible state.

---

# 132. Branch Isolation Test

For two branches:

```text
S
├── B1
└── B2
```

apply:

```text
B1:
modify resource X
```

verify:

```text
B2.X = S.X
```

and:

```text
Parent.X = S.X
```

---

# 133. Perturbation Reproducibility Test

Given:

```text
Snapshot S
+
Perturbation P
```

the resulting perturbed state should be reproducible under identical configuration.

---

# 134. Branch Replay Test

A branch should be replayable using:

```text
snapshot_id
+
perturbation_id
+
agent configuration
+
environment configuration
+
seed
```

where deterministic replay is supported.

---

# 135. Snapshot Corruption Test

Intentionally modify stored snapshot data.

Expected:

```text
integrity check fails
```

and:

```text
snapshot cannot be used for valid branching
```

---

# 136. Incomplete Snapshot Test

Remove a required state component.

Expected:

```text
restore validation fails
```

The system must not silently substitute an arbitrary default.

---

# 137. Version Compatibility Test

Attempt to restore an incompatible snapshot version.

Expected:

```text
SCHEMA_FAILURE
```

unless an explicitly tested migration exists.

---

# 138. Budget Enforcement Test

Attempt to create more branches than the configured budget permits.

Expected:

```text
branch request rejected
```

and:

```text
experiment budget remains valid
```

---

# 139. Branch Contamination Test

Run:

```text
Branch A
Branch B
Branch C
```

with distinct state mutations.

Verify that each branch observes only its own mutations plus explicitly shared state.

---

# 140. State Snapshot Acceptance Criteria

The subsystem passes its initial acceptance criteria when:

* [ ] Interesting states can be detected.
* [ ] Snapshot eligibility can be evaluated.
* [ ] Valid state can be serialized.
* [ ] Snapshot hashes can be generated.
* [ ] Snapshots can be stored.
* [ ] Stored snapshots can be validated.
* [ ] Snapshots can be restored.
* [ ] Restored state matches the snapshot.
* [ ] Branch environments are isolated.
* [ ] Perturbations can be applied.
* [ ] Branch lineage is preserved.
* [ ] Branch costs are measured.
* [ ] Snapshot costs are measured.
* [ ] Restore costs are measured.
* [ ] Branch outcomes can be evaluated.
* [ ] Snapshot failures are distinguished from agent failures.
* [ ] Branch isolation failures are detectable.
* [ ] Branches respect experiment budgets.
* [ ] Snapshot versions are tracked.
* [ ] Branches can be reproduced under documented conditions.

---

# 141. Snapshot Invariants

The subsystem shall enforce:

### INV-SNAP-001

A snapshot must represent a valid execution state.

### INV-SNAP-002

A stored snapshot must pass integrity validation.

### INV-SNAP-003

Restoring a valid snapshot must not modify the parent execution.

### INV-SNAP-004

Restored state must match the snapshot's canonical state.

### INV-SNAP-005

Unsupported snapshot versions must not be silently restored.

### INV-SNAP-006

A non-snapshotable state must not be treated as snapshotable.

### INV-SNAP-007

Snapshot provenance must be preserved.

---

# 142. Branch Invariants

### INV-BR-001

Every branch must have exactly one parent snapshot.

### INV-BR-002

Every branch must have an explicit perturbation configuration or an explicitly defined no-perturbation mode.

### INV-BR-003

Branch state must be isolated from sibling branches.

### INV-BR-004

Branch state must be isolated from the parent execution.

### INV-BR-005

Every branch must respect the global evaluation budget.

### INV-BR-006

Branch perturbations must be recorded.

### INV-BR-007

Branch execution must begin only after restore validation succeeds.

### INV-BR-008

Branch failures must distinguish evaluator/environment failures from agent failures.

### INV-BR-009

Branch lineage must remain queryable.

---

# 143. Snapshot and Branch Data Model

Recommended entities:

```text
Snapshot
SnapshotComponent
SnapshotValidation
RestoreOperation
Branch
BranchPerturbation
BranchExecution
BranchCost
BranchLineage
```

Relationships:

```text
Execution
   │
   └── Snapshot
          │
          ├── RestoreOperation
          │
          └── Branch
                 │
                 ├── Perturbation
                 ├── Execution
                 └── Cost
```

---

# 144. Snapshot Schema Example

```yaml
snapshot:
  snapshot_id: SNAP-0042

  provenance:
    experiment_id: EXP-001
    scenario_id: S14
    execution_id: EXEC-101
    trajectory_id: TRAJ-101
    step_index: 7

  versions:
    environment: "1.0"
    agent: "0.1"
    policy: "1.0"
    tools: "1.0"
    schema: "1.0"

  state:
    identity:
      user_id: user_001
      agent_id: support_agent

    authorization:
      permissions:
        - customer_read
        - ticket_read

    task:
      status: ticket_loaded

    faults:
      active: []

  integrity:
    state_hash: "..."
```

---

# 145. Branch Schema Example

```yaml
branch:
  branch_id: BR-0042-01

  parent:
    snapshot_id: SNAP-0042
    execution_id: EXEC-101
    step_index: 7

  perturbation:
    id: P-017
    type: TOOL_RESPONSE
    target: ticket_search
    mode: malformed_response

  execution:
    mode: BRANCH
    seed: 4821

  status: COMPLETED
```

---

# 146. End-to-End Branching Algorithm

```python
def create_branch(snapshot, perturbation, budget):

    validate_snapshot(snapshot)

    validate_perturbation(
        perturbation,
        snapshot
    )

    estimated_cost = estimate_branch_cost(
        snapshot,
        perturbation
    )

    reserve_budget(
        estimated_cost
    )

    branch = create_branch_record(
        snapshot=snapshot,
        perturbation=perturbation
    )

    environment = restore_snapshot(
        snapshot
    )

    validate_restored_environment(
        environment,
        snapshot
    )

    apply_perturbation(
        environment,
        perturbation
    )

    validate_branch_state(
        environment
    )

    result = execute_branch(
        environment
    )

    evaluate_invariants(
        result
    )

    record_cost(
        branch,
        result
    )

    finalize_branch(
        branch,
        result
    )

    return result
```

---

# 147. End-to-End Snapshot Algorithm

```python
def create_snapshot(execution, state):

    if not is_valid_state(state):
        raise SnapshotError("Invalid state")

    if not is_snapshotable(state):
        return None

    frozen_state = freeze_state(state)

    canonical_state = canonicalize(
        frozen_state
    )

    state_hash = hash_state(
        canonical_state
    )

    serialized = serialize(
        canonical_state
    )

    snapshot = persist_snapshot(
        serialized,
        state_hash
    )

    verify_snapshot(
        snapshot
    )

    return snapshot
```

---

# 148. Full Branching Workflow

```text
Agent Execution
      │
      ▼
Trajectory Event
      │
      ▼
State Extraction
      │
      ▼
Interesting-State Detector
      │
      ├── NOT INTERESTING
      │        ↓
      │    Continue
      │
      └── INTERESTING
               │
               ▼
       Snapshot Compatibility
               │
          ┌────┴────┐
          ▼         ▼
       Invalid    Valid
          │         │
          │         ▼
          │      Snapshot
          │         │
          │         ▼
          │   Branch Candidates
          │         │
          │         ▼
          │    Budget Check
          │         │
          │         ▼
          │    Branch Selection
          │         │
          │         ▼
          │       Restore
          │         │
          │         ▼
          │   Apply Perturbation
          │         │
          │         ▼
          │  Validate Branch State
          │         │
          │         ▼
          │  Execute Continuation
          │         │
          │         ▼
          │  Evaluate Invariants
          │         │
          │         ▼
          │  Record Outcome + Cost
          │
          ▼
       Continue
```

---

# 149. Relationship to Adaptive Test Selection

The State Snapshot & Branching subsystem and Adaptive Test Selection subsystem must remain separate.

Adaptive selection answers:

> **Which candidate should be executed?**

Branching answers:

> **From this reusable state, which alternative continuation should be explored?**

The systems interact through branch candidates.

```text
Adaptive Selector
       ↓
Scenario
       ↓
Execution
       ↓
Interesting State
       ↓
Snapshot
       ↓
Branch Candidates
       ↓
Branch Selector
       ↓
Branch Execution
```

The first implementation may use uniform branch selection while adaptive scenario selection is being studied.

---

# 150. Relationship to Failure Detection

Branching does not determine whether a branch is successful.

The flow remains:

```text
Branch Execution
      ↓
Trajectory
      ↓
Invariant Evaluation
      ↓
Failure Detection
      ↓
Failure Classification
      ↓
Failure Clustering
      ↓
Validation
```

This separation is required for scientifically interpretable results.

---

# 151. Relationship to Reproducibility

A branch-discovered failure shall preserve:

```text
snapshot_id
branch_id
perturbation_id
scenario_id
execution_id
configuration_versions
random_seeds
state_hash
failure_signature
```

This allows independent replay.

---

# 152. Relationship to Metamorphic Testing

A snapshot may also serve as a controlled base state for metamorphic experiments when the transformation semantics permit it.

However, metamorphic evaluation must still execute:

```text
Base
+
Transformation
```

and compare actual outcomes.

A branch is not automatically a metamorphic test.

---

# 153. Relationship to Hidden Holdout

Snapshots and branches from hidden holdout experiments must remain isolated from the adaptive training/evaluation loop.

Holdout snapshots must not be used to tune:

* interestingness thresholds,
* branch-selection weights,
* perturbation priorities,
* cost models.

until the holdout evaluation phase is complete.

---

# 154. Research Experiment: Branching vs Independent Execution

The minimum branching experiment shall compare:

### Condition A

Independent full executions.

### Condition B

Shared-prefix execution with state snapshots and branching.

Control:

```text same scenario
same agent
same environment
same perturbations
same branch count
same validation
same budget
```

Measure:

```text total cost
wall-clock time
snapshot overhead
restore overhead
number of failures discovered
number of failure families
```

---

# 155. Example Experiment

Suppose three continuations are required:

```text
P + C1
P + C2
P + C3
```

where `P` is the common prefix.

Independent:

$$
C_{independent}
=
3C_P+C_{C1}+C_{C2}+C_{C3}
$$

Branching:

$$
C_{branching}
=
C_P+C_{snapshot}
+
C_{restore1}+C_{C1}
+
C_{restore2}+C_{C2}
+
C_{restore3}+C_{C3}
$$

The experiment measures the actual values.

---

# 156. Scientific Interpretation

A successful branch mechanism requires more than:

```text
snapshot works
```

The research claim requires evidence that:

```text
snapshot works
+
branches are isolated
+
state is restored correctly
+
branch outcomes are valid
+
branching cost is measured
+
branching provides useful exploration
+
branching is beneficial under relevant budgets
```

---

# 157. What Does Not Count as Branching Evidence

The following do not establish a research result:

* copying a Python object without testing restoration,
* hard-coded branch outputs,
* simulated branch cost,
* claiming zero prefix cost,
* assuming snapshot overhead is negligible,
* assuming branches are isolated,
* using a fake state hash,
* treating model KV-cache reuse as implemented when it is not,
* counting unvalidated branch anomalies as failures.

---

# 158. Recommended Initial Implementation

The first working implementation should use:

```text
Python
+
SQLite
+
JSON serialization
+
SHA-256 state hashes
+
Controlled in-memory environment
+
Full-copy branch isolation
+
Rule-based interesting-state detection
+
Explicit perturbations
```

This is intentionally conservative.

The first goal is to establish **correct branching semantics**, not to build an elaborate distributed snapshot infrastructure before anyone knows whether the research hypothesis survives contact with reality.

---

# 159. Recommended Implementation Order

Implement in this sequence:

```text
1. Environment State Manager
        ↓
2. Canonical State Representation
        ↓
3. State Hashing
        ↓
4. Snapshot Serializer
        ↓
5. Snapshot Store
        ↓
6. Snapshot Validation
        ↓
7. Restore Engine
        ↓
8. Restore Verification
        ↓
9. Full-Copy Branch Isolation
        ↓
10. Perturbation Engine
        ↓
11. Branch Manager
        ↓
12. Branch Cost Tracking
        ↓
13. Interesting-State Detector
        ↓
14. Automatic Snapshot Trigger
        ↓
15. Branch Candidate Generation
        ↓
16. Branch Execution
        ↓
17. Branch Invariant Evaluation
        ↓
18. Replay Testing
        ↓
19. Branching Efficiency Experiments
```

---

# 160. Recommended Repository Structure

```text
src/
└── agent_eval/
    ├── states/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── state_manager.py
    │   ├── canonicalization.py
    │   ├── hashing.py
    │   └── diff.py
    │
    ├── snapshots/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── manager.py
    │   ├── serializer.py
    │   ├── validator.py
    │   ├── store.py
    │   └── restore.py
    │
    └── branching/
        ├── __init__.py
        ├── models.py
        ├── manager.py
        ├── perturbations.py
        ├── isolation.py
        ├── lineage.py
        ├── scheduler.py
        └── cost.py
```

Tests:

```text
tests/
├── states/
│   ├── test_canonicalization.py
│   ├── test_hashing.py
│   └── test_state_diff.py
│
├── snapshots/
│   ├── test_creation.py
│   ├── test_restore.py
│   ├── test_integrity.py
│   └── test_versioning.py
│
└── branching/
    ├── test_isolation.py
    ├── test_perturbations.py
    ├── test_lineage.py
    ├── test_budget.py
    └── test_branch_execution.py
```

---

# 161. Minimum Implementation Configuration

```yaml
snapshot:
  enabled: true

  schema_version: "1.0"

  serializer:
    type: json

  integrity:
    hash_algorithm: sha256

  isolation:
    mode: full_copy

  max_per_execution: 5
  max_per_experiment: 500


branching:
  enabled: true

  max_branches_per_snapshot: 5
  max_branches_per_execution: 10
  max_branches_per_experiment: 500

  nested_branches: false
  max_depth: 1

  perturbations:
    enabled:
      - TOOL_RESPONSE
      - TOOL_TIMEOUT
      - PERMISSION
      - STATE
```

---

# 162. Definition of Done

The State Snapshot & Branching subsystem is complete enough for the first research experiment when:

* [ ] Environment state has an explicit schema.
* [ ] State ownership is defined.
* [ ] Relevant state can be canonicalized.
* [ ] State hashes can be calculated.
* [ ] Interesting states can be detected.
* [ ] Snapshot compatibility can be checked.
* [ ] Valid states can be serialized.
* [ ] Snapshots can be persisted.
* [ ] Snapshot integrity can be verified.
* [ ] Snapshots can be restored.
* [ ] Restored state matches the captured state.
* [ ] Snapshot schema versions are validated.
* [ ] Branches can be created.
* [ ] Branches can be restored from snapshots.
* [ ] Branches are isolated from parents.
* [ ] Branches are isolated from siblings.
* [ ] Perturbations can be applied.
* [ ] Perturbations are recorded.
* [ ] Branch lineage is preserved.
* [ ] Branch execution can be completed.
* [ ] Branch costs are measured.
* [ ] Snapshot costs are measured.
* [ ] Restore costs are measured.
* [ ] Branch outcomes are evaluated using invariants.
* [ ] Snapshot failures are separated from agent failures.
* [ ] Branch isolation failures are detectable.
* [ ] Budget limits are enforced.
* [ ] Replay can reproduce a branch under documented conditions.
* [ ] Branching can be compared experimentally against independent execution.

---

# 163. Final Architecture

The final State Snapshot & Branching architecture is:

```text
                       AGENT EXECUTION
                              │
                              ▼
                         Trajectory
                              │
                              ▼
                    ┌───────────────────┐
                    │ State Extraction  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Interesting State │
                    │     Detector      │
                    └─────────┬─────────┘
                              │
                         Interesting
                              │
                              ▼
                    ┌───────────────────┐
                    │ Snapshot Manager  │
                    └─────────┬─────────┘
                              │
                    Snapshot Compatibility
                              │
                              ▼
                    ┌───────────────────┐
                    │  Snapshot Store   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Branch Candidates │
                    └─────────┬─────────┘
                              │
                         Budget Check
                              │
                              ▼
                    ┌───────────────────┐
                    │ Branch Selection  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Restore State   │
                    └─────────┬─────────┘
                              │
                         Verify State
                              │
                              ▼
                    ┌───────────────────┐
                    │ Apply Perturbation│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Branch Execution  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Invariant Engine  │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                  PASS                FAILURE
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       Branch Evidence
                              │
                              ▼
                     Cost + Lineage + Result
```

---

# 164. Final Design Principles

The State Snapshot & Branching subsystem shall follow these principles:

1. **Snapshot explicit execution/environment state, not assumed LLM internal state.**
2. **A state must be valid before it can be snapshotted.**
3. **An interesting state is not automatically snapshot-compatible.**
4. **Every snapshot has provenance and integrity metadata.**
5. **Restoration must be independently verified.**
6. **Branches must be isolated from their parent and siblings.**
7. **Every perturbation must be explicit and reproducible.**
8. **Branching overhead must be measured.**
9. **Snapshot and restore costs must be included in the evaluation budget.**
10. **Branching must not be assumed to be cheaper than independent execution.**
11. **Evaluator failures must be distinguished from agent failures.**
12. **Branch lineage must remain traceable from scenario to failure.**
13. **Nested branching is disabled by default.**
14. **Full-copy isolation is preferred for the initial prototype because correctness is easier to verify.**
15. **Adaptive branch selection should remain separable from adaptive scenario selection.**
16. **Hidden holdout states and results must remain isolated.**
17. **A branch result is evidence only when the snapshot, restore, perturbation, and execution are valid.**
18. **All claims about branching efficiency must come from measured experiments.**

---

# 165. Final Specification Boundary

The subsystem can be summarized as:

$$
\boxed{
Trajectory
\rightarrow
Interesting\ State
\rightarrow
Snapshot
\rightarrow
Restore
\rightarrow
Perturb
\rightarrow
Branch
\rightarrow
Evaluate
}
$$

with the experimental cost model:

$$
\boxed{
C_{branching}
=
C_{prefix}
+
C_{snapshot}
+
\sum_i
(C_{restore_i}
+
C_{perturbation_i}
+
C_{continuation_i})
+
C_{analysis}
+
C_{verification}
}
$$

and the comparison baseline:

$$
\boxed{
C_{independent}
=
\sum_i
C_{full\ execution_i}
}
$$

The research system must empirically determine whether:

$$
C_{branching} < C_{independent}
$$

and, more importantly, whether any cost advantage is accompanied by **valid and useful failure discovery**.

The actual contribution is therefore not “we can copy a state and run it twice.” The contribution is a controlled experimental mechanism for **reusing validated intermediate agent-environment states to explore alternative security-relevant continuations under a fixed evaluation budget, while preserving isolation, provenance, reproducibility, and measurable cost accounting.**
