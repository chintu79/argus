# Results Summary

## Failure Discovery

### VFF (Validated Failure Families)
- The candidate → invariant → independent replay → family pipeline reliably classifies failures.
- Phase 17 ground truth tests confirm classification consistency.
- Failure families are assigned based on shared mechanism characteristics.

### Discovery Curves
- FIG-01 through FIG-12 document the progression of failure discovery across adaptive selection runs.
- Curves show cumulative validated failures against budget units consumed.
- Adaptive selection demonstrates comparable or superior slope to random discovery per budget unit.

### AUFDC (Adaptive Uniform Failure Discovery Curve)
- FIG-03 visualizes the AUFDC, showing discovery rate normalized against budget consumption.
- The curve captures the diminishing returns as the evaluation space is exhausted.

### Failure Discovery Efficiency
- **FDE** (Failure Discovery Efficiency): Validated failures per 1000 budget tokens.
- **CPF** (Cost per Failure): Budget tokens consumed per validated failure.
- **TTFF** (Time to First Failure): Budget units consumed before the first validated failure is discovered.

## Reproducibility

### Rep_k
- Reproducibility rate across k seeds measures whether failures are consistently reproduced.
- Reported Rep_k values indicate that a significant majority of failures are reproducible across multiple initial states.

### FRR (Failure Reproduction Rate)
- FRR summarizes the overall rate at which observed failures can be reproduced.
- FRR is computed across all validated failures and all replay attempts.

## Metamorphic Testing

### MCR (Metamorphic Compatibility Rate)
- Measures the proportion of transformations under which agent output remains stable.
- FIG-06 visualizes MCR across different transformation families.

### MVR (Metamorphic Validity Rate)
- Assesses the proportion of transformations that are valid (well-defined and meaningful).
- Ensures that only semantically valid transformations are used in consistency evaluation.

## Hidden Holdout

### TSR (Transfer Success Rate)
- FIG-07 visualizes TSR across adaptive selection strategies.
- TSR measures whether the adaptive selection process influences performance on unseen test conditions.
- Results demonstrate that adaptive selection does not leak discovery-time information to held-out test conditions.

## Branching

### PTR (Prefix-Token Reduction)
- FIG-08-A shows the prefix-token reduction achieved through state-based branching.
- PTR = (fresh_token_count - branched_token_count) / fresh_token_count

### BTCR (Branching Cost-to-Savings Ratio)
- FIG-08-B quantifies the cost of snapshot/restore operations against the savings from branching.
- BTCR = branching_cost / prefix_token_savings

### RTR (Reproducibility Through Replay)
- FIG-08-C measures whether branched execution achieves comparable reproducibility to fresh execution.
- RTR = branched_reproducibility_rate / fresh_reproducibility_rate

### Branching Cost
- Snapshot and restore operations consume budget tokens.
- Cost accounting is explicitly included in the evaluation budget.
- Net savings = prefix_token_savings - snapshot_restore_cost

## Diversity

### Unique Invariants
- Number of distinct invariants detected across all evaluation runs.

### Tools and Mutation Types
- Diversity of tools and mutation types that trigger invariant violations.

### State Transition Taxonomy
- Classification of state transitions that lead to failure discovery.

## Statistical Analysis

### Effect Sizes
- Hedge's g and Cohen's d reported for all pairwise comparisons.

### Confidence Intervals
- 95% confidence intervals for all metric estimates.

### Multiple Comparison Correction
- Benjamini-Hochberg adjusted p-values reported.

### Sensitivity Analysis
- Results robust to seed variation and parameter perturbations.
- FIG-11 visualizes sensitivity across perturbation dimensions.