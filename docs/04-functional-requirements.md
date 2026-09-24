# Functional Requirements

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** FR-01
**Document Type:** Functional Requirements Specification
**Version:** 1.0
**Status:** Draft for Implementation
**Related Documents:**

* Project Specification
* Research Questions & Success Criteria
* System Architecture

---

# 1. Purpose

This document defines the **functional requirements** of the Budget-Constrained Adaptive Security Evaluation of AI Agents platform.

The requirements describe what the system must actually do during an evaluation experiment, from generating candidate scenarios through adaptive selection, controlled agent execution, trajectory analysis, state-based branching, failure detection, validation, reproducibility analysis, metamorphic testing, hidden-holdout evaluation, and result generation.

The requirements are intentionally implementation-oriented so that each requirement can be converted into:

* a software component,
* an interface,
* a test case,
* an acceptance criterion,
* or an experiment-level validation condition.

The system is a **research prototype**, not a production security certification platform.

---

# 2. System Functional Objective

The system shall evaluate an AI agent under a fixed and explicitly measured evaluation budget and determine whether adaptive evaluation techniques can discover and validate security and reliability failures more efficiently than predefined baselines.

The functional loop is:

```text
Generate Candidates
        ↓
Build Candidate Pool
        ↓
Select Candidate
        ↓
Execute Agent
        ↓
Capture Trajectory
        ↓
Analyze Intermediate States
        ↓
Identify Interesting State
        ↓
Create Snapshot
        ↓
Generate Branches
        ↓
Execute Branches
        ↓
Evaluate Invariants
        ↓
Detect Failures
        ↓
Classify & Cluster Failures
        ↓
Replay / Reproduce
        ↓
Metamorphic Validation
        ↓
Hidden-Holdout Evaluation
        ↓
Calculate Metrics
        ↓
Update Adaptive Selection
        ↓
Select Next Candidate
```

---

# 3. Requirement Conventions

Each functional requirement has the following structure:

| Field               | Meaning                                     |
| ------------------- | ------------------------------------------- |
| ID                  | Unique requirement identifier               |
| Requirement         | Required system behavior                    |
| Inputs              | Data required by the function               |
| Outputs             | Data produced                               |
| Preconditions       | Conditions that must exist before execution |
| Acceptance Criteria | Conditions used to verify implementation    |

Requirement priority:

* **MUST**: required for the core research system.
* **SHOULD**: required for a complete experimental implementation but can be temporarily stubbed during early development.
* **MAY**: optional extension.

---

# 4. Experiment Management Requirements

## FR-EXP-001: Create Experiment

**Priority:** MUST

The system shall allow a researcher to create an evaluation experiment with a unique experiment identifier.

The experiment configuration shall contain at minimum:

```yaml
experiment_id:
agent_id:
agent_version:
model:
task_set:
environment:
tool_configuration:
policy_configuration:
selection_policy:
budget:
random_seed:
evaluation_mode:
branching_enabled:
metamorphic_testing_enabled:
holdout_enabled:
reproducibility_enabled:
```

### Inputs

* Experiment configuration.

### Outputs

* Unique experiment ID.
* Persisted experiment configuration.

### Acceptance Criteria

* An experiment can be created without manually editing database records.
* The configuration is persisted before execution begins.
* The experiment ID uniquely identifies all resulting artifacts.

---

## FR-EXP-002: Load Experiment Configuration

The system shall load a previously created experiment configuration and reconstruct the required evaluation components.

### Acceptance Criteria

A previously saved experiment shall be executable without manually recreating its configuration.

---

## FR-EXP-003: Validate Experiment Configuration

The system shall validate the experiment configuration before execution.

Validation shall detect at minimum:

* missing agent configuration,
* missing task source,
* invalid budget,
* invalid selection policy,
* invalid environment configuration,
* unavailable tool definitions,
* incompatible branching configuration,
* missing random seed when deterministic reproduction is required,
* invalid holdout configuration.

### Acceptance Criteria

An invalid experiment shall fail before agent execution begins and provide a machine-readable validation error.

---

## FR-EXP-004: Start Experiment

The system shall initialize all experiment components and begin evaluation according to the configured execution policy.

Initialization shall include:

1. configuration loading,
2. random seed initialization,
3. budget initialization,
4. environment initialization,
5. candidate pool initialization,
6. metric initialization,
7. experiment logging initialization.

---

## FR-EXP-005: Resume Experiment

**Priority:** SHOULD

The system should allow an interrupted experiment to resume from its latest valid checkpoint.

A resumed experiment shall preserve:

* consumed budget,
* evaluated candidates,
* candidate scores,
* random seed state where supported,
* failure records,
* snapshots,
* branches,
* validation results,
* experiment lineage.

---

## FR-EXP-006: Terminate Experiment

The system shall terminate evaluation when any configured stopping condition is reached.

Possible stopping conditions include:

* evaluation budget exhausted,
* maximum number of executions reached,
* maximum number of validated failures reached,
* maximum experiment duration,
* candidate pool exhausted,
* unrecoverable experiment error.

The termination reason shall be recorded.

---

# 5. Budget Management Requirements

## FR-BUD-001: Initialize Evaluation Budget

The system shall initialize a measurable evaluation budget before candidate execution begins.

The budget shall support at least one primary cost unit, such as:

* execution count,
* model calls,
* generated tokens,
* estimated monetary cost,
* compute time.

The implementation should support multiple cost dimensions where available.

---

## FR-BUD-002: Track Total Evaluation Cost

The system shall maintain cumulative evaluation cost.

The cost model shall support:

```text
C_total =
C_generation
+ C_execution
+ C_branch
+ C_snapshot
+ C_restore
+ C_analysis
+ C_verification
```

Each component shall be recorded independently when measurable.

---

## FR-BUD-003: Track Candidate Cost

Before selecting a candidate where possible, the system shall estimate its expected evaluation cost.

The estimate may consider:

* expected number of agent steps,
* expected tool calls,
* expected model calls,
* expected branch count,
* snapshot creation cost,
* restore cost.

---

## FR-BUD-004: Reserve Budget

The system shall prevent a candidate from being selected when executing it would exceed the remaining allowed budget.

Where exact cost is unknown, the system shall use the configured estimation policy.

---

## FR-BUD-005: Charge Actual Cost

After execution, the system shall replace or reconcile estimated cost with measured cost where measurement is available.

---

## FR-BUD-006: Prevent Budget Bypass

No execution path shall bypass the centralized budget manager.

This includes:

* normal execution,
* branch execution,
* replay,
* metamorphic execution,
* holdout execution,
* validation execution.

---

## FR-BUD-007: Record Budget Events

Every budget-consuming operation shall generate an auditable budget event containing:

```text
experiment_id
operation_id
operation_type
estimated_cost
actual_cost
budget_before
budget_after
timestamp
```

---

# 6. Candidate Test Generation Requirements

## FR-GEN-001: Generate Seed Tasks

The system shall generate or load initial evaluation tasks.

Tasks shall contain sufficient information to execute an agent scenario.

A task may include:

```yaml
task_id:
task_description:
goal:
initial_state:
available_tools:
security_context:
expected_behavior:
invariants:
difficulty:
tags:
```

---

## FR-GEN-002: Generate Security Scenarios

The system shall support generation of security-oriented scenarios involving relevant agent behaviors such as:

* unauthorized actions,
* unsafe tool use,
* policy bypass,
* privilege boundary violations,
* sensitive-data handling,
* malicious or adversarial inputs,
* unsafe action sequences,
* tool misuse.

The exact scenario categories shall be configurable.

---

## FR-GEN-003: Generate Reliability Scenarios

The system shall support scenarios designed to expose reliability failures such as:

* inconsistent behavior,
* incorrect state transitions,
* invalid tool sequencing,
* failure recovery problems,
* state-dependent failures,
* repeated execution instability.

---

## FR-GEN-004: Generate Perturbations

The system shall generate controlled perturbations of selected scenarios or states.

Perturbations may modify:

* input parameters,
* tool responses,
* environmental state,
* task context,
* timing/fault conditions,
* selected action constraints.

Every perturbation shall have a unique identifier.

---

## FR-GEN-005: Generate Candidate Pool

The system shall maintain a candidate pool containing unevaluated candidate scenarios.

Each candidate shall contain:

```text
candidate_id
parent_candidate_id
scenario_definition
generation_method
estimated_cost
novelty_features
risk_features
priority_features
creation_seed
status
```

---

## FR-GEN-006: Track Candidate Lineage

When a candidate is generated from another candidate or state, the system shall preserve its parent-child relationship.

This shall allow the system to determine whether a discovered failure originated from:

* a seed task,
* an adaptive mutation,
* a state branch,
* a metamorphic transformation,
* a failure-driven exploration strategy.

---

# 7. Adaptive Selection Requirements

## FR-SEL-001: Select Next Candidate

The system shall select the next candidate from the available candidate pool using the configured selection policy.

The selection mechanism shall consider the configured acquisition components.

Conceptually:

```text
Acquisition Score =
Expected Yield
+ Exploration Value
+ Novelty Value
+ Severity Value
- Cost Penalty
```

---

## FR-SEL-002: Support Selection Policies

The system shall support pluggable selection policies.

The initial implementation shall support at least:

1. Random selection.
2. Uniform selection.
3. Adaptive selection.

---

## FR-SEL-003: Support Exploration

The adaptive selector shall support exploration of candidates that have limited historical evaluation information.

---

## FR-SEL-004: Support Exploitation

The adaptive selector shall support prioritizing candidates associated with previously productive regions of the evaluation space.

Productivity may be based on observed:

* invariant violations,
* failures,
* failure severity,
* novel failure signatures,
* useful intermediate states.

---

## FR-SEL-005: Support Novelty

The adaptive selector shall calculate or approximate candidate novelty based on configurable candidate features.

Novelty may consider:

* scenario features,
* tool sequence features,
* state features,
* failure signatures,
* perturbation type,
* trajectory characteristics.

---

## FR-SEL-006: Account for Cost

The adaptive selector shall incorporate evaluation cost when the configured acquisition policy supports cost-aware selection.

The system shall not claim cost-aware optimization if cost is not actually included in the selection calculation.

---

## FR-SEL-007: Support Variance-Aware Selection

**Priority:** SHOULD

The selection framework shall support empirical reward variance.

If UCB-V is implemented, the system shall maintain empirical reward variance and use it in the UCB-V calculation.

The system shall not label a heuristic as **UCB-V** unless the implementation actually uses the required empirical variance information.

---

## FR-SEL-008: Record Selection Decision

For every selected candidate, the system shall record:

```text
candidate_id
selection_policy
selection_score
component_scores
estimated_cost
remaining_budget
selection_rank
selection_timestamp
selection_seed
```

This shall allow researchers to reconstruct why a candidate was selected.

---

## FR-SEL-009: Update Selection Statistics

After candidate evaluation, the adaptive selector shall update its statistics using the observed evaluation result.

Possible observations include:

* failure discovered,
* failure severity,
* novel failure,
* invariant violation,
* branch yield,
* reproduction result,
* cost consumed.

---

# 8. Agent Execution Requirements

## FR-AGT-001: Execute Agent Task

The system shall execute the configured AI agent against a selected task in the controlled evaluation environment.

---

## FR-AGT-002: Support Agent Adapter

The system shall expose a standard agent adapter interface.

Conceptually:

```python
class AgentAdapter:
    def initialize(...)
    def execute(...)
    def reset(...)
    def get_metadata(...)
```

The evaluation engine shall not depend directly on one specific LLM provider.

---

## FR-AGT-003: Provide Agent Context

The agent execution environment shall provide the configured:

* task,
* instructions,
* context,
* memory,
* available tools,
* policy constraints,
* environment state.

---

## FR-AGT-004: Enforce Tool Access Through Tool Gateway

Agent tool calls shall pass through the controlled Tool Gateway.

The agent shall not directly access external tools or services during controlled evaluation.

---

## FR-AGT-005: Enforce Capability Restrictions

The environment shall enforce configured agent capabilities.

An attempted operation shall be evaluated against the configured capability and policy rules before execution.

---

## FR-AGT-006: Capture Tool Calls

The system shall capture each tool invocation.

Each tool event shall contain at minimum:

```text
tool_call_id
tool_name
arguments
agent_step
policy_decision
execution_result
timestamp
```

Sensitive fields shall follow the configured redaction policy.

---

## FR-AGT-007: Handle Agent Failure

The system shall capture agent execution failures without corrupting the experiment database.

Failure types shall distinguish, where possible:

* agent error,
* environment error,
* tool error,
* timeout,
* policy denial,
* evaluator error.

---

## FR-AGT-008: Enforce Execution Limits

The system shall enforce configured limits such as:

* maximum agent steps,
* maximum tool calls,
* maximum execution time,
* maximum model calls,
* maximum generated tokens where measurable.

---

# 9. Controlled Environment Requirements

## FR-ENV-001: Initialize Environment

The system shall create an isolated environment for each independent evaluation execution.

---

## FR-ENV-002: Maintain Environment State

The environment shall maintain explicit state required to reproduce the scenario.

State may include:

```text
database state
user/account state
permissions
tool state
external service state
task state
fault configuration
policy state
```

---

## FR-ENV-003: Tool Gateway

The Tool Gateway shall:

1. receive agent tool requests,
2. validate the request,
3. identify the requested tool,
4. forward the request to the controlled tool implementation,
5. capture the response,
6. record the security decision,
7. return the result to the agent.

---

## FR-ENV-004: Policy Engine

The Policy Engine shall evaluate whether an agent action is allowed under the configured policy.

The decision shall be recorded as:

```text
allowed
denied
requires_review
error
```

where applicable.

---

## FR-ENV-005: Tool Registry

The system shall maintain a registry of available evaluation tools.

Each tool definition shall contain:

```text
tool_id
name
description
input_schema
output_schema
required_capabilities
risk_tags
implementation
```

---

## FR-ENV-006: Fault Injection

The environment shall support controlled fault injection.

Faults may affect:

* tool responses,
* external service responses,
* database operations,
* network-like behavior,
* timing,
* resource availability.

Each injected fault shall be recorded.

---

# 10. Trajectory Collection Requirements

## FR-TRACE-001: Capture Full Observable Trajectory

The system shall capture the observable execution trajectory.

The conceptual representation shall be:

```text
τ = {
    s0, a0, o0,
    s1, a1, o1,
    ...
    sn
}
```

where:

* `s` = observable state,
* `a` = agent action,
* `o` = observation/result.

---

## FR-TRACE-002: Capture State Transitions

The system shall record relevant state transitions after significant agent/environment events.

---

## FR-TRACE-003: Capture Agent Actions

The trace shall record observable agent actions, including:

* tool requests,
* tool parameters,
* task-level decisions where observable,
* termination actions,
* externally visible outputs.

The system shall not require private chain-of-thought.

---

## FR-TRACE-004: Capture Environment Observations

The trace shall record observations returned to the agent.

---

## FR-TRACE-005: Capture Policy Events

The trace shall record policy decisions associated with actions.

---

## FR-TRACE-006: Capture Cost Events

The trace shall associate measurable cost with relevant trajectory events.

---

## FR-TRACE-007: Assign Trace IDs

Every execution shall receive a unique:

```text
experiment_id
execution_id
trajectory_id
```

Every event shall reference the appropriate execution and trajectory.

---

# 11. Interesting-State Detection Requirements

## FR-STATE-001: Extract Observable State

The system shall derive an evaluation state representation from observable execution data.

The representation may include:

* current environment state,
* active task state,
* tool history,
* capability state,
* policy state,
* resource state,
* recent actions,
* invariant-relevant variables.

---

## FR-STATE-002: Detect Interesting States

The system shall identify states that satisfy configured interesting-state criteria.

Examples include:

* unusual tool sequences,
* policy boundary proximity,
* privilege changes,
* sensitive data exposure,
* invariant-relevant transitions,
* high novelty,
* unexpected environment changes,
* failure precursor conditions.

---

## FR-STATE-003: Score State Interestingness

The system shall assign an interestingness score to candidate intermediate states.

The score shall be reproducible from the configured scoring method and observable state data.

---

## FR-STATE-004: Prevent Unbounded Snapshotting

The system shall apply configured rules to prevent snapshotting every intermediate state unnecessarily.

Snapshot decisions may consider:

* interestingness threshold,
* remaining budget,
* maximum snapshots per trajectory,
* state novelty,
* duplicate-state detection.

---

# 12. State Snapshot Requirements

## FR-SNAP-001: Create State Snapshot

The system shall create a snapshot of the controlled execution state at a selected intermediate point.

A snapshot shall contain sufficient information to restore the supported evaluation state.

---

## FR-SNAP-002: Serialize Snapshot

The snapshot system shall serialize environment state using a deterministic or controlled serialization mechanism.

---

## FR-SNAP-003: Store Snapshot Metadata

Each snapshot shall contain:

```text
snapshot_id
experiment_id
trajectory_id
execution_id
parent_state_id
state_hash
snapshot_version
created_at
creation_cost
storage_location
```

---

## FR-SNAP-004: Validate Snapshot

The system shall validate a snapshot after creation.

Validation shall detect:

* serialization failure,
* missing state,
* invalid state references,
* corrupted snapshot,
* inconsistent state hash.

---

## FR-SNAP-005: Restore Snapshot

The system shall restore a valid snapshot into a new isolated execution context.

---

## FR-SNAP-006: Maintain Snapshot Isolation

Restoring a snapshot for one branch shall not modify the source execution or another branch.

---

## FR-SNAP-007: Distinguish Environment State from Model Cache

The implementation shall explicitly distinguish:

```text
Environment / Execution State Snapshot
```

from:

```text
LLM KV-Cache Snapshot
```

The baseline system shall not assume that LLM KV-cache restoration is available.

---

# 13. Branching Requirements

## FR-BRN-001: Create Branch

The system shall create a new evaluation branch from a valid snapshot.

A branch shall contain:

```text
branch_id
parent_snapshot_id
parent_execution_id
branch_configuration
perturbation_id
branch_seed
status
```

---

## FR-BRN-002: Generate Branch Perturbations

The system shall generate one or more controlled perturbations from the selected state.

---

## FR-BRN-003: Restore Parent State

Before branch execution, the system shall restore the branch's parent snapshot.

---

## FR-BRN-004: Apply Perturbation

The system shall apply the configured perturbation after restoring the parent state and before continuing branch execution.

---

## FR-BRN-005: Execute Branch

The system shall execute the agent/environment from the restored state under the branch configuration.

---

## FR-BRN-006: Isolate Branches

Branches originating from the same snapshot shall execute independently.

A state mutation in one branch shall not affect another branch.

---

## FR-BRN-007: Maintain Branch Lineage

The system shall maintain:

```text
seed task
    ↓
execution
    ↓
trajectory
    ↓
state
    ↓
snapshot
    ↓
branch
    ↓
perturbation
    ↓
branch execution
    ↓
failure
```

This lineage shall be queryable.

---

## FR-BRN-008: Track Branching Cost

The system shall measure or estimate:

* snapshot cost,
* restore cost,
* branch creation cost,
* branch execution cost,
* analysis cost.

---

## FR-BRN-009: Compare Branching Against Independent Execution

The system shall preserve enough information to calculate whether branching reduced redundant evaluation work relative to independent execution.

---

# 14. Invariant Management Requirements

## FR-INV-001: Register Invariant

The system shall allow researchers to register executable evaluation invariants.

An invariant shall contain:

```text
invariant_id
name
description
category
scope
evaluation_function
severity
version
```

---

## FR-INV-002: Support Invariant Categories

The invariant framework shall support categories such as:

* security,
* authorization,
* privacy,
* tool safety,
* state consistency,
* reliability,
* policy compliance,
* resource constraints.

---

## FR-INV-003: Evaluate Invariant

The system shall evaluate applicable invariants against:

* execution state,
* trajectory,
* action,
* tool result,
* final state,
* branch state.

---

## FR-INV-004: Record Invariant Evidence

Each evaluation shall record evidence sufficient to determine why the invariant passed or failed.

Evidence shall reference observable execution data.

---

## FR-INV-005: Version Invariants

Invariant definitions shall be versioned.

Changing an invariant shall not silently change the interpretation of historical experiment results.

---

# 15. Failure Detection Requirements

## FR-FAIL-001: Detect Failure

The system shall create a failure record when an executable evaluation condition is violated.

A failure shall not be created solely because the agent behaved differently from an expected textual response.

---

## FR-FAIL-002: Create Failure Record

A failure record shall contain at minimum:

```text
failure_id
experiment_id
execution_id
trajectory_id
branch_id
invariant_id
failure_type
severity
evidence
state_reference
action_reference
timestamp
```

---

## FR-FAIL-003: Capture Failure Evidence

The system shall associate each failure with observable evidence.

Evidence may include:

* violating state,
* action,
* tool call,
* tool response,
* policy decision,
* invariant result,
* trajectory segment,
* environment state.

---

## FR-FAIL-004: Classify Failure

The system shall assign a configurable failure category.

Examples:

```text
authorization_violation
unsafe_tool_use
policy_bypass
sensitive_data_exposure
state_inconsistency
reliability_failure
unexpected_action
resource_violation
```

---

## FR-FAIL-005: Assign Severity

The system shall assign a configured severity level based on the invariant or classification policy.

The severity mechanism shall be documented and deterministic where possible.

---

## FR-FAIL-006: Distinguish Discovery from Validation

A first observed violation shall be recorded as a **discovered failure candidate** until the configured validation process confirms it.

The system shall distinguish:

```text
Discovered
Validated
Reproduced
Generalized
```

rather than treating every initial observation as a confirmed failure.

---

# 16. Failure Signature and Clustering Requirements

## FR-CLUST-001: Generate Failure Signature

The system shall generate a normalized failure signature from observable failure characteristics.

The signature may use:

* invariant ID,
* failure type,
* action sequence,
* tool sequence,
* state features,
* perturbation characteristics,
* relevant environment state.

---

## FR-CLUST-002: Normalize Failure Records

The system shall normalize equivalent failure records to reduce duplicate representation.

---

## FR-CLUST-003: Calculate Failure Similarity

The system shall calculate configurable similarity between failure records.

---

## FR-CLUST-004: Create Failure Families

The system shall group sufficiently similar failures into failure families.

Each family shall contain:

```text
family_id
representative_failure
member_failures
signature
family_features
creation_method
confidence
```

---

## FR-CLUST-005: Distinguish Unique Failures

The system shall allow genuinely different failures to remain separate even when they violate the same high-level invariant.

---

## FR-CLUST-006: Track Family Evolution

When new executions produce related failures, the system shall update the corresponding failure family rather than silently creating duplicate families.

---

# 17. Reproducibility Requirements

## FR-REP-001: Replay Failure

The system shall support replaying a discovered failure under an isolated execution.

---

## FR-REP-002: Reproduce Environment

Replay shall reconstruct the relevant:

* task,
* initial state,
* tool configuration,
* policy configuration,
* perturbation,
* random seed where applicable.

---

## FR-REP-003: Record Replay Result

Each replay shall record:

```text
original_failure_id
replay_id
reproduction_result
environment_match
trajectory_match
invariant_result
cost
```

---

## FR-REP-004: Calculate Reproduction Rate

The system shall calculate reproduction rate for a failure or failure family.

A basic formulation is:

```text
Reproduction Rate =
Successful Reproductions / Valid Replay Attempts
```

---

## FR-REP-005: Classify Stability

The system shall classify observed failures based on configured reproduction thresholds.

The classification shall distinguish, where configured:

* reproducible,
* intermittent,
* non-reproduced,
* insufficient evidence.

Low reproducibility shall not automatically cause the system to discard the failure.

---

# 18. Metamorphic Testing Requirements

## FR-META-001: Register Transformation

The system shall support registered metamorphic transformations.

A transformation shall define:

```text
transformation_id
name
input_constraints
transformation_function
expected_invariant_relation
version
```

---

## FR-META-002: Generate Transformed Task

The system shall generate a transformed version of a valid base task.

---

## FR-META-003: Execute Base Task

The system shall execute the original task and preserve its relevant observable results.

---

## FR-META-004: Execute Transformed Task

The system shall execute the transformed task under controlled conditions.

---

## FR-META-005: Compare Base and Transformed Results

The system shall compare the two executions against the registered metamorphic relation.

---

## FR-META-006: Detect Metamorphic Violation

The system shall create a metamorphic failure record when the expected relation is violated.

The result shall include evidence from both executions.

---

## FR-META-007: Prevent Hard-Coded Metamorphic Results

The system shall derive metamorphic outcomes from actual execution results.

A static `TRUE`, `PASS`, or `Genuine Defect` value shall not be accepted as an implementation of metamorphic evaluation.

---

# 19. Hidden Holdout Requirements

## FR-HOLD-001: Create Holdout Set

The system shall create or load a hidden evaluation set that is isolated from adaptive selection.

---

## FR-HOLD-002: Prevent Training Leakage

The adaptive selector shall not use hidden holdout outcomes during candidate selection before the holdout evaluation phase.

---

## FR-HOLD-003: Execute Holdout

The system shall execute the final evaluation method against hidden scenarios.

---

## FR-HOLD-004: Match Failure Families

The system shall determine whether failures discovered during adaptive evaluation correspond to failures observed in the holdout set.

---

## FR-HOLD-005: Calculate Generalization

The system shall calculate configured generalization metrics.

Possible metrics include:

```text
holdout failure detection rate
family generalization rate
invariant generalization rate
false discovery rate
```

---

## FR-HOLD-006: Preserve Holdout Integrity

Holdout data shall remain inaccessible to the adaptive selection mechanism until the configured evaluation phase.

---

# 20. Metrics Requirements

## FR-MET-001: Calculate Discovery Metrics

The system shall calculate at minimum:

* total executions,
* total failures discovered,
* validated failures,
* unique failure families,
* failures per unit budget.

---

## FR-MET-002: Calculate Efficiency Metrics

The system shall calculate:

```text
Cost per validated failure
Cost per unique failure family
Executions per validated failure
Branching overhead
Snapshot overhead
Restore overhead
```

---

## FR-MET-003: Calculate Reproducibility Metrics

The system shall calculate:

* reproduction rate,
* replay success rate,
* intermittent failure rate,
* validation rate.

---

## FR-MET-004: Calculate Generalization Metrics

The system shall calculate hidden-holdout performance according to the configured evaluation protocol.

---

## FR-MET-005: Calculate Adaptive Selection Metrics

The system shall record:

* candidate selections,
* candidate rewards,
* candidate costs,
* exploration selections,
* exploitation selections,
* novelty-driven selections.

---

## FR-MET-006: Calculate Baseline Comparison Metrics

The system shall calculate equivalent metrics for each configured baseline.

Comparisons shall use equivalent budget definitions.

---

## FR-MET-007: Preserve Raw Measurements

Derived metrics shall not replace raw experimental measurements.

The system shall preserve:

* raw event counts,
* raw execution costs,
* raw failure records,
* raw replay outcomes,
* raw trajectory records.

---

# 21. Baseline Execution Requirements

## FR-BASE-001: Support Random Baseline

The system shall support a random candidate selection baseline.

---

## FR-BASE-002: Support Uniform Baseline

The system shall support a predefined/uniform evaluation strategy.

---

## FR-BASE-003: Support Adaptive Without Branching

The system shall support adaptive selection with state-based branching disabled.

---

## FR-BASE-004: Support Branching Without Adaptive Selection

The system shall support state-based branching using non-adaptive candidate selection.

---

## FR-BASE-005: Support Combined Method

The system shall support the complete proposed evaluation method:

```text
Adaptive Selection + State-Based Branching
```

---

## FR-BASE-006: Maintain Comparable Configuration

Baseline experiments shall preserve equivalent relevant:

* agent configuration,
* task distribution,
* environment,
* invariant definitions,
* budget,
* validation procedure,
* holdout procedure.

Only the intended experimental factor shall change.

---

# 22. Ablation Requirements

## FR-ABL-001: Disable Adaptive Selection

The experiment framework shall allow adaptive selection to be disabled without modifying unrelated components.

---

## FR-ABL-002: Disable Branching

The experiment framework shall allow branching to be disabled.

---

## FR-ABL-003: Disable Novelty

The selection mechanism shall allow novelty contribution to be disabled where supported.

---

## FR-ABL-004: Disable Cost Component

The adaptive selection mechanism shall allow cost-aware selection to be disabled for ablation experiments.

---

## FR-ABL-005: Compare Ablation Results

The system shall store component configuration alongside results so that ablation outcomes can be compared.

---

# 23. Experiment Tracking Requirements

## FR-TRACK-001: Record Configuration

Every experiment shall store its complete configuration.

---

## FR-TRACK-002: Record Software Version

The system shall record the software version or source revision used for the experiment.

---

## FR-TRACK-003: Record Model Metadata

The system shall record relevant model metadata, including:

```text
model identifier
provider
model version
temperature where applicable
generation parameters
```

---

## FR-TRACK-004: Record Random Seeds

The system shall record random seeds for all controlled stochastic components where practical.

---

## FR-TRACK-005: Record Environment Version

The system shall record the environment and tool configuration version.

---

## FR-TRACK-006: Record Invariant Version

The experiment shall record the exact invariant definitions used.

---

## FR-TRACK-007: Record Selection Policy Version

The experiment shall record the exact selection algorithm and configuration.

---

# 24. Data Persistence Requirements

## FR-DATA-001: Persist Experiment Metadata

The system shall persist experiment metadata in structured storage.

---

## FR-DATA-002: Persist Candidate Records

Candidate generation and selection records shall be persisted.

---

## FR-DATA-003: Persist Trajectories

Execution trajectories shall be persisted in a queryable format.

---

## FR-DATA-004: Persist Snapshots

Snapshots shall be stored independently from normal trajectory records.

---

## FR-DATA-005: Persist Branches

Branch lineage and branch execution results shall be persisted.

---

## FR-DATA-006: Persist Failures

Every discovered failure shall be persisted with its evidence and lineage.

---

## FR-DATA-007: Persist Validation Results

Replay, metamorphic, and holdout results shall be persisted.

---

## FR-DATA-008: Maintain Referential Integrity

Records shall maintain valid references between:

```text
Experiment
→ Candidate
→ Execution
→ Trajectory
→ State
→ Snapshot
→ Branch
→ Failure
→ Failure Family
→ Validation
```

---

# 25. Dashboard and Reporting Requirements

## FR-UI-001: Display Experiment Status

The dashboard shall display:

* experiment state,
* elapsed time,
* consumed budget,
* remaining budget,
* execution count.

---

## FR-UI-002: Display Candidate Selection

The dashboard shall display:

* selected candidates,
* selection scores,
* selection policy,
* estimated cost,
* actual cost.

---

## FR-UI-003: Display Trajectory Information

The dashboard shall allow researchers to inspect observable trajectory information.

---

## FR-UI-004: Display State and Branch Lineage

The dashboard shall show the relationship:

```text
Execution → State → Snapshot → Branch → Failure
```

---

## FR-UI-005: Display Failure Families

The dashboard shall show:

* discovered failures,
* validated failures,
* failure families,
* family membership,
* reproduction status,
* severity.

---

## FR-UI-006: Display Reproducibility

The dashboard shall show reproduction results and reproduction rates.

---

## FR-UI-007: Display Metamorphic Results

The dashboard shall show:

* base execution,
* transformed execution,
* expected relation,
* observed relation,
* metamorphic result.

---

## FR-UI-008: Display Holdout Results

The dashboard shall clearly distinguish holdout results from adaptive-training/evaluation results.

---

## FR-UI-009: Display Budget Breakdown

The dashboard shall display the contribution of:

```text
generation
execution
branching
snapshot
restore
analysis
verification
```

to total cost where measured.

---

## FR-UI-010: Prevent Fabricated Results

The dashboard shall display only values derived from stored experiment data.

Illustrative or simulated values must be explicitly labeled as such and shall never appear as actual experiment measurements.

---

# 26. Auditability Requirements

## FR-AUD-001: Record Selection Decisions

Every adaptive selection decision shall be reconstructable from stored data.

---

## FR-AUD-002: Record Failure Evidence

Every failure shall point to the evidence used to detect it.

---

## FR-AUD-003: Record Branch Lineage

Every branch shall identify its source snapshot.

---

## FR-AUD-004: Record Configuration Versions

Results shall be linked to the configuration versions used to produce them.

---

## FR-AUD-005: Preserve Experiment History

Updating configuration for a new experiment shall not overwrite historical experiment configuration.

---

# 27. Error Handling Requirements

## FR-ERR-001: Isolate Execution Errors

An agent execution failure shall not automatically terminate the entire experiment unless configured as fatal.

---

## FR-ERR-002: Isolate Branch Errors

A failed branch shall not corrupt its parent snapshot or sibling branches.

---

## FR-ERR-003: Detect Corrupt Snapshots

The system shall reject corrupted or invalid snapshots before branch execution.

---

## FR-ERR-004: Record Evaluator Errors

Evaluator failures shall be distinguished from agent failures.

For example:

```text
AGENT_FAILURE
TOOL_FAILURE
ENVIRONMENT_FAILURE
SNAPSHOT_FAILURE
RESTORE_FAILURE
INVARIANT_ENGINE_FAILURE
EVALUATOR_FAILURE
```

---

## FR-ERR-005: Continue When Safe

Where the experiment configuration permits recovery, the system shall continue evaluation after recoverable errors.

---

## FR-ERR-006: Mark Invalid Results

If an evaluator error prevents reliable interpretation of an execution, the system shall mark the result invalid rather than treating it as a successful or failed agent evaluation.

---

# 28. Security Boundary Requirements

## FR-SEC-001: Enforce Agent Isolation

The agent shall execute inside the configured evaluation boundary.

---

## FR-SEC-002: Enforce Tool Boundary

All controlled tool calls shall pass through the Tool Gateway.

---

## FR-SEC-003: Enforce Policy Boundary

Tool actions shall be evaluated against the Policy Engine before execution where policy enforcement is configured.

---

## FR-SEC-004: Isolate Experiment State

Independent experiments shall not share mutable environment state unless explicitly configured.

---

## FR-SEC-005: Isolate Holdout Data

Adaptive evaluation components shall not access hidden holdout information before the holdout evaluation phase.

---

## FR-SEC-006: Protect Snapshot Integrity

A branch or agent execution shall not be allowed to modify stored parent snapshots directly.

---

# 29. Configuration Requirements

## FR-CONF-001: Configure Agent

The system shall allow researchers to configure:

* agent adapter,
* model,
* instructions,
* generation parameters,
* context,
* memory behavior.

---

## FR-CONF-002: Configure Environment

The system shall allow configuration of:

* tools,
* tool responses,
* policy rules,
* database state,
* external service mocks,
* fault injection.

---

## FR-CONF-003: Configure Selection

The system shall allow configuration of:

* selection policy,
* exploration coefficient,
* exploitation parameters,
* novelty weighting,
* severity weighting,
* cost weighting,
* candidate limits.

---

## FR-CONF-004: Configure Branching

The system shall allow configuration of:

* interesting-state threshold,
* maximum snapshots,
* maximum branches,
* perturbation strategies,
* branch budget.

---

## FR-CONF-005: Configure Validation

The system shall allow configuration of:

* replay count,
* reproduction thresholds,
* metamorphic transformations,
* holdout size,
* holdout evaluation policy.

---

## FR-CONF-006: Validate Configuration Before Execution

Configuration validation shall occur before the experiment consumes evaluation budget.

---

# 30. API / Internal Interface Requirements

The implementation shall expose clear internal interfaces between major components.

At minimum, the architecture shall support interfaces conceptually equivalent to:

```python
CandidateGenerator
SelectionPolicy
BudgetManager
AgentAdapter
Environment
ToolGateway
PolicyEngine
TrajectoryRecorder
StateAnalyzer
SnapshotManager
BranchingEngine
InvariantEvaluator
FailureDetector
FailureClassifier
FailureClusterer
ReplayManager
MetamorphicEngine
HoldoutEvaluator
MetricsEngine
ExperimentStore
```

Each interface shall have a stable contract so that research components can be replaced independently.

---

# 31. End-to-End Functional Acceptance Test

The implementation shall be considered functionally complete only when it can execute the following end-to-end flow without manually modifying stored results:

```text
1. Create experiment
2. Validate configuration
3. Initialize budget
4. Generate candidate tasks
5. Create candidate pool
6. Select candidate
7. Execute agent
8. Capture trajectory
9. Detect interesting state
10. Create snapshot
11. Generate branch
12. Restore snapshot
13. Apply perturbation
14. Execute branch
15. Evaluate invariants
16. Detect failure
17. Create failure record
18. Generate failure signature
19. Assign failure family
20. Replay failure
21. Calculate reproduction result
22. Execute metamorphic test
23. Evaluate hidden holdout
24. Calculate metrics
25. Update adaptive selection statistics
26. Continue until budget termination
27. Persist final experiment state
28. Generate experiment report
```

---

# 32. Minimum Functional Implementation

The minimum implementation required for the research experiment shall include:

### Required

* Experiment configuration.
* Budget manager.
* Candidate generation.
* Random selection.
* Uniform selection.
* Adaptive selection.
* Agent adapter.
* Controlled environment.
* Tool Gateway.
* Policy Engine.
* Trajectory recorder.
* Observable state extraction.
* Interesting-state detection.
* Environment state snapshotting.
* Snapshot restoration.
* Branch generation.
* Branch isolation.
* Executable invariants.
* Failure detection.
* Failure records.
* Failure signatures.
* Failure clustering.
* Independent replay.
* Reproduction measurement.
* Metamorphic testing.
* Hidden holdout evaluation.
* Metrics engine.
* Experiment persistence.
* Baseline execution.
* Experiment reporting.

### Not required for the initial implementation

* LLM KV-cache snapshotting.
* Production-scale distributed execution.
* Real-world unrestricted external tool access.
* Production security certification.
* Automatic claims of OWASP compliance.
* Unsupported token-cost reduction claims.
* Automatic remediation of discovered agent failures.

---

# 33. Functional Dependency Chain

The functional dependencies shall follow this order:

```text
Experiment
    ↓
Configuration
    ↓
Budget
    ↓
Candidate Generation
    ↓
Candidate Selection
    ↓
Agent Execution
    ↓
Environment + Tools
    ↓
Trajectory
    ↓
State Analysis
    ↓
Snapshot
    ↓
Branching
    ↓
Invariant Evaluation
    ↓
Failure Detection
    ↓
Failure Classification
    ↓
Failure Clustering
    ↓
Reproduction
    ↓
Metamorphic Validation
    ↓
Hidden Holdout
    ↓
Metrics
    ↓
Experiment Results
```

The adaptive selection loop additionally depends on previous evaluation outcomes:

```text
Evaluation Result
       ↓
Reward / Yield / Novelty / Severity / Cost
       ↓
Selection Statistics
       ↓
Candidate Score Update
       ↓
Next Candidate
```

---

# 34. Requirements Traceability

Each major functional requirement shall map to at least one:

* architecture component,
* implementation module,
* test case,
* experimental metric,
* or research question.

Example:

| Requirement Area    | Architecture Component     | Research Purpose |
| ------------------- | -------------------------- | ---------------- |
| Adaptive selection  | Adaptive Selection Layer   | RQ1              |
| Budget accounting   | Budget Manager             | RQ8              |
| State snapshot      | Snapshot Manager           | RQ2              |
| Branching           | Branching Engine           | RQ2              |
| Failure detection   | Invariant & Failure Engine | RQ3              |
| Failure clustering  | Failure Analysis Layer     | RQ5              |
| Replay              | Reproducibility Layer      | RQ4              |
| Metamorphic testing | Metamorphic Engine         | RQ6              |
| Hidden holdout      | Holdout Engine             | RQ7              |
| Baselines           | Experiment Controller      | RQ1/RQ2/RQ9      |
| Metrics             | Metrics Engine             | All RQs          |
| Experiment tracking | Experiment Store           | RQ10             |

---

# 35. Functional Completion Criteria

The Functional Requirements implementation shall be considered complete when:

1. An experiment can be configured entirely from structured configuration.
2. A fixed evaluation budget is enforced.
3. Candidate scenarios can be generated and selected.
4. Multiple selection policies can be compared.
5. The agent can execute inside a controlled environment.
6. Tool access is mediated by the Tool Gateway.
7. Observable trajectories are recorded.
8. Interesting intermediate states can be detected.
9. Environment state can be snapshotted.
10. Snapshots can be restored into isolated branches.
11. Branches can execute controlled perturbations.
12. Executable invariants can identify violations.
13. Failures contain observable evidence.
14. Failures can be grouped into families.
15. Failures can be independently replayed.
16. Reproduction rates can be calculated.
17. Metamorphic relations are actually executed and evaluated.
18. Hidden holdout evaluation is isolated from adaptive selection.
19. Baseline and proposed methods can be executed under comparable budgets.
20. Raw measurements and derived metrics are persisted.
21. Experiment configuration and software metadata are preserved.
22. Results can be reconstructed from stored experiment data.
23. The dashboard/reporting layer displays actual experiment data rather than hard-coded values.
24. The complete evaluation loop can run end-to-end.

---

# 36. Functional Boundary

This specification defines **what the system must do**.

It does not define:

* detailed implementation algorithms,
* database table-level schemas,
* statistical tests,
* exact UI design,
* deployment infrastructure,
* threat-model methodology,
* detailed experimental methodology,
* literature claims,
* final research conclusions.

Those concerns belong in their respective project documents.

The critical implementation boundary is:

> **The evaluator must be capable of producing, observing, validating, and reproducing evidence from actual AI-agent executions under a controlled and explicitly measured budget.**

The system must therefore never substitute:

```text
hard-coded result
```

for:

```text
measured experiment result
```

and must never substitute:

```text
assumed capability
```

for:

```text
implemented and validated capability
```

This distinction is central to the credibility of the research prototype.
