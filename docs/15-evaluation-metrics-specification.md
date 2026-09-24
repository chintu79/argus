# Evaluation Metrics Specification

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** MET-01
**Document Type:** Evaluation Metrics Specification
**Version:** 1.0
**Status:** Draft for Implementation

---

# 1. Purpose

This document defines the quantitative metrics used to evaluate the proposed **Budget-Constrained Adaptive Security Evaluation of AI Agents** framework.

The metric system must determine whether the proposed evaluation strategy provides measurable improvements in:

1. Failure discovery
2. Unique failure-family discovery
3. Budget efficiency
4. Discovery speed
5. Failure validation quality
6. Failure reproducibility
7. Metamorphic robustness
8. Hidden-holdout generalization
9. Branching efficiency
10. Evaluator reliability
11. Adaptive-selection quality
12. Statistical stability

The metrics are designed to answer the project's research questions without collapsing different properties into a single arbitrary score.

---

# 2. Measurement Philosophy

The evaluation framework must distinguish:

```text
Finding a failure
        ≠
Finding a new failure family
        ≠
Validating a failure
        ≠
Reproducing a failure
        ≠
Generalizing a failure
        ≠
Finding it efficiently
```

Therefore, the project will report a **metric vector** rather than one overall “performance score.”

The primary result should look conceptually like:

$$
M =
(
D,
F,
E,
R,
MCR,
G,
B,
V
)
$$

where:

* \(D\) = discovery metrics
* \(F\) = failure-family metrics
* \(E\) = efficiency metrics
* \(R\) = reproducibility metrics
* \(MCR\) = metamorphic consistency
* \(G\) = generalization metrics
* \(B\) = branching metrics
* \(V\) = evaluator reliability

---

# 3. Measurement Unit

Every metric must specify its denominator and population.

Possible populations:

```text
Execution
Scenario
Candidate
Invariant Evaluation
Failure Occurrence
Validated Failure
Failure Family
Metamorphic Test
Holdout Scenario
Experiment Run
```

A metric must never mix incompatible populations without explicitly defining the aggregation method.

---

# 4. Metric Categories

The framework defines the following metric groups:

| Group                 | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| Discovery             | How many failures are found                          |
| Novelty               | How many distinct failure families are found         |
| Efficiency            | How much budget is required                          |
| Time-to-Discovery     | How quickly failures are discovered                  |
| Validation            | How many detected failures survive validation        |
| Reproducibility       | Whether failures can be independently reproduced     |
| Metamorphic           | Whether protected properties survive transformations |
| Generalization        | Whether findings transfer to unseen scenarios        |
| Branching             | Whether state-based branching saves evaluation cost  |
| Adaptive Selection    | Whether selection prioritizes useful candidates      |
| Evaluator Reliability | Whether the evaluator itself is trustworthy          |
| Statistical Stability | Whether conclusions survive repeated runs            |

---

# 5. Primary Research Metrics

The primary metrics for the main experiment are:

```text
M1  Validated Failure Count
M2  Unique Failure Family Count
M3  Failure Discovery Rate
M4  Failure-Family Discovery Rate
M5  Cost per Validated Failure
M6  Cost per New Failure Family
M7  Time/Execution to First Validated Failure
M8  Reproduction Rate
M9  Metamorphic Consistency Rate
M10 Hidden-Holdout Generalization Rate
```

Secondary metrics provide diagnostic information.

---

# 6. Metric Status

Each metric should have a status:

```text
PRIMARY
SECONDARY
DIAGNOSTIC
```

Only primary metrics should be used for the main hypothesis tests.

---

# 7. Metric Definition Template

Every implemented metric must define:

```yaml
metric:
  metric_id:
  name:
  category:

  numerator:
  denominator:

  population:
  aggregation:

  direction:
  higher_is_better:

  confidence_interval:
  statistical_test:

  exclusions:
  interpretation:
```

---

# 8. Direction of Improvement

Metrics must explicitly define whether higher or lower is desirable.

Examples:

```text
Validated failures       → higher
Failure families         → higher
Discovery rate            → higher
Reproduction rate         → higher
Generalization rate       → higher
Cost per failure          → lower
Cost per family           → lower
Time to first failure     → lower
Evaluator error rate      → lower
Inconclusive rate         → lower
```

This avoids the classic human tradition of creating a chart and deciding afterward which direction means “good.”

---

# 9. Failure Occurrence Count

Define:

$$
F_{occ}
=
N(\text{validated failure occurrences})
$$

This counts validated failure instances.

It does **not** count:

* raw anomalies,
* invalid executions,
* evaluator errors,
* unvalidated candidates.

---

# 10. Validated Failure Count

Primary metric:

$$
VFC = N_{validated\ failures}
$$

This is the number of failure records that survive the validation process.

It is a core discovery metric.

---

# 11. Unique Failure Fingerprint Count

Let each validated failure have a canonical fingerprint.

Then:

$$
UFF =
|\{fingerprint(f): f \in F_{validated}\}|
$$

This measures distinct observed failure signatures.

It should not be interpreted as the number of causal root causes.

---

# 12. Failure Family Count

After clustering:

$$
FFC =
N_{failure\ families}
$$

where each family is generated using a versioned clustering configuration.

This is the main novelty/discovery metric.

---

# 13. Important Distinction

The system must report:

```text
Validated Failure Occurrences
Unique Failure Fingerprints
Failure Families
```

separately.

Example:

```text
120 validated failures
42 unique fingerprints
15 failure families
```

These numbers answer different questions.

---

# 14. Failure Discovery Rate

Define:

$$
FDR =
\frac{
N_{validated\ failures}
}{
N_{valid\ executions}
}
$$

This measures the rate at which valid executions produce validated failures.

It is useful but should not be treated as sufficient evidence of evaluator quality.

---

# 15. Failure-Family Discovery Rate

Define:

$$
FFDR =
\frac{
N_{new\ validated\ failure\ families}
}{
N_{valid\ executions}
}
$$

This measures the rate of discovering previously unseen validated families.

---

# 16. Unique Family Discovery Yield

For budget \(B\):

$$
Y_{family}(B)
=
N_{unique\ validated\ families\ discovered\ by\ }B
$$

This is especially important for comparing:

```text
Random
Uniform
UCB-V
Cost-aware UCB-V
Novelty-augmented
Branch-aware
```

---

# 17. Cumulative Failure Discovery Curve

For each execution budget \(b\):

$$
D_F(b)
=
N_{validated\ failures\ discovered\ by\ }b
$$

Plot:

```text
Budget
   vs
Cumulative Validated Failures
```

This is one of the primary experiment visualizations.

---

# 18. Cumulative Failure-Family Curve

Similarly:

$$
D_{FF}(b)
=
N_{failure\ families\ discovered\ by\ }b
$$

This should be plotted independently from raw failure count.

---

# 19. Discovery Area Under Curve

For comparing discovery efficiency across a fixed budget:

$$
AUC_{family}
=
\int_0^B D_{FF}(b)\,db
$$

For discrete experiments:

$$
AUC_{family}
\approx
\sum_{i=1}^{n}
D_{FF}(b_i)\Delta b_i
$$

Higher values indicate more cumulative discovery over the budget horizon.

---

# 20. Why AUC Is Useful

Two methods may discover the same final number of families.

Example:

```text
Method A:
discovers most families early

Method B:
discovers them near the end
```

Final family count is identical.

AUC distinguishes their discovery trajectories.

---

# 21. Cost per Validated Failure

Define:

$$
CPF =
\frac{
C_{total}
}{
N_{validated\ failures}
}
$$

where:

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

Lower is better.

If zero validated failures are found, report:

```text
N/A
```

rather than infinity unless the statistical analysis explicitly requires a transformed representation.

---

# 22. Cost per New Failure Family

Primary efficiency metric:

$$
CPFF =
\frac{
C_{total}
}{
N_{new\ validated\ failure\ families}
}
$$

This is more directly aligned with the project's adaptive-selection objective.

---

# 23. Cost Normalization

Cost must be measured using the same budget definition across compared methods.

Possible budget units:

```text
MODEL_CALLS
TOKENS
EXECUTION_UNITS
COMPUTE_TIME
WALL_CLOCK
MONETARY_COST
COMPOSITE_COST
```

The selected budget unit must be declared before experiments.

---

# 24. Composite Cost

If multiple cost dimensions matter:

$$
C =
w_mC_{model}
+
w_eC_{execution}
+
w_bC_{branch}
+
w_sC_{snapshot}
+
w_aC_{analysis}
+
w_vC_{verification}
$$

Weights must be predefined.

They must not be tuned after observing experimental results.

---

# 25. Budget Utilization

$$
BU =
\frac{
C_{actual}
}{
C_{allocated}
}
$$

This measures whether the evaluation system used its available budget correctly.

Values above the permitted threshold indicate budget overshoot.

---

# 26. Budget Overshoot

$$
BO =
\max(0,C_{actual}-C_{allocated})
$$

Report both:

```text
absolute overshoot
relative overshoot
```

The preferred implementation should keep overshoot at zero or within an explicitly defined execution tolerance.

---

# 27. Time to First Validated Failure

$$
TTFV =
C_{until\ first\ validated\ failure}
$$

The cost unit should match the experiment budget.

Possible units:

```text
executions
model calls
tokens
compute time
monetary cost
```

---

# 28. Time to First New Failure Family

$$
TTFF =
C_{until\ first\ new\ failure\ family}
$$

This is often more informative than first raw failure discovery.

---

# 29. Discovery at Fixed Budget

For a fixed budget \(B\):

$$
DF(B)=
N_{validated\ failures}(B)
$$

and:

$$
DFF(B)=
N_{failure\ families}(B)
$$

These are primary comparison values.

---

# 30. Relative Discovery Improvement

For a proposed method \(P\) and baseline \(B\):

$$
RDI =
\frac{
D_P-D_B
}{
D_B
}
$$

This should be reported only when the baseline denominator is non-zero.

If the baseline finds zero failures, report the absolute difference and avoid an unstable percentage.

---

# 31. Relative Cost Reduction

$$
RCR =
\frac{
C_B-C_P
}{
C_B
}
$$

where lower cost represents improved efficiency.

Again, this should not be used when the denominator is zero.

---

# 32. Validation Rate

Let:

* \(F_c\) = detected failure candidates
* \(F_v\) = validated failures

Then:

$$
VR =
\frac{
F_v
}{
F_c
}
$$

This measures how many detected candidates survive validation.

A low rate may indicate noisy detection or weak scenario construction.

---

# 33. Candidate Invalidity Rate

$$
CIR =
\frac{
N_{invalid\ candidates}
}{
N_{failure\ candidates}
}
$$

Possible causes include:

* invalid scenario,
* invalid execution,
* evaluator error,
* corrupted evidence,
* environment failure.

These causes should be reported separately.

---

# 34. Evidence Completeness

For a failure candidate:

$$
EC =
\frac{
RequiredEvidencePresent
}{
RequiredEvidenceTotal
}
$$

Aggregate:

$$
MeanEC =
\frac{1}{N}
\sum_i EC_i
$$

Validated failures should normally have complete required evidence.

---

# 35. Invariant Coverage

Define:

$$
IC =
\frac{
N_{evaluated\ applicable\ invariants}
}{
N_{applicable\ invariants}
}
$$

This measures evaluation coverage.

It should not count `NOT_APPLICABLE` invariants in the numerator.

---

# 36. Invariant Failure Rate

For invariant \(I\):

$$
IFR_I =
\frac{
N_{FAIL}(I)
}{
N_{valid\ evaluations}(I)
}
$$

This allows analysis by invariant.

Example:

```text
I-AUTH-001 → 8.2%
I-DATA-001 → 3.4%
I-POL-001  → 5.7%
```

These are measurements, not rankings of invariants.

---

# 37. Inconclusive Rate

$$
IR =
\frac{
N_{INCONCLUSIVE}
}{
N_{evaluation\ attempts}
}
$$

High inconclusive rates may indicate:

* poor observability,
* incomplete traces,
* inadequate evidence requirements,
* unstable infrastructure.

---

# 38. Evaluator Error Rate

$$
EER =
\frac{
N_{ERROR}
}{
N_{evaluation\ attempts}
}
$$

This measures failures of the evaluation infrastructure itself.

---

# 39. Evaluator Determinism

Given identical:

```text
trace
invariant
configuration
state
```

define:

$$
ED =
\frac{
N_{identical\ repeated\ results}
}{
N_{repeated\ evaluations}
}
$$

Target:

$$
ED \approx 1
$$

for deterministic invariant evaluators.

---

# 40. Known-Failure Detection Rate

For a reference set of known seeded failures:

$$
KFDR =
\frac{
N_{known\ failures\ detected}
}{
N_{known\ failures}
}
$$

This measures whether the evaluator detects deliberately injected violations.

---

# 41. Known-Failure False Negative Rate

$$
KFN =
1-KFDR
$$

This should be measured on a controlled reference suite.

---

# 42. False Positive Rate

When a trusted negative/reference set exists:

$$
FPR =
\frac{
N_{incorrectly\ flagged\ valid\ executions}
}{
N_{valid\ negative\ executions}
}
$$

This requires a sufficiently controlled reference population.

It should not be invented from ordinary experimental runs without a ground-truth construction.

---

# 43. Precision of Failure Detection

When ground truth is available:

$$
Precision =
\frac{
TP
}{
TP+FP
}
$$

---

# 44. Recall of Failure Detection

$$
Recall =
\frac{
TP
}{
TP+FN
}
$$

These metrics are appropriate for evaluator validation where known ground truth exists.

They are not automatically available for open-ended failure discovery.

---

# 45. F1 Score

When both precision and recall can be established:

$$
F1 =
2
\frac{
Precision\cdot Recall
}{
Precision+Recall
}
$$

This is a diagnostic evaluator metric.

It should not be used as the primary metric for open-ended discovery.

---

# 46. Failure Family Purity

For controlled synthetic experiments where true family labels are known:

$$
Purity =
\frac{1}{N}
\sum_k
\max_j |C_k \cap T_j|
$$

where:

* \(C_k\) = discovered cluster,
* \(T_j\) = reference family.

This is appropriate only when a trustworthy reference family assignment exists.

---

# 47. Failure Family Completeness

For controlled reference families:

$$
Completeness =
\frac{1}{N}
\sum_j
\max_k |T_j \cap C_k|
$$

This complements cluster purity.

---

# 48. Adjusted Rand Index

For synthetic validation datasets with trusted family labels:

$$
ARI =
AdjustedRandIndex(
PredictedFamilies,
ReferenceFamilies
)
$$

This is a clustering-validation metric.

It should not be presented as evidence that the discovered families represent causal root causes.

---

# 49. Failure Family Stability

Run clustering multiple times under controlled perturbations.

Define:

$$
FamilyStability =
Agreement(
ClusterRun_1,\ldots,ClusterRun_n
)
$$

Possible measures:

```text
Adjusted Rand Index
Normalized Mutual Information
Jaccard overlap
pairwise co-clustering agreement
```

The exact measure should be fixed before the analysis.

---

# 50. Family Reproduction Rate

Let \(F_f\) be a family.

$$
FRR_f =
\frac{
N_{reproduced\ occurrences}
}{
N_{valid\ reproduction\ attempts}
}
$$

Aggregate family reproduction can be reported as:

```text
micro-average
macro-average
```

Both should be distinguished.

---

# 51. Overall Reproduction Rate

$$
ORR =
\frac{
N_{reproduced\ attempts}
}{
N_{valid\ reproduction\ attempts}
}
$$

This excludes invalid and evaluator-error attempts from the denominator.

---

# 52. Reproduction Stability

For each failure \(f\):

$$
R_f =
\frac{
N_{reproduced}
}{
N_{valid\ reproduction\ attempts}
}
$$

Classify:

```text
STABLE
VARIABLE
FLAKY
NON_REPRODUCED
INCONCLUSIVE
```

Thresholds must be predefined.

---

# 53. Flakiness Rate

For failures with repeated valid attempts:

$$
FlakinessRate =
\frac{
N_{FLAKY\ failures}
}{
N_{repeated\ failures}
}
$$

Flaky failures must remain visible in the results.

They must not automatically be discarded.

---

# 54. Metamorphic Consistency Rate

For valid metamorphic tests:

$$
MCR =
\frac{
N_{relations\ satisfied}
}{
N_{valid\ metamorphic\ tests}
}
$$

Higher values indicate greater consistency with the declared metamorphic relations.

---

# 55. Metamorphic Violation Rate

$$
MVR =
\frac{
N_{relations\ violated}
}{
N_{valid\ metamorphic\ tests}
}
$$

This measures robustness violations under defined transformations.

---

# 56. Metamorphic Inconclusive Rate

$$
MIR =
\frac{
N_{inconclusive\ metamorphic\ tests}
}{
N_{metamorphic\ attempts}
}
$$

This is important because transformations can fail independently of agent behavior.

---

# 57. Transformation-Specific Metrics

For transformation \(T\):

$$
MCR_T =
\frac{
N_{passed}(T)
}{
N_{valid}(T)
}
$$

Report separately for:

```text
FORMAT_ONLY
SYNTHETIC_ID_RENAME
IRRELEVANT_CONTEXT
TASK_PARAPHRASE
```

---

# 58. Relation-Specific Metrics

For relation \(R\):

$$
MCR_R =
\frac{
N_{satisfied}(R)
}{
N_{valid}(R)
}
$$

This prevents a strong performance on one relation type from hiding weakness on another.

---

# 59. Hidden-Holdout Generalization

Let:

* \(F_{dev}\) = validated failure families discovered during development
* \(F_{holdout}\) = corresponding families observed on holdout scenarios

A basic transfer metric is:

$$
HGR =
\frac{
N_{holdout\ families\ matching\ validated\ development\ mechanisms}
}{
N_{eligible\ holdout\ families}
}
$$

The matching rule must be frozen before holdout evaluation.

---

# 60. Holdout Family Generalization Rate

For development failure families:

$$
FG =
\frac{
N_{development\ families\ observed\ on\ holdout}
}{
N_{eligible\ development\ families}
}
$$

This measures whether discovered failure mechanisms transfer beyond the development scenarios.

---

# 61. Holdout Detection Rate

For holdout scenarios with expected seeded violations:

$$
HDR =
\frac{
N_{holdout\ violations\ detected}
}{
N_{holdout\ violations}
}
$$

This requires known ground truth.

---

# 62. Holdout False Positive Rate

When holdout negative cases exist:

$$
HFPR =
\frac{
N_{valid\ holdout\ executions\ incorrectly\ flagged}
}{
N_{valid\ holdout\ negative\ executions}
}
$$

---

# 63. Generalization Gap

If the same metric can be computed on development and holdout sets:

$$
GG =
Metric_{development}
-
Metric_{holdout}
$$

For metrics where lower is better, the interpretation must account for direction.

Report the signed gap and the absolute gap.

---

# 64. Branching Metrics

Branching exists to reuse valuable execution states instead of repeatedly executing the complete scenario from scratch.

Therefore branching must be evaluated independently.

---

# 65. Branch Yield

$$
BY =
\frac{
N_{validated\ failures\ discovered\ through\ branches}
}{
N_{branch\ executions}
}
$$

This measures failure discovery yield per branch.

---

# 66. Branch Failure-Family Yield

$$
BFY =
\frac{
N_{new\ families\ discovered\ through\ branches}
}{
N_{branch\ executions}
}
$$

This is more aligned with novelty discovery.

---

# 67. Branching Cost

Total branching cost:

$$
C_{branch,total}
=
C_{snapshot}
+
C_{restore}
+
C_{branch\ execution}
+
C_{branch\ analysis}
$$

All components must be measured.

---

# 68. Branch Cost per New Family

$$
BCPF =
\frac{
C_{branch,total}
}{
N_{new\ branch\ families}
}
$$

Lower is better.

---

# 69. Branching Efficiency Gain

Compare branching against independent complete execution:

$$
BEG =
\frac{
C_{independent}-C_{branching}
}{
C_{independent}
}
$$

Positive values indicate lower cost under the defined cost model.

---

# 70. Snapshot Overhead

$$
SO =
\frac{
C_{snapshot}+C_{restore}
}{
C_{branch,total}
}
$$

This determines whether state snapshotting itself consumes a substantial fraction of the branching budget.

---

# 71. Branch Reuse Ratio

$$
BRR =
\frac{
N_{branch\ executions}
}{
N_{snapshots}
}
$$

This measures how many branches are produced per snapshot.

---

# 72. Branch Isolation Failure Rate

$$
BIFR =
\frac{
N_{branches\ violating\ isolation}
}{
N_{valid\ branches}
}
$$

A branch isolation violation is primarily a state/evaluator correctness issue and must be classified separately from ordinary agent failures.

---

# 73. Adaptive Selection Metrics

Adaptive selection must be evaluated independently from final failure counts.

---

# 74. Selection Novelty Yield

$$
SNY =
\frac{
N_{new\ failure\ families}
}{
N_{selected\ candidates}
}
$$

This measures the selector's ability to choose productive candidates.

---

# 75. Selection Failure Yield

$$
SFY =
\frac{
N_{validated\ failures}
}{
N_{selected\ candidates}
}
$$

---

# 76. Selection Cost Efficiency

$$
SCE =
\frac{
N_{new\ families}
}{
C_{selection}+C_{execution}
}
$$

This measures family discovery per unit cost.

---

# 77. Candidate Utilization

$$
CU =
\frac{
N_{executed\ candidates}
}{
N_{available\ candidates}
}
$$

This is descriptive and should not be interpreted as selection quality by itself.

---

# 78. Exploration Rate

For a selector:

$$
ER =
\frac{
N_{previously\ untested\ candidates\ selected}
}{
N_{selected\ candidates}
}
$$

This helps characterize exploration behavior.

---

# 79. Exploitation Rate

$$
EXR =
\frac{
N_{previously\ tested\ candidates\ selected}
}{
N_{selected\ candidates}
}
$$

The two rates should be reported together.

---

# 80. Adaptive Reward

For the recommended initial experiment:

$$
r_t =
\begin{cases}
1 & \text{if execution discovers a new validated failure family}\\
0 & \text{otherwise}
\end{cases}
$$

The reward must be generated after validation and clustering.

---

# 81. Cumulative Reward

$$
CR_T =
\sum_{t=1}^{T}r_t
$$

Under the binary new-family reward definition:

$$
CR_T =
N_{new\ validated\ families}
$$

assuming each family can generate reward only on its first validated discovery.

---

# 82. Reward Density

$$
RD =
\frac{
\sum_t r_t
}{
C_{total}
}
$$

This measures reward per unit evaluation cost.

---

# 83. Selector Overhead

Adaptive selection itself consumes resources.

Measure:

$$
SOH =
C_{selection}
$$

and:

$$
SOHR =
\frac{
C_{selection}
}{
C_{total}
}
$$

This is essential because an adaptive strategy that spends enormous resources choosing the next test may erase its execution savings. Humanity has invented enough optimization loops that cost more than the thing being optimized.

---

# 84. Baseline Comparison Metrics

Every main experiment should report:

```text
Random
Uniform
Adaptive
```

at minimum.

Recommended extended comparison:

```text
Random
Uniform
UCB-V
Cost-Aware UCB-V
Novelty-Augmented UCB-V
Branch-Aware Adaptive
```

---

# 85. Fixed-Budget Comparison

For every method \(m\):

$$
D_m(B)
=
N_{families\ discovered\ by\ budget\ }B
$$

Methods must receive equivalent budgets.

---

# 86. Equal-Candidate Comparison

All methods must use the same candidate pool unless candidate-generation diversity is itself being studied.

This isolates the selection effect.

---

# 87. Equal-Execution Comparison

For an execution-count analysis:

$$
B_{execution}
=
N_{executions}
$$

This is useful when monetary or token costs are unavailable.

---

# 88. Equal-Cost Comparison

For realistic efficiency evaluation:

$$
B_{cost}
=
C_{total}
$$

This is the preferred comparison when execution costs differ materially.

---

# 89. Statistical Unit

The independent statistical unit should normally be the **experiment run/seed**, not the individual event.

For example:

```text
20 experiment seeds
×
same evaluation method
```

is preferable to treating:

```text
20,000 tool events
```

as 20,000 independent samples.

---

# 90. Repeated Runs

Each method should be executed over multiple independent seeds.

Recommended initial target:

```text
20 independent runs
```

unless computational constraints require fewer.

The actual number must be declared before final analysis.

---

# 91. Per-Run Metrics

Compute metrics independently per run before aggregation.

Example:

```text
Run 1 → 12 families
Run 2 → 9 families
Run 3 → 15 families
...
```

Do not pool all executions first and then pretend the resulting observations are independent.

---

# 92. Mean and Median

For each primary metric report:

```text
mean
median
standard deviation
interquartile range
```

The median is especially useful for skewed cost metrics.

---

# 93. Confidence Intervals

For primary metrics, report:

$$
95\%\ CI
$$

using an appropriate method.

For small samples or non-normal metrics, bootstrap confidence intervals are recommended.

---

# 94. Bootstrap Procedure

For a metric \(M\):

1. Collect one metric value per independent run.
2. Resample runs with replacement.
3. Recompute the aggregate.
4. Repeat sufficiently many times.
5. Use the empirical interval for the confidence bounds.

Bootstrap settings must be recorded.

---

# 95. Comparing Adaptive vs Baseline

For paired experiments where runs use matched seeds:

$$
\Delta_i =
M_{adaptive,i}
-
M_{baseline,i}
$$

Analyze the paired differences.

---

# 96. Non-Parametric Comparison

For small or non-normal samples, use an appropriate paired non-parametric test such as:

```text
Wilcoxon signed-rank test
```

The exact statistical test should be fixed before inspecting final outcomes.

---

# 97. Effect Size

Statistical significance alone is insufficient.

Report effect size.

Possible choices:

```text
paired standardized mean difference
Cliff's delta
rank-biserial correlation
```

The selected effect-size measure must be consistent across the study.

---

# 98. Multiple Comparisons

If many pairwise comparisons are performed, control the false discovery rate or family-wise error rate using a predefined method.

Example:

```text
Benjamini-Hochberg
```

Do not silently run dozens of comparisons and celebrate whichever p-value survives.

---

# 99. Statistical Significance

The project may use:

$$
\alpha = 0.05
$$

as the conventional threshold.

This threshold must be declared before final hypothesis testing.

Statistical significance must not be interpreted as practical importance.

---

# 100. Practical Effect

For each main result report:

```text
absolute difference
relative difference where valid
effect size
confidence interval
p-value where applicable
```

---

# 101. Main Hypothesis Metrics

### H1: Adaptive discovery efficiency

Primary:

```text
Failure-family AUC
Cost per new family
Fixed-budget family count
```

### H2: Branching efficiency

Primary:

```text
Cost per new family
Branching efficiency gain
```

### H3: Failure quality

Primary:

```text
Validated failure count
Validated family count
Validation rate
```

### H4: Reproducibility

Primary:

```text
Overall reproduction rate
Family reproduction rate
```

### H5: Metamorphic robustness

Primary:

```text
Metamorphic consistency rate
Metamorphic violation rate
```

### H6: Generalization

Primary:

```text
Holdout generalization rate
Holdout detection rate where ground truth exists
```

---

# 102. Discovery Quality Vector

Rather than a single discovery score:

$$
DQ =
(
VFC,
FFC,
AUC_{family},
CPFF,
TTFF
)
$$

This provides a multidimensional view of discovery quality.

---

# 103. Validation Quality Vector

$$
VQ =
(
VR,
EC,
ORR,
MCR
)
$$

where:

* \(VR\) = validation rate
* \(EC\) = evidence completeness
* \(ORR\) = reproduction rate
* \(MCR\) = metamorphic consistency

---

# 104. Generalization Quality Vector

$$
GQ =
(
HGR,
HDR,
GG
)
$$

---

# 105. Evaluator Reliability Vector

$$
ER =
(
KFDR,
FPR,
EER,
IR,
ED
)
$$

where:

* \(KFDR\) = known-failure detection rate
* \(FPR\) = false positive rate
* \(EER\) = evaluator error rate
* \(IR\) = inconclusive rate
* \(ED\) = evaluator determinism

---

# 106. No Overall Composite Score

The main research results must **not** be reduced to:

$$
OverallScore =
w_1M_1+w_2M_2+\cdots+w_nM_n
$$

unless a separate, explicitly justified study is designed for that purpose.

The project should not manufacture a magical “87.4% evaluator goodness” number by assigning arbitrary weights to unrelated properties.

---

# 107. Failure Discovery Curve

Primary visualization:

```text
Y-axis:
Cumulative validated failure families

X-axis:
Cumulative evaluation budget
```

Plot one curve per method.

---

# 108. Cost-Efficiency Curve

Plot:

```text
X:
Evaluation cost

Y:
Cumulative validated failure families
```

This directly visualizes budget efficiency.

---

# 109. Failure Family Saturation

Measure the point at which additional budget produces few or no new families.

A simple diagnostic:

$$
MarginalYield_t =
\frac{
F_t-F_{t-k}
}{
C_t-C_{t-k}
}
$$

where \(k\) is a predefined window.

---

# 110. Discovery Saturation Point

Define a threshold \(\epsilon\).

The saturation point may be estimated as the earliest budget \(B_s\) where:

$$
MarginalYield(B_s)<\epsilon
$$

for a predefined number of consecutive evaluation windows.

This is a diagnostic metric and should not be tuned after seeing the curves.

---

# 111. Failure Distribution Metrics

Report failures by:

```text
category
subcategory
mechanism
scenario
invariant
tool
branch depth
execution mode
severity
```

These are descriptive metrics.

---

# 112. Scenario Coverage

$$
SC =
\frac{
N_{scenarios\ executed}
}{
N_{scenarios\ available}
}
$$

This does not imply security coverage.

It only measures execution coverage.

---

# 113. Invariant Coverage by Scenario

For scenario \(s\):

$$
IC_s =
\frac{
N_{evaluated\ applicable\ invariants}
}{
N_{applicable\ invariants}
}
$$

This identifies scenarios with weak observability.

---

# 114. Tool Coverage

$$
TC =
\frac{
N_{tools\ exercised}
}{
N_{tools\ available}
}
$$

Report separately by:

```text
read
write
notification
database
external service
```

---

# 115. Attack-Surface Coverage

Let \(A\) be defined attack surfaces:

```text
task input
tool arguments
tool responses
database content
identity
authorization
policy
state
sequence
fault
resource
```

Then:

$$
ASC =
\frac{
N_{attack\ surfaces\ exercised}
}{
N_{attack\ surfaces\ in\ experiment}
}
$$

This is coverage, not effectiveness.

---

# 116. Branch Depth

For branch \(b\):

$$
Depth(b)
=
N_{branch\ transformations\ from\ root}
$$

Report:

```text
mean
median
maximum
distribution
```

---

# 117. Branch Failure Depth

For a discovered failure:

$$
FD =
Depth(branch\ containing\ failure)
$$

This can help determine whether deeper branching explores useful states.

---

# 118. Snapshot Reuse Efficiency

$$
SRE =
\frac{
N_{branch\ executions}
}{
N_{snapshots}
}
$$

Higher values mean each snapshot supports more branch executions.

This must be interpreted alongside branch quality.

---

# 119. Snapshot Correctness

$$
SCorrect =
\frac{
N_{successful\ snapshot\ restores}
}{
N_{snapshot\ restore\ attempts}
}
$$

A failed restoration must not be silently counted as a valid branch.

---

# 120. Reproducibility Cost

$$
CRC =
\frac{
C_{reproduction}
}{
N_{reproduced\ failures}
}
$$

This measures the cost of validating discovered failures.

---

# 121. Metamorphic Cost

$$
MTC =
\frac{
C_{metamorphic}
}{
N_{valid\ metamorphic\ tests}
}
$$

---

# 122. Holdout Cost

$$
HOC =
\frac{
C_{holdout}
}{
N_{holdout\ executions}
}
$$

Holdout cost must be reported separately from development cost.

---

# 123. End-to-End Evaluation Cost

$$
C_{end-to-end}
=
C_{discovery}
+
C_{reproduction}
+
C_{metamorphic}
+
C_{holdout}
$$

This is useful for practical deployment analysis.

---

# 124. Failure Evidence Density

A diagnostic measure:

$$
FED =
\frac{
N_{evidence\ objects}
}{
N_{validated\ failures}
}
$$

This measures how much structured evidence supports each failure.

It is not inherently “better” to have a larger value.

---

# 125. Failure Family Compression

$$
FFC =
\frac{
N_{validated\ failure\ occurrences}
}{
N_{failure\ families}
}
$$

This indicates how many observed failures are represented by each discovered family on average.

A high value may indicate repeated manifestations of the same mechanism.

---

# 126. Family Novelty Rate

$$
FNR_t =
\frac{
N_{new\ families\ at\ }t
}{
N_{families\ discovered\ by\ }t
}
$$

This decreases naturally as the search space becomes saturated.

---

# 127. Duplicate Discovery Rate

$$
DDR =
\frac{
N_{validated\ failures\ assigned\ to\ existing\ families}
}{
N_{validated\ failures}
}
$$

This is useful for analyzing whether the selector spends excessive budget rediscovering known mechanisms.

---

# 128. Adaptive Improvement in Duplicate Rate

Compare:

$$
DDR_{adaptive}
$$

with:

$$
DDR_{baseline}
$$

A lower duplicate rate may indicate better novelty targeting, but it should always be interpreted alongside total discovery.

---

# 129. Exploration-Diversity Metric

Let \(F_t\) represent discovered families.

A simple diversity metric can be calculated over:

```text
failure categories
mechanisms
attack surfaces
tool paths
scenario classes
```

Example:

$$
CategoryEntropy
=
-\sum_i p_i\log p_i
$$

This is secondary.

Higher entropy is not automatically better because a real evaluator may legitimately discover concentrated weaknesses.

---

# 130. Failure Severity Distribution

Report:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

by:

```text
count
percentage
family count
reproduction rate
```

Severity must not replace discovery metrics.

---

# 131. Reproduced Family Count

$$
RFC =
N_{families\ with\ at\ least\ one\ reproduced\ occurrence}
$$

This is stronger evidence than merely counting observed families.

---

# 132. Metamorphically Supported Family Count

$$
MSFC =
N_{families\ supported\ by\ valid\ metamorphic\ evidence}
$$

This should be reported separately from raw family count.

---

# 133. Generalized Family Count

$$
GFC =
N_{development\ families\ with\ valid\ holdout\ evidence}
$$

This provides an absolute complement to the generalization rate.

---

# 134. Evidence Maturity Distribution

Every validated family can be assigned its highest achieved evidence level:

```text
OBSERVED
VALIDATED
REPRODUCED
METAMORPHICALLY_SUPPORTED
GENERALIZED
```

Report the distribution.

Do not collapse these into a single “genuine defect” flag.

---

# 135. Main Result Table

The main experiment should produce a table like:

| Method   | Budget | Validated Failures | Families | Family AUC | Cost/Family | TTF | Reproduction | Holdout Generalization |
| -------- | -----: | -----------------: | -------: | ---------: | ----------: | --: | -----------: | ---------------------: |
| Random   |    ... |                ... |      ... |        ... |         ... | ... |          ... |                    ... |
| Uniform  |    ... |                ... |      ... |        ... |         ... | ... |          ... |                    ... |
| UCB-V    |    ... |                ... |      ... |        ... |         ... | ... |          ... |                    ... |
| Proposed |    ... |                ... |      ... |        ... |         ... | ... |          ... |                    ... |

Values must come directly from experiment records.

---

# 136. Ablation Metrics

For each ablation:

```text
adaptive selection removed
branching removed
novelty term removed
cost term removed
variance term removed
reproduction removed
metamorphic validation removed
```

measure the same primary metrics.

---

# 137. Ablation Effect

For component \(X\):

$$
AblationEffect_X =
M_{full}
-
M_{withoutX}
$$

Use the appropriate direction for the metric.

Report absolute differences and confidence intervals.

---

# 138. Sensitivity Analysis

Metrics should be tested against:

```text
budget size
number of candidate scenarios
number of seeds
branch depth
clustering threshold
reproduction attempts
metamorphic transformations
```

This determines whether results are robust to configuration choices.

---

# 139. Clustering Sensitivity

Because family counts depend on clustering:

$$
FFC(\theta)
$$

should be evaluated over a predefined range of clustering parameters \(\theta\).

The final primary result must use one frozen configuration.

Sensitivity analysis can show whether conclusions depend heavily on it.

---

# 140. Reproduction Attempt Sensitivity

If each failure receives \(k\) reproduction attempts:

$$
R_f(k)
$$

can be evaluated for:

```text
k = 1
k = 3
k = 5
```

if computationally feasible.

The primary value must be declared in advance.

---

# 141. Bootstrap for Family Metrics

Failure-family counts can be discrete and skewed.

When estimating uncertainty:

* resample experiment runs,
* recompute family metrics per run,
* do not resample individual failure records as if independent.

---

# 142. Run-Level Data Model

Every experiment run should produce a metrics record:

```yaml
run_metrics:
  experiment_id:
  run_id:
  method:
  seed:

  budget:
    allocated:
    actual:

  discovery:
    validated_failures:
    fingerprints:
    families:
    family_auc:

  efficiency:
    cost_per_failure:
    cost_per_family:
    time_to_first_failure:
    time_to_first_family:

  validation:
    validation_rate:
    evidence_completeness:
    inconclusive_rate:
    evaluator_error_rate:

  reproduction:
    reproduction_rate:
    reproduced_families:
    flaky_rate:

  metamorphic:
    consistency_rate:
    violation_rate:

  holdout:
    generalization_rate:
    detection_rate:

  branching:
    branch_yield:
    branch_family_yield:
    snapshot_overhead:

  adaptive:
    cumulative_reward:
    selection_overhead:
```

---

# 143. Metric Provenance

Every metric must be traceable to:

```text
experiment_id
run_id
method
seed
budget
metric_definition_version
source_records
```

---

# 144. Metric Versioning

Metrics must be versioned.

If the definition of:

```text
Cost per Family
Failure Family
Generalization Rate
Reproduction Rate
```

changes, the metric version must change.

Historical results must not be silently recomputed under new semantics without preserving the old values.

---

# 145. Missing Data

Metrics must distinguish:

```text
0
N/A
missing
inconclusive
error
```

These are not interchangeable.

Example:

```text
0 families
```

means the method found no families.

```text
N/A
```

may mean the metric cannot be computed.

```text
missing
```

means data was not recorded.

---

# 146. Zero-Denominator Handling

For:

$$
\frac{a}{b}
$$

when \(b=0\):

* report `N/A`,
* retain the denominator,
* do not silently substitute zero.

Example:

```text
0 validated failures
→ Cost per failure = N/A
```

---

# 147. Aggregation Rules

For each metric:

### Count Metrics

Report:

```text
mean
median
IQR
```

across runs.

### Rate Metrics

Compute per run first, then aggregate across runs.

### Cost Metrics

Report:

```text
median
IQR
mean
```

because they may be highly skewed.

---

# 148. Micro vs Macro Averaging

For categories or families:

### Micro-average

Pool underlying observations.

### Macro-average

Compute metric per category/family and average.

Both may be useful.

The report must clearly state which is used.

---

# 149. Avoiding Data Leakage

Metrics used to adapt the selector must not include:

```text
hidden holdout outcomes
future execution results
future cluster assignments
post-hoc manual labels
```

before the corresponding selection decision.

---

# 150. Online vs Offline Metrics

### Online metrics

Available during adaptive evaluation:

```text
past rewards
past failures
past costs
past family discoveries
past variance
```

### Offline metrics

Computed after the experiment:

```text
holdout generalization
final family clustering
final reproducibility analysis
statistical significance
```

These boundaries must remain explicit.

---

# 151. Primary Metric Freeze

Before running the final hypothesis experiments, freeze:

```text
primary metrics
metric formulas
budget definition
family definition
clustering configuration
reproduction policy
metamorphic policy
holdout rules
statistical tests
```

No primary metric may be changed based on observed results.

---

# 152. Recommended Primary Metric Set

The final project should use the following primary metrics:

### Discovery

$$
DFF(B)
=
\text{validated failure families at budget }B
$$

### Discovery Efficiency

$$
CPFF
=
\frac{C_{total}}{N_{new\ families}}
$$

### Discovery Speed

$$
TTFF
=
\text{cost to first new family}
$$

### Validation

$$
VR
=
\frac{validated\ failures}{failure\ candidates}
$$

### Reproducibility

$$
ORR
=
\frac{reproduced\ attempts}{valid\ reproduction\ attempts}
$$

### Metamorphic

$$
MCR
=
\frac{satisfied\ relations}{valid\ metamorphic\ tests}
$$

### Generalization

$$
HGR
=
\frac{development\ mechanisms\ observed\ on\ holdout}
{eligible\ development\ mechanisms}
$$

### Evaluator Reliability

$$
KFDR
=
\frac{known\ failures\ detected}
{known\ failures}
$$

---

# 153. Secondary Metric Set

Recommended secondary metrics:

```text
Validated Failure Count
Unique Fingerprint Count
Failure-Family AUC
Cost per Validated Failure
Budget Utilization
Budget Overshoot
Inconclusive Rate
Evaluator Error Rate
False Positive Rate
False Negative Rate
Family Reproduction Rate
Flakiness Rate
Metamorphic Violation Rate
Holdout Detection Rate
Branch Yield
Branch Family Yield
Snapshot Overhead
Selection Novelty Yield
Selection Overhead
Scenario Coverage
Invariant Coverage
Attack-Surface Coverage
```

---

# 154. Required Visualizations

The final evaluation should contain at least:

1. Cumulative family discovery vs budget
2. Cumulative validated failures vs budget
3. Cost per family by method
4. Time to first family
5. Failure-family distribution
6. Reproduction-rate distribution
7. Metamorphic consistency by transformation
8. Development vs holdout generalization
9. Branching cost/yield comparison
10. Evaluator error/inconclusive rates
11. Ablation results
12. Run-to-run variability

---

# 155. Main Discovery Plot

Recommended:

```text
X-axis:
Cumulative evaluation budget

Y-axis:
Cumulative validated failure families

Lines:
Random
Uniform
Adaptive
```

Add confidence bands derived from independent experiment runs.

---

# 156. Cost-Efficiency Plot

Recommended:

```text
X-axis:
Total evaluation cost

Y-axis:
Validated failure families discovered
```

This directly addresses the project's budget-constrained research question.

---

# 157. Reproducibility Plot

For each method:

```text
X-axis:
Failure family

Y-axis:
Reproduction rate
```

Alternatively, show the distribution across families.

---

# 158. Holdout Plot

Compare:

```text
Development discovery
vs
Holdout transfer
```

Do not combine them into one number without preserving the underlying values.

---

# 159. Dashboard Data Source

The dashboard must read from:

```text
experiment records
metrics tables
failure records
family records
validation records
```

It must never contain manually hard-coded experimental values.

---

# 160. Metrics Storage

Recommended SQLite tables:

```text
experiment_runs
metric_definitions
run_metrics
invariant_results
failure_records
failure_families
reproduction_results
metamorphic_results
holdout_results
branch_results
```

---

# 161. Metric Record Schema

```sql
CREATE TABLE run_metrics (
    metric_id TEXT NOT NULL,
    metric_version TEXT NOT NULL,
    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    method TEXT NOT NULL,
    seed INTEGER,
    value REAL,
    denominator REAL,
    unit TEXT,
    aggregation TEXT,
    created_at TEXT NOT NULL
);
```

---

# 162. Metric Integrity Constraints

The system must ensure:

```text
metric_id exists
metric_version exists
experiment_id exists
run_id exists
denominator is recorded where applicable
unit is recorded
```

---

# 163. Metric Auditability

A metric must be reproducible from raw records.

For example:

```text
Cost per Family
```

must be recomputable from:

```text
total cost
family count
```

without requiring undocumented manual calculations.

---

# 164. Metric Test Cases

The implementation must include tests for:

```text
zero failures
one failure
multiple families
zero denominator
all inconclusive
all evaluator errors
budget overshoot
duplicate families
reproduced failures
flaky failures
metamorphic violations
holdout generalization
branching cost
```

---

# 165. Example Metric Unit Tests

```python
def test_cost_per_family():
    assert cost_per_family(
        total_cost=100,
        families=5
    ) == 20


def test_zero_family_count():
    assert cost_per_family(
        total_cost=100,
        families=0
    ) is None


def test_reproduction_rate():
    assert reproduction_rate(
        reproduced=8,
        valid_attempts=10
    ) == 0.8
```

---

# 166. Metric Sanity Checks

The system should validate:

```text
0 ≤ rates ≤ 1
counts ≥ 0
costs ≥ 0
budget_actual ≥ 0
budget_overshoot ≥ 0
```

A cumulative discovery curve should not decrease.

If it does, either the implementation or the laws of arithmetic have suffered a preventable incident.

---

# 167. Cumulative Metric Monotonicity

For cumulative discovery:

$$
D(B_{i+1}) \ge D(B_i)
$$

must hold.

If not, the reporting pipeline is invalid.

---

# 168. Family Count Consistency

The following should hold:

$$
FFC
\le
UFF
\le
VFC
$$

when every family contains at least one fingerprint and every fingerprint belongs to a validated failure.

Violations indicate data-integrity problems.

---

# 169. Reproduction Consistency

For:

$$
ORR =
\frac{R}{A}
$$

must satisfy:

$$
0 \le ORR \le 1
$$

and:

$$
R \le A
$$

---

# 170. Metamorphic Consistency

Similarly:

$$
0 \le MCR \le 1
$$

and:

$$
N_{satisfied}
\le
N_{valid}
$$

---

# 171. Generalization Consistency

If:

$$
HGR =
\frac{N_{generalized}}{N_{eligible}}
$$

then:

$$
0 \le HGR \le 1
$$

and:

$$
N_{generalized}
\le
N_{eligible}
$$

---

# 172. Interpretation Rules

The project must avoid statements such as:

> Method X is better because it has the highest score.

Instead report:

> Under the fixed budget and experimental configuration, Method X discovered more validated failure families on average, while its cost per family was lower/higher. Confidence intervals and repeated-run results are reported separately.

This preserves the distinction between measurement and conclusion.

---

# 173. Evidence Hierarchy

Metric interpretation should follow:

```text
Observed execution
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
Hidden-holdout evidence
      ↓
Cross-run replication
```

A metric based on a lower evidence level must not be presented as equivalent to one based on a higher level.

---

# 174. Reporting Template

Each primary result should contain:

```text
Metric:
Definition:
Population:
Budget:
Method:
Mean:
Median:
IQR:
95% CI:
Baseline:
Absolute Difference:
Relative Difference:
Effect Size:
Statistical Test:
Interpretation:
```

---

# 175. Main Research Result Structure

The final research report should organize metrics as:

## A. Discovery

```text
validated failures
unique fingerprints
failure families
family AUC
```

## B. Efficiency

```text
cost per failure
cost per family
time to first family
budget utilization
```

## C. Validation

```text
validation rate
evidence completeness
reproduction rate
```

## D. Robustness

```text
metamorphic consistency
metamorphic violations
```

## E. Generalization

```text
holdout family transfer
holdout detection
generalization gap
```

## F. Evaluator Reliability

```text
known-failure detection
false positive rate
evaluator error
inconclusive rate
determinism
```

## G. Component Contribution

```text
ablation effects
```

---

# 176. Definition of Done

The Evaluation Metrics subsystem is complete when:

* [ ] Every primary research question has at least one defined metric.
* [ ] Every metric has a formal definition.
* [ ] Every rate has an explicit denominator.
* [ ] Every metric has a defined population.
* [ ] Zero-denominator behavior is specified.
* [ ] Discovery and validation metrics are separate.
* [ ] Failure occurrences and failure families are separate.
* [ ] Reproducibility metrics are implemented.
* [ ] Metamorphic metrics are implemented.
* [ ] Holdout generalization metrics are implemented.
* [ ] Branching metrics are implemented.
* [ ] Adaptive-selection metrics are implemented.
* [ ] Evaluator reliability metrics are implemented.
* [ ] Costs include snapshot/restore and verification where applicable.
* [ ] Metrics are computed per independent experiment run.
* [ ] Confidence intervals are supported.
* [ ] Effect sizes are supported.
* [ ] Multiple-comparison handling is defined.
* [ ] Metric definitions are versioned.
* [ ] Metric provenance is stored.
* [ ] Dashboard values come from experiment data.
* [ ] No fabricated experimental values exist.
* [ ] Golden metric test cases exist.
* [ ] Sanity checks are implemented.
* [ ] Primary metrics are frozen before final hypothesis testing.

---

# 177. Final Metric Architecture

The complete evaluation measurement chain is:

$$
\boxed{
Execution
\rightarrow
Invariant Results
\rightarrow
Validated Failures
\rightarrow
Failure Families
\rightarrow
Validation Evidence
\rightarrow
Generalization
\rightarrow
Metrics
}
$$

The principal research comparison is:

$$
\boxed{
Method
\rightarrow
Fixed\ Budget
\rightarrow
Discovery\ Curve
\rightarrow
Validated\ Families
\rightarrow
Cost\ Efficiency
\rightarrow
Reproducibility
\rightarrow
Generalization
}
$$

The project therefore evaluates the proposed framework along five central dimensions:

$$
\boxed{
Discovery
+
Efficiency
+
Validation
+
Generalization
+
Evaluator\ Reliability
}
$$

No single metric is sufficient.

The central outcome is not merely:

> “How many failures did the evaluator find?”

It is:

> **How many distinct, evidence-backed, reproducible and generalizable failure mechanisms can the evaluator discover under a fixed budget, and at what cost, while maintaining reliable evaluation behavior?**

That is the metric structure required to test the actual research contribution rather than merely producing a dashboard full of numbers.
