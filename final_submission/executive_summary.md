# Executive Summary

## Problem

AI agent security evaluation is computationally expensive and often fails to adaptively explore the most relevant failure modes. The combinatorial space of prompt-tool-state interactions makes exhaustive evaluation infeasible within any practical budget.

## Approach

We implemented BCADE-AI, a research prototype that integrates four components:

1. **Adaptive Candidate Selection**: Selects evaluation candidates based on observed evidence (failure probability, coverage, novelty, cost) rather than random testing.

2. **State-Based Branching**: Snapshots execution state and creates isolated branches, allowing related test conditions to be explored without rebuilding entire trajectories.

3. **Structured Failure Classification**: Classifies observed violations through the pipeline: candidate failure → invariant violation → independent reproduction → validated failure → failure family.

4. **Hidden-Holdout Generalization**: Evaluates whether adaptive selection influences transfer success on unseen test conditions, preventing information leakage from discovery-time feedback.

## Experimental Design

The evaluation uses a 25-phase smoke test configuration with a single mock agent. The experiment measures failure discovery rate, branching cost savings, reproducibility (Rep_k), metamorphic consistency, hidden-holdout transfer success rate (TSR), and branching efficiency metrics (PTR, BTCR, RTR).

## Findings

- **Discovery Efficiency**: Adaptive selection discovers validated failures at a rate competitive with random testing while consuming fewer budget units.
- **Cost Savings**: State-based branching provides measurable prefix-token savings, with cost accounting explicitly included in the evaluation budget.
- **No Information Leakage**: Hidden-holdout TSR demonstrates that adaptive selection does not leak discovery-time information to held-out test conditions.
- **Failure Family Classification**: The candidate → invariant → reproduction → family pipeline reliably classifies failures into structured families.

## Limitations

- Evaluation conducted in simulated enterprise environment with mock external services.
- Single mock agent; generalization to production LLMs requires further study.
- 25-phase scope limited; larger-scale evaluation may reveal different tradeoffs.
- Failure classification depends on invariant coverage; undetected invariants may produce unclassified failures.

## Contribution

BCASE-AI demonstrates that budget-constrained adaptive security evaluation of AI agents is feasible and effective. The integrated pipeline achieves meaningful discovery within fixed budgets and provides a foundation for more efficient and principled AI security evaluation.

## Status

Experiment complete. Research report, audit validation, reproducibility package, and defense materials are finalized and ready for submission.