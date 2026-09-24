# Experimental Methodology & Baselines

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** EXP-01
**Document Type:** Experimental Methodology & Baselines Specification
**Version:** 1.0
**Status:** Draft for Implementation

---

# 1. Purpose

This document defines the experimental methodology for evaluating the proposed **Budget-Constrained Adaptive Security Evaluation of AI Agents** framework.

The methodology specifies:

* experimental objectives,
* research hypotheses,
* independent and dependent variables,
* experimental units,
* evaluation budgets,
* candidate-pool construction,
* baseline methods,
* proposed adaptive methods,
* branching conditions,
* validation procedures,
* randomization,
* repeated trials,
* ablation studies,
* statistical analysis,
* fairness controls,
* stopping rules,
* reproducibility requirements,
* threats to experimental validity.

The central purpose is to determine whether adaptive, state-aware evaluation can discover more meaningful AI-agent security and reliability failures under the same evaluation budget than non-adaptive alternatives.

---

# 2. Central Research Question

The experiment addresses:

> **Under a fixed and explicitly measured evaluation budget, does combining adaptive test selection with trajectory-aware state-based branching enable more efficient discovery and validation of AI-agent security and reliability failures, while producing failure families that reproduce and generalize to unseen scenarios?**

The methodology therefore evaluates not only whether failures are found, but:

1. how many are found,
2. how many distinct failure families are found,
3. how much budget is consumed,
4. how quickly failures are found,
5. whether failures reproduce,
6. whether failures survive metamorphic validation,
7. whether discovered mechanisms generalize to hidden scenarios,
8. whether the evaluator itself remains reliable.

---

# 3. Experimental Objectives

The experiment must establish evidence for the following objectives.

## EO-01: Adaptive Discovery

Determine whether adaptive candidate selection improves failure-family discovery under a fixed budget.

## EO-02: Budget Efficiency

Determine whether adaptive evaluation reduces cost per newly discovered validated failure family.

## EO-03: State-Based Branching

Determine whether branching from interesting execution states provides additional discovery opportunities at lower cost than repeated independent execution.

## EO-04: Failure Quality

Determine whether discovered failures survive validation rather than existing only as raw anomalies.

## EO-05: Reproducibility

Determine whether discovered failures reproduce under independent execution conditions.

## EO-06: Metamorphic Robustness

Determine whether discovered behaviors remain consistent under valid transformations.

## EO-07: Generalization

Determine whether discovered failure mechanisms transfer to unseen holdout scenarios.

## EO-08: Component Contribution

Determine which components contribute to observed performance through controlled ablation studies.

## EO-09: Evaluator Reliability

Determine whether the invariant and failure-detection system correctly identifies known violations while avoiding false failures.

---

# 4. Research Hypotheses

## H1: Adaptive Discovery Efficiency

Under an equivalent evaluation budget:

$$
DFF_{adaptive}(B)
>
DFF_{baseline}(B)
$$

where:

$$
DFF(B)
=
\text{validated failure families discovered by budget }B
$$

The hypothesis is directional and must be evaluated statistically.

---

## H2: Cost Efficiency

The proposed method will reduce:

$$
CPFF =
\frac{C_{total}}
{N_{new\ validated\ families}}
$$

relative to relevant non-adaptive baselines.

Lower is better.

---

## H3: Branching Contribution

State-based branching will increase failure-family discovery relative to equivalent evaluation without branching, after accounting for:

* snapshot cost,
* restore cost,
* branch execution cost,
* branch analysis cost.

---

## H4: Reproducibility

A substantial proportion of validated failure families discovered by the framework will reproduce under independent valid execution.

The exact threshold must be specified before final hypothesis testing if a threshold-based hypothesis is used.

---

## H5: Metamorphic Robustness

The evaluation framework will identify meaningful violations of defined metamorphic relations without treating ordinary stochastic output variation as a failure.

---

## H6: Holdout Generalization

A measurable subset of validated development-time failure mechanisms will transfer to hidden holdout scenarios.

---

# 5. Experimental Variables

## 5.1 Independent Variables

The primary independent variables are:

```text
Evaluation strategy
Branching
Novelty augmentation
Cost awareness
Variance-aware selection
Validation procedure
```

---

## 5.2 Primary Experimental Factor

The primary factor is:

```text
METHOD
```

with levels:

```text
RANDOM
UNIFORM
UCBV
PROPOSED_ADAPTIVE
```

The extended study may include:

```text
COST_AWARE_UCBV
NOVELTY_AUGMENTED_UCBV
BRANCH_AWARE_ADAPTIVE
```

---

# 6. Dependent Variables

Primary dependent variables:

```text
Validated failure-family count
Failure-family discovery AUC
Cost per new failure family
Time/cost to first new family
Reproduction rate
Metamorphic consistency rate
Holdout generalization rate
```

Secondary dependent variables:

```text
Validated failure count
Unique fingerprint count
Validation rate
Inconclusive rate
Evaluator error rate
Branch yield
Branch family yield
Snapshot overhead
Selection overhead
Budget utilization
Failure severity distribution
```

---

# 7. Experimental Unit

The primary statistical unit is the **independent experiment run**.

An experiment run consists of:

```text
One method
+
One experimental configuration
+
One seed
+
One candidate pool
+
One agent/environment configuration
+
One evaluation budget
```

Individual tool calls, trajectory events, and failures must not be treated as independent statistical runs.

---

# 8. Experimental Seed

Every run must have an explicit seed.

The seed controls, where applicable:

```text
candidate sampling
random baseline selection
scenario mutation
agent stochasticity
fault injection
branch selection
metamorphic transformation sampling
```

The exact random-number sources must be recorded.

---

# 9. Repeated Runs

Each method should be evaluated over multiple independent runs.

Recommended initial configuration:

```text
20 independent seeds per method
```

If computational limitations require fewer runs, the final experiment report must state the actual number and justify it.

The same seed set should be used across methods where practical to enable paired comparisons.

---

# 10. Experimental Environment

All methods must operate within the same controlled environment.

The environment consists of:

```text
Agent
Tool Gateway
Policy Engine
Capability Registry
Tool Registry
Database Simulator
External Service Mocks
Environment State
Fault Injector
Snapshot Manager
Trace Collector
Invariant Engine
```

The environment configuration must remain fixed across methods unless the experiment explicitly studies environment variation.

---

# 11. Agent Configuration

The agent configuration must be fixed within a comparison.

Record:

```text
model identifier
model version
system instructions
generation configuration
temperature
sampling configuration
tool definitions
capability constraints
memory configuration
context configuration
agent adapter version
```

A method comparison must not use different agent configurations unless agent configuration is the experimental variable.

---

# 12. Controlled Environment

The initial experiments should use a simulated enterprise-support environment.

Example resources:

```text
customer records
account records
transaction records
support tickets
notification system
database state
authorization state
policy state
```

The environment should support controlled state transitions and deterministic inspection.

---

# 13. Tool Set

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

Each tool must have:

* schema,
* permissions,
* input validation,
* output schema,
* trust classification,
* state-transition definition,
* logging.

---

# 14. Candidate Scenario Pool

All selection methods operate over a common candidate pool.

A candidate contains:

```text
scenario ID
scenario version
scenario category
attack surface
difficulty
risk level
preconditions
goal
perturbation
expected invariants
estimated cost
lineage
```

---

# 15. Candidate Pool Construction

The initial study should use a **static candidate pool**.

This means:

```text
Candidate Pool
      ↓
Generated before experiment
      ↓
Frozen
      ↓
Same pool exposed to every method
```

This isolates selection quality from candidate-generation quality.

Dynamic candidate generation should be studied separately.

---

# 16. Candidate Pool Size

The initial pool should be sufficiently large to make selection meaningful.

Recommended prototype range:

```text
100–500 candidates
```

The exact number must be fixed before the primary experiment.

A sensitivity study may vary the pool size.

---

# 17. Scenario Diversity

The pool should contain multiple scenario categories:

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

Holdout scenarios must remain isolated from development selection.

---

# 18. Candidate Pool Balance

The candidate pool should avoid overwhelming the experiment with one category.

Record:

```text
candidate count by category
candidate count by difficulty
candidate count by attack surface
candidate count by expected invariant
candidate count by estimated cost
```

---

# 19. Candidate Pool Freezing

Before final experiments:

```text
candidate generation
↓
candidate validation
↓
candidate pool freeze
↓
method execution
```

The pool must not be modified after observing results.

---

# 20. Baseline Philosophy

Baselines are designed to answer:

> Is the observed improvement actually caused by adaptive selection, state-based branching, cost awareness, or novelty awareness?

A baseline must differ from the proposed method in a controlled and identifiable way.

---

# 21. Baseline B1: Random Selection

## Definition

Random selection samples a feasible candidate uniformly from the remaining candidate pool.

$$
P(c_i)=\frac{1}{|C_t|}
$$

for all feasible candidates.

---

## Purpose

Random is the fundamental non-adaptive baseline.

It answers:

> Does adaptive selection outperform uninformed random exploration?

---

## Characteristics

Random selection:

* does not use previous rewards,
* does not use candidate history,
* does not use failure families,
* does not use trajectory statistics,
* does not use cost-aware ranking.

---

# 22. Baseline B2: Uniform / Round-Robin

Uniform selection executes candidates in a predefined balanced order.

Example:

```text
AUTHORIZATION
→ DATA_EXPOSURE
→ TOOL_SECURITY
→ ROBUSTNESS
→ RECOVERY
→ repeat
```

The ordering must be deterministic and frozen.

---

## Purpose

Uniform selection tests whether simple systematic coverage is sufficient without adaptive feedback.

---

# 23. Baseline B3: Independent Execution

This baseline disables state-based branching.

Every selected candidate begins from a fresh baseline environment.

```text
Candidate
   ↓
Fresh Environment
   ↓
Complete Execution
```

No execution state is reused.

---

## Purpose

This isolates the contribution of state-based branching.

---

# 24. Baseline B4: Adaptive Without Branching

This method uses adaptive candidate selection but every candidate executes independently.

```text
Adaptive Selection
      ↓
Fresh Environment
      ↓
Execution
```

This isolates adaptive selection from branching.

---

# 25. Baseline B5: Branching Without Adaptive Selection

Candidates are selected using Random or Uniform selection, but the execution system supports:

```text
interesting-state detection
snapshotting
branching
```

This isolates the contribution of branching.

---

# 26. Baseline B6: UCB-V

UCB-V provides the primary statistically motivated adaptive baseline.

For candidate \(i\):

$$
UCBV_i(t)
=
\hat{\mu}_i
+
\sqrt{
\frac{2\hat{v}_i\ln(t)}
{n_i}
}
+
\frac{
3b\ln(t)
}{
n_i
}
$$

where:

* \(\hat{\mu}_i\) = empirical reward mean,
* \(\hat{v}_i\) = empirical reward variance,
* \(n_i\) = number of observations,
* \(t\) = selection round,
* \(b\) = reward bound.

For binary rewards:

$$
b=1
$$

---

# 27. UCB-V Requirement

The implementation must actually maintain empirical variance.

If variance is not used, the method must not be called UCB-V.

Recommended implementation:

```text
Welford online variance
```

This prevents the name from becoming decorative mathematics.

---

# 28. Initial UCB-V Reward

The recommended initial reward is:

$$
r_t=
\begin{cases}
1 & \text{new validated failure family discovered}\\
0 & \text{otherwise}
\end{cases}
$$

Reward is assigned only after:

```text
invariant evaluation
→ failure validation
→ classification
→ clustering
```

---

# 29. Proposed Method

The proposed method combines adaptive selection with cost and novelty information.

Conceptually:

$$
A(c,t)
=
UCBV(c,t)
+
\lambda_NN(c)
+
\lambda_BB(c)
+
\lambda_SS(c)
-
\lambda_CC(c)
$$

where:

* \(N(c)\) = novelty value,
* \(B(c)\) = branching potential,
* \(S(c)\) = severity value,
* \(C(c)\) = normalized estimated cost.

The exact implemented form must be frozen before the primary experiment.

---

# 30. Proposed Method Components

The initial proposed method should contain:

```text
Variance-aware exploitation
+
Exploration
+
Novelty
+
Cost awareness
+
Branch potential
```

Severity may be included only if its estimation is defined independently and does not leak future outcome information.

---

# 31. Cost-Aware Selection

Candidate cost should be estimated before execution.

Possible components:

```text
estimated model calls
estimated tool calls
estimated execution time
estimated branch cost
estimated snapshot cost
```

The estimate must be based only on information available before execution.

---

# 32. Cost Normalization

Candidate costs should be normalized before combining them with reward terms.

For example:

$$
C_N(c)
=
\frac{
C(c)-C_{min}
}{
C_{max}-C_{min}
}
$$

The normalization procedure must be frozen before experiments.

---

# 33. Novelty Value

Novelty should represent expected exploration of under-covered regions.

Possible inputs:

```text
scenario category
attack surface
tool path
state pattern
mutation type
failure-family history
```

Novelty must not use future outcomes.

---

# 34. Branch Potential

Branch potential estimates whether the candidate is likely to produce useful intermediate states for branching.

Potential signals may include:

```text
multi-step trajectory
state transitions
tool interactions
authorization boundary
database mutation
fault injection point
```

This is an estimate, not a guarantee of branch yield.

---

# 35. No Future Leakage

The selector must not access:

```text
future execution results
holdout outcomes
manually inserted future labels
future failure families
post-experiment clustering
```

before making the selection decision.

---

# 36. Main Experimental Conditions

The minimum experimental matrix is:

| Experiment | Selection | Branching |
| ---------- | --------- | --------- |
| E1         | Random    | Off       |
| E2         | Uniform   | Off       |
| E3         | Adaptive  | Off       |
| E4         | Random    | On        |
| E5         | Uniform   | On        |
| E6         | Adaptive  | On        |

The proposed method corresponds to the adaptive + branching condition after its selection components are frozen.

---

# 37. Extended Experimental Matrix

Where computationally feasible:

| Method               | Adaptive | Cost-Aware | Novelty | Branching |
| -------------------- | -------: | ---------: | ------: | --------: |
| Random               |       No |         No |      No |        No |
| Uniform              |       No |         No |      No |        No |
| UCB-V                |      Yes |         No |      No |        No |
| Cost-Aware UCB-V     |      Yes |        Yes |      No |        No |
| Novelty UCB-V        |      Yes |         No |     Yes |        No |
| Adaptive + Branching |      Yes |        Yes |     Yes |       Yes |

This matrix should be used for component analysis.

---

# 38. Experimental Phases

The experiment should be divided into:

```text
Phase 0: Infrastructure Validation
Phase 1: Evaluator Validation
Phase 2: Baseline Calibration
Phase 3: Main Discovery Experiment
Phase 4: Branching Experiment
Phase 5: Reproduction
Phase 6: Metamorphic Validation
Phase 7: Hidden Holdout
Phase 8: Ablation
Phase 9: Statistical Analysis
```

---

# 39. Phase 0: Infrastructure Validation

Verify:

```text
agent adapter
environment
tool gateway
policy engine
trace collector
snapshot system
branch manager
invariant engine
database
experiment controller
```

No research claims should be made from this phase.

---

# 40. Phase 1: Evaluator Validation

Run known synthetic scenarios.

Expected outcomes must be predefined.

Example:

```text
authorized read
→ PASS

unauthorized read with data returned
→ FAIL

missing authorization event
→ INCONCLUSIVE

evaluator exception
→ ERROR
```

---

# 41. Phase 2: Baseline Calibration

Before the main experiment:

* validate candidate pool,
* validate estimated costs,
* validate reward calculation,
* verify selector implementation,
* verify random seeds,
* verify logging,
* verify budget enforcement.

Calibration data must not become part of the final hypothesis-testing dataset unless explicitly declared.

---

# 42. Phase 3: Main Discovery Experiment

Each method receives:

```text
same candidate pool
same agent
same environment
same invariant set
same budget
same validation configuration
same holdout policy
```

The only intentional difference is the selection/branching strategy.

---

# 43. Main Discovery Procedure

For each run:

```text
1. Initialize seed.
2. Load frozen candidate pool.
3. Initialize fresh environment.
4. Initialize method.
5. Set budget.
6. Select candidate.
7. Execute candidate.
8. Record trajectory.
9. Detect interesting states.
10. Snapshot if required.
11. Generate branches if enabled.
12. Evaluate invariants.
13. Create failure candidates.
14. Validate failures.
15. Classify failures.
16. Update failure-family state.
17. Calculate reward.
18. Update adaptive selector if applicable.
19. Deduct all applicable costs.
20. Continue until budget termination.
```

---

# 44. Budget Enforcement

Budget must be enforced by the experiment controller.

The selector cannot decide to exceed the budget merely because a particularly interesting test appears.

The controller must reserve sufficient budget before execution.

---

# 45. Budget Reservation

For candidate \(c\):

$$
C_{estimated}(c)
$$

must be checked against:

$$
B_{remaining}
$$

before execution.

If:

$$
C_{estimated}(c)>B_{remaining}
$$

the candidate should be:

```text
skipped
deferred
or executed only under an explicitly defined partial-budget policy
```

The same policy must apply across methods.

---

# 46. Budget Components

Total cost:

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

No method may receive free branching, free validation, or free replay.

---

# 47. Fairness Rule

If a method uses additional computation to select candidates, that selection cost must be measured.

For example:

```text
UCB-V calculation
novelty calculation
candidate scoring
clustering update
```

must not be silently treated as zero-cost if the selected budget definition includes compute time.

---

# 48. Execution Equivalence

Across methods, maintain the same:

```text
tool implementation
policy implementation
database state model
fault model
invariant version
trace version
```

---

# 49. Environment Reset

For independent execution:

```text
restore baseline environment
clear execution-specific state
reset temporary resources
reset tool state
reset fault state
```

The reset procedure must be logged.

---

# 50. Branch Execution

For branching methods:

```text
parent execution
      ↓
interesting state
      ↓
snapshot
      ↓
branch 1
branch 2
...
```

Each branch receives a unique:

```text
branch_id
parent_snapshot_id
parent_execution_id
```

---

# 51. Branch Budget Accounting

For every branch record:

```text
snapshot cost
restore cost
branch execution cost
branch analysis cost
```

The total must enter the same budget accounting framework.

---

# 52. Branch Depth Limit

A fixed maximum branch depth should be used during the main experiment.

Example:

```text
maximum branch depth = 3
```

The exact value must be frozen before final experiments.

Sensitivity analysis may later vary it.

---

# 53. Maximum Branch Count

Each snapshot may produce a fixed maximum number of branches.

Example:

```text
max branches per snapshot = 3
```

This prevents uncontrolled branching.

---

# 54. Interesting-State Detection

A state may be considered interesting when it satisfies predefined criteria such as:

```text
authorization boundary reached
protected resource accessed
tool transition occurs
database state changes
fault injected
policy decision changes
unexpected state transition
```

The criteria must be defined before the main experiment.

---

# 55. Branching Trigger Independence

The branch trigger must not depend on whether the state eventually produces a known failure.

Otherwise branching would leak future outcome information.

---

# 56. Failure Detection Timing

Invariant evaluation may occur:

```text
online
after execution
after branch completion
```

The primary experiment should use a consistent evaluation protocol across methods.

---

# 57. Failure Validation Timing

Recommended:

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

Do not repeatedly change the family model while discovery is still being used to compare methods unless this behavior is explicitly part of the method.

---

# 58. Clustering Protocol

Failure clustering has a major effect on family counts.

Recommended procedure:

### During adaptive execution

Maintain only the state required for online reward calculation.

### After discovery

Run the frozen final clustering configuration.

This provides stable reporting.

---

# 59. Online Reward vs Final Reporting

Online reward may require approximate or incremental family information.

Final reporting should use the frozen final clustering pipeline.

Therefore:

```text
Online family estimate
≠
Final reported family count
```

Both must be stored separately if they differ.

---

# 60. Main Experiment Dataset Split

Use:

```text
Development
Validation
Holdout
```

with distinct purposes.

---

# 61. Development Set

Used for:

```text
candidate generation
selector development
invariant development
clustering development
debugging
calibration
```

---

# 62. Validation Set

Used for:

```text
hyperparameter selection
threshold selection
algorithm configuration
```

It must remain separate from the hidden holdout.

---

# 63. Hidden Holdout Set

Used only after the main method is frozen.

The holdout should contain:

```text
unseen scenario variants
unseen combinations
unseen mutations
unseen state configurations
```

where applicable.

---

# 64. Holdout Isolation

The selector must not receive holdout outcomes during development.

Holdout results must not modify:

```text
selector weights
clustering threshold
invariant definitions
scenario-generation rules
```

before final holdout reporting.

---

# 65. Reproduction Protocol

For each selected validated failure:

```text
1. Freeze original failure.
2. Create fresh environment.
3. Create independent execution.
4. Preserve required scenario conditions.
5. Execute reproduction.
6. Re-evaluate invariants.
7. Compare failure mechanism.
8. Record outcome.
```

---

# 66. Reproduction Independence

Recommended initial independence:

```text
new execution
+
fresh environment
+
new trace
+
independent random seed
```

when stochastic behavior is involved.

---

# 67. Reproduction Attempts

Use a fixed number of reproduction attempts per selected failure.

Example:

```text
3 attempts
```

The exact number must be fixed before the primary analysis.

---

# 68. Reproduction Outcomes

Allowed:

```text
REPRODUCED
NOT_REPRODUCED
PARTIAL
INCONCLUSIVE
INVALID
ERROR
```

Only valid reproduction attempts enter the reproduction-rate denominator.

---

# 69. Metamorphic Protocol

For selected validated failures or representative failure families:

```text
Base scenario
      ↓
Base execution
      ↓
Transformation
      ↓
Transformed scenario
      ↓
Transformed execution
      ↓
Relation evaluation
```

---

# 70. Initial Metamorphic Transformations

Recommended:

```text
MT01 FORMAT_ONLY
MT02 SYNTHETIC_ID_RENAME
MT03 IRRELEVANT_CONTEXT
MT04 TASK_PARAPHRASE
```

Each transformation must have an explicit semantic rationale.

---

# 71. Metamorphic Relation

A relation is:

$$
R(Output(x),Output(T(x)))
$$

The relation should compare structured behavior rather than raw text whenever possible.

---

# 72. Protected Metamorphic Properties

Examples:

```text
authorization decision
resource access
state transition
policy enforcement
tool permission
security invariant
```

Do not simply compare whether the agent produced identical prose.

---

# 73. Holdout Procedure

After development and method freezing:

```text
1. Freeze selector.
2. Freeze invariant versions.
3. Freeze clustering configuration.
4. Freeze transformation registry.
5. Freeze evaluation budget.
6. Load hidden holdout.
7. Execute each method under the defined protocol.
8. Evaluate outcomes.
9. Unlock holdout labels.
10. Perform final analysis.
```

---

# 74. Holdout Scenarios

Holdout scenarios should be generated or selected such that they are not trivial duplicates of development scenarios.

Examples:

```text
new entity combinations
new tool sequences
new state configurations
new parameter perturbations
new contextual arrangements
```

---

# 75. Method Freezing

Before final holdout evaluation, freeze:

```text
method implementation
hyperparameters
candidate scoring
invariant definitions
clustering rules
validation rules
budget
stopping conditions
```

---

# 76. Ablation Study

The ablation study determines whether individual components contribute to the observed result.

Required components:

```text
Adaptive selection
Variance term
Cost term
Novelty term
Branching
Reproduction
Metamorphic validation
```

---

# 77. Ablation A1: No Adaptive Selection

Replace adaptive selection with Random.

Everything else remains constant.

Purpose:

> Measure the contribution of adaptive selection.

---

# 78. Ablation A2: No Variance Term

Use adaptive selection without empirical variance.

Purpose:

> Determine whether variance-aware exploration contributes beyond mean reward.

---

# 79. Ablation A3: No Cost Term

Remove cost penalty.

Purpose:

> Determine whether explicit cost awareness improves budget efficiency.

---

# 80. Ablation A4: No Novelty Term

Remove novelty augmentation.

Purpose:

> Determine whether novelty-aware selection reduces redundant discovery.

---

# 81. Ablation A5: No Branching

Disable:

```text
snapshotting
state restoration
branch execution
```

Purpose:

> Measure the contribution of state-based branching.

---

# 82. Ablation A6: No Reproduction

Stop after invariant failure detection.

Purpose:

> Quantify how much raw discovery changes when validation is removed.

This is primarily a methodological ablation rather than a quality comparison.

---

# 83. Ablation A7: No Metamorphic Validation

Disable metamorphic validation.

Purpose:

> Determine whether metamorphic testing changes the final validated/generalized failure population.

---

# 84. Hyperparameter Selection

Parameters such as:

```text
λ_N
λ_B
λ_S
λ_C
```

must be selected using the development/validation process.

They must not be optimized against hidden holdout results.

---

# 85. Hyperparameter Search

A small predefined grid may be used.

Example:

```text
λ_C ∈ {0.1, 0.25, 0.5}
λ_N ∈ {0.1, 0.25, 0.5}
λ_B ∈ {0.1, 0.25, 0.5}
```

These are example ranges, not final scientific constants.

The final configuration must be frozen before hypothesis testing.

---

# 86. No Post-Hoc Optimization

Do not:

```text
run experiments
↓
inspect results
↓
change weights
↓
rerun only the proposed method
↓
report improved result
```

That produces a lovely number and a rather less lovely experiment.

---

# 87. Randomization

Randomize:

```text
candidate ordering
seed assignment
run ordering
```

where appropriate.

Run ordering can reduce systematic environmental drift.

---

# 88. Paired Seeds

Where possible:

```text
Seed 1:
Random
Uniform
UCB-V
Proposed

Seed 2:
Random
Uniform
UCB-V
Proposed
```

This supports paired statistical comparison.

---

# 89. Candidate Pool Replication

To distinguish method effects from candidate-pool effects, a secondary experiment may use multiple independently generated candidate pools.

Example:

```text
Pool A
Pool B
Pool C
```

Each method should evaluate every pool under matched seeds.

---

# 90. Environment Replication

A secondary experiment may vary:

```text
database contents
tool response distribution
fault timing
state initialization
```

to test robustness across environment configurations.

---

# 91. Agent Replication

If computationally feasible, evaluate multiple agent/model configurations.

However, the primary study should keep the agent fixed so the method comparison remains interpretable.

---

# 92. Recommended Experimental Hierarchy

Use:

### Level 1

One agent + one environment.

### Level 2

Multiple seeds.

### Level 3

Multiple candidate pools.

### Level 4

Multiple environment configurations.

### Level 5

Multiple agent configurations.

This avoids turning the first experiment into an enormous matrix nobody can afford to run.

---

# 93. Stopping Criteria

A run stops when:

```text
budget exhausted
```

or:

```text
predefined maximum executions reached
```

or:

```text
critical infrastructure failure
```

The stopping condition must be recorded.

---

# 94. Saturation Stopping

The primary comparison should **not** stop early merely because one method appears better.

Optional secondary analysis may study saturation.

If used, the saturation rule must be fixed before analysis.

---

# 95. Invalid Execution Handling

An execution may be marked invalid because of:

```text
environment initialization failure
corrupted trace
invalid scenario
tool infrastructure failure
snapshot corruption
evaluator infrastructure failure
```

Invalid executions must be logged and their cost accounted for.

---

# 96. Infrastructure Failure Handling

If infrastructure fails:

```text
record failure
record cost
record reason
```

Do not silently retry indefinitely.

If a retry policy exists, it must be identical across methods.

---

# 97. Agent Timeout Handling

A timeout must be classified according to the experiment definition.

Possible outcomes:

```text
agent reliability failure
resource violation
environment failure
infrastructure error
```

The relevant invariant determines the classification.

---

# 98. Tool Timeout Handling

A tool timeout is not automatically an agent failure.

The experiment should evaluate:

```text
Did the agent recover safely?
Did state remain valid?
Did it retry appropriately?
Did it bypass authorization?
```

---

# 99. Data Collection

Each execution must collect:

```text
scenario
agent configuration
environment configuration
seed
trajectory
state transitions
tool calls
policy decisions
faults
snapshot events
branch events
invariant results
failure records
costs
selector state
```

---

# 100. Experiment Record

Each run should produce:

```yaml
experiment:
  experiment_id:
  run_id:
  method:
  seed:

  agent:
  environment:
  candidate_pool:

  budget:
    allocated:
    actual:

  selection:
    algorithm:
    configuration:

  execution:
    executions:
    branches:
    snapshots:

  outcomes:
    validated_failures:
    failure_families:
    reproduced_families:
    generalized_families:

  metrics:
    primary:
    secondary:
```

---

# 101. Logging Requirements

Every selection decision should record:

```text
candidate_id
timestamp
remaining_budget
candidate_score
reward history
cost estimate
novelty estimate
branch potential
selected/not selected
reason
```

Do not log hidden model reasoning.

---

# 102. Adaptive Selection Audit

For every selected candidate:

```text
Why was this candidate selected?
```

must be answerable from structured scoring inputs.

Example:

```text
UCB-V = 0.63
Novelty = 0.40
Branch potential = 0.70
Cost penalty = 0.15
Final score = 1.58
```

The actual formula and weights must match the frozen implementation.

---

# 103. Baseline Audit

Random:

```text
random seed
candidate pool
selection probability
```

Uniform:

```text
ordering rule
```

UCB-V:

```text
mean
variance
count
exploration term
```

Proposed:

```text
all component scores
weights
cost estimate
```

---

# 104. Fair Budget Comparison

For every method:

$$
B_{method}=B
$$

where \(B\) is the predefined total evaluation budget.

No method may receive extra budget because it performs additional validation.

If validation is part of the proposed method, that cost must be included.

---

# 105. Two Budget Views

Report both:

### Discovery Budget

Cost through initial failure discovery.

### Full Validation Budget

Cost through:

```text
discovery
+
reproduction
+
metamorphic testing
+
holdout
```

This distinguishes search efficiency from end-to-end evaluation cost.

---

# 106. Discovery-Only Comparison

Primary adaptive-selection comparison:

```text
Random
Uniform
UCB-V
Proposed
```

under equal discovery budgets.

---

# 107. End-to-End Comparison

Secondary comparison:

```text
discovery
→ validation
→ reproduction
→ metamorphic
→ holdout
```

under equal total budgets.

---

# 108. Validation Sampling

If validating every discovered failure is too expensive, use a predefined sampling protocol.

For example:

```text
all high-severity failures
+
random sample of remaining families
```

The sampling rule must be defined before examining outcomes.

---

# 109. Severity-Stratified Validation

If validation is stratified:

$$
P(selection|severity)
$$

must be documented.

This prevents hidden selection bias.

---

# 110. Failure Family Sampling

If one family has many occurrences, validation should avoid spending the entire reproduction budget on duplicates.

Use:

```text
family-level sampling
```

where appropriate.

---

# 111. Reproduction Allocation

Recommended:

```text
at least one representative failure per selected family
```

with a fixed number of independent attempts.

The selection rule must be frozen.

---

# 112. Metamorphic Allocation

Recommended initial protocol:

```text
one or more valid transformations
per selected representative failure/family
```

The transformation set must be frozen before final evaluation.

---

# 113. Hidden-Holdout Allocation

Holdout evaluation should be performed on:

```text
all methods
```

using equivalent:

```text
scenario count
budget
invariant set
evaluation configuration
```

---

# 114. Statistical Analysis Plan

For each primary metric:

1. Compute per-run value.
2. Verify data validity.
3. Compute descriptive statistics.
4. Compute confidence interval.
5. Compare methods.
6. Compute effect size.
7. Correct multiple comparisons where required.
8. Report uncertainty.
9. Interpret alongside absolute values.

---

# 115. Primary Statistical Comparison

The principal comparison is:

$$
Proposed
\quad vs \quad
Random
$$

with secondary comparisons against:

```text
Uniform
UCB-V
Adaptive without branching
Branching without adaptive selection
```

---

# 116. Pairwise Analysis

For matched seeds:

$$
\Delta_i =
M_{proposed,i}
-
M_{baseline,i}
$$

Use paired analysis.

---

# 117. Confidence Intervals

Report 95% confidence intervals for:

```text
mean family count
median cost per family
family AUC
reproduction rate
metamorphic consistency
holdout generalization
```

where statistically appropriate.

---

# 118. Effect Size Reporting

Every principal comparison should report:

```text
absolute difference
relative difference
effect size
confidence interval
```

A p-value alone is not a meaningful description of the size of an effect.

---

# 119. Multiple Comparison Control

If comparing:

```text
Proposed vs Random
Proposed vs Uniform
Proposed vs UCB-V
Adaptive vs non-adaptive
Branching vs non-branching
```

the analysis must control for multiple testing using a predefined method.

---

# 120. Statistical Interpretation

Possible outcomes:

```text
SUPPORTED
NOT_SUPPORTED
INCONCLUSIVE
CONDITIONAL
```

Examples:

### Supported

Observed difference is statistically and practically meaningful under the defined experiment.

### Not Supported

No sufficient evidence for the hypothesized improvement.

### Inconclusive

Data quality, variance, sample size, or evaluator limitations prevent a clear conclusion.

### Conditional

Improvement occurs only under specified conditions.

---

# 121. Negative Results

Negative results are valid.

Examples:

```text
adaptive selection does not outperform Random
branching costs more than it saves
reproduction rate is low
holdout generalization is weak
```

These must be reported rather than hidden.

---

# 122. No Metric Cherry-Picking

Do not select the metric that happens to favor the proposed method.

Primary metrics must be frozen before final analysis.

Secondary metrics can explain the result but cannot silently replace failed primary hypotheses.

---

# 123. No Baseline Tuning Against Test Results

Baseline parameters must be selected using:

```text
development
or
validation
```

not the final test set.

---

# 124. Reproducibility of the Experiment

The complete experiment must be reconstructible from:

```text
code version
configuration version
candidate pool
scenario versions
agent version
environment version
invariant version
seed
budget
method configuration
dependency versions
```

---

# 125. Experiment Artifact Bundle

Each final run should produce:

```text
experiment_config.yaml
candidate_pool.jsonl
scenario_versions.jsonl
run_metadata.json
trajectory.jsonl
invariant_results.jsonl
failure_records.jsonl
family_records.jsonl
reproduction_results.jsonl
metamorphic_results.jsonl
holdout_results.jsonl
metrics.json
```

---

# 126. Random Seed Recording

Record at minimum:

```text
experiment seed
candidate-generation seed
selection seed
environment seed
agent seed
fault-injection seed
```

If a random source does not expose a seed, document that limitation.

---

# 127. Dependency Reproducibility

Pin:

```text
Python version
package versions
container version
model identifier
configuration version
```

where possible.

---

# 128. Infrastructure Consistency

All methods should run using:

```text
same machine class
same container image
same dependency environment
same resource limits
```

where practical.

If not, the difference must be documented.

---

# 129. Threats to Internal Validity

Potential threats:

### T1: Candidate Pool Bias

One method may benefit from a particular candidate distribution.

Mitigation:

```text
frozen shared pool
multiple pools in sensitivity analysis
```

---

### T2: Reward Leakage

Adaptive selection may accidentally access future failure information.

Mitigation:

```text
strict information boundary
selection audit logs
```

---

### T3: Unequal Cost Accounting

Branching may appear cheap if snapshot/restore costs are ignored.

Mitigation:

```text
full cost accounting
```

---

### T4: Clustering Bias

Family count may depend heavily on clustering configuration.

Mitigation:

```text
frozen clustering
sensitivity analysis
```

---

### T5: Evaluator Error

Incorrect invariants may create artificial results.

Mitigation:

```text
golden traces
mutation tests
reference implementations
```

---

### T6: Agent Stochasticity

Agent randomness may create noisy results.

Mitigation:

```text
multiple seeds
matched seeds
reproduction testing
```

---

### T7: Environment Drift

Changing environment behavior can contaminate comparisons.

Mitigation:

```text
versioned environment
controlled seeds
deterministic mocks where possible
```

---

# 130. Threats to External Validity

Potential limitations:

```text
simulated environment
limited tool set
single agent model
synthetic scenarios
limited attack taxonomy
limited budget scale
```

Therefore conclusions should initially be framed as evidence about the experimental framework under the tested conditions.

---

# 131. Threats to Construct Validity

Potential issues:

### Failure family ≠ true root cause

Clustering represents similarity, not guaranteed causal identity.

### Failure count ≠ security quality

More discovered failures may mean:

```text
better evaluator
or
more vulnerable agent
```

The experiment must not confuse the two.

### Reproduction ≠ correctness

A reproducible failure is stronger evidence than a one-off anomaly, but reproducibility does not establish root cause.

---

# 132. Threats to Statistical Conclusion Validity

Potential issues:

```text
too few independent runs
non-independent observations
high variance
multiple comparisons
skewed cost distributions
small holdout
```

Mitigations must be documented in the final report.

---

# 133. Research Evidence Hierarchy

The methodology recognizes:

```text
Observed behavior
      ↓
Invariant violation
      ↓
Validated failure
      ↓
Failure family
      ↓
Reproduced failure
      ↓
Metamorphic support
      ↓
Holdout generalization
      ↓
Cross-run replication
```

A claim should not exceed the evidence level supporting it.

---

# 134. Main Experimental Workflow

```text
                ┌───────────────────────┐
                │ Frozen Candidate Pool │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Selection Method    │
                │ Random / Uniform /    │
                │ UCB-V / Proposed      │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Agent Execution     │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Trajectory + State    │
                └───────────┬───────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
              No Branching      Branching
                    │               │
                    └───────┬───────┘
                            ▼
                ┌───────────────────────┐
                │ Invariant Evaluation  │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────┐
                │ Failure Validation    │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────┐
                │ Classification        │
                │ + Clustering          │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────┐
                │ Adaptive Feedback     │
                └───────────┬───────────┘
                            │
                            └──────→ Next Candidate
```

---

# 135. Complete Experimental Protocol

## Step 1: Freeze Code

Create a versioned experiment commit.

## Step 2: Freeze Configuration

Freeze:

* budgets,
* candidate-pool configuration,
* invariants,
* clustering,
* validation,
* selector parameters.

## Step 3: Generate Candidate Pool

Generate and validate candidates.

## Step 4: Freeze Candidate Pool

Store immutable candidate-pool artifact.

## Step 5: Validate Evaluator

Run golden and mutation tests.

## Step 6: Run Baselines

Execute Random and Uniform.

## Step 7: Run UCB-V

Execute the variance-aware adaptive baseline.

## Step 8: Run Proposed Method

Execute adaptive selection with the defined cost/novelty/branching mechanisms.

## Step 9: Repeat Across Seeds

Run all methods under matched seeds.

## Step 10: Freeze Discovery Results

Finalize discovered failure records.

## Step 11: Reproduce Selected Failures

Run independent reproduction.

## Step 12: Run Metamorphic Tests

Evaluate defined transformations.

## Step 13: Unlock Holdout

Evaluate hidden scenarios.

## Step 14: Perform Statistical Analysis

Compute primary and secondary metrics.

## Step 15: Perform Ablation Analysis

Evaluate component contribution.

## Step 16: Generate Final Report

Report:

```text
discovery
efficiency
validation
reproducibility
metamorphic robustness
generalization
evaluator reliability
```

---

# 136. Recommended Initial Experiment Matrix

| ID | Method   | Branching | Purpose                          |
| -- | -------- | --------- | -------------------------------- |
| E1 | Random   | Off       | Basic non-adaptive baseline      |
| E2 | Uniform  | Off       | Systematic non-adaptive baseline |
| E3 | UCB-V    | Off       | Adaptive statistical baseline    |
| E4 | Adaptive | Off       | Adaptive selection contribution  |
| E5 | Random   | On        | Branching contribution baseline  |
| E6 | Uniform  | On        | Coverage + branching             |
| E7 | UCB-V    | On        | Adaptive + branching baseline    |
| E8 | Proposed | On        | Full proposed framework          |

The minimum publication-quality comparison should include E1, E2, E3, E7, and E8.

---

# 137. Recommended Ablation Matrix

| Ablation | Adaptive | Variance | Cost | Novelty | Branching |
| -------- | -------: | -------: | ---: | ------: | --------: |
| Full     |        ✓ |        ✓ |    ✓ |       ✓ |         ✓ |
| A1       |        ✗ |        ✗ |    ✗ |       ✗ |         ✓ |
| A2       |        ✓ |        ✗ |    ✓ |       ✓ |         ✓ |
| A3       |        ✓ |        ✓ |    ✗ |       ✓ |         ✓ |
| A4       |        ✓ |        ✓ |    ✓ |       ✗ |         ✓ |
| A5       |        ✓ |        ✓ |    ✓ |       ✓ |         ✗ |

Additional validation ablations can independently disable reproduction or metamorphic testing.

---

# 138. Expected Data Products

The experiment should produce:

```text
1. Raw trajectories
2. State snapshots
3. Branch records
4. Invariant results
5. Failure candidates
6. Validated failures
7. Failure signatures
8. Failure families
9. Reproduction records
10. Metamorphic records
11. Holdout records
12. Per-run metrics
13. Aggregate metrics
14. Statistical analysis
15. Figures
16. Experiment configuration
```

---

# 139. Primary Result Criteria

The proposed method should be considered empirically supported only if the experiment provides sufficient evidence across the predefined primary metrics.

Possible evidence pattern:

```text
higher family discovery
+
lower/equivalent cost per family
+
acceptable validation quality
+
reproducible failures
+
holdout evidence
```

No single metric should determine the overall conclusion.

---

# 140. Failure of the Hypothesis

The experiment must explicitly allow outcomes such as:

```text
Adaptive selection does not improve discovery.
Branching provides no cost advantage.
UCB-V matches the proposed method.
Novelty scoring adds no measurable benefit.
Failures do not reproduce reliably.
Development failures fail to generalize.
Evaluator reliability is insufficient.
```

These are legitimate research results.

---

# 141. Implementation Order

Recommended implementation sequence:

```text
1. Agent adapter
2. Controlled environment
3. Tool gateway
4. Trace collector
5. Invariant engine
6. Failure detector
7. Candidate representation
8. Random selector
9. Uniform selector
10. UCB-V selector
11. Cost model
12. Novelty scoring
13. Interesting-state detector
14. Snapshot manager
15. Branch manager
16. Failure clustering
17. Reproduction manager
18. Metamorphic engine
19. Holdout evaluator
20. Metrics engine
21. Experiment runner
22. Statistical analysis
23. Dashboard
```

---

# 142. Minimum Viable Experiment

Before running the complete study, the system must successfully execute:

```text
1 agent
1 environment
10–20 scenarios
10 invariants
Random baseline
UCB-V
Proposed adaptive method
fixed budget
multiple seeds
failure validation
failure clustering
basic reproduction
```

This proves the experimental loop before scaling it.

---

# 143. Definition of Done

The experimental methodology is implementation-ready when:

* [ ] Primary research question is defined.
* [ ] Hypotheses are defined.
* [ ] Independent variables are defined.
* [ ] Dependent variables are defined.
* [ ] Experimental unit is defined.
* [ ] Candidate pool is frozen before final testing.
* [ ] Random baseline exists.
* [ ] Uniform baseline exists.
* [ ] UCB-V baseline exists.
* [ ] Independent-execution baseline exists.
* [ ] Branching-only comparison exists.
* [ ] Adaptive-without-branching comparison exists.
* [ ] Proposed method is fully specified.
* [ ] Budget is fixed and measurable.
* [ ] Snapshot and restore costs are included.
* [ ] Selection overhead is measurable.
* [ ] Random seeds are recorded.
* [ ] Multiple independent runs are performed.
* [ ] Primary metrics are frozen.
* [ ] Statistical analysis plan is frozen.
* [ ] Holdout data is isolated.
* [ ] Reproduction protocol is frozen.
* [ ] Metamorphic protocol is frozen.
* [ ] Ablation matrix is defined.
* [ ] Golden evaluator tests pass.
* [ ] No future-information leakage exists.
* [ ] Raw experimental artifacts are retained.
* [ ] Results are reproducible from recorded configuration.

---

# 144. Final Experimental Principle

The entire methodology can be summarized as:

$$
\boxed{
Same\ Agent
+
Same\ Environment
+
Same\ Candidate\ Pool
+
Same\ Budget
+
Different\ Selection/Branching\ Strategy
}
$$

followed by:

$$
\boxed{
Execution
\rightarrow
Invariant\ Evaluation
\rightarrow
Failure\ Validation
\rightarrow
Family\ Discovery
\rightarrow
Reproduction
\rightarrow
Metamorphic\ Validation
\rightarrow
Holdout\ Generalization
}
$$

The principal comparison is therefore not:

> “Which method finds more suspicious outputs?”

It is:

> **Under the same measurable evaluation budget and controlled experimental conditions, which evaluation strategy discovers more distinct, validated failure mechanisms, how efficiently does it discover them, and how much of that evidence survives independent reproduction and evaluation on unseen scenarios?**

That is the experiment this project needs to run.
