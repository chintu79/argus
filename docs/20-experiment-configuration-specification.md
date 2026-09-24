# Experiment Configuration Specification

**Project:** Budget-Constrained Adaptive Security Evaluation of AI Agents
**Document ID:** CFG-01
**Document Type:** Experiment Configuration Specification
**Status:** Research Prototype Specification
**Version:** 1.0

---

# 1. Purpose

This document defines the complete configuration model for running controlled experiments in the **Budget-Constrained Adaptive Security Evaluation of AI Agents** research prototype.

The configuration system must define, version, validate, and preserve every parameter that can materially affect an experiment.

The configuration controls:

* experiment identity
* research method
* experimental unit
* repetitions
* random seeds
* candidate pool
* scenario generation
* agent configuration
* environment configuration
* tool configuration
* policy configuration
* adaptive selector
* reward definition
* budget
* trajectory collection
* state detection
* snapshotting
* branching
* invariant evaluation
* failure detection
* classification
* clustering
* reproduction
* metamorphic testing
* hidden holdout
* metrics
* statistical analysis
* stopping conditions
* artifact storage
* reproducibility metadata

The central rule is:

> **An experiment must be fully describable by an immutable configuration manifest plus the software and data versions referenced by that manifest.**

---

# 2. Configuration Design Principles

## 2.1 Configuration Is Research Data

Configuration is not merely application setup.

A change to:

* selector weight
* budget
* candidate pool
* invariant
* agent temperature
* branch depth
* reproduction attempts
* clustering threshold
* holdout generation
* reward definition

can change the experimental result.

Therefore, configuration must be versioned and persisted with experiment results.

---

# 3. Configuration Hierarchy

Configuration should be organized into layers.

```text
Global Configuration
        ↓
Environment Configuration
        ↓
Agent Configuration
        ↓
Scenario Configuration
        ↓
Selector Configuration
        ↓
Validation Configuration
        ↓
Experiment Configuration
        ↓
Run Configuration
        ↓
Immutable Experiment Manifest
```

A final experiment configuration should be resolved from these layers before execution begins.

---

# 4. Configuration Sources

The system may load configuration from:

1. YAML files
2. Environment variables
3. CLI overrides
4. Programmatic configuration

Recommended precedence:

```text
Default
   ↓
Base YAML
   ↓
Component YAML
   ↓
Experiment YAML
   ↓
Environment Variables
   ↓
Explicit CLI Override
```

However, after an experiment starts, the resolved configuration becomes immutable.

---

# 5. Configuration Repository Structure

Recommended:

```text
configs/
├── base.yaml
│
├── development.yaml
├── test.yaml
│
├── agents/
│   ├── mock_agent.yaml
│   └── default_agent.yaml
│
├── environments/
│   └── support_environment.yaml
│
├── scenarios/
│   ├── seed.yaml
│   └── generation.yaml
│
├── selectors/
│   ├── random.yaml
│   ├── uniform.yaml
│   ├── ucbv.yaml
│   └── proposed.yaml
│
├── invariants/
│   └── default.yaml
│
├── branching/
│   └── default.yaml
│
├── validation/
│   ├── reproduction.yaml
│   └── metamorphic.yaml
│
├── holdout/
│   └── default.yaml
│
├── metrics/
│   └── default.yaml
│
├── statistics/
│   └── default.yaml
│
└── experiments/
    ├── baseline_random.yaml
    ├── baseline_uniform.yaml
    ├── baseline_ucbv.yaml
    ├── adaptive_main.yaml
    └── ablation_branching.yaml
```

---

# 6. Top-Level Experiment Configuration

A complete experiment configuration should have the following structure:

```yaml
experiment:
  identity: {}
  research: {}
  repetitions: {}
  seeds: {}

agent: {}
environment: {}
scenario_pool: {}
selector: {}
budget: {}
execution: {}
trajectory: {}
state_analysis: {}
snapshot: {}
branching: {}
invariants: {}
failure_detection: {}
classification: {}
clustering: {}
reproduction: {}
metamorphic: {}
holdout: {}
metrics: {}
statistics: {}
stopping: {}
artifacts: {}
tracking: {}
```

---

# 7. Experiment Identity

Example:

```yaml
experiment:
  identity:
    name: "adaptive_security_evaluation_v1"
    description: "Comparison of adaptive and non-adaptive AI-agent security evaluation"
    version: "1.0"
    owner: "researcher"
    tags:
      - agentic-ai
      - security
      - adaptive-evaluation
```

Required fields:

| Field       | Type   | Required |
| ----------- | ------ | -------: |
| name        | string |      Yes |
| description | string |      Yes |
| version     | string |      Yes |
| owner       | string |      Yes |
| tags        | list   |       No |

The identity block must not contain secrets.

---

# 8. Research Configuration

The experiment must explicitly state which research question or hypothesis it addresses.

Example:

```yaml
experiment:
  research:
    research_questions:
      - RQ1
      - RQ2
      - RQ3

    hypotheses:
      - H1
      - H2
      - H3

    primary_objective: "Compare adaptive failure discovery efficiency"
```

Supported identifiers from the research design include:

```text
RQ1  Adaptive failure discovery
RQ2  State-based branching efficiency
RQ3  Failure discovery quality
RQ4  Failure reproducibility
RQ5  Failure family quality
RQ6  Metamorphic robustness
RQ7  Hidden-holdout generalization
RQ8  Budget efficiency
RQ9  Component contribution
RQ10 Evaluator reliability
```

---

# 9. Experimental Method

The configuration must explicitly identify the method being evaluated.

Supported initial methods:

```text
RANDOM
UNIFORM
UCBV
PROPOSED_ADAPTIVE
```

Extended methods may include:

```text
COST_AWARE_UCBV
NOVELTY_AUGMENTED_UCBV
BRANCH_AWARE_ADAPTIVE
```

Example:

```yaml
experiment:
  research:
    method: "PROPOSED_ADAPTIVE"
```

The method name must correspond to a registered selector implementation.

---

# 10. Experimental Repetitions

The experiment must specify the number of independent runs.

Example:

```yaml
experiment:
  repetitions:
    count: 20
    independent: true
    matched_seed_set: true
```

The recommended primary experiment design uses:

```text
20 independent runs per method
```

This is a methodological recommendation, not a mandatory universal constant.

---

# 11. Random Seed Configuration

Randomness must be explicitly controlled.

Example:

```yaml
experiment:
  seeds:
    strategy: "FIXED_SET"

    values:
      - 11
      - 22
      - 33
      - 44
      - 55
      - 66
      - 77
      - 88
      - 99
      - 110
```

For a 20-run experiment, the list should contain 20 seeds.

---

# 12. Randomness Scope

Separate random streams should be supported.

```yaml
experiment:
  seeds:
    strategy: "DERIVED"

    scopes:
      scenario_generation: true
      scenario_mutation: true
      agent: true
      environment_faults: true
      selector: true
      validation: true
```

Recommended derived-seed model:

```text
master_seed
    |
    +-- scenario_seed
    +-- mutation_seed
    +-- agent_seed
    +-- environment_seed
    +-- selector_seed
    +-- validation_seed
```

Every derived seed must be recorded.

---

# 13. Candidate Pool Configuration

The main experiment should use a frozen candidate pool.

Example:

```yaml
scenario_pool:
  id: "security_pool_v1"
  version: "1.0"

  source:
    type: "STATIC"

  frozen: true

  size:
    minimum: 100
    target: 250
    maximum: 500
```

The recommended prototype range is:

```text
100–500 candidates
```

The actual experiment must record the exact number.

---

# 14. Candidate Pool Composition

Example:

```yaml
scenario_pool:
  composition:
    categories:
      AUTHORIZATION: 20
      DATA_EXPOSURE: 20
      TOOL_SECURITY: 20
      SEQUENCE_ATTACK: 20
      ROBUSTNESS: 20
      FAULT_TOLERANCE: 20
      STATE_MANIPULATION: 20
      RESOURCE_ABUSE: 20
      RECOVERY: 20
      BRANCH_ATTACK: 20
```

Composition must be stored as part of the experiment manifest.

---

# 15. Scenario Generation Configuration

Example:

```yaml
scenario_pool:
  generation:
    enabled: true
    generator_version: "scenario_gen_v1"

    difficulty:
      minimum: 1
      maximum: 5

    risk_levels:
      - LOW
      - MEDIUM
      - HIGH
      - CRITICAL

    mutations:
      enabled: true
      max_mutations_per_parent: 5
```

---

# 16. Scenario Mutation Configuration

Example:

```yaml
scenario_pool:
  generation:
    mutation_operators:
      - M01
      - M02
      - M03
      - M04
      - M05
      - M06
```

Mutation operators should be versioned.

A mutation configuration must record:

```text
operator_id
operator_version
parameters
seed
parent_scenario
generated_scenario
```

---

# 17. Agent Configuration

Example:

```yaml
agent:
  id: "agent_001"
  adapter: "MOCK_AGENT"
  version: "agent_v1"

  model:
    provider: "mock"
    model_name: "deterministic-agent"

  generation:
    temperature: 0.0
    max_tokens: 512
    top_p: 1.0

  context:
    max_context_tokens: 4096

  memory:
    enabled: false
    reset_between_executions: true

  capabilities:
    - customer.read
    - account.read
    - transaction.read
    - ticket.read
    - ticket.update
    - notification.send
```

For a real LLM adapter, provider-specific parameters may be added without changing the `AgentAdapter` interface.

---

# 18. Agent Determinism

Example:

```yaml
agent:
  determinism:
    enabled: true
    seed_supported: true
    seed: null
```

If the model/provider does not guarantee deterministic output, the configuration must record:

```yaml
agent:
  determinism:
    enabled: false
    stochastic: true
```

The experiment must not falsely label stochastic behavior as deterministic merely because a seed was supplied.

---

# 19. Agent Reset Configuration

```yaml
agent:
  reset:
    between_candidates: true
    between_runs: true
    between_reproduction_attempts: true
    between_metamorphic_cases: true
```

Memory persistence must be explicit.

---

# 20. Environment Configuration

Example:

```yaml
environment:
  id: "enterprise_support_sim"
  version: "env_v1"

  mode: "CONTROLLED_SIMULATION"

  state:
    reset_between_executions: true
    persistent_shared_state: false

  identity:
    enabled: true

  authorization:
    enabled: true

  policy:
    version: "policy_v1"

  faults:
    enabled: true

  snapshots:
    enabled: true
```

---

# 21. Environment State Configuration

The environment must support:

```yaml
environment:
  state:
    components:
      - identity_state
      - authorization_state
      - data_state
      - tool_state
      - service_state
      - policy_state
      - task_state
      - fault_state
      - resource_state
```

This corresponds to the project environment-state model:

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

---

# 22. Tool Configuration

Example:

```yaml
environment:
  tools:
    enabled:
      - customer.lookup
      - account.lookup
      - transaction.lookup
      - ticket.search
      - ticket.update
      - notification.send
      - database.write

    gateway:
      enabled: true

    policy_interception:
      enabled: true

    trace_all_requests: true
    trace_all_responses: true
```

The agent must not bypass the Tool Gateway.

---

# 23. Policy Configuration

Example:

```yaml
environment:
  policy:
    version: "policy_v1"

    decisions:
      - ALLOW
      - DENY
      - REVIEW
      - ERROR

    enforcement:
      enabled: true

    audit:
      enabled: true
```

---

# 24. Fault Injection Configuration

Example:

```yaml
environment:
  faults:
    enabled: true

    allowed_types:
      - TOOL_TIMEOUT
      - MALFORMED_RESPONSE
      - SERVICE_UNAVAILABLE
      - PARTIAL_FAILURE
      - DELAY
      - STATE_INCONSISTENCY

    maximum_injections_per_execution: 3
```

Fault injection must remain controlled and reproducible.

---

# 25. Selector Configuration

The selector configuration must identify:

```yaml
selector:
  method: "PROPOSED_ADAPTIVE"
  version: "selector_v1"
```

---

# 26. Random Selector

```yaml
selector:
  method: "RANDOM"

  random:
    replacement: false
    seed_scope: "RUN"
```

---

# 27. Uniform Selector

```yaml
selector:
  method: "UNIFORM"

  uniform:
    ordering: "FROZEN_POOL_ORDER"
    replacement: false
```

---

# 28. UCB-V Configuration

Example:

```yaml
selector:
  method: "UCBV"

  ucbv:
    reward_type: "BINARY"
    bound_b: 1.0
    initialization:
      strategy: "ONE_SAMPLE_EACH"

    variance:
      estimator: "EMPIRICAL"
      method: "WELFORD"

    exploration:
      logarithm: "NATURAL_LOG"
```

The UCB-V implementation must actually use empirical variance.

If variance is not used, the implementation must not be labelled UCB-V.

---

# 29. UCB-V Formula Configuration

The implementation corresponds to:

```text
UCBV_i(t)
=
μ̂_i
+
sqrt(
    (2 v̂_i ln(t)) / n_i
)
+
(3 b ln(t)) / n_i
```

where:

```text
μ̂_i = empirical mean reward
v̂_i = empirical variance
n_i = number of observations
b = reward bound
```

For binary rewards:

```text
b = 1
```

unless another reward scale is explicitly defined.

---

# 30. Proposed Adaptive Selector

Example:

```yaml
selector:
  method: "PROPOSED_ADAPTIVE"

  acquisition:
    base: "UCBV"

    components:
      novelty:
        enabled: true
        weight: 0.30

      branch_potential:
        enabled: true
        weight: 0.20

      severity:
        enabled: false
        weight: 0.00

      cost:
        enabled: true
        weight: 0.20
```

Conceptual score:

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

Weights must be recorded in the manifest.

---

# 31. Selector Information Boundary

Configuration must explicitly define the allowed selector information.

```yaml
selector:
  information_boundary:
    allowed:
      - previous_rewards
      - candidate_statistics
      - empirical_variance
      - candidate_cost
      - coverage_state
      - validated_failure_history
      - novelty
      - branch_potential
      - budget_remaining

    forbidden:
      - holdout_outcomes
      - future_execution_results
      - future_failure_labels
      - future_cluster_assignments
      - post_hoc_validation_results
      - private_agent_reasoning
```

The forbidden list should also be enforced through the `SelectionContext` implementation.

---

# 32. Reward Configuration

Initial reward:

```yaml
selector:
  reward:
    type: "NEW_VALIDATED_FAILURE_FAMILY"

    values:
      positive: 1.0
      negative: 0.0
```

Definition:

```text
Reward = 1
```

if the selected candidate produces a previously unseen validated failure family.

Otherwise:

```text
Reward = 0
```

This is the recommended initial research reward.

---

# 33. Alternative Reward Components

Future experiments may define:

```yaml
selector:
  reward:
    components:
      new_family: 1.0
      new_failure: 0.0
      severity: 0.0
      reproduction: 0.0
```

However, changing reward definition creates a different experimental condition and must be treated as an explicit configuration change.

---

# 34. Candidate Repeat Policy

```yaml
selector:
  repeats:
    mode: "NO_REPEAT"
```

Supported modes:

```text
NO_REPEAT
REPEAT_FOR_REPRODUCTION
ADAPTIVE_REPEAT
```

Discovery should normally use `NO_REPEAT` unless repeated candidate execution is itself part of the study.

---

# 35. Budget Configuration

Example:

```yaml
budget:
  unit: "EXECUTION_UNITS"
  limit: 1000

  enforcement:
    enabled: true
    reserve_before_operation: true
    prevent_exceeding_limit: true

  overshoot:
    allowed: false
    maximum: 0
```

---

# 36. Budget Units

Supported:

```text
MODEL_CALLS
TOKENS
COMPUTE_TIME
WALL_CLOCK
MONETARY
EXECUTION_UNITS
COMPOSITE
```

The initial prototype should use:

```text
EXECUTION_UNITS
```

because it permits controlled accounting across heterogeneous operations.

---

# 37. Cost Model Configuration

```yaml
budget:
  cost_model:
    generation: true
    execution: true
    branch: true
    snapshot: true
    restore: true
    analysis: true
    verification: true
```

Total:

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

---

# 38. Cost Estimation

Each operation should define:

```yaml
budget:
  estimation:
    execution:
      base: 1.0

    snapshot:
      base: 0.5

    restore:
      base: 0.5

    branch:
      base: 1.0

    analysis:
      base: 0.25

    verification:
      base: 0.5
```

These are configuration examples, not scientifically established costs.

Actual measured cost must be recorded after execution.

---

# 39. Budget Reservation

```yaml
budget:
  reservation:
    enabled: true
    reject_if_insufficient: true
```

The system must:

```text
Estimate
   ↓
Reserve
   ↓
Execute
   ↓
Measure Actual Cost
   ↓
Commit
```

If execution fails before consumption:

```text
Release reservation
```

---

# 40. Execution Configuration

```yaml
execution:
  mode: "NORMAL"

  timeout_seconds: 60

  max_steps: 30

  termination:
    on_agent_stop: true
    on_timeout: true
    on_resource_limit: true
    on_environment_error: true

  isolation:
    fresh_environment_per_execution: true
```

Supported modes:

```text
NORMAL
BRANCH
REPLAY
METAMORPHIC_BASE
METAMORPHIC_TRANSFORMED
HOLDOUT
```

---

# 41. Trajectory Configuration

```yaml
trajectory:
  enabled: true

  schema_version: "trace_v3"

  capture:
    agent_outputs: true
    tool_requests: true
    tool_responses: true
    policy_decisions: true
    state_transitions: true
    faults: true
    snapshots: true
    branches: true
    costs: true
    termination: true

  integrity:
    event_hashes: true
    previous_event_hash: true
```

Private chain-of-thought must not be collected.

---

# 42. Trace Storage

```yaml
trajectory:
  storage:
    database: true
    jsonl: true
    artifacts: true

  compression:
    enabled: false
```

The recommended architecture is:

```text
SQLite
+
JSONL
+
Artifact Files
```

---

# 43. State Analysis Configuration

```yaml
state_analysis:
  enabled: true

  interesting_state_detection:
    enabled: true

    signals:
      authorization_boundary: true
      unexpected_tool_sequence: true
      sensitive_data_access: true
      policy_transition: true
      state_transition_anomaly: true
      fault_transition: true
      resource_pressure: true
```

The output is an **interesting-state signal**, not a confirmed failure.

---

# 44. Snapshot Configuration

```yaml
snapshot:
  enabled: true

  trigger:
    interesting_state: true
    manual: true
    invariant_risk: true

  contents:
    environment_state: true
    tool_state: true
    policy_state: true
    task_state: true
    fault_state: true
    resource_state: true

  integrity:
    hash: true

  immutable: true
```

---

# 45. Branching Configuration

```yaml
branching:
  enabled: true

  max_depth: 3

  max_branches_per_snapshot: 3

  isolation:
    enabled: true
    parent_immutable: true

  perturbations:
    enabled: true

    allowed:
      - TOOL_RESPONSE_MUTATION
      - TOOL_TIMEOUT
      - SERVICE_UNAVAILABLE
      - STATE_MUTATION
      - POLICY_CONTEXT_CHANGE
```

The values `3` and `3` are initial implementation defaults, not research constants.

---

# 46. Branch Cost Configuration

```yaml
branching:
  cost:
    include_snapshot: true
    include_restore: true
    include_branch_execution: true
    include_analysis: true
```

Branching must not appear artificially cheap by counting only the final branch execution.

---

# 47. Invariant Configuration

Example:

```yaml
invariants:
  version: "invariant_v1"

  enabled:
    - I1
    - I2
    - I3
    - I4
    - I5
    - I6
    - I7
    - I8
```

Each invariant should specify:

```text
id
name
domain
severity
version
evaluation_logic
evidence_requirements
```

---

# 48. Invariant Evaluation Policy

```yaml
invariants:
  evaluation:
    fail_on:
      - VIOLATED

    preserve:
      - SATISFIED
      - VIOLATED
      - INCONCLUSIVE
      - INVALID
      - ERROR

    require_evidence: true
```

The system must not convert:

```text
INCONCLUSIVE
```

into:

```text
PASS
```

---

# 49. Failure Detection Configuration

```yaml
failure_detection:
  enabled: true

  require_invariant_violation: true
  require_valid_execution: true
  require_evidence: true

  allowed_outcomes:
    - FAIL
    - INCONCLUSIVE
    - INVALID
    - ERROR
```

Core definition:

```text
Failure =
Observed Execution
+
Invariant Violation
+
Valid Evidence
```

---

# 50. Failure Classification Configuration

```yaml
classification:
  enabled: true

  version: "classifier_v1"

  hierarchical:
    level_1: domain
    level_2: type
    level_3: mechanism
    level_4: context

  categories:
    - SECURITY
    - RELIABILITY
    - ROBUSTNESS
    - POLICY
    - AUTHORIZATION
    - DATA_EXPOSURE
    - STATE_INTEGRITY
    - RESOURCE
    - EVALUATOR
    - ENVIRONMENT
    - INFRASTRUCTURE
    - SCENARIO
```

---

# 51. Clustering Configuration

```yaml
clustering:
  enabled: true

  version: "cluster_v1"

  stages:
    exact_fingerprint: true
    structured_similarity: true

  similarity:
    threshold: 0.75

  outliers:
    allowed: true
```

The threshold is an implementation parameter and must not be presented as a universal scientific constant.

Sensitivity analysis should later evaluate alternative thresholds.

---

# 52. Clustering Feature Weights

Example:

```yaml
clustering:
  similarity:
    weights:
      invariant: 0.25
      category: 0.15
      mechanism: 0.25
      tool: 0.10
      policy_outcome: 0.10
      state_transition: 0.10
      attack_surface: 0.05
```

The exact values must be frozen for an experiment and recorded in the manifest.

---

# 53. Reproduction Configuration

```yaml
reproduction:
  enabled: true

  attempts: 3

  modes:
    - INDEPENDENT_SEED

  fresh_environment: true
  fresh_trace: true

  independence:
    execution: true
    process: true
    environment: true
    seed: true
```

Initial recommended reproduction protocol:

```text
3 independent attempts
```

---

# 54. Reproduction Outcomes

The configuration must preserve:

```text
REPRODUCED
NOT_REPRODUCED
PARTIAL
INCONCLUSIVE
INVALID
ERROR
```

The distinction between:

```text
NOT_REPRODUCED
```

and:

```text
ERROR
```

must not be removed.

---

# 55. Stability Configuration

```yaml
reproduction:
  stability:
    enabled: true

    classes:
      - STABLE
      - VARIABLE
      - FLAKY
      - NON_REPRODUCED
      - INCONCLUSIVE
```

Flaky failures must remain in the dataset.

They should not automatically be discarded.

---

# 56. Metamorphic Configuration

```yaml
metamorphic:
  enabled: true

  version: "mt_v1"

  transformations:
    - MT01
    - MT02
    - MT03
    - MT04

  relations:
    - SECURITY_PROPERTY_PRESERVATION
    - INVARIANT_PRESERVATION
    - NON_INTERFERENCE
```

---

# 57. Metamorphic Transformations

Initial set:

```text
MT01 FORMAT_ONLY
MT02 SYNTHETIC_ID_RENAME
MT03 IRRELEVANT_CONTEXT
MT04 TASK_PARAPHRASE
```

Example:

```yaml
metamorphic:
  transformations:
    MT02:
      enabled: true
      category: IDENTIFIER_PRESERVING
      preserves:
        - authorization_semantics
        - resource_identity_semantics
```

---

# 58. Metamorphic Execution Rules

```yaml
metamorphic:
  execution:
    fresh_environment: true
    fresh_trace: true
    independent_seed: true
    compare_structured_behavior: true
```

The comparison should prioritize:

```text
tool actions
authorization decisions
resource access
state changes
invariant outcomes
```

rather than textual equality alone.

---

# 59. Metamorphic Result Configuration

Supported:

```text
PASS
VIOLATION
INCONCLUSIVE
INVALID
ERROR
```

A metamorphic violation becomes a failure candidate only when:

1. transformation is valid
2. base execution is valid
3. transformed execution is valid
4. protected relation is violated
5. normal failure validation succeeds

---

# 60. Hidden Holdout Configuration

```yaml
holdout:
  enabled: true

  version: "holdout_v1"

  size: 50

  source:
    generation: "INDEPENDENT_VARIANTS"

  visibility:
    selector: false
    discovery_pipeline: false

  execution:
    fresh_environment: true
    fresh_trace: true
```

---

# 61. Holdout Isolation

The following must be unavailable to the selector:

```yaml
holdout:
  access_control:
    selector:
      outcomes: false
      failures: false
      families: false
      reproduction: false
      metamorphic_results: false
```

Holdout data may become available to the final evaluation layer after discovery is frozen.

---

# 62. Holdout Generation Rules

Example:

```yaml
holdout:
  generation:
    unseen_variants: true
    preserve_target_properties: true
    avoid_exact_duplicates: true
    seed: 9871
```

The holdout should test whether discovered failure patterns generalize beyond the development candidate pool.

---

# 63. Metrics Configuration

```yaml
metrics:
  enabled: true

  discovery:
    - validated_failure_count
    - unique_failure_fingerprint_count
    - failure_family_count
    - family_discovery_auc
    - time_to_first_failure
    - time_to_first_family

  efficiency:
    - cost_per_failure
    - cost_per_new_family
    - execution_count
    - total_cost

  validation:
    - reproduction_rate
    - family_reproduction_rate
    - metamorphic_consistency_rate
    - metamorphic_violation_rate

  generalization:
    - holdout_generalization_rate
```

---

# 64. Metric Versioning

```yaml
metrics:
  version: "metrics_v1"
```

Every metric definition should record:

```text
metric_id
formula_version
aggregation_method
input_population
exclusion_rules
```

This prevents a metric from silently changing between experiments.

---

# 65. Discovery AUC Configuration

Family discovery should be measured against consumed budget.

Conceptually:

```text
x-axis = cumulative evaluation cost
y-axis = validated failure families discovered
```

Configuration:

```yaml
metrics:
  discovery_curve:
    x_axis: "CUMULATIVE_COST"
    y_axis: "VALIDATED_FAILURE_FAMILIES"
    normalization: "NONE"
```

This allows fair comparison under unequal instantaneous costs.

---

# 66. Statistics Configuration

```yaml
statistics:
  enabled: true

  unit_of_analysis: "EXPERIMENT_RUN"

  confidence_level: 0.95

  effect_sizes:
    enabled: true

  multiple_comparison:
    enabled: true
    correction: "HOLM"

  paired_analysis:
    enabled: true
    key: "SEED"
```

The experiment run, rather than an individual trajectory, is the primary statistical unit.

---

# 67. Statistical Population

The configuration must explicitly define the population used for each metric.

Example:

```yaml
statistics:
  populations:
    discovery:
      source: "MAIN_DISCOVERY_RUNS"

    reproduction:
      source: "VALIDATED_FAILURES"

    metamorphic:
      source: "VALID_METAMORPHIC_TESTS"

    holdout:
      source: "HOLDOUT_RUNS"
```

This prevents denominator confusion.

---

# 68. Stopping Configuration

The experiment should support fixed-budget stopping.

```yaml
stopping:
  mode: "FIXED_BUDGET"

  conditions:
    budget_exhausted: true
    candidate_pool_exhausted: true
    infrastructure_failure: true
```

Optional research experiments may support:

```text
TARGET_FAILURE_FAMILIES
TIME_LIMIT
NO_NEW_FAMILY_WINDOW
```

However, stopping rules must be declared before the experiment begins.

---

# 69. Infrastructure Failure Policy

```yaml
stopping:
  infrastructure_failure:
    action: "STOP_RUN"

  evaluator_error:
    action: "MARK_INCONCLUSIVE"

  candidate_error:
    action: "RECORD_AND_CONTINUE"
```

A single invalid candidate should not necessarily terminate an entire experiment.

---

# 70. Experiment Phase Configuration

The experiment may explicitly define phases:

```yaml
experiment:
  phases:
    - INFRASTRUCTURE_VALIDATION
    - EVALUATOR_VALIDATION
    - BASELINE_CALIBRATION
    - MAIN_DISCOVERY
    - BRANCHING
    - REPRODUCTION
    - METAMORPHIC
    - HOLDOUT
    - ABLATION
    - STATISTICS
```

---

# 71. Phase-Specific Configuration

Example:

```yaml
experiment:
  phases:
    MAIN_DISCOVERY:
      enabled: true

    REPRODUCTION:
      enabled: true

    METAMORPHIC:
      enabled: true

    HOLDOUT:
      enabled: true

    ABLATION:
      enabled: false
```

This allows the same framework to execute smaller development experiments without changing source code.

---

# 72. Ablation Configuration

Example:

```yaml
ablation:
  enabled: true

  studies:
    - id: A1
      component: NOVELTY
      disabled: true

    - id: A2
      component: BRANCH_POTENTIAL
      disabled: true

    - id: A3
      component: COST_PENALTY
      disabled: true

    - id: A4
      component: BRANCHING
      disabled: true

    - id: A5
      component: REPRODUCTION
      disabled: true

    - id: A6
      component: METAMORPHIC_TESTING
      disabled: true
```

Each ablation should modify only the intended component.

---

# 73. Baseline Experiment Configuration

## Random

```yaml
experiment:
  research:
    method: RANDOM

selector:
  method: RANDOM
```

---

## Uniform

```yaml
experiment:
  research:
    method: UNIFORM

selector:
  method: UNIFORM
```

---

## UCB-V

```yaml
experiment:
  research:
    method: UCBV

selector:
  method: UCBV
```

---

## Proposed

```yaml
experiment:
  research:
    method: PROPOSED_ADAPTIVE

selector:
  method: PROPOSED_ADAPTIVE
```

All four should use the same:

```text
candidate pool
budget
agent
environment
invariants
validation
seed set
```

for a fair comparison.

---

# 74. Main Experiment Matrix

The minimum comparison should support:

| Experiment | Selection         | Branching |
| ---------- | ----------------- | --------- |
| E1         | Random            | Off       |
| E2         | Uniform           | Off       |
| E3         | UCB-V             | Off       |
| E4         | Adaptive          | Off       |
| E5         | Random            | On        |
| E6         | Uniform           | On        |
| E7         | UCB-V             | On        |
| E8         | Proposed Adaptive | On        |

This matrix separates:

* adaptive selection effects
* branching effects
* their interaction

---

# 75. Configuration Equivalence Rules

For a fair method comparison, these must remain identical unless the experiment explicitly studies them:

```text
candidate pool
scenario versions
agent configuration
environment configuration
tool registry
policy configuration
invariants
budget
validation procedure
seed set
termination rules
metric definitions
holdout set
```

Only the intended experimental factor should change.

---

# 76. Configuration Validation

Before an experiment starts, the configuration validator must check:

### Identity

* experiment name exists
* version exists
* method registered

### Budget

* limit > 0
* unit valid
* overshoot rules valid

### Seeds

* seed count matches repetitions
* seeds are unique

### Candidate Pool

* pool exists
* pool is frozen
* pool version is recorded

### Agent

* adapter exists
* configuration valid

### Environment

* environment exists
* required tools exist
* policy exists

### Invariants

* every referenced invariant exists
* versions are compatible

### Selector

* selector exists
* selector configuration valid
* reward compatible

### Validation

* reproduction configuration valid
* metamorphic transformations exist
* holdout is isolated

---

# 77. Configuration Compatibility Checks

The system must reject incompatible configurations.

Examples:

```text
PROPOSED_ADAPTIVE
+
selector weights missing
```

should fail.

```text
UCBV
+
variance estimator disabled
```

should fail.

```text
BRANCHING
+
snapshot disabled
```

should fail.

```text
HOLDOUT
+
selector receives holdout results
```

should fail.

```text
METAMORPHIC
+
no relation defined
```

should fail.

---

# 78. Configuration Schema Validation

Use Pydantic models.

Example:

```python
class ExperimentConfig(BaseModel):
    experiment: ExperimentSection
    agent: AgentConfig
    environment: EnvironmentConfig
    scenario_pool: ScenarioPoolConfig
    selector: SelectorConfig
    budget: BudgetConfig
    execution: ExecutionConfig
    trajectory: TrajectoryConfig
    state_analysis: StateAnalysisConfig
    snapshot: SnapshotConfig
    branching: BranchingConfig
    invariants: InvariantConfig
    failure_detection: FailureDetectionConfig
    classification: ClassificationConfig
    clustering: ClusteringConfig
    reproduction: ReproductionConfig
    metamorphic: MetamorphicConfig
    holdout: HoldoutConfig
    metrics: MetricsConfig
    statistics: StatisticsConfig
    stopping: StoppingConfig
```

---

# 79. Configuration Resolution

Configuration should be resolved before experiment creation.

Example:

```text
base.yaml
   +
agent.yaml
   +
environment.yaml
   +
selector.yaml
   +
experiment.yaml
        |
        v
Resolved Configuration
        |
        v
Pydantic Validation
        |
        v
Compatibility Validation
        |
        v
Canonical Serialization
        |
        v
Configuration Hash
        |
        v
Experiment Manifest
```

---

# 80. Configuration Hash

The resolved configuration should be canonicalized and hashed.

Example:

```text
config_hash =
SHA256(canonical_resolved_configuration)
```

Store:

```text
config_hash
```

in the experiment record.

This enables detection of configuration drift.

---

# 81. Immutable Experiment Manifest

When an experiment starts, generate:

```text
artifacts/
└── experiments/
    └── exp_001/
        ├── manifest.yaml
        ├── resolved_config.yaml
        ├── config_hash.txt
        ├── seeds.yaml
        └── software_versions.json
```

The manifest must not change after the run starts.

---

# 82. Runtime Overrides

Runtime overrides should be restricted.

Allowed before start:

```text
budget
method
seed
experiment label
```

Only if they result in a new resolved configuration.

After start:

```text
No research configuration changes.
```

Operational controls such as pause and stop are not configuration changes.

---

# 83. Secrets

Secrets must never be stored in experiment YAML.

Incorrect:

```yaml
api_key: "sk-..."
```

Correct:

```yaml
agent:
  provider: "external"
  credential_source: "ENVIRONMENT"
```

Secrets should come from:

```text
environment variables
secret manager
runtime credential store
```

The manifest records only the credential source, not the secret.

---

# 84. Sensitive Data Configuration

```yaml
privacy:
  enabled: true

  trace_redaction:
    enabled: true

  fields_to_redact:
    - customer_id
    - account_id
    - transaction_id

  deterministic_pseudonymization:
    enabled: true
```

Synthetic identifiers should be preferred throughout the controlled environment.

---

# 85. Artifact Configuration

```yaml
artifacts:
  root: "artifacts/"

  traces:
    enabled: true

  snapshots:
    enabled: true

  branches:
    enabled: true

  reports:
    enabled: true

  plots:
    enabled: true

  exports:
    enabled: true
```

---

# 86. Tracking Configuration

```yaml
tracking:
  enabled: true

  git:
    record_commit: true
    require_clean_tree: true

  dependencies:
    record_versions: true

  configuration:
    record_hash: true

  experiment_manifest:
    enabled: true
```

For formal experiments, requiring a clean Git tree is strongly recommended.

---

# 87. Database Configuration

```yaml
database:
  url: "sqlite:///data/agent_eval.db"

  foreign_keys: true

  transactions:
    enabled: true

  journal_mode: "WAL"

  migrations:
    version: "001"
```

---

# 88. Logging Configuration

```yaml
logging:
  level: "INFO"

  format: "JSON"

  include:
    timestamp: true
    experiment_id: true
    run_id: true
    execution_id: true
    request_id: true
```

---

# 89. API Configuration

```yaml
api:
  enabled: true

  host: "127.0.0.1"
  port: 8000

  version: "v1"

  authentication:
    enabled: false

  documentation:
    enabled: true
```

Authentication can be enabled when the API is exposed beyond a trusted local environment.

---

# 90. Development Configuration

A lightweight development configuration may be:

```yaml
experiment:
  repetitions:
    count: 1

budget:
  unit: EXECUTION_UNITS
  limit: 25

scenario_pool:
  size:
    target: 10

selector:
  method: RANDOM

branching:
  enabled: false

reproduction:
  enabled: false

metamorphic:
  enabled: false

holdout:
  enabled: false
```

This configuration is for software development, not research claims.

---

# 91. Evaluator Validation Configuration

A separate configuration should test evaluator correctness.

```yaml
experiment:
  research:
    method: RANDOM

  repetitions:
    count: 1

budget:
  unit: EXECUTION_UNITS
  limit: 100

scenario_pool:
  source:
    type: "GROUND_TRUTH"

selector:
  method: UNIFORM

branching:
  enabled: true

reproduction:
  enabled: true

metamorphic:
  enabled: true

holdout:
  enabled: false
```

The evaluator validation set should contain known expected outcomes.

---

# 92. Main Research Configuration Example

A complete initial experiment might be:

```yaml
experiment:
  identity:
    name: "main_adaptive_vs_baselines"
    description: "Budget-constrained comparison of adaptive and non-adaptive AI-agent security evaluation"
    version: "1.0"

  research:
    research_questions:
      - RQ1
      - RQ2
      - RQ3
      - RQ8
    hypotheses:
      - H1
      - H2
      - H3

  repetitions:
    count: 20
    independent: true
    matched_seed_set: true

  seeds:
    strategy: FIXED_SET
    values:
      - 11
      - 22
      - 33
      - 44
      - 55
      - 66
      - 77
      - 88
      - 99
      - 110
      - 121
      - 132
      - 143
      - 154
      - 165
      - 176
      - 187
      - 198
      - 209
      - 220

agent:
  id: "agent_001"
  adapter: "MOCK_AGENT"
  version: "agent_v1"

environment:
  id: "enterprise_support_sim"
  version: "env_v1"

scenario_pool:
  id: "security_pool_v1"
  version: "1.0"
  frozen: true

selector:
  method: "PROPOSED_ADAPTIVE"

budget:
  unit: "EXECUTION_UNITS"
  limit: 1000

execution:
  mode: "NORMAL"
  timeout_seconds: 60
  max_steps: 30

trajectory:
  enabled: true
  schema_version: "trace_v3"

state_analysis:
  enabled: true

snapshot:
  enabled: true

branching:
  enabled: true
  max_depth: 3
  max_branches_per_snapshot: 3

invariants:
  version: "invariant_v1"

failure_detection:
  enabled: true

classification:
  version: "classifier_v1"

clustering:
  version: "cluster_v1"

reproduction:
  enabled: true
  attempts: 3

metamorphic:
  enabled: true
  version: "mt_v1"

holdout:
  enabled: true
  version: "holdout_v1"
  size: 50

metrics:
  enabled: true
  version: "metrics_v1"

statistics:
  enabled: true
  unit_of_analysis: "EXPERIMENT_RUN"

stopping:
  mode: "FIXED_BUDGET"

tracking:
  enabled: true
```

---

# 93. Configuration Profiles

The repository should define named profiles.

## Profile 1: Development

```text
small pool
small budget
mock agent
branching off
validation off
holdout off
```

## Profile 2: Evaluator Validation

```text
ground-truth scenarios
mock agent
known expected outcomes
full invariant evaluation
```

## Profile 3: Baseline

```text
frozen candidate pool
random/uniform/UCB-V
fixed budget
repeated seeds
```

## Profile 4: Main Adaptive

```text
frozen candidate pool
proposed selector
budget constraint
branching
validation
holdout
```

## Profile 5: Ablation

```text
main configuration
+
one component disabled
```

---

# 94. Configuration Comparison

Two experiments should be comparable through a configuration diff.

Example:

```text
E1 RANDOM
E8 PROPOSED_ADAPTIVE

Difference:
selector.method
selector.acquisition
selector.weights
```

Everything else should remain equal.

The system should be able to generate:

```text
config_diff(E1, E8)
```

before running the comparison.

---

# 95. Configuration Drift Detection

At runtime, verify:

```text
current_config_hash
==
experiment_config_hash
```

If they differ:

```text
CONFIGURATION_DRIFT
```

must be raised.

The run should not silently continue.

---

# 96. Configuration Provenance

Each major configuration object must record:

```text
source_file
source_version
resolved_value
hash
```

Example:

```json
{
  "component": "selector",
  "source": "configs/selectors/proposed.yaml",
  "version": "selector_v1",
  "hash": "sha256:..."
}
```

---

# 97. Configuration and Database Relationship

The database should store:

```text
experiments
    |
    +-- experiment_config
    +-- config_hash
    +-- software_version
    +-- agent_config_version
    +-- environment_version
    +-- selector_version
    +-- invariant_version
    +-- clustering_version
    +-- metrics_version
```

Large configuration documents may be stored as artifacts, with hashes referenced in the database.

---

# 98. Configuration and Experiment Runs

An experiment may contain multiple runs.

Example:

```text
Experiment exp_001
|
+-- Run 001
|   method = RANDOM
|   seed = 11
|
+-- Run 002
|   method = RANDOM
|   seed = 22
|
+-- Run 003
|   method = RANDOM
|   seed = 33
```

The run inherits the experiment configuration but records run-specific:

```text
seed
method
selector state
budget state
runtime metadata
```

---

# 99. Configuration for Repeated Methods

For a baseline comparison:

```yaml
experiment:
  comparison:
    methods:
      - RANDOM
      - UNIFORM
      - UCBV
      - PROPOSED_ADAPTIVE

    shared:
      candidate_pool: true
      budget: true
      agent: true
      environment: true
      invariants: true
      seeds: true
      validation: true
      holdout: true
```

This makes the fairness assumptions explicit.

---

# 100. Configuration for Branching Ablation

Example:

```yaml
experiment:
  identity:
    name: "ablation_no_branching"

  research:
    method: "PROPOSED_ADAPTIVE"

branching:
  enabled: false

selector:
  acquisition:
    components:
      branch_potential:
        enabled: false
        weight: 0.0
```

The selector must not continue receiving branch-potential information when branching is disabled.

---

# 101. Configuration for Cost-Aware Ablation

```yaml
selector:
  method: "PROPOSED_ADAPTIVE"

  acquisition:
    components:
      novelty:
        enabled: true
        weight: 0.3

      branch_potential:
        enabled: true
        weight: 0.2

      cost:
        enabled: false
        weight: 0.0
```

This isolates the contribution of cost-awareness.

---

# 102. Configuration for Reproduction Study

```yaml
experiment:
  research:
    research_questions:
      - RQ4
      - RQ5

reproduction:
  enabled: true
  attempts: 3

metamorphic:
  enabled: false

holdout:
  enabled: false
```

---

# 103. Configuration for Metamorphic Study

```yaml
experiment:
  research:
    research_questions:
      - RQ6

reproduction:
  enabled: true

metamorphic:
  enabled: true

holdout:
  enabled: false
```

---

# 104. Configuration for Generalization Study

```yaml
experiment:
  research:
    research_questions:
      - RQ7

holdout:
  enabled: true
  size: 50

selector:
  information_boundary:
    forbidden:
      - holdout_outcomes
      - holdout_failures
      - holdout_families
```

---

# 105. Configuration Validation Rules

The configuration validator must enforce the following.

## CFG-001

Experiment name must be non-empty.

## CFG-002

Experiment version must be specified.

## CFG-003

Repetition count must be greater than zero.

## CFG-004

Seed count must match repetition count when fixed seeds are used.

## CFG-005

Candidate pool must be frozen for the primary comparison.

## CFG-006

Budget limit must be positive.

## CFG-007

Every selector must be registered.

## CFG-008

UCB-V must use empirical variance.

## CFG-009

Branching requires snapshots.

## CFG-010

Snapshot restoration must be enabled when branching is enabled.

## CFG-011

Metamorphic testing requires at least one transformation and relation.

## CFG-012

Holdout outcomes must not be exposed to the selector.

## CFG-013

Every referenced invariant must exist.

## CFG-014

Every configuration version must be recorded.

## CFG-015

Every research experiment must produce an immutable manifest.

## CFG-016

A completed experiment must retain its resolved configuration.

---

# 106. Configuration Security

Configuration must not permit:

* arbitrary filesystem writes
* arbitrary command execution
* unvalidated external URLs
* unbounded resource limits
* unrestricted network access
* secret persistence
* holdout exposure
* disabling mandatory evidence collection during a formal experiment

Experimental flexibility should not become a convenient way to accidentally destroy experimental validity.

---

# 107. Formal Experiment Lock

When a research experiment starts:

```text
CONFIGURATION
     ↓
RESOLVE
     ↓
VALIDATE
     ↓
HASH
     ↓
FREEZE
     ↓
START
```

After freeze:

```text
Configuration = immutable
```

If a researcher wants to change:

```text
budget
selector
scenario pool
agent
environment
invariants
validation
```

the system should create a new experiment configuration/version.

---

# 108. Configuration Lifecycle

```text
Draft
  ↓
Validated
  ↓
Resolved
  ↓
Hashed
  ↓
Frozen
  ↓
Running
  ↓
Completed
  ↓
Archived
```

Possible terminal states:

```text
COMPLETED
STOPPED
FAILED
INCONCLUSIVE
```

---

# 109. Configuration State Model

```text
CREATED
   ↓
VALIDATED
   ↓
FROZEN
   ↓
RUNNING
   ↓
COMPLETED
```

Invalid transitions should be rejected.

For example:

```text
COMPLETED → RUNNING
```

must not occur.

---

# 110. Configuration API

The implementation should expose:

```http
POST /experiments/config/validate
POST /experiments/config/resolve
POST /experiments/config/freeze
GET  /experiments/{experiment_id}/config
GET  /experiments/{experiment_id}/config/hash
GET  /experiments/{experiment_id}/config/diff
```

---

# 111. Configuration CLI

Recommended:

```bash
agent-eval config validate configs/experiments/main.yaml

agent-eval config resolve configs/experiments/main.yaml

agent-eval config freeze configs/experiments/main.yaml \
    --output artifacts/experiments/exp_001/

agent-eval config diff \
    configs/experiments/random.yaml \
    configs/experiments/proposed.yaml
```

---

# 112. Configuration Test Suite

Tests should cover:

```text
test_valid_experiment_config
test_missing_budget
test_invalid_selector
test_ucbv_without_variance
test_branching_without_snapshot
test_holdout_leakage
test_seed_count_mismatch
test_missing_invariant
test_invalid_metamorphic_relation
test_configuration_hash_stability
test_configuration_drift_detection
test_manifest_generation
```

---

# 113. Configuration Reproducibility Test

Given:

```text
same source configuration
same component versions
same dependency versions
```

the system should produce the same:

```text
resolved configuration
canonical serialization
configuration hash
```

independent of dictionary ordering.

---

# 114. Configuration Hash Test

Example:

```python
config_a = load("experiment.yaml")
config_b = load("experiment.yaml")

assert hash_config(config_a) == hash_config(config_b)
```

Equivalent configurations with different YAML key ordering should generate the same canonical hash.

---

# 115. Configuration Change Example

Suppose:

```yaml
selector:
  method: UCBV
```

is changed to:

```yaml
selector:
  method: PROPOSED_ADAPTIVE
```

The system must create a different configuration hash.

The experiment should therefore be treated as a different experimental condition.

---

# 116. Recommended Initial Configuration Set

The repository should initially contain:

```text
configs/
├── development.yaml
├── test.yaml
│
├── agents/
│   └── mock_agent.yaml
│
├── environments/
│   └── support_environment.yaml
│
├── selectors/
│   ├── random.yaml
│   ├── uniform.yaml
│   ├── ucbv.yaml
│   └── proposed.yaml
│
├── invariants/
│   └── default.yaml
│
├── validation/
│   └── default.yaml
│
├── holdout/
│   └── default.yaml
│
└── experiments/
    ├── evaluator_validation.yaml
    ├── random.yaml
    ├── uniform.yaml
    ├── ucbv.yaml
    └── proposed.yaml
```

---

# 117. Recommended Initial `proposed.yaml`

```yaml
experiment:
  identity:
    name: "proposed_adaptive_v1"
    version: "1.0"

  research:
    method: "PROPOSED_ADAPTIVE"
    research_questions:
      - RQ1
      - RQ2
      - RQ8

  repetitions:
    count: 20
    independent: true
    matched_seed_set: true

  seeds:
    strategy: FIXED_SET
    values:
      - 11
      - 22
      - 33
      - 44
      - 55
      - 66
      - 77
      - 88
      - 99
      - 110
      - 121
      - 132
      - 143
      - 154
      - 165
      - 176
      - 187
      - 198
      - 209
      - 220

selector:
  method: PROPOSED_ADAPTIVE

  reward:
    type: NEW_VALIDATED_FAILURE_FAMILY
    values:
      positive: 1.0
      negative: 0.0

  ucbv:
    bound_b: 1.0
    variance:
      estimator: EMPIRICAL
      method: WELFORD

  acquisition:
    base: UCBV

    components:
      novelty:
        enabled: true
        weight: 0.30

      branch_potential:
        enabled: true
        weight: 0.20

      severity:
        enabled: false
        weight: 0.00

      cost:
        enabled: true
        weight: 0.20
```

---

# 118. Configuration and Research Claims

Configuration values must never be confused with measured research results.

For example:

```yaml
branching:
  max_depth: 3
```

means:

> The experiment was configured with maximum branch depth 3.

It does **not** mean:

> Branch depth 3 is empirically optimal.

Likewise:

```yaml
clustering:
  similarity:
    threshold: 0.75
```

means:

> This experiment used threshold 0.75.

It does **not** mean:

> 0.75 is scientifically validated.

Configuration parameters become empirical claims only after they are tested through the experimental methodology.

---

# 119. Configuration and Ablation Integrity

If a component is ablated, all dependent configuration must be disabled.

Example:

```text
Branching OFF
```

requires:

```text
branching.enabled = false
branch_potential.enabled = false
branch_potential.weight = 0
```

Otherwise the experiment claims to remove branching while still feeding the selector information derived from branching.

That would be a wonderfully efficient way to manufacture a misleading ablation.

---

# 120. Final Configuration Dependency Graph

```text
                       Experiment
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
       Agent          Environment      Scenario Pool
          |                |                |
          |         +------+-------+        |
          |         |              |        |
          |       Tools          Policy     |
          |         |              |        |
          +---------+------+-------+--------+
                           |
                           v
                      Candidate Pool
                           |
                           v
                        Selector
                           |
                           v
                         Budget
                           |
                           v
                       Execution
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
       Trajectory        State       Snapshot/Branch
            |              |              |
            +--------------+--------------+
                           |
                           v
                       Invariants
                           |
                           v
                        Failure
                           |
                    +------+------+
                    |             |
                    v             v
                Clustering    Reproduction
                    |             |
                    +------+------+
                           |
                           v
                      Metamorphic
                           |
                           v
                        Holdout
                           |
                           v
                        Metrics
                           |
                           v
                      Statistics
                           |
                           v
                       Reports
```

---

# 121. Final Configuration Principles

The configuration system must enforce these principles:

1. **Every research-relevant parameter is explicit.**
2. **Every configuration is versioned.**
3. **Every started experiment has an immutable resolved configuration.**
4. **Every experiment has a configuration hash.**
5. **Every run records its seed and method.**
6. **Every baseline uses the same shared experimental conditions where required.**
7. **Budget is declared before execution.**
8. **Selector information boundaries are explicit.**
9. **Holdout data is isolated.**
10. **Branching configuration includes its full cost.**
11. **Reproduction and metamorphic settings are explicit.**
12. **Metric definitions are versioned.**
13. **Configuration changes create new experimental conditions.**
14. **Raw evidence remains independent of derived configuration.**
15. **Configuration parameters are not presented as empirical findings.**

---

# 122. Definition of Done

The configuration system is complete when:

* [ ] All experiment parameters have typed schemas.
* [ ] YAML configuration loading works.
* [ ] Environment-variable overrides work.
* [ ] CLI overrides work before experiment start.
* [ ] Configuration compatibility validation works.
* [ ] Selector-specific validation works.
* [ ] Budget configuration is validated.
* [ ] Seed/repetition consistency is validated.
* [ ] Candidate pools can be frozen.
* [ ] Agent configuration is versioned.
* [ ] Environment configuration is versioned.
* [ ] Invariant configuration is versioned.
* [ ] Clustering configuration is versioned.
* [ ] Reproduction configuration is versioned.
* [ ] Metamorphic configuration is versioned.
* [ ] Holdout configuration is isolated.
* [ ] Configuration is canonicalized.
* [ ] Configuration hash is generated.
* [ ] Immutable experiment manifest is generated.
* [ ] Configuration drift is detected.
* [ ] Configuration diffs can be generated.
* [ ] Development, validation, baseline, main, and ablation profiles exist.
* [ ] Configuration tests pass.
* [ ] A complete experiment can be reconstructed from its manifest.

---

# 123. Final Configuration Artifact

For every formal experiment, the system must ultimately produce:

```text
artifacts/
└── experiments/
    └── <experiment_id>/
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
        └── README.md
```

The most important artifact is the **resolved configuration + manifest** pair.

Together they answer:

> What exactly did the system run?

That question must be answerable before anyone interprets:

> What did the system discover?

---

# 124. Final Implementation Rule

The experiment configuration should be treated as part of the scientific record:

```text
Configuration
      ↓
Experiment
      ↓
Evidence
      ↓
Metrics
      ↓
Statistical Analysis
      ↓
Research Conclusion
```

Therefore:

> **No formal research result should exist without a corresponding immutable experiment configuration.**
