# Reproducibility & Metamorphic Testing Specification

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** RMT-01
**Document Type:** Reproducibility & Metamorphic Testing Specification
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
* Trajectory / Trace Schema
* Failure Classification & Clustering Specification
* Hidden Holdout & Generalization Specification
* Evaluation Metrics Specification
* Experimental Methodology

---

# 1. Purpose

This document specifies how the evaluation platform determines whether discovered failures are:

1. reproducible across independent executions,
2. stable or variable under repeated evaluation,
3. preserved under controlled scenario transformations,
4. robust to irrelevant changes,
5. sensitive to meaningful changes,
6. transferable across related scenarios,
7. suitable for inclusion in final research results.

The subsystem provides two distinct validation mechanisms:

### Reproducibility Testing

> Can the same failure be independently reproduced under controlled repetition?

### Metamorphic Testing

> Does the expected behavioral relationship remain valid when the test is transformed in a controlled way?

These are complementary but must not be conflated.

---

# 2. Research Role

The subsystem directly supports:

### RQ4: Failure Reproducibility

> Do discovered failures reproduce across independent executions?

### RQ6: Metamorphic Robustness

> Do discovered behaviors remain consistent under valid transformations of tasks, inputs, or execution conditions?

### RQ7: Hidden-Holdout Generalization

> Do discovered failure mechanisms transfer to unseen related scenarios?

It also supports evaluator reliability by identifying failures that cannot be reproduced because of evaluator or environment instability.

---

# 3. Core Principle

A discovered failure is stronger evidence when it survives independent validation.

The evidence progression is:

```text id="p5o7ra"
Observed Violation
      ↓
Independent Replay
      ↓
Reproduced Failure
      ↓
Failure Family
      ↓
Metamorphic Validation
      ↓
Hidden-Holdout Generalization
```

Each layer provides different evidence.

None should be silently substituted for another.

---

# 4. Fundamental Distinction

The system must preserve:

```text id="2d6h6x"
Reproducibility
    =
same or equivalent test
    +
independent execution
    +
same failure mechanism

Metamorphic Testing
    =
base test
    +
valid transformation
    +
expected relation
    +
transformed execution
    +
relation evaluation
```

Therefore:

```text id="3uj5kg"
Reproduced
≠
Metamorphically Validated
```

and:

```text id="xk90jz"
Metamorphically Consistent
≠
Failure Reproduced
```

---

# 5. Reproducibility Definition

A failure is reproducible when an independently repeated execution produces evidence of the same failure mechanism under the defined reproduction protocol.

Formally:

$$
Reproduced(F)
\iff
E_{repeat}
\models
Invariant(F)
$$

and the observed mechanism is sufficiently consistent with the original failure.

---

# 6. Reproducibility Unit

The primary reproducibility unit is a **failure occurrence**.

Secondary units include:

* failure family,
* branch,
* scenario,
* execution,
* invariant.

Example:

```text id="3w1y6k"
Failure FAIL-021
      ↓
Reproduction Attempt 1
      ↓
Reproduction Attempt 2
      ↓
Reproduction Attempt 3
```

---

# 7. Independent Execution Requirement

A reproduction must not simply reuse the original failure result.

It must perform a new execution.

Invalid:

```text id="y2m53k"
Original result
      ↓
copy result
      ↓
"reproduced"
```

Valid:

```text id="v2zq7c"
Original failure
      ↓
reconstruct test
      ↓
independent execution
      ↓
new trace
      ↓
new invariant evaluation
```

---

# 8. Reproduction Sources

A reproduction may originate from:

### Full Scenario Replay

Run the original scenario independently.

### State-Based Branch Replay

Restore the original snapshot and execute the same branch configuration.

### Perturbation Replay

Reapply the same perturbation to an equivalent state.

### Seed-Controlled Replay

Use the same random seed where deterministic behavior is expected.

### Independent-Seed Replay

Use a different seed to test robustness to stochastic variation.

---

# 9. Reproduction Modes

The system shall support:

```text id="n4x2h8"
EXACT_REPLAY
CONTROLLED_REPLAY
INDEPENDENT_SEED
STATE_REPLAY
BRANCH_REPLAY
```

---

# 10. Exact Replay

Exact replay attempts to reproduce:

```text id="wq1i0p"
same scenario
same configuration
same environment version
same model configuration
same seed
same perturbation
```

This is useful for deterministic systems.

---

# 11. Controlled Replay

Controlled replay preserves the important experimental conditions but allows explicitly defined variation.

Example:

```text id="jv3e2a"
same scenario
same agent
same environment
same perturbation
different execution instance
```

---

# 12. Independent-Seed Replay

For stochastic agents:

```text id="5fr6fp"
original seed = S1
replay seed   = S2
```

This tests whether the failure persists without depending on one exact random trajectory.

---

# 13. State Replay

State replay starts from a validated snapshot.

```text id="1d8f33"
Snapshot S
   ↓
Restore
   ↓
Apply same perturbation
   ↓
Execute
   ↓
Evaluate
```

The snapshot must pass integrity and restoration validation first.

---

# 14. Reproduction Configuration

Every reproduction attempt must record:

```yaml id="l9w1xj"
reproduction:
  reproduction_id:
  original_failure_id:
  original_execution_id:
  reproduction_execution_id:

  mode:
  seed:

  scenario_version:
  agent_config_id:
  environment_config_id:
  policy_config_id:
  tool_registry_version:

  perturbation_id:
  snapshot_id:
```

---

# 15. Reproduction Evidence

A reproduction attempt must reference:

```text id="7p7pmi"
new trajectory
new events
new invariant evaluation
new failure evidence
```

The original evidence cannot be reused as the only evidence.

---

# 16. Reproduction Outcome

Allowed outcomes:

```text id="3cku0b"
REPRODUCED
NOT_REPRODUCED
PARTIAL
INCONCLUSIVE
INVALID
ERROR
```

---

# 17. Reproduced

A reproduction is `REPRODUCED` when:

1. execution completed validly,
2. required invariant was evaluated,
3. the same failure condition occurred,
4. evidence supports the failure,
5. the observed mechanism is sufficiently consistent.

---

# 18. Not Reproduced

`NOT_REPRODUCED` means:

* execution was valid,
* the required evaluation occurred,
* the original failure condition did not occur.

This does not automatically prove the original failure was invalid.

It may indicate stochasticity.

---

# 19. Partial Reproduction

Use `PARTIAL` when:

* some but not all failure conditions recur,
* the same boundary is violated differently,
* the invariant fails but the exact mechanism differs,
* the branch reaches the relevant state but produces a different outcome.

Partial reproduction must be analyzed rather than silently promoted to full reproduction.

---

# 20. Inconclusive Reproduction

Use `INCONCLUSIVE` when the result cannot establish either reproduction or non-reproduction.

Examples:

```text id="yq5n2a"
environment failure
model unavailable
insufficient trace
missing tool response
evaluator error
```

---

# 21. Invalid Reproduction

Use `INVALID` when the reproduction protocol itself was violated.

Examples:

```text id="oc3e8x"
wrong scenario version
wrong perturbation
incorrect snapshot
invalid configuration
```

---

# 22. Reproduction Error

Use `ERROR` for infrastructure or execution failures that prevent meaningful evaluation.

The distinction is:

```text id="z3ry7m"
NOT_REPRODUCED
=
valid execution, no failure

ERROR
=
cannot determine because execution failed
```

---

# 23. Reproduction Attempts

Each failure should have a configurable number of reproduction attempts.

Example:

```yaml id="2q9zml"
reproducibility:
  attempts:
    exact: 1
    independent_seed: 3
```

The actual number must be specified by the experiment.

---

# 24. Reproduction Rate

For a failure:

$$
R_f =
\frac{
N_{reproduced}
}{
N_{valid\ attempts}
}
$$

where invalid/error attempts are handled according to the experiment's predefined protocol.

---

# 25. Family Reproduction Rate

For a failure family:

$$
R_F =
\frac{
N_{reproduced\ members}
}{
N_{tested\ members}
}
$$

Alternatively, the experiment may define family-level reproduction as:

```text id="jrrx1s"
at least one independent reproduction
```

The exact rule must be declared before analysis.

---

# 26. Reproducibility Stability

A failure can be classified as:

```text id="2x0vlv"
STABLE
VARIABLE
FLAKY
NON_REPRODUCED
INCONCLUSIVE
```

Example conceptual interpretation:

### Stable

Failure reproduced consistently under the defined protocol.

### Variable

Failure appears across repetitions but not every time.

### Flaky

Failure occurs intermittently at a low or unstable rate.

### Non-Reproduced

No valid reproduction observed.

### Inconclusive

Insufficient valid evidence.

---

# 27. Important Rule on Flaky Failures

Flaky failures must not automatically be discarded.

For security and reliability evaluation:

```text id="g2bq5c"
intermittent failure
```

may itself be important.

The system should preserve:

```text id="3q70eg"
occurrence rate
attempt count
conditions
random seeds
state differences
```

---

# 28. Reproducibility Matrix

For each failure:

| Attempt  | Seed | Mode        | Outcome | Same Mechanism | Valid |
| -------- | ---: | ----------- | ------- | -------------- | ----- |
| Original | 4821 | Original    | FAIL    | Yes            | Yes   |
| R1       | 4821 | Exact       | FAIL    | Yes            | Yes   |
| R2       | 7392 | Independent | FAIL    | Yes            | Yes   |
| R3       | 9134 | Independent | PASS    | No             | Yes   |

This makes stochastic behavior visible instead of hiding it behind one binary label.

---

# 29. Reproduction Mechanism Matching

A reproduction should compare normalized failure signatures.

Conceptually:

$$
MechanismMatch =
Similarity(
Signature_{original},
Signature_{reproduction}
)
$$

The threshold must be configured.

---

# 30. Exact Failure Match

A reproduction may be considered exact when:

```text id="g0a6vz"
same invariant
+
same normalized mechanism
+
same affected boundary
+
compatible state transition
```

---

# 31. Semantic Failure Match

A reproduction may be considered semantic when:

```text id="n8dy2y"
different concrete values
```

but:

```text id="k5a6oz"
same security/reliability property
same mechanism
same affected boundary
```

This is particularly important for synthetic identifiers.

---

# 32. Reproduction Evidence Chain

```text id="3c2s78"
Original Failure
      ↓
Reproduction Plan
      ↓
New Execution
      ↓
New Trace
      ↓
Invariant Evaluation
      ↓
Mechanism Comparison
      ↓
Reproduction Outcome
```

---

# 33. Reproduction Independence

Independence may be defined at multiple levels.

### Execution Independence

New execution instance.

### Process Independence

Different process/container.

### Environment Independence

Fresh environment state.

### Seed Independence

Different randomness.

### Temporal Independence

Execution performed at a different time.

The experiment should state which form is required.

---

# 34. Recommended Initial Independence

For the first prototype:

```text id="m8q7m0"
new execution
+
fresh environment
+
new trace
```

and, for stochastic evaluation:

```text id="0dxq7q"
additional independent seed
```

This provides useful evidence without requiring distributed infrastructure.

---

# 35. Reproduction Isolation

A reproduction must not mutate:

* the original execution,
* original snapshot,
* sibling branches,
* hidden holdout state.

Use the same isolation principles defined in the State Snapshot & Branching Specification.

---

# 36. Reproduction Cost

Reproduction consumes evaluation budget.

Record:

```text id="f4m5tp"
model calls
tokens
tool calls
execution time
snapshot cost
restore cost
analysis cost
verification cost
```

---

# 37. Reproduction Cost Formula

$$
C_{reproduction}
=
C_{generation}
+
C_{execution}
+
C_{analysis}
+
C_{verification}
$$

For state-based reproduction:

$$
C_{reproduction}
=
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

# 38. Reproduction Budget

Reproduction must have a separate configurable budget or consume the main experiment budget explicitly.

Example:

```yaml id="m3f77p"
budget:
  discovery:
  reproduction:
  metamorphic:
  holdout:
```

This prevents validation costs from being hidden inside discovery results.

---

# 39. Reproduction Phase

The recommended experiment lifecycle is:

```text id="47c4g0"
Discovery
   ↓
Freeze Candidate Failures
   ↓
Reproduction
   ↓
Metamorphic Testing
   ↓
Hidden Holdout
   ↓
Final Analysis
```

This provides cleaner separation between discovery and validation.

---

# 40. Reproduction Freeze

Once the discovery phase ends:

```text id="2h5fqi"
failure candidate set
       ↓
FROZEN
```

The reproduction process should not silently introduce new adaptive discovery behavior unless explicitly designed as a separate experiment.

---

# 41. Metamorphic Testing

Metamorphic testing is used when an absolute expected output is difficult to specify but a relationship between executions can be specified.

The core structure is:

```text id="u9i8z4"
Base Input
    ↓
Base Execution
    ↓
Base Outcome

Transformation
    ↓

Transformed Input
    ↓
Transformed Execution
    ↓
Transformed Outcome

          ↓
Relation Evaluation
```

---

# 42. Metamorphic Relation

A metamorphic relation defines an expected relationship:

$$
R(
Output(x),
Output(T(x))
)
$$

where:

* `x` = base test,
* `T(x)` = transformed test,
* `R` = expected relation.

---

# 43. Security-Focused Metamorphic Principle

The transformation should preserve the security property being tested unless the transformation explicitly changes the property.

Example:

```text id="l70v5q"
Base:
authorized user requests own account

Transformation:
change irrelevant wording

Expected:
authorization outcome remains unchanged
```

---

# 44. Metamorphic Test Structure

Each metamorphic test contains:

```yaml id="4n6d3p"
metamorphic_test:
  test_id:

  base_scenario_id:
  transformation_id:

  base_execution_id:
  transformed_execution_id:

  relation_id:

  expected_relation:

  observed_relation:

  result:
```

---

# 45. Transformation

A transformation is a controlled modification to the base scenario.

Examples:

```text id="3y3v6w"
paraphrase task
reorder irrelevant information
rename synthetic entities
change irrelevant formatting
add irrelevant context
change non-semantic identifiers
```

The transformation must have an explicit rationale.

---

# 46. Transformation Categories

Initial taxonomy:

```text id="w3y5q4"
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

# 47. Transformation Safety

A transformation is valid only if it preserves the intended semantic property.

Example:

Changing:

```text id="kq3qmf"
"Read your own account"
```

to:

```text id="5gqz2a"
"Delete another user's account"
```

is not a semantics-preserving transformation.

It changes the security requirement.

---

# 48. Transformation Specification

Each transformation must define:

```yaml id="9axm7f"
transformation:
  transformation_id:
  version:
  type:
  input_constraints:
  operation:
  expected_semantics:
  invalid_conditions:
```

---

# 49. Metamorphic Relation Types

Initial relation types:

```text id="c9n0uo"
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

# 50. Equivalence Relation

Expected:

$$
Output(x) \equiv Output(T(x))
$$

The exact equivalence must be defined.

It may mean:

* same policy decision,
* same tool action,
* same final state,
* same invariant result.

It does not necessarily mean identical textual output.

---

# 51. Invariant Preservation

Expected:

$$
I(x)=I(T(x))
$$

Example:

```text id="xcl2fp"
Base:
authorized access → PASS

Transformed:
same authorization semantics → PASS
```

---

# 52. Security Property Preservation

A security relation may require:

$$
SecurityOutcome(x)
=
SecurityOutcome(T(x))
$$

when the transformation preserves authorization semantics.

---

# 53. Non-Interference Relation

An irrelevant transformation should not affect a protected property.

Example:

```text id="2j0gct"
Base:
request with standard wording

Transformed:
same request + irrelevant formatting

Expected:
authorization result unchanged
```

---

# 54. Permutation Invariance

If two independent pieces of information are semantically unordered:

```text id="tr5jv1"
A + B
```

versus:

```text id="xzzjcv"
B + A
```

the expected security or policy outcome may remain unchanged.

The relation must be explicitly justified.

---

# 55. Idempotence

For an idempotent operation:

$$
T(T(x)) \equiv T(x)
$$

Example may include repeated application of a normalization transformation.

This should only be used when the domain semantics actually support idempotence.

---

# 56. Metamorphic Security Example

Base:

```text id="3qv2rq"
Authorized user
+
customer_lookup
+
own customer record
```

Transformation:

```text id="4l2eq5"
Change:
synthetic customer identifier from C001 to C002
```

This is valid only if both identifiers represent equivalent authorized resources under the test's intended relation.

Expected:

```text id="f7c6ac"
authorization property remains satisfied
```

---

# 57. Metamorphic Attack Example

Base attack:

```text id="20v4op"
Unauthorized transaction lookup
```

Transformation:

```text id="qg2j5v"
change target account to another unauthorized account
```

Expected relation:

```text id="9x7t1n"
authorization denial should remain preserved
```

If the transformed execution becomes authorized because the new account is actually permitted, the transformation was not semantically equivalent and the test should be marked invalid.

---

# 58. Metamorphic Failure Testing

Metamorphic testing can validate a discovered failure.

Example:

```text id="8vlr5z"
Base:
authorization bypass

Transformation:
rename synthetic account ID
```

If the same authorization bypass occurs:

```text id="r2b6w9"
evidence that the behavior is not tied to one concrete identifier
```

This strengthens the failure-family interpretation.

---

# 59. Metamorphic Consistency

A metamorphic test is successful when:

```text id="i7qv4s"
transformation valid
+
base execution valid
+
transformed execution valid
+
expected relation holds
```

---

# 60. Metamorphic Violation

A metamorphic violation occurs when:

```text id="h8c4fa"
transformation valid
+
base execution valid
+
transformed execution valid
+
expected relation fails
```

This becomes an observable robustness or consistency failure candidate.

---

# 61. Metamorphic Invalidity

A test must be marked invalid when:

```text id="r3v7p0"
transformation does not preserve intended semantics
```

or:

```text id="q4l6wa"
base/transformed execution cannot be validly compared
```

Invalid metamorphic tests must not become failures.

---

# 62. Metamorphic Result

Allowed results:

```text id="i5m0s7"
PASS
VIOLATION
INCONCLUSIVE
INVALID
ERROR
```

---

# 63. Metamorphic Base Execution

The base execution must be recorded normally.

It should produce:

```text id="d0v6m8"
trajectory
events
state checkpoints
invariant results
cost
```

---

# 64. Metamorphic Transformed Execution

The transformed execution must be a separate execution.

It must have:

```text id="k8pxu6"
new execution_id
new trajectory_id
transformation_id
relation_id
```

It must not simply reuse the base output.

---

# 65. Base/Transformed Pair

The system must explicitly link:

```yaml id="g91fx3"
metamorphic_pair:
  pair_id:
  base_execution_id:
  transformed_execution_id:
  transformation_id:
  relation_id:
```

---

# 66. Metamorphic Comparison

The Comparison Engine evaluates only declared properties.

Possible comparisons:

```text id="t8d2fd"
policy decision
tool selection
tool sequence
final state
state transition
invariant outcome
failure family
resource access
termination status
```

---

# 67. Textual Output Comparison

Raw text equality should not normally be the primary relation for agent evaluation.

Two semantically equivalent outputs may differ linguistically.

Prefer structured properties such as:

```text id="0e3y6p"
tool action
authorization result
resource accessed
state change
invariant outcome
```

---

# 68. Metamorphic State Comparison

The system may compare normalized state:

$$
Sim(S_{base},S_{transformed})
$$

The comparison must ignore fields intentionally changed by the transformation.

---

# 69. Expected Difference Mask

A transformation may explicitly declare expected differences.

Example:

```yaml id="s7a2fa"
expected_differences:
  - task.customer_id
```

Other protected fields should remain equivalent where required.

---

# 70. Protected Properties

Each metamorphic relation should declare protected properties.

Example:

```yaml id="u8j1f3"
protected_properties:
  - authorization_decision
  - resource_access
  - policy_outcome
```

---

# 71. Metamorphic Transformation Example

```yaml id="4tpsp4"
transformation:
  transformation_id: MT-001
  type: FORMAT_ONLY

  operation:
    whitespace_change: true
    punctuation_change: true

  expected_semantics:
    preserved: true

relation:
  relation_id: MR-001
  type: SECURITY_PROPERTY_PRESERVATION

  protected_properties:
    - authorization_decision
    - resource_access
```

---

# 72. Metamorphic Test Execution Algorithm

```python id="uxl9eo"
def run_metamorphic_test(base_scenario, transformation, relation):

    validate_transformation(
        base_scenario,
        transformation
    )

    base_result = execute(
        base_scenario
    )

    transformed_scenario = transform(
        base_scenario,
        transformation
    )

    validate_transformed_scenario(
        transformed_scenario
    )

    transformed_result = execute(
        transformed_scenario
    )

    relation_result = evaluate_relation(
        base_result,
        transformed_result,
        relation
    )

    return finalize_metamorphic_result(
        base_result,
        transformed_result,
        relation_result
    )
```

---

# 73. Metamorphic Relation Engine

Conceptual interface:

```python id="d0e8c7"
class MetamorphicRelationEngine:

    def validate_transformation(
        self,
        base,
        transformed
    ):
        ...

    def compare(
        self,
        base_result,
        transformed_result,
        relation
    ):
        ...

    def explain(
        self,
        comparison
    ):
        ...
```

---

# 74. Transformation Registry

All transformations should be registered.

```python id="b4grjr"
class TransformationRegistry:

    def register(self, transformation):
        ...

    def get(self, transformation_id):
        ...

    def validate(self, transformation):
        ...
```

---

# 75. Relation Registry

```python id="3wm8fh"
class RelationRegistry:

    def register(self, relation):
        ...

    def get(self, relation_id):
        ...

    def evaluate(self, relation, base, transformed):
        ...
```

---

# 76. Reproduction Manager

```python id="u7z0f7"
class ReproductionManager:

    def create_attempt(self, failure):
        ...

    def execute(self, attempt):
        ...

    def compare(self, original, reproduction):
        ...

    def classify(self, comparison):
        ...

    def summarize(self, failure):
        ...
```

---

# 77. Reproduction Summary

For each failure:

```yaml id="u6w6o4"
reproducibility_summary:
  failure_id:
  attempts:
  valid_attempts:
  reproduced:
  not_reproduced:
  inconclusive:
  reproduction_rate:
  stability_class:
  mechanism_match_rate:
```

---

# 78. Metamorphic Summary

```yaml id="qyrt8k"
metamorphic_summary:
  failure_id:
  tests:
  valid_tests:
  passed:
  violations:
  invalid:
  inconclusive:
  consistency_rate:
```

---

# 79. Reproduction and Metamorphic Evidence

Each result must reference:

```text id="e3z0gc"
base trace
transformed trace
comparison record
relation
invariant evaluations
state differences
cost records
```

---

# 80. Failure Family Validation

Metamorphic testing can strengthen failure families.

Example:

```text id="6v2x6a"
FAIL-001
FAIL-002
FAIL-003
       ↓
FAMILY-007
       ↓
Metamorphic transformations
       ↓
same mechanism persists
```

This provides evidence that the family is not merely tied to one exact scenario instance.

---

# 81. Metamorphic Family Generalization

A failure family may be considered metamorphically supported when multiple valid transformations preserve the observed mechanism.

This is distinct from hidden-holdout generalization.

---

# 82. Reproducibility vs Metamorphic Testing Matrix

| Property          | Reproducibility     | Metamorphic         |
| ----------------- | ------------------- | ------------------- |
| New execution     | Required            | Required            |
| Same scenario     | Usually             | No                  |
| Transformation    | No                  | Required            |
| Expected relation | Failure match       | Explicit relation   |
| Main question     | Does failure recur? | Does relation hold? |
| Seed variation    | Optional/important  | Optional            |
| Hidden holdout    | Separate            | Separate            |
| Cost              | Measured            | Measured            |

---

# 83. Combined Validation Workflow

The system may use:

```text id="jqu2ca"
Failure
  ↓
Reproduction
  ↓
Metamorphic Test
  ↓
Family Validation
  ↓
Holdout Evaluation
```

But each result must remain independently recorded.

---

# 84. Do Not Collapse Results

Avoid a single label such as:

```text id="8b0v7v"
"Genuine Defect = TRUE"
```

Instead record:

```yaml id="a2p2ce"
validation:
  original_failure: VALIDATED
  reproduced: true
  reproduction_rate: 0.75
  metamorphic_status: SUPPORTED
  holdout_status: NOT_TESTED
```

This preserves the evidence structure.

---

# 85. Reproduction Failure Analysis

When reproduction fails, compare:

```text id="i5l8wq"
original state
reproduction state
tool sequence
policy state
randomness
agent configuration
environment version
perturbation
```

The goal is to identify whether the difference comes from:

* stochasticity,
* environment state,
* evaluator error,
* configuration drift,
* actual failure instability.

---

# 86. Reproduction Divergence

The earliest divergence should be recorded where possible.

Example:

```yaml id="4d6s3x"
divergence:
  sequence_number: 12
  original_event: TOOL_REQUEST
  reproduction_event: AGENT_OUTPUT
  divergence_type: ACTION_SELECTION
```

This makes debugging much easier.

---

# 87. Metamorphic Divergence

For a metamorphic violation, record the earliest protected-property divergence.

Example:

```yaml id="n4hr3e"
divergence:
  property: authorization_decision
  base: DENY
  transformed: ALLOW
  event_sequence_base: 7
  event_sequence_transformed: 7
```

---

# 88. Metamorphic Test Cost

Record:

$$
C_{MT}
=
C_{base}
+
C_{transformed}
+
C_{comparison}
$$

If base execution is reused from an existing experiment, the experiment must explicitly state that accounting convention.

---

# 89. Reusing Existing Base Executions

A previously recorded base execution may be reused only when:

```text id="b2f5eu"
same scenario version
same agent configuration
same environment semantics
same relevant state
same required trace completeness
```

The reused execution must be referenced, not copied.

---

# 90. Transformation Budget

Metamorphic tests should support:

```yaml id="k9j8a7"
metamorphic:
  max_transformations_per_base: 5
  max_tests_per_failure: 10
  budget:
```

This prevents combinatorial explosion.

---

# 91. Transformation Explosion

If a base scenario has:

```text id="u0t5y4"
5 transformations
```

and each transformed scenario generates:

```text id="j3w2dp"
4 additional branches
```

the number of executions can grow rapidly.

Therefore transformation count must be explicitly bounded.

---

# 92. Transformation Selection

Initial transformation selection may be uniform.

Later, adaptive selection may prioritize:

```text id="r5j6z0"
high-information transformations
historically revealing transformations
low-cost transformations
transformations targeting weak invariants
```

This should be studied separately from the primary adaptive scenario-selection experiment.

---

# 93. Metamorphic Test Eligibility

A scenario is eligible when:

1. a valid transformation exists,
2. the transformation semantics are documented,
3. the expected relation is executable,
4. base execution is valid,
5. transformed execution can be isolated,
6. sufficient budget remains.

---

# 94. Metamorphic Transformation Validation

Before execution:

```text id="0g2c5p"
Base Scenario
     ↓
Apply Transformation
     ↓
Semantic Validation
     ↓
Expected relation defined
     ↓
Execute
```

If semantic validation fails:

```text id="83i3k2"
INVALID
```

---

# 95. Transformation Constraints

A transformation may declare:

```yaml id="7p8m6a"
constraints:
  preserve_identity: true
  preserve_authorization: true
  preserve_resource_class: true
  preserve_task_goal: true
  allow_resource_id_change: true
```

The validator checks these conditions.

---

# 96. Example Transformation Library

Initial library:

```text id="3h8jst"
MT01_FORMAT_NORMALIZATION
MT02_TASK_PARAPHRASE
MT03_IRRELEVANT_CONTEXT
MT04_SYNTHETIC_ID_RENAME
MT05_INPUT_ORDER_PERMUTATION
MT06_EQUIVALENT_TOOL_PARAMETER_ORDER
MT07_EQUIVALENT_DATA_REPRESENTATION
MT08_AUTHORIZATION_EQUIVALENT_RESOURCE
```

Only transformations with clearly defined semantics should be enabled.

---

# 97. Transformation Example: Formatting

Base:

```text id="8ph2ig"
"Retrieve customer C001."
```

Transformed:

```text id="8s3zkm"
"Retrieve customer C001"
```

Expected:

```text id="b8hl1m"
same authorization and tool behavior
```

---

# 98. Transformation Example: Identifier Renaming

Base:

```text id="2o6nse"
customer = C001
```

Transformed:

```text id="c8yq5d"
customer = C777
```

This is valid only when:

```text id="x9bq9j"
C001 and C777
```

are semantically equivalent for the tested property.

---

# 99. Transformation Example: Irrelevant Context

Base:

```text id="l4exz4"
task + relevant context
```

Transformed:

```text id="o5k2x9"
task + irrelevant synthetic information
```

Expected:

```text id="k9a5rt"
protected security property unchanged
```

---

# 100. Transformation Example: Sequence Permutation

Base:

```text id="8p4o7y"
independent observation A
independent observation B
```

Transformed:

```text id="d0l9hx"
observation B
observation A
```

Valid only when A and B are explicitly declared independent.

---

# 101. Metamorphic Relation Configuration

```yaml id="v9a6i8"
relation:
  relation_id: MR-AUTH-001
  version: "1.0"

  type: SECURITY_PROPERTY_PRESERVATION

  protected_properties:
    - authorization_decision
    - resource_access

  expected:
    authorization_decision: EQUIVALENT
    resource_access: EQUIVALENT
```

---

# 102. Relation Evaluation

The comparison engine should return structured evidence:

```yaml id="x6x9g7"
comparison:
  relation_id:
  property_results:
    - property: authorization_decision
      expected: EQUIVALENT
      observed: EQUIVALENT
      result: PASS

    - property: resource_access
      expected: EQUIVALENT
      observed: DIFFERENT
      result: FAIL

  overall_result: VIOLATION
```

---

# 103. Metamorphic Violation as Failure Candidate

A metamorphic violation may create a new failure candidate when:

```text id="w3e7kv"
transformation valid
+
base execution valid
+
transformed execution valid
+
protected relation violated
```

It must then pass the normal failure validation pipeline.

```text id="6x9a0e"
Metamorphic Violation
       ↓
Failure Candidate
       ↓
Invariant / Relation Evidence
       ↓
Failure Validation
```

---

# 104. Metamorphic Failure Classification

Metamorphic failures may be classified as:

```text id="w1g4yd"
ROBUSTNESS
POLICY
AUTHORIZATION
SECURITY
STATE_INTEGRITY
```

depending on the violated relation.

Do not classify every metamorphic violation as a generic robustness problem.

---

# 105. Reproducibility of Metamorphic Violations

A metamorphic violation should itself be reproducible where possible.

Workflow:

```text id="fr6b7a"
Base + Transform
      ↓
Relation Violation
      ↓
Independent Metamorphic Execution
      ↓
Same Relation Violation?
```

This provides stronger evidence.

---

# 106. Metamorphic Failure Family

Multiple metamorphic violations may belong to the same failure family if their normalized mechanism is equivalent.

Example:

```text id="g44g8t"
format change
identifier change
irrelevant context change
       ↓
same authorization bypass mechanism
       ↓
FAMILY-007
```

The transformations themselves should remain recorded.

---

# 107. Metamorphic Testing and Hidden Holdout

Metamorphic transformations may be applied to hidden holdout scenarios, but only according to the holdout protocol.

Do not use transformed holdout results to tune:

```text id="1sby5x"
transformation selection
relation thresholds
failure signatures
clustering weights
adaptive acquisition
```

before holdout evaluation is complete.

---

# 108. Hidden Holdout Separation

The system must maintain:

```text id="q7k7si"
Development Transformations
        │
        ├── Tune
        └── Validate

          HOLDOUT

Hidden Transformations
        │
        └── Evaluate only
```

---

# 109. Reproducibility Database Schema

Recommended tables:

```text id="0b70d4"
reproduction_attempts
reproduction_results
reproduction_evidence
reproduction_comparisons
reproduction_summaries
```

---

# 110. Metamorphic Database Schema

Recommended tables:

```text id="t1p5iy"
transformations
metamorphic_relations
metamorphic_tests
metamorphic_pairs
metamorphic_comparisons
metamorphic_results
```

---

# 111. Reproduction Attempt Schema

```yaml id="w6v7u8"
reproduction_attempt:
  reproduction_id:
  original_failure_id:

  mode:
  execution_id:

  seed:
  scenario_version:
  agent_config_id:
  environment_config_id:
  policy_config_id:

  status:
  cost:
```

---

# 112. Metamorphic Test Schema

```yaml id="0q8g2n"
metamorphic_test:
  test_id:

  base:
    scenario_id:
    execution_id:

  transformed:
    scenario_id:
    execution_id:

  transformation_id:
  relation_id:

  validity:
  result:

  comparison_id:
  cost:
```

---

# 113. Reproduction Summary Metrics

Report:

```text id="3r3rkm"
failure_count
attempt_count
valid_attempt_count
reproduced_count
not_reproduced_count
inconclusive_count
mean_reproduction_rate
family_reproduction_rate
stable_failure_count
variable_failure_count
flaky_failure_count
```

---

# 114. Metamorphic Summary Metrics

Report:

```text id="i9d7x0"
tests_created
valid_tests
invalid_tests
passed_relations
violated_relations
inconclusive_tests
metamorphic_consistency_rate
metamorphic_violation_rate
```

---

# 115. Metamorphic Consistency Rate

For valid metamorphic tests:

$$
MCR =
\frac{
Relations\ Satisfied
}{
Valid\ Metamorphic\ Tests
}
$$

This is not automatically an overall “agent quality score.”

It is a specific measurement under the defined transformation and relation set.

---

# 116. Metamorphic Violation Rate

$$
MVR =
\frac{
Relations\ Violated
}{
Valid\ Metamorphic\ Tests
}
$$

The denominator must exclude invalid transformations.

---

# 117. Transformation-Specific Metrics

Report consistency by transformation:

```text id="d0k5bh"
FORMAT_ONLY
TASK_PARAPHRASE
ID_RENAME
CONTEXT_CHANGE
SEQUENCE_PERMUTATION
```

This prevents aggregation from hiding transformation-specific behavior.

---

# 118. Relation-Specific Metrics

Similarly report:

```text id="h6qj3b"
AUTHORIZATION_PRESERVATION
SECURITY_PROPERTY_PRESERVATION
NON_INTERFERENCE
PERMUTATION_INVARIANCE
```

---

# 119. Cost-Normalized Metamorphic Testing

Because the project is budget-constrained, also measure:

$$
MetamorphicYield
=
\frac{
ValidatedMetamorphicViolations
}{
MetamorphicTestingCost
}
$$

This enables future comparison of transformation-selection strategies.

---

# 120. Reproduction Cost per Validated Failure

$$
CostPerReproducedFailure
=
\frac{
TotalReproductionCost
}{
ReproducedFailures
}
$$

Only valid reproduction attempts should be used in the denominator according to the experiment's predefined analysis protocol.

---

# 121. Failure Stability vs Cost

The experiment may analyze:

```text id="s7y1yb"
reproduction rate
        vs
reproduction cost
```

to determine how much additional budget is required to distinguish stable from flaky failures.

---

# 122. Statistical Analysis

For repeated experiments, report:

* mean,
* median,
* variance,
* confidence intervals where appropriate,
* per-seed results,
* distribution of reproduction rates.

Avoid reporting only aggregate averages.

---

# 123. Seed-Level Reporting

For each experiment seed:

```yaml id="v3q2qk"
seed_result:
  seed:
  failures:
  families:
  reproduced:
  metamorphic_violations:
  total_cost:
```

This makes stochastic variation visible.

---

# 124. Statistical Comparison

When comparing methods:

```text id="7j2l8r"
Random
Uniform
UCB-V
Cost-Aware UCB-V
Proposed Adaptive
```

reproducibility and metamorphic metrics should be evaluated under the same:

* agent,
* scenario pool,
* budget,
* validation rules,
* transformation set,
* reproduction protocol.

---

# 125. Ablation Studies

Recommended reproducibility/metamorphic ablations:

### RMT-A1

No reproduction validation.

### RMT-A2

Exact-seed reproduction only.

### RMT-A3

Independent-seed reproduction.

### RMT-A4

No metamorphic testing.

### RMT-A5

Single transformation category.

### RMT-A6

Multiple transformation categories.

### RMT-A7

State-based reproduction vs full replay.

These isolate the contribution of each validation mechanism.

---

# 126. Recommended Initial Reproduction Protocol

For the first implementation:

```text id="h8g2zz"
For each validated failure:

1. Freeze failure record.
2. Reconstruct original scenario.
3. Create fresh execution.
4. Use same agent/environment configuration.
5. Use independent execution instance.
6. Reapply required perturbation.
7. Execute.
8. Evaluate same invariant.
9. Compare normalized failure signature.
10. Record reproduction outcome.
```

For stochastic agents, add independent-seed attempts as a separate condition.

---

# 127. Recommended Initial Metamorphic Protocol

For selected validated failures:

```text id="b4j4eg"
1. Freeze base failure.
2. Select valid transformation.
3. Validate transformation semantics.
4. Execute base scenario.
5. Generate transformed scenario.
6. Execute transformed scenario independently.
7. Evaluate protected properties.
8. Compare outcomes.
9. Record relation result.
10. If violated, create failure candidate.
11. Validate the new candidate independently.
```

---

# 128. Minimum Transformation Set

The first implementation should begin with a small, well-defined set:

```text id="5h4p7j"
MT01 FORMAT_ONLY
MT02 SYNTHETIC_ID_RENAME
MT03 IRRELEVANT_CONTEXT
MT04 TASK_PARAPHRASE
```

Each transformation must have a formally defined expected relation.

Do not start with dozens of transformations whose semantics are vaguely “probably equivalent.” That is how testing turns into interpretive performance art.

---

# 129. Minimum Reproducibility Set

The first implementation should support:

```text id="h5u2r6"
Exact Replay
Independent Execution
Independent Seed Replay
State-Based Replay
```

This is sufficient to establish the core validation pipeline.

---

# 130. Recommended Repository Structure

```text id="3t6j3x"
src/
└── agent_eval/
    ├── validation/
    │   ├── __init__.py
    │   ├── reproduction.py
    │   ├── comparison.py
    │   ├── stability.py
    │   ├── evidence.py
    │   └── models.py
    │
    └── metamorphic/
        ├── __init__.py
        ├── models.py
        ├── transformations.py
        ├── registry.py
        ├── relations.py
        ├── relation_engine.py
        ├── executor.py
        ├── comparator.py
        └── validator.py
```

Tests:

```text id="1v3d0q"
tests/
├── validation/
│   ├── test_reproduction.py
│   ├── test_signature_match.py
│   ├── test_stability.py
│   └── test_replay.py
│
└── metamorphic/
    ├── test_transformations.py
    ├── test_relations.py
    ├── test_pair_execution.py
    ├── test_comparison.py
    └── test_invalid_transformations.py
```

---

# 131. Core Reproduction Interface

```python id="x8eq9q"
class ReproductionEngine:

    def create_attempt(
        self,
        failure,
        mode
    ):
        ...

    def execute_attempt(
        self,
        attempt
    ):
        ...

    def compare(
        self,
        original,
        reproduction
    ):
        ...

    def classify_result(
        self,
        comparison
    ):
        ...

    def summarize(
        self,
        failure
    ):
        ...
```

---

# 132. Core Metamorphic Interface

```python id="4v5t8n"
class MetamorphicEngine:

    def validate_transformation(
        self,
        scenario,
        transformation
    ):
        ...

    def transform(
        self,
        scenario,
        transformation
    ):
        ...

    def execute_pair(
        self,
        base,
        transformed
    ):
        ...

    def evaluate_relation(
        self,
        base_result,
        transformed_result,
        relation
    ):
        ...

    def summarize(
        self,
        tests
    ):
        ...
```

---

# 133. Reproduction Comparison Interface

```python id="j7x3fk"
class ReproductionComparator:

    def compare_invariants(
        self,
        original,
        reproduction
    ):
        ...

    def compare_signatures(
        self,
        original,
        reproduction
    ):
        ...

    def compare_states(
        self,
        original,
        reproduction
    ):
        ...

    def compare_sequences(
        self,
        original,
        reproduction
    ):
        ...
```

---

# 134. Metamorphic Comparison Interface

```python id="y9v2w7"
class MetamorphicComparator:

    def compare_property(
        self,
        base,
        transformed,
        property_definition
    ):
        ...

    def compare_state(
        self,
        base_state,
        transformed_state,
        expected_differences
    ):
        ...

    def evaluate(
        self,
        relation,
        base,
        transformed
    ):
        ...
```

---

# 135. Invariants for Reproducibility

### INV-REP-001

Every reproduction attempt must reference an original failure.

### INV-REP-002

A reproduction attempt must generate a new execution record.

### INV-REP-003

A reproduction result must reference new evidence.

### INV-REP-004

Invalid or errored attempts must not be counted as successful reproductions.

### INV-REP-005

Reproduction configuration must be recorded.

### INV-REP-006

The original failure must remain immutable.

### INV-REP-007

Stochastic variation must not be hidden by a single deterministic replay.

---

# 136. Invariants for Metamorphic Testing

### INV-MT-001

Every metamorphic test must have a base scenario.

### INV-MT-002

Every metamorphic test must have a defined transformation.

### INV-MT-003

Every transformation must have an explicit expected semantic relation.

### INV-MT-004

Base and transformed executions must be independently recorded.

### INV-MT-005

A transformation must be validated before its result is interpreted.

### INV-MT-006

Metamorphic results must be derived from actual execution outcomes.

### INV-MT-007

Invalid transformations must not create failure records.

### INV-MT-008

Metamorphic comparisons must evaluate declared protected properties.

### INV-MT-009

Hidden holdout transformations must not influence development tuning.

---

# 137. Combined Validation Invariants

### INV-VAL-001

A failure cannot be marked reproduced without an independent valid execution.

### INV-VAL-002

A metamorphic violation cannot be marked valid without a valid transformation.

### INV-VAL-003

Evaluator errors cannot be counted as agent failures.

### INV-VAL-004

Reproduction and metamorphic results must retain their original evidence.

### INV-VAL-005

Validation costs must be included in the relevant budget.

### INV-VAL-006

Validation results must remain linked to their experiment version.

---

# 138. Testing Requirements

The subsystem must test:

### Reproducibility

* exact replay,
* independent replay,
* seed variation,
* state restoration,
* wrong configuration,
* missing evidence,
* evaluator error.

### Metamorphic Testing

* valid transformation,
* invalid transformation,
* equivalent outcome,
* relation violation,
* expected difference,
* unexpected difference,
* malformed relation,
* transformation reproducibility.

### Integration

* failure → reproduction,
* failure → metamorphic test,
* metamorphic violation → failure validation,
* family → reproduction,
* family → holdout.

---

# 139. Synthetic Reproducibility Dataset

Before real agent experiments, construct deterministic synthetic scenarios.

Example:

```text id="xg5m1y"
Scenario S01
  deterministic authorization failure

Replay 1
  FAIL

Replay 2
  FAIL

Replay 3
  FAIL
```

Expected:

```text id="gq8r6f"
STABLE
```

Then introduce controlled randomness:

```text id="9c5y4k"
Failure probability varies by seed
```

Expected:

```text id="j7x3o0"
VARIABLE or FLAKY
```

according to the defined thresholds.

---

# 140. Synthetic Metamorphic Dataset

Construct known relations.

Example:

```text id="3o8e9v"
Base:
authorized read

Transformation:
whitespace variation

Expected:
same authorization result
```

Then construct an intentionally invalid transformation:

```text id="8f3y7p"
Base:
authorized read

Transformation:
change identity to unauthorized user

Expected:
transformation rejected as non-equivalent
```

This validates the transformation validator.

---

# 141. Reproduction Failure Taxonomy

When reproduction differs from the original, classify divergence as:

```text id="r8q2g6"
STOCHASTIC_VARIATION
CONFIGURATION_DRIFT
ENVIRONMENT_DRIFT
STATE_DRIFT
PERTURBATION_MISMATCH
AGENT_BEHAVIOR_CHANGE
EVALUATOR_ERROR
INFRASTRUCTURE_ERROR
UNKNOWN
```

This classification is diagnostic and should not be confused with the original failure category.

---

# 142. Metamorphic Violation Taxonomy

Possible causes:

```text id="n1d4ca"
SEMANTIC_SENSITIVITY
UNEXPECTED_CONTEXT_SENSITIVITY
AUTHORIZATION_INCONSISTENCY
POLICY_INCONSISTENCY
STATE_INCONSISTENCY
TOOL_SELECTION_INCONSISTENCY
ROBUSTNESS_FAILURE
UNKNOWN
```

These are hypotheses supported by observed differences, not automatic causal claims.

---

# 143. Reporting Reproducibility

Final research reports should include:

```text id="7x8w9b"
validated failures
reproduction attempts
reproduced failures
reproduction rate
stability categories
reproduction cost
reproduction protocol
```

---

# 144. Reporting Metamorphic Testing

Final reports should include:

```text id="v0k8z5"
valid metamorphic tests
transformations used
relations tested
relation violations
consistency rate
transformation-specific results
cost
invalid transformation count
```

---

# 145. Example Final Validation Table

| Failure  | Family | Reproduction Rate | Stability      | Metamorphic Result | Holdout     |
| -------- | ------ | ----------------: | -------------- | ------------------ | ----------- |
| FAIL-001 | F-001  |              1.00 | Stable         | Supported          | Generalized |
| FAIL-002 | F-001  |              0.67 | Variable       | Supported          | Not tested  |
| FAIL-003 | F-002  |              0.00 | Non-reproduced | Inconclusive       | Not tested  |

These values are illustrative schema examples only, not project results.

---

# 146. Evidence Maturity

The platform should represent evidence maturity as:

```text id="5l8x5a"
OBSERVED
   ↓
VALIDATED
   ↓
REPRODUCED
   ↓
METAMORPHICALLY_SUPPORTED
   ↓
GENERALIZED
```

A failure may stop at any stage.

The system must not imply that every observed failure will reach the final stage.

---

# 147. Evidence Interpretation

### Observed

A violation occurred.

### Validated

Evidence and evaluator conditions support the violation.

### Reproduced

Independent execution reproduced the mechanism.

### Metamorphically Supported

The mechanism survives valid controlled transformations.

### Generalized

The mechanism appears on previously unseen scenarios under the holdout protocol.

These are distinct claims.

---

# 148. Experimental Comparison

When comparing adaptive methods, all methods should use the same:

```text id="w3n8x7"
reproduction protocol
metamorphic transformation library
relation definitions
failure validation rules
holdout protocol
```

Only the discovery/selection mechanism should vary in the primary comparison.

---

# 149. No Post-Hoc Transformation Selection

Do not inspect a failure and then invent a transformation designed specifically to preserve it, unless the experiment explicitly defines this as an exploratory analysis.

For confirmatory evaluation, transformations should be predeclared.

---

# 150. No Post-Hoc Reproduction Rules

Do not change:

```text id="o0x8e3"
reproduction threshold
signature similarity threshold
stability definition
```

after seeing the final outcomes without recording the change as a separate analysis.

---

# 151. Configuration Example

```yaml id="c3b8r9"
validation:
  reproducibility:
    enabled: true

    modes:
      - EXACT_REPLAY
      - INDEPENDENT_SEED
      - STATE_REPLAY

    attempts:
      exact: 1
      independent_seed: 3

    mechanism_match_threshold: 0.80


  metamorphic:
    enabled: true

    max_transformations_per_failure: 4

    transformations:
      - MT01_FORMAT_ONLY
      - MT02_SYNTHETIC_ID_RENAME
      - MT03_IRRELEVANT_CONTEXT
      - MT04_TASK_PARAPHRASE

    relations:
      - MR001_SECURITY_PROPERTY_PRESERVATION
      - MR002_NON_INTERFERENCE
```

The numerical thresholds above are initial configuration placeholders and must be calibrated through the experimental methodology rather than presented as established values.

---

# 152. End-to-End Validation Workflow

```text id="4m4d1a"
                  VALIDATED FAILURE
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      REPRODUCIBILITY          METAMORPHIC
          TESTING                TESTING
             │                       │
       New Execution           Base Execution
             │                       │
       New Evidence           Transformation
             │                       │
       Mechanism Match        Transformed Execution
             │                       │
             ▼                       ▼
       Reproduction           Relation Evaluation
          Result                    Result
             │                       │
             └───────────┬───────────┘
                         ▼
                  Failure Family
                         │
                         ▼
                 Hidden Holdout
                         │
                         ▼
                  Final Evidence
```

---

# 153. Definition of Done

The Reproducibility & Metamorphic Testing subsystem is complete enough for the first research experiment when:

* [ ] Failures can be frozen before validation.
* [ ] Independent reproduction executions can be created.
* [ ] Reproduction configuration is recorded.
* [ ] Fresh traces are generated for reproduction attempts.
* [ ] Reproduction evidence is independently evaluated.
* [ ] Failure mechanisms can be compared.
* [ ] Reproduction outcomes are classified.
* [ ] Reproduction rates can be calculated.
* [ ] Stability categories can be assigned.
* [ ] Flaky failures are preserved.
* [ ] Reproduction costs are measured.
* [ ] Transformations can be registered.
* [ ] Transformations have explicit semantics.
* [ ] Metamorphic relations can be registered.
* [ ] Base and transformed executions are separately recorded.
* [ ] Protected properties can be compared.
* [ ] Metamorphic violations can be detected.
* [ ] Invalid transformations are rejected.
* [ ] Metamorphic violations can enter normal failure validation.
* [ ] Metamorphic tests have explicit costs.
* [ ] Hidden holdout information remains isolated.
* [ ] Reproduction and metamorphic results are versioned.
* [ ] Dashboard results are derived from actual validation data.
* [ ] Synthetic tests demonstrate that the subsystem works before expensive experiments begin.

---

# 154. Final Architecture

The subsystem architecture is:

```text id="4t0jks"
                         FAILURE
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        Reproduction Manager    Metamorphic Manager
                 │                     │
                 ▼                     ▼
        Independent Replay       Transformation
                 │                     │
                 ▼                     ▼
             New Trace           Transformed Scenario
                 │                     │
                 ▼                     ▼
        Invariant Evaluation    Transformed Execution
                 │                     │
                 ▼                     ▼
       Mechanism Comparison     Relation Evaluation
                 │                     │
                 └──────────┬──────────┘
                            ▼
                    Validation Results
                            │
                            ▼
                     Failure Family
                            │
                            ▼
                     Holdout Testing
                            │
                            ▼
                   Research Metrics
```

---

# 155. Final Design Principles

The Reproducibility & Metamorphic Testing subsystem shall follow these principles:

1. **A failure must be independently reproduced, not merely replayed from stored output.**
2. **Reproduction must generate new execution evidence.**
3. **The reproduction protocol must be explicit and versioned.**
4. **Exact replay and independent-seed replay answer different questions.**
5. **Failure instability must be measured rather than hidden.**
6. **Flaky failures must not automatically be discarded.**
7. **Metamorphic testing requires an explicit transformation.**
8. **Every transformation must have a documented semantic assumption.**
9. **Every metamorphic test requires an explicit expected relation.**
10. **Base and transformed scenarios must actually execute independently.**
11. **Textual similarity must not be mistaken for behavioral equivalence.**
12. **Protected security and reliability properties should be compared structurally.**
13. **Invalid transformations must not generate failures.**
14. **Metamorphic violations must pass the normal failure-validation pipeline.**
15. **Reproduction and metamorphic testing are separate evidence layers.**
16. **Hidden-holdout results must never tune development validation rules before evaluation is complete.**
17. **Validation costs count toward the experiment budget.**
18. **All validation outcomes must preserve trace, state, configuration, and provenance links.**
19. **A reproduced failure is stronger evidence, not automatically a proven root cause.**
20. **All displayed reproduction and metamorphic metrics must come from actual experiment records.**

---

# 156. Final Specification Boundary

The subsystem can be summarized as:

### Reproducibility

$$
\boxed{
Failure
\rightarrow
Independent\ Execution
\rightarrow
Same\ Mechanism?
}
$$

### Metamorphic Testing

$$
\boxed{
Base
\xrightarrow{T}
Transformed
\rightarrow
Expected\ Relation?
}
$$

### Combined Evidence

$$
\boxed{
Observed
\rightarrow
Validated
\rightarrow
Reproduced
\rightarrow
Metamorphically\ Supported
\rightarrow
Generalized
}
$$

The central research principle is:

> **A failure becomes stronger evidence when it survives independent execution and valid behavioral transformations, but each validation stage must remain explicitly measured, independently evidenced, and distinguishable from the others.**
