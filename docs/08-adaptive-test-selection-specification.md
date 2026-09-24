# Adaptive Test Selection Specification

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** ATS-01
**Document Type:** Adaptive Test Selection Specification
**Version:** 1.0
**Status:** Draft for Implementation
**Related Documents:**

* Project Specification
* Research Questions & Success Criteria
* System Architecture
* Functional Requirements
* Agent / Environment Specification
* Test Scenario & Attack Specification
* Budget & Cost Model
* Experimental Methodology

---

# 1. Purpose

This document specifies the **adaptive test selection mechanism** used by the evaluation platform to decide which candidate test scenario should be executed next under a finite evaluation budget.

The selector is responsible for allocating limited evaluation resources among candidate scenarios according to their expected research value.

The selector must balance:

* exploitation of historically productive scenarios,
* exploration of insufficiently tested scenarios,
* scenario novelty,
* expected failure yield,
* failure severity or value,
* state coverage,
* branch potential,
* evaluation cost,
* remaining budget.

The selector is an experimental component. Its effectiveness must be measured against defined baselines rather than assumed from the algorithm name.

---

# 2. Research Role

Adaptive test selection is one of the central mechanisms being evaluated in this project.

The research question is:

> Under a fixed evaluation budget, can adaptive selection identify more validated security and reliability failures, or achieve equivalent validated failure discovery at lower evaluation cost, than non-adaptive selection strategies?

The selector therefore exists to test a research hypothesis.

It is not merely an optimization layer.

---

# 3. Core Principle

The system shall not execute all generated scenarios indiscriminately.

Instead:

```text
Scenario Generator
        ↓
Candidate Pool
        ↓
Candidate Scoring
        ↓
Adaptive Selector
        ↓
Budget Check
        ↓
Scenario Execution
        ↓
Observed Evidence
        ↓
Reward Update
        ↓
Candidate Statistics Update
        ↓
Next Selection
```

The process repeats until the configured experiment budget is exhausted or the experiment termination condition is reached.

---

# 4. Selection Problem

Let the candidate set at selection round `t` be:

$$
C_t = \{c_1,c_2,\ldots,c_n\}
$$

Each candidate `c` has:

* estimated cost,
* historical reward,
* reward variance,
* execution count,
* novelty,
* expected failure yield,
* state coverage value,
* branch potential,
* severity/value,
* feasibility.

The selector chooses:

$$
c_t^* = \arg\max_{c \in C_t^{feasible}} Score(c,t)
$$

subject to:

$$
Cost(c) \leq Budget_{remaining}
$$

The exact scoring function depends on the configured selection policy.

---

# 5. Selection Objectives

The selector shall optimize the configured primary objective.

Supported primary objectives should include:

### Objective O1: Validated Failure Discovery

Maximize:

$$
\text{ValidatedFailures}
$$

### Objective O2: Failure Family Discovery

Maximize:

$$
\text{NewFailureFamilies}
$$

### Objective O3: Budget Efficiency

Maximize:

$$
\frac{\text{ValidatedFailures}}{\text{EvaluationCost}}
$$

### Objective O4: State Coverage

Maximize newly evaluated relevant states.

### Objective O5: Composite Research Yield

Combine multiple measurable outcomes.

The initial experiments should primarily use **validated failure discovery under a fixed budget**.

---

# 6. What the Selector Is Not

The adaptive selector is not:

* a vulnerability detector by itself,
* a failure classifier,
* a security policy engine,
* a replacement for invariant evaluation,
* a replacement for validation,
* a predictor of real-world attack probability,
* a model reasoning interpreter.

The selector chooses what to test.

The execution and validation systems determine what actually happened.

---

# 7. Candidate Test Definition

A candidate is an executable scenario that has passed scenario validation.

A candidate shall contain:

```yaml
candidate_id:
scenario_id:
scenario_version:
scenario_family:
attack_type:
task:
initial_state_config:
agent_config:
environment_config:
perturbations:
invariants:
estimated_cost:
metadata:
```

The candidate must be executable without requiring the selector to modify its semantic definition.

---

# 8. Candidate Lifecycle

Each candidate follows:

```text
GENERATED
    ↓
VALIDATED
    ↓
CANDIDATE_POOL
    ↓
SELECTED
    ↓
EXECUTING
    ↓
COMPLETED
    ↓
REWARDED
    ↓
STATISTICS_UPDATED
```

Alternative terminal states:

```text
INVALID
CANCELLED
BUDGET_EXCLUDED
EXECUTION_ERROR
```

---

# 9. Candidate Eligibility

A candidate is eligible for selection only when:

1. scenario validation passed,
2. required tools exist,
3. required environment state can be created,
4. required invariants exist,
5. estimated cost is known or bounded,
6. candidate is not already completed when duplicates are disallowed,
7. sufficient budget remains,
8. candidate is not in a protected holdout set,
9. candidate is not blocked by experiment constraints.

---

# 10. Candidate Metadata

The selector should receive:

```yaml
candidate_id:
scenario_family:
attack_type:
difficulty:
estimated_cost:
novelty_score:
state_features:
tool_features:
identity_features:
permission_features:
branchability:
historical_statistics:
```

The selector should not receive information that is explicitly hidden by the experiment design.

---

# 11. Candidate Statistics

For candidate `c`, maintain:

```text
n_c
```

number of executions,

```text
μ_c
```

empirical mean reward,

```text
v_c
```

empirical reward variance,

```text
cost_c
```

observed or estimated evaluation cost.

Additional statistics may include:

```text
failure_count
validated_failure_count
new_family_count
interesting_state_count
branch_count
state_coverage_gain
reproduction_success_count
```

---

# 12. Reward Definition

The selector requires a measurable reward.

The reward must be derived from **observed experimental outcomes**, not manually assigned after seeing the results.

A basic reward may be:

$$
R_t =
\begin{cases}
1 & \text{if a new validated failure is discovered}\\
0 & \text{otherwise}
\end{cases}
$$

A richer reward may be:

$$
R_t =
w_fF_t +
w_nN_t +
w_sS_t +
w_cC_t -
w_kK_t
$$

where:

* `F_t` = validated failure discovery,
* `N_t` = novel failure-family discovery,
* `S_t` = relevant state coverage gain,
* `C_t` = branch yield,
* `K_t` = cost penalty.

The weights must be specified before the relevant experiment.

---

# 13. Reward Requirements

Reward calculations shall:

1. use observable outcomes,
2. be deterministic given the same inputs,
3. be recorded,
4. be versioned,
5. not use hidden holdout outcomes,
6. not depend on manually selected winners,
7. remain consistent across compared algorithms.

---

# 14. Binary Reward Mode

For the first experiment, the recommended reward is binary.

```text
Reward = 1
```

when the selected candidate produces a previously unseen **validated failure family**.

Otherwise:

```text
Reward = 0
```

This creates a simple initial bandit problem.

---

# 15. Failure Validation Boundary

A candidate shall not receive a positive validated-failure reward merely because:

```text
attack succeeded
```

or:

```text
invariant violation was observed once
```

The project requires validation.

A positive validated-failure reward should be issued only after the configured validation procedure confirms the failure.

---

# 16. Failure Family Novelty

A discovered failure may be considered novel when its normalized signature does not match an existing validated failure family under the configured similarity threshold.

Conceptually:

```text
Execution
    ↓
Failure
    ↓
Signature
    ↓
Existing Families?
    ├── Yes → Existing Family
    └── No  → New Failure Family
```

The selector may use this signal after validation.

---

# 17. Selection Information Boundary

The selector may use:

### Allowed

* previous candidate rewards,
* candidate execution counts,
* empirical variance,
* observed cost,
* scenario metadata,
* state coverage,
* validated failure history,
* novelty,
* branch yield.

### Not Allowed

* hidden holdout outcomes,
* future execution outcomes,
* manually inserted failure labels,
* information from future experiment rounds,
* private model reasoning,
* information unavailable to the corresponding baseline.

---

# 18. Exploration vs Exploitation

The selector must explicitly balance:

### Exploration

Test candidates about which the system has insufficient information.

### Exploitation

Test candidates that have historically produced valuable outcomes.

This is fundamental to the adaptive evaluation hypothesis.

---

# 19. UCB-V Policy

The project may implement **UCB-V** as one adaptive selection policy.

However, the implementation may be called UCB-V only if it actually uses:

* empirical mean reward,
* empirical reward variance,
* number of observations,
* total selection count,
* a confidence parameter.

A generic UCB-V form is:

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
\frac{3b\ln(t)}
{n_i}
$$

where:

* `μ̂_i` = empirical mean reward,
* `v̂_i` = empirical variance,
* `n_i` = number of times candidate `i` was selected,
* `t` = selection round,
* `b` = known reward upper bound.

The exact formula and constants used by the implementation shall be documented and cited in the implementation/research methodology.

---

# 20. Reward Bound

For bounded UCB-V, the reward range must be explicitly defined.

For binary reward:

$$
R \in [0,1]
$$

therefore:

$$
b = 1
$$

may be used under the selected UCB-V formulation.

If composite rewards can exceed 1, the reward must be normalized or an appropriate bound must be specified.

The system shall not silently assume bounded reward.

---

# 21. Empirical Mean

For candidate `i`:

$$
\hat{\mu}_i =
\frac{1}{n_i}
\sum_{j=1}^{n_i}R_{i,j}
$$

The implementation shall maintain the statistic incrementally where practical.

---

# 22. Empirical Variance

The selector must calculate empirical reward variance if UCB-V is claimed.

A numerically stable online variance algorithm such as Welford's method should be used.

Conceptually:

```python
update_mean_and_variance(reward)
```

The implementation should not repeatedly calculate variance from the full history unless required.

---

# 23. Initial Candidate Selection

Candidates with:

```text
n_i = 0
```

must receive an exploration treatment.

The selector may:

### Strategy A

Select every candidate once before normal UCB-V begins.

### Strategy B

Assign untested candidates an infinite priority.

### Strategy C

Use a mathematically defined initialization rule.

The chosen strategy must be fixed before an experiment.

The recommended initial implementation is **explicit one-time initialization for the candidate set used in the experiment**.

---

# 24. Candidate Pool Growth

New candidates may be generated after execution begins.

When a new candidate enters the pool:

```text
n_i = 0
μ_i = 0
v_i = 0
```

or the equivalent uninitialized state.

The candidate must enter the same initialization procedure as other untested candidates.

---

# 25. Novelty Component

UCB-V alone does not necessarily represent scenario novelty.

The selector may therefore use a composite policy:

$$
Score_i =
UCBV_i
+
\lambda_N Novelty_i
+
\lambda_S Severity_i
+
\lambda_B BranchValue_i
-
\lambda_C CostPenalty_i
$$

However, once additional terms are introduced, the resulting policy should be named something such as:

> **Cost-Aware Novelty-Augmented UCB-V**

rather than simply “UCB-V.”

This distinction must remain explicit in the research report.

---

# 26. Cost-Aware Selection

The selector must account for evaluation cost.

At minimum:

$$
Cost_i =
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

Not every candidate incurs every cost.

---

# 27. Cost Estimate

Before execution, each candidate should have:

```text
estimated_cost
```

After execution, the system records:

```text
observed_cost
```

The selector may update its cost estimate using observed measurements.

---

# 28. Cost Model

A candidate's total evaluation cost shall be decomposed into:

```text
C_total =
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

The project shall not equate model token cost with total evaluation cost.

---

# 29. Model Generation Cost

Where supported, record:

```text
input_tokens
output_tokens
model_calls
latency
provider_cost
```

If provider pricing is unavailable, the system may use model-call or token counts as a resource metric.

---

# 30. Execution Cost

Execution cost may include:

```text
agent steps
tool calls
environment transitions
wall-clock execution time
model calls
```

---

# 31. Branch Cost

Branch cost includes:

```text
branch creation
branch initialization
branch execution
branch cleanup
```

---

# 32. Snapshot Cost

Snapshot cost includes:

```text
serialization
storage
hashing
I/O
```

---

# 33. Restore Cost

Restore cost includes:

```text
snapshot loading
deserialization
state reconstruction
state validation
```

---

# 34. Analysis Cost

Analysis cost includes:

```text
trajectory processing
state feature extraction
failure detection
signature generation
clustering
```

---

# 35. Verification Cost

Verification cost includes:

```text
independent replay
metamorphic execution
failure reproduction
holdout evaluation
```

Verification costs must be included when they are part of the candidate's evaluation process.

---

# 36. Cost Penalty

A normalized cost penalty may be defined as:

$$
CostPenalty_i =
\frac{Cost_i}{Budget_{total}}
$$

or another explicitly defined normalization.

The same cost normalization must be used across adaptive methods being compared.

---

# 37. Remaining Budget Constraint

Before selecting a candidate:

$$
Cost_{estimated}(i)
\leq
Budget_{remaining}
$$

must hold.

If not, the candidate is not executable under the remaining budget.

---

# 38. Budget Manager

The Budget Manager is authoritative for resource consumption.

The selector may request:

```text
CanExecute(candidate, estimated_cost)
```

The Budget Manager returns:

```text
APPROVED
REJECTED
```

The selector shall not independently override the budget.

---

# 39. Budget Reservation

For expensive operations, the system should reserve estimated budget before execution.

Example:

```text
Selector
   ↓
Candidate selected
   ↓
Budget reservation
   ↓
Execution
   ↓
Actual cost
   ↓
Reservation reconciliation
```

---

# 40. Budget Overshoot

If actual cost exceeds estimated cost:

1. record the difference,
2. update cost statistics,
3. prevent unauthorized additional budget consumption,
4. mark the execution appropriately,
5. update future cost estimates.

The system shall never silently exceed the configured experiment budget.

---

# 41. Budget Units

The experiment shall define its primary budget unit.

Possible units:

```text
MODEL_CALLS
TOKENS
COMPUTE_TIME
WALL_CLOCK_TIME
MONETARY_COST
EXECUTION_UNITS
COMPOSITE_RESOURCE
```

The initial research implementation should use a measurable resource such as **model calls plus explicit execution cost**, with any monetary conversion documented separately.

---

# 42. Candidate Feasibility

A candidate may be infeasible because:

```text
estimated cost > remaining budget
```

or:

```text
required resource unavailable
```

or:

```text
scenario invalidated
```

Infeasible candidates shall not be treated as failed tests.

---

# 43. Selection Round

A selection round consists of:

```text
1. Refresh candidate pool
2. Remove invalid candidates
3. Update budget state
4. Calculate candidate statistics
5. Calculate acquisition scores
6. Filter infeasible candidates
7. Select candidate
8. Reserve budget
9. Execute candidate
10. Validate result
11. Calculate reward
12. Update statistics
13. Generate new candidates if configured
14. Repeat
```

---

# 44. Selection Algorithm

Conceptual algorithm:

```python
def select_next_candidate(candidates, budget, policy):

    feasible = [
        c for c in candidates
        if c.estimated_cost <= budget.remaining
        and c.is_valid
    ]

    if not feasible:
        return None

    scores = {}

    for candidate in feasible:
        scores[candidate.id] = policy.score(candidate)

    selected = max(
        feasible,
        key=lambda c: scores[c.id]
    )

    return selected
```

The actual policy implementation shall remain separate from the candidate store and execution engine.

---

# 45. UCB-V Selection Pseudocode

```python
def ucb_v(candidate, round_index, reward_bound=1.0):

    if candidate.count == 0:
        return float("inf")

    mean = candidate.mean_reward
    variance = candidate.reward_variance
    count = candidate.count

    exploration = sqrt(
        (2 * variance * log(round_index))
        / count
    )

    correction = (
        3 * reward_bound * log(round_index)
    ) / count

    return mean + exploration + correction
```

The implementation must use the exact UCB-V formulation documented by the experiment.

The pseudocode is illustrative of the required structure, not a substitute for specifying the final mathematical variant.

---

# 46. Why Variance Matters

Two candidates can have the same average reward while having different uncertainty.

Example:

```text
Candidate A:
rewards = [0, 0, 0, 1, 1]

Candidate B:
rewards = [0, 0, 0, 0, 0.4]
```

Their means may be similar depending on the sample, but their observed variance differs.

UCB-V uses empirical variance to influence exploration.

Therefore, an implementation that stores a `variance` field but never uses it is **not an implementation of UCB-V**.

---

# 47. Novelty Score

Novelty should be calculated from scenario characteristics and/or observed state characteristics.

Possible feature representation:

```text
scenario family
attack type
tool sequence
identity
permission set
resource type
state features
perturbation type
```

A distance-based novelty score may be:

$$
Novelty(c) =
1 -
\max_{x \in ExecutedTests}
Similarity(c,x)
$$

The similarity function must be explicitly defined.

---

# 48. State Novelty

A candidate may be valuable because it is likely to reach previously unexplored states.

Possible state novelty:

$$
StateNovelty(c)
=
1 -
\max_{s \in S_{observed}}
Similarity(features(c),s)
$$

This is an optional research feature and must be measured separately from basic UCB-V.

---

# 49. Branch Potential

A candidate may have high branching value if it is expected to reach a state from which multiple meaningful continuations can be generated.

Possible features:

```text
snapshot compatibility
interesting-state probability
number of supported perturbations
historical branch yield
```

A simple branch value:

$$
BranchValue(c)
=
ExpectedUsefulBranches(c)
$$

must be estimated from documented data.

---

# 50. Severity Value

Severity may be included in reward or selection only if the experiment defines a reproducible severity function.

Possible evidence-based dimensions:

```text
invariant category
resource sensitivity
state impact
number of affected resources
```

Severity must not be assigned solely through subjective manual ranking after observing the result.

---

# 51. Composite Acquisition Function

The recommended extended policy is:

$$
A(c,t)
=
UCBV(c,t)
+
\lambda_N N(c)
+
\lambda_B B(c)
+
\lambda_S S(c)
-
\lambda_C C(c)
$$

where:

* `UCBV` = empirical reward acquisition,
* `N` = novelty,
* `B` = branch potential,
* `S` = severity/value,
* `C` = normalized cost.

The coefficients:

```text
λN
λB
λS
λC
```

must be experiment parameters.

---

# 52. Normalization

The components of the composite score may have different scales.

Before combining them, each component shall be normalized.

Possible methods:

```text
min-max normalization
z-score normalization
bounded [0,1] transformation
rank normalization
```

The normalization method must remain fixed within a comparison.

---

# 53. Avoiding Information Leakage

If the selector uses observed failure information to score a candidate, that information must come only from previously completed evaluations.

The system must prevent:

```text
Candidate C
   ↓
future failure information
   ↓
Candidate score
```

because that would invalidate the experiment.

---

# 54. Candidate Statistics Update

After execution:

```python
candidate.count += 1
candidate.mean_reward = update_mean(...)
candidate.reward_variance = update_variance(...)
candidate.total_cost += observed_cost
```

Additional statistics shall also be updated.

---

# 55. Family-Level Statistics

Candidate-level statistics may be insufficient because scenarios can belong to families.

The system may maintain:

```text
family_execution_count
family_failure_count
family_validated_failure_count
family_new_failure_count
family_cost
family_branch_yield
```

Family-level statistics can be used for candidate generation and adaptive selection.

---

# 56. Hierarchical Selection

A future extension may select:

```text
Scenario Family
       ↓
Scenario
       ↓
Branch
```

This is not required for the first implementation.

The initial selector should operate at the **candidate scenario level**.

---

# 57. Branch-Level Adaptive Selection

Branch selection can use the same conceptual framework.

Given a snapshot:

```text
S
```

and branches:

```text
B1, B2, ..., Bn
```

the system may estimate:

```text
branch yield
branch cost
branch novelty
branch historical reward
```

The initial experiment may use uniform branch exploration before introducing adaptive branch selection.

---

# 58. Adaptive Branching Research Separation

The project must distinguish:

### Test Selection Adaptivity

Which scenario should be executed?

from:

### Branch Selection Adaptivity

Which continuation from an interesting state should be executed?

These may be studied independently through ablation experiments.

---

# 59. Cold Start Strategy

At experiment start, the selector has no historical information.

Recommended sequence:

```text
Candidate Generation
      ↓
Candidate Validation
      ↓
Initial Exploration
      ↓
Statistics Collection
      ↓
Adaptive Selection
```

The number of initialization rounds shall be recorded.

---

# 60. Exploration Policy Alternatives

The system should support at least:

### Random

Uniform random candidate selection.

### Uniform

Round-robin candidate selection.

### UCB-V

Variance-aware adaptive selection.

### Cost-Aware UCB-V

UCB-V combined with cost.

### Composite Adaptive

UCB-V + novelty + branch value + cost.

The proposed method used in the main experiment must be explicitly identified.

---

# 61. Random Baseline

The random baseline selects:

$$
c_t \sim Uniform(C_t^{feasible})
$$

The random seed must be recorded.

---

# 62. Uniform Baseline

The uniform baseline selects candidates in a deterministic round-robin order.

Example:

```text
C1 → C2 → C3 → C4 → C1 → ...
```

This separates adaptive selection from randomized selection.

---

# 63. Non-Adaptive Budget Matching

All selection policies must receive equivalent:

* candidate pools,
* initial scenarios,
* budget,
* agent configuration,
* environment,
* validation procedure,
* failure definitions.

Only the selection strategy should differ where possible.

---

# 64. Selection Fairness

For a fair comparison:

```text
Same candidate generation
Same initial pool
Same execution budget
Same agent
Same environment
Same invariant set
Same validation
Same randomization protocol
Different selection policy
```

Any intentional difference must be documented.

---

# 65. Selection Metrics

The selector shall be evaluated using:

### Primary

```text
validated failures discovered
validated failure families discovered
```

### Secondary

```text
cost per validated failure
failure discovery rate
time to first validated failure
time to new failure family
state coverage
scenario coverage
branch yield
reproduction rate
holdout generalization
```

---

# 66. Cumulative Failure Discovery

For evaluation round `t`:

$$
F(t)
=
\text{number of validated unique failure families discovered by }t
$$

The primary comparison may plot:

```text
Cumulative Validated Failure Families
vs.
Evaluation Cost
```

---

# 67. Discovery Efficiency

Define:

$$
Efficiency =
\frac{ValidatedFailureFamilies}
{EvaluationCost}
$$

The denominator must use the project's documented cost unit.

---

# 68. Time to First Failure

Measure:

$$
T_{first}
=
\text{cost consumed before first validated failure}
$$

This metric should be reported separately from total failure count.

---

# 69. Failure Discovery Curve

For each policy, produce:

```text
Evaluation Cost
        vs
Cumulative Validated Failures
```

This allows the experiment to evaluate whether adaptive selection finds useful failures earlier under the same budget.

---

# 70. Regret

If bandit analysis is used, cumulative regret may be reported.

For reward:

$$
R_t
$$

and best expected candidate reward:

$$
\mu^*
$$

define:

$$
Regret(T)
=
\sum_{t=1}^{T}
(\mu^*-\mu_{a_t})
$$

The interpretation must account for the fact that candidate availability and rewards may change as the scenario generator creates new candidates.

---

# 71. Dynamic Candidate Pool

The candidate pool may change over time.

Therefore, classical stationary bandit assumptions may not always hold.

Sources of non-stationarity include:

* newly generated candidates,
* changing failure-family novelty,
* changing budget,
* adaptive scenario generation,
* changing environment state distributions.

The experiment must document whether the candidate pool is:

```text
STATIC
DYNAMIC
```

---

# 72. Recommended First Experiment

The first adaptive selection experiment should use a **static candidate pool**.

Reason:

```text
Static Pool
→ easier bandit interpretation
→ easier baseline comparison
→ easier reproduction
→ easier statistical analysis
```

Dynamic candidate generation should then be studied separately.

---

# 73. Candidate Pool Size

The experiment shall record:

```text
initial_candidate_count
maximum_candidate_count
executed_candidate_count
remaining_candidate_count
```

This prevents ambiguous claims such as “the adaptive system tested more scenarios” without defining the available candidate population.

---

# 74. Duplicate Execution Policy

The experiment configuration shall define whether a candidate can be selected more than once.

Possible modes:

```text
NO_REPEAT
REPEAT_FOR_REPRODUCTION
ADAPTIVE_REPEAT
```

For initial bandit experiments, repeated selection should be allowed when reward estimation requires multiple observations.

However, repeat executions should be distinguishable from independent scenario candidates.

---

# 75. Repetition Policy

A candidate may be repeated when:

* reward variance is important,
* stochastic agent behavior is present,
* reproduction is required,
* the selector needs additional evidence.

Repeated execution must not automatically create a new scenario.

---

# 76. Reward Update for Repeated Candidates

Each repeat contributes a new reward observation:

```text
R_i1
R_i2
R_i3
...
R_in
```

The candidate's:

```text
mean
variance
count
```

are updated accordingly.

---

# 77. Stochastic Agent Consideration

If the agent is stochastic, the same scenario may produce different outcomes.

Therefore:

```text
Same Scenario
      +
Different Run
      →
Different Reward
```

is valid.

The selector must distinguish:

```text
Scenario Identity
```

from:

```text
Execution Identity
```

---

# 78. Deterministic Agent Consideration

If the agent and environment are deterministic, repeated executions may provide little new reward information.

The experiment should therefore document whether repetition is meaningful.

---

# 79. Selection Confidence

The system may record:

```text
confidence_score
uncertainty
selection_margin
```

but these values must be derived from the defined selection policy.

The system should not label a candidate “high confidence” merely because it was selected frequently.

---

# 80. Selection Logging

Every selection decision shall produce a selection record.

Example:

```yaml
selection_id:
round:
candidate_id:
policy:
score:
ucbv_score:
mean_reward:
variance:
count:
novelty:
branch_value:
severity:
cost_estimate:
remaining_budget:
selection_reason:
timestamp:
```

---

# 81. Selection Auditability

A researcher must be able to reconstruct:

> Why was candidate `C123` selected at round 27?

The system should therefore preserve:

```text
candidate statistics
score components
budget state
policy version
candidate pool
random seed
selection timestamp
```

---

# 82. Selection Explanation

The selector may generate an explanation such as:

```text
Candidate C123 selected because:

UCB-V score: 0.74
Novelty: 0.82
Branch value: 0.63
Cost penalty: 0.11
Remaining budget: 420 units
```

This is an **observed selection summary**, not an explanation of the LLM's reasoning.

---

# 83. Selection Failure Handling

If the selector fails:

```text
selector error
```

the system shall not silently substitute a different algorithm.

The experiment should record:

```text
SELECTION_ERROR
```

and follow the configured experiment failure policy.

Possible policies:

```text
STOP
FALLBACK
SKIP_ROUND
```

For scientific comparison, `STOP` or explicit fallback logging is preferable to silently changing algorithms.

---

# 84. Candidate Execution Failure

If the selected scenario fails because of an evaluator error:

```text
EXECUTION_ERROR
```

it should not receive a failure-discovery reward.

The cost may still be recorded.

The candidate may be retried according to experiment configuration.

---

# 85. Invalid Candidate After Selection

If a candidate becomes invalid between selection and execution:

```text
Candidate
  ↓
Selected
  ↓
Validation
  ↓
Invalid
```

the system shall record:

```text
SELECTION_INVALIDATION
```

rather than treating it as a failed agent test.

---

# 86. Budget Exhaustion

When:

$$
Budget_{remaining} < MinimumExecutableCost
$$

the selection loop terminates.

The experiment shall record:

```text
termination_reason = BUDGET_EXHAUSTED
```

---

# 87. Selection Termination Conditions

The adaptive loop may terminate when:

1. budget is exhausted,
2. no feasible candidates remain,
3. configured maximum executions reached,
4. maximum experiment duration reached,
5. critical evaluator error occurs,
6. experiment-specific stopping criterion is met.

The stopping condition shall be recorded.

---

# 88. Adaptive Selection Configuration

Example:

```yaml
adaptive_selection:

  enabled: true

  policy: ucb_v

  initialization:
    strategy: sample_each_candidate_once

  reward:
    type: validated_failure_family
    bound: 1.0

  cost:
    enabled: true
    normalization: total_budget

  novelty:
    enabled: false

  branch_value:
    enabled: false

  severity:
    enabled: false

  repeat:
    allowed: true

  termination:
    condition: budget_exhausted
```

This represents a clean initial UCB-V experiment.

---

# 89. Composite Policy Configuration

An extended policy may be configured as:

```yaml
adaptive_selection:

  enabled: true

  policy: cost_aware_novelty_ucbv

  ucb_v:
    reward_bound: 1.0

  weights:
    novelty: 0.20
    branch_value: 0.15
    severity: 0.10
    cost: 0.25

  initialization:
    strategy: sample_each_candidate_once
```

The exact weights must be fixed before evaluation.

---

# 90. Recommended Research Progression

The project should implement adaptive selection incrementally.

## Phase 1

Random selection.

## Phase 2

Uniform selection.

## Phase 3

Basic UCB-V.

## Phase 4

Cost-aware UCB-V.

## Phase 5

Novelty-augmented selection.

## Phase 6

Branch-aware selection.

This prevents several interacting heuristics from becoming impossible to evaluate scientifically.

---

# 91. Required Ablations

At minimum, compare:

```text
A1: Random
A2: Uniform
A3: UCB-V
A4: UCB-V + Cost
A5: UCB-V + Novelty
A6: Full Proposed Policy
```

Not every experiment needs all six, but the contribution of each major component must be measurable.

---

# 92. Main Experimental Comparison

The main comparison should be:

```text
Random Selection
        vs
Proposed Adaptive Selection
```

under:

```text
same budget
same candidate pool
same agent
same environment
same invariants
same validation
```

---

# 93. Adaptive Selection With Branching

When branching is enabled:

```text
Candidate Scenario
      ↓
Execute Prefix
      ↓
Interesting State
      ↓
Snapshot
      ↓
Branch Candidates
      ↓
Adaptive Branch Selection
```

The experiment must separately account for:

```text
prefix cost
snapshot cost
restore cost
branch cost
```

---

# 94. Prefix Cost Consideration

The selector should recognize that a candidate reaching a reusable intermediate state may have different value from a candidate requiring a completely independent execution.

A candidate's expected value can therefore include:

```text
Expected Failure Yield
+
Expected Reusable State Value
-
Expected Execution Cost
```

This is one of the mechanisms through which state-based branching may improve budget efficiency.

---

# 95. State Reuse Value

A state may have high reuse value if:

```text
many meaningful perturbations
+
low snapshot/restore cost
+
high historical branch yield
```

are associated with it.

The initial implementation may use a simple branch-count estimate.

---

# 96. Adaptive Branching Cost Model

For a parent execution reaching snapshot `S`:

Independent execution:

$$
Cost_{independent}
=
\sum_{i=1}^{k}
Cost(prefix_i + continuation_i)
$$

Branching:

$$
Cost_{branching}
=
Cost(prefix)
+
Cost(snapshot)
+
\sum_{i=1}^{k}
(Cost(restore_i)+Cost(continuation_i))
$$

The evaluator shall measure both rather than assuming branching is cheaper.

---

# 97. Branching Break-Even Condition

Branching is economically useful only when:

$$
Cost_{branching}
<
Cost_{independent}
$$

for the relevant set of continuations.

The system shall record actual costs so this can be experimentally evaluated.

---

# 98. Selection and Hidden Holdout

The adaptive selector shall never optimize directly against holdout outcomes.

The correct flow is:

```text
Training / Adaptive Set
        ↓
Adaptive Selection
        ↓
Freeze Evaluation Policy
        ↓
Hidden Holdout
        ↓
Generalization Measurement
```

---

# 99. Selection Freeze

Before hidden-holdout evaluation, the following should be frozen:

* adaptive policy,
* weights,
* reward definition,
* candidate-generation configuration,
* selection thresholds,
* stopping rules.

This prevents tuning against holdout outcomes.

---

# 100. Selection Reproducibility

An adaptive experiment must be reproducible from:

```text
experiment configuration
+
candidate pool
+
candidate metadata
+
selection policy version
+
random seeds
+
reward history
+
observed costs
+
execution results
```

---

# 101. Selection Run Record

Each experiment shall store:

```yaml
selection_run:
  experiment_id:
  policy_name:
  policy_version:
  initial_candidate_count:
  total_budget:
  budget_unit:
  initialization_strategy:
  reward_definition:
  reward_bound:
  cost_model_version:
  novelty_model_version:
  random_seed:
  total_rounds:
  termination_reason:
```

---

# 102. Candidate Score Storage

The system should preserve historical scores.

Example:

```yaml
score_record:
  round: 17
  candidate_id: C042
  ucb_v: 0.73
  novelty: 0.64
  branch_value: 0.42
  severity: 0.50
  cost_penalty: 0.12
  final_score: 0.91
```

This enables post-experiment audit.

---

# 103. Selection Data Model

Recommended entities:

```text
Candidate
CandidateStatistics
SelectionPolicy
SelectionRound
SelectionDecision
RewardObservation
BudgetState
CostObservation
```

Relationships:

```text
Candidate
   │
   ├── CandidateStatistics
   │
   └── SelectionDecision
             │
             └── RewardObservation
```

---

# 104. Candidate Statistics Schema

```yaml
candidate_statistics:
  candidate_id:
  count:
  mean_reward:
  reward_variance:
  total_cost:
  average_cost:
  validated_failures:
  new_failure_families:
  interesting_states:
  branch_yield:
  last_selected_round:
```

---

# 105. Selection Decision Schema

```yaml
selection_decision:
  decision_id:
  experiment_id:
  round:
  candidate_id:
  policy:
  score:
  score_components:
  budget_before:
  estimated_cost:
  budget_after_reservation:
  selected:
```

---

# 106. Reward Observation Schema

```yaml
reward_observation:
  observation_id:
  candidate_id:
  execution_id:
  reward:
  reward_type:
  validated_failure_count:
  new_failure_family_count:
  state_coverage_gain:
  branch_yield:
  observed_cost:
```

---

# 107. Adaptive Selector Interface

Conceptual interface:

```python
class AdaptiveSelector:

    def initialize(self, candidates, config):
        ...

    def score(self, candidate, context):
        ...

    def select(self, candidates, budget):
        ...

    def update(self, candidate, observation):
        ...

    def get_statistics(self):
        ...

    def get_policy_metadata(self):
        ...
```

---

# 108. Selection Policy Interface

The policy should be separately implemented:

```python
class SelectionPolicy:

    def initialize(self, candidates):
        ...

    def score(self, candidate, context):
        ...

    def update(self, candidate, reward):
        ...

    def reset(self):
        ...
```

This allows Random, Uniform, UCB-V, and composite policies to share the same interface.

---

# 109. Random Policy Interface

```python
class RandomSelectionPolicy(SelectionPolicy):

    def select(self, candidates):
        ...
```

The policy must use an explicit random generator.

---

# 110. Uniform Policy Interface

```python
class UniformSelectionPolicy(SelectionPolicy):

    def select(self, candidates):
        ...
```

Selection order shall be deterministic given the candidate ordering.

---

# 111. UCB-V Policy Interface

```python
class UCBVSelectionPolicy(SelectionPolicy):

    def score(self, candidate, round_index):
        ...

    def update(self, candidate, reward):
        ...
```

The implementation must maintain empirical variance.

---

# 112. Cost-Aware Policy Interface

```python
class CostAwareSelectionPolicy(SelectionPolicy):

    def score(self, candidate, context):
        ...

    def estimate_cost(self, candidate):
        ...
```

---

# 113. Selection Policy Versioning

Every selection policy shall have:

```yaml
policy_name:
policy_version:
implementation_version:
configuration_hash:
```

A change to the mathematical formulation requires a new policy version.

---

# 114. Selection Invariants

The adaptive selection subsystem shall maintain:

### INV-SEL-001

The selector never selects an invalid candidate.

### INV-SEL-002

The selector never intentionally exceeds the experiment budget.

### INV-SEL-003

Holdout outcomes are unavailable during adaptive selection.

### INV-SEL-004

Reward updates use only completed observations.

### INV-SEL-005

UCB-V uses empirical variance when identified as UCB-V.

### INV-SEL-006

Candidate statistics correspond to the correct candidate.

### INV-SEL-007

Selection decisions are reproducibly logged.

### INV-SEL-008

Baseline policies use equivalent budgets and candidate pools.

### INV-SEL-009

Evaluator errors are not counted as agent failures.

### INV-SEL-010

Selection policy changes are versioned.

---

# 115. Selection Unit Tests

The implementation should include tests for:

### Test SEL-01

Untested candidate receives initialization treatment.

### Test SEL-02

Mean reward is updated correctly.

### Test SEL-03

Empirical variance is updated correctly.

### Test SEL-04

UCB-V score changes when variance changes.

### Test SEL-05

Higher observed reward increases exploitation value.

### Test SEL-06

Low-count candidates receive exploration value.

### Test SEL-07

Infeasible candidates are excluded.

### Test SEL-08

Budget cannot become negative.

### Test SEL-09

Holdout candidates cannot enter the adaptive pool.

### Test SEL-10

Selection decisions are reproducible with the same seed/configuration.

---

# 116. UCB-V Specific Verification

A dedicated test shall construct candidates with controlled reward histories.

Example:

```text
Candidate A:
[0, 1, 0, 1]

Candidate B:
[0, 0, 0, 1]
```

The test shall verify that:

* means are calculated correctly,
* variances are calculated correctly,
* scores use variance,
* count affects the confidence term.

This prevents the implementation from being called UCB-V while secretly functioning as plain UCB with decorative variance.

---

# 117. Adaptive Selection Experiment

A minimal experiment should execute:

```text
Candidate Pool
      ↓
Random Baseline
      ↓
Fixed Budget
      ↓
Validated Failure Count

Candidate Pool
      ↓
UCB-V
      ↓
Same Fixed Budget
      ↓
Validated Failure Count
```

Repeat across multiple seeds where stochasticity exists.

---

# 118. Statistical Comparison

For each selection method, record across repeated runs:

```text
validated failures
new failure families
cost
time to first failure
state coverage
branch yield
holdout generalization
```

The statistical analysis plan shall specify the appropriate comparison method.

Do not rely on a single run.

---

# 119. Repeated Experiments

If the agent or environment is stochastic, use multiple independent experiment seeds.

Each run shall have:

```text
experiment_seed
agent_seed
environment_seed
selection_seed
scenario_generation_seed
```

where supported.

---

# 120. Confidence Intervals

Aggregate metrics should be reported with uncertainty estimates where appropriate.

For example:

```text
mean validated failures
+
95% confidence interval
```

The exact statistical procedure belongs in the Statistical Analysis Plan.

---

# 121. Effect Measurement

The main comparison should report the observed difference between adaptive and baseline methods.

Possible metrics:

$$
\Delta F =
F_{adaptive} - F_{baseline}
$$

and:

$$
RelativeGain =
\frac{
F_{adaptive}-F_{baseline}
}{
F_{baseline}
}
$$

Relative metrics require care when the baseline is zero.

---

# 122. Budget-Normalized Comparison

The key comparison should be performed at equivalent budget levels.

Example:

```text
Budget = 100 units
Random → F_R
UCB-V  → F_U
```

then:

```text
Budget = 250 units
Random → F_R
UCB-V  → F_U
```

This produces a discovery-efficiency curve rather than a single arbitrary endpoint.

---

# 123. Selection Curve

The main visualization should plot:

```text
X-axis:
Cumulative Evaluation Cost

Y-axis:
Cumulative Validated Failure Families
```

Each policy receives its own curve.

Do not convert the chart into a claim of superiority unless the experiment actually demonstrates one.

---

# 124. Cost-Performance Frontier

The system may additionally report:

```text
Cost per validated failure family
```

This is particularly relevant to the research objective of budget-constrained evaluation.

---

# 125. Selection Failure Analysis

When adaptive selection performs worse than a baseline, analyze:

* poor reward definition,
* insufficient exploration,
* misleading novelty,
* inaccurate cost estimates,
* sparse failures,
* non-stationary candidate rewards,
* candidate pool imbalance,
* noisy agent behavior,
* excessive repeated selection.

A negative result is scientifically valid.

---

# 126. Common Implementation Errors

The implementation must avoid:

### Error 1: Fake UCB-V

Using:

```python
sqrt(log(t) / n)
```

while storing but not using reward variance.

This is not UCB-V.

---

### Error 2: Hard-Coded Rewards

Assigning rewards manually based on expected scenario importance.

Rewards must come from execution evidence.

---

### Error 3: Hidden Holdout Leakage

Using holdout outcomes to tune the selector.

This invalidates generalization results.

---

### Error 4: Budget Blindness

Selecting expensive candidates without checking remaining budget.

---

### Error 5: Token-Only Cost

Treating token consumption as the complete evaluation cost when branching, execution, analysis, and verification also consume resources.

---

### Error 6: Post-Hoc Tuning

Changing policy weights after observing the results without separating tuning and evaluation data.

---

### Error 7: Candidate/Failure Confusion

Treating a candidate attack as a discovered failure.

---

### Error 8: Branching Free-of-Charge

Ignoring snapshot, restore, isolation, and branch execution overhead.

---

### Error 9: Single-Run Conclusions

Declaring an adaptive policy effective from one experiment.

---

# 127. Recommended Implementation Order

Implement the subsystem in this order:

```text
1. Candidate data model
        ↓
2. Candidate validation
        ↓
3. Budget interface
        ↓
4. Random policy
        ↓
5. Uniform policy
        ↓
6. Reward recording
        ↓
7. Candidate statistics
        ↓
8. Empirical variance
        ↓
9. UCB-V policy
        ↓
10. Cost tracking
        ↓
11. Cost-aware selection
        ↓
12. Novelty calculation
        ↓
13. Composite policy
        ↓
14. Selection logging
        ↓
15. Experimental comparison
```

Do not implement the composite policy first.

That would make it extremely difficult to determine which component actually produced an observed effect.

---

# 128. Recommended Repository Structure

```text
src/
└── agent_eval/
    └── selection/
        ├── __init__.py
        ├── base.py
        ├── random_policy.py
        ├── uniform_policy.py
        ├── ucb_v.py
        ├── cost_aware.py
        ├── novelty.py
        ├── composite.py
        ├── candidate_stats.py
        ├── reward.py
        ├── budget.py
        ├── selector.py
        └── models.py
```

Tests:

```text
tests/
└── selection/
    ├── test_candidate_stats.py
    ├── test_reward.py
    ├── test_ucb_v.py
    ├── test_budget.py
    ├── test_random_policy.py
    ├── test_uniform_policy.py
    ├── test_cost_aware.py
    └── test_selector.py
```

---

# 129. Configuration Example

```yaml
selection:
  policy: ucb_v

  budget:
    total: 1000
    unit: execution_units

  initialization:
    strategy: sample_each_candidate_once

  reward:
    type: new_validated_failure_family
    min: 0
    max: 1

  ucb_v:
    reward_bound: 1.0

  cost:
    enabled: false

  novelty:
    enabled: false

  branch_value:
    enabled: false

  repetition:
    enabled: true
```

This configuration represents the clean baseline UCB-V experiment.

---

# 130. Extended Configuration Example

```yaml
selection:
  policy: cost_aware_novelty_ucbv

  budget:
    total: 1000
    unit: execution_units

  initialization:
    strategy: sample_each_candidate_once

  reward:
    type: composite
    components:
      validated_failure: 1.0
      new_failure_family: 1.0
      state_coverage: 0.25

  ucb_v:
    reward_bound: 1.0

  cost:
    enabled: true
    normalization: total_budget
    weight: 0.25

  novelty:
    enabled: true
    weight: 0.20

  branch_value:
    enabled: true
    weight: 0.15
```

The exact weights are experimental parameters, not universal constants.

---

# 131. Selection Output

The selector shall return:

```yaml
selection_output:
  candidate_id:
  policy:
  score:
  estimated_cost:
  budget_remaining:
  selection_round:
  decision_id:
```

The execution engine then consumes the candidate.

---

# 132. Feedback Loop

The complete adaptive loop is:

```text
              ┌─────────────────────┐
              │   Candidate Pool    │
              └──────────┬──────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Adaptive Scorer │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Budget Manager  │
                └────────┬────────┘
                         │
                         ▼
                  Selected Test
                         │
                         ▼
                ┌─────────────────┐
                │ Agent Execution │
                └────────┬────────┘
                         │
                         ▼
                 Observed Result
                         │
                         ▼
              ┌─────────────────────┐
              │ Validation Engine   │
              └──────────┬──────────┘
                         │
                         ▼
                    Reward
                         │
                         ▼
              ┌─────────────────────┐
              │ Statistics Update  │
              └──────────┬──────────┘
                         │
                         └───────────────┐
                                         │
                                         ▼
                                Adaptive Scorer
```

This feedback loop is the core adaptive mechanism of the research system.

---

# 133. Research Interpretation

The adaptive selector should be considered successful only if experimental evidence demonstrates an improvement on a predefined metric under a fair comparison.

Possible outcomes include:

```text
SUPPORTED
NOT SUPPORTED
INCONCLUSIVE
CONDITIONAL
```

For example:

> Adaptive selection produced more validated failure families under the tested budget and experimental conditions.

is an evidence-based result.

The system must not assume beforehand that:

> Adaptive selection is better.

---

# 134. Definition of Done

The Adaptive Test Selection subsystem is complete enough for the first research experiment when:

* [ ] Candidate scenarios can be represented.
* [ ] Candidate validation exists.
* [ ] Candidate eligibility is enforced.
* [ ] A centralized budget manager exists.
* [ ] Random selection works.
* [ ] Uniform selection works.
* [ ] Candidate rewards are recorded.
* [ ] Candidate execution counts are recorded.
* [ ] Empirical means are calculated.
* [ ] Empirical reward variance is calculated.
* [ ] UCB-V is implemented according to a documented formulation.
* [ ] Untested candidates receive explicit exploration treatment.
* [ ] Selection decisions are logged.
* [ ] Budget reservation is enforced.
* [ ] Actual cost is recorded.
* [ ] Reward updates occur only after valid execution/validation.
* [ ] Holdout information is isolated.
* [ ] Candidate statistics are reproducible.
* [ ] Multiple selection policies can use the same interface.
* [ ] Baseline comparisons can be executed under equivalent budgets.
* [ ] Selection curves can be generated from actual experiment data.
* [ ] Selection policy versions are recorded.
* [ ] Unit tests verify the mathematical behavior of the selector.
* [ ] At least one repeated-seed experiment can compare adaptive and non-adaptive selection.

---

# 135. Final Specification

The adaptive test selection mechanism is defined as:

$$
\boxed{
\text{Generate}
\rightarrow
\text{Validate}
\rightarrow
\text{Estimate}
\rightarrow
\text{Select}
\rightarrow
\text{Execute}
\rightarrow
\text{Validate Outcome}
\rightarrow
\text{Reward}
\rightarrow
\text{Update}
\rightarrow
\text{Select Again}
}
$$

under:

$$
\boxed{
Cost_{total}
\leq
Budget_{experiment}
}
$$

The initial scientifically clean configuration is:

```text
Static Candidate Pool
        +
Fixed Evaluation Budget
        +
Binary Validated-Failure Reward
        +
Random Baseline
        +
Uniform Baseline
        +
UCB-V Adaptive Selection
```

The extended proposed mechanism may subsequently add:

```text
Cost Awareness
+
Novelty
+
State Coverage
+
Branch Potential
```

but these additions must be introduced through controlled ablations.

The central experimental question remains:

> **Does adaptive selection allocate a fixed evaluation budget more effectively for discovering and validating AI-agent security and reliability failures than non-adaptive selection strategies?**

The answer must come from measured experiments, not from the sophistication of the scoring formula. A 40-line equation is still just a 40-line equation until the data has had its unpleasant little say.
