# Algorithm Defense

## Adaptive Selection

### Candidate Pool

The candidate pool consists of all evaluation scenarios that can be tested in the current experiment. Each candidate is defined by:
- A prompt (or prompt variant)
- A tool configuration
- An initial agent state
- A budget cost estimate

### Exploration vs. Exploitation

The adaptive selector balances exploration and exploitation using an epsilon-greedy strategy:

- **Exploration** (probability ε): Randomly select from the candidate pool to discover novel failure modes that the estimated model has not considered.
- **Exploitation** (probability 1 - ε): Select the candidate with the highest expected value, considering:
  - Failure probability (estimated from previous validated failures)
  - Coverage (how much of the remaining space this candidate explores)
  - Novelty (how different this candidate is from already-tested scenarios)
  - Cost (budget tokens consumed per candidate)

### Deterministic Selection

Given the same state and seed, the selector produces the same candidate ranking. This ensures reproducibility of the selection process.

### Cost Accounting

Each candidate has an associated budget cost estimate. The selector includes cost in the expected value calculation, preferring candidates that are expected to yield validated failures per budget token rather than just maximizing raw discovery rate.

## State-Based Branching

### State Snapshot

A state snapshot captures the agent's execution state at a specific point in the trajectory. The snapshot includes:
- Agent internal memory
- Tool session state
- Environment configuration
- Budget consumed up to the snapshot point

### Restore

Restoring a snapshot returns the agent and environment to the snapshotted state. This allows a new execution branch to be created from the same starting point.

### Branch

A branch is an isolated execution environment created from a state snapshot. Key properties:
- Shares the parent's state up to the snapshot point
- Diverges from the parent after the snapshot point
- Has its own budget account, separate from the parent
- Snapshot and restore operations consume budget tokens (explicitly accounted for)

### Lineage

Branches maintain a lineage to their parent snapshot, allowing the experiment to trace which branch originated from which snapshot. This is essential for cost accounting and for the integrity audit.

### Cost Accounting

- **Snapshot cost**: Budget tokens consumed to create the snapshot
- **Restore cost**: Budget tokens consumed to restore from the snapshot
- **Prefix savings**: Budget tokens saved by reusing the snapped prefix instead of rebuilding from scratch
- **Net savings**: prefix_savings - snapshot_cost - restore_cost

The experiment tracks all cost components and includes them in the total budget accounting.

## Failure Validation

### Candidate Failure → Independent Replay → Reproduced Failure → Failure Family

The failure validation pipeline has four stages:

1. **Candidate Failure**: An invariant violation observed during trajectory execution. The candidate failure is recorded with the observed violation, the invariant, and the execution state.

2. **Independent Replay**: The candidate failure is independently replayed from the same (or a different) initial state. The replay uses the same prompt and tool configuration but with a different seed to test reproducibility.

3. **Reproduced Failure**: If the independent replay produces the same invariant violation, the failure is "reproduced." Reproduction confirms the failure is consistent and not a stochastic artifact.

4. **Failure Family**: Reproduced failures are grouped into families based on shared mechanism characteristics. Family assignment considers:
   - Shared invariant violations
   - Similar tool usage patterns
   - Comparable state transition characteristics
   - Causal mechanism similarity (when deducible)

The pipeline ensures that only failures with strong evidence of consistency are counted as validated failures.

## Reproducibility

### Rep_k

Rep_k measures the proportion of failures that are reproducibly observed across k different seeds:

```
Rep_k = (number of failures reproduced across k seeds) / (total number of validated failures)
```

A high Rep_k indicates that the discovered failures are robust and not dependent on a specific initial state.

### FRR

Failure Reproduction Rate (FRR) summarizes the overall rate at which observed failures can be reproduced:

```
FRR = (total reproduction attempts yielding the same violation) / (total reproduction attempts)
```

Rep_k and FRR are computed across all validated failures and all replay attempts with varying seeds.

## Hidden Holdout

### Why Hidden Holdout is Necessary

During adaptive selection, the selector observes which candidates yield validated failures. If the same discovery-time feedback influences which candidates are tested in the holdout phase, the holdout evaluation is compromised. Hidden holdout ensures that the holdout test conditions are selected before the adaptive selection process begins, so no discovery-time information can influence them.

### Leakage Prevention

- Holdout test conditions (prompts, tools, initial states) are generated and fixed before the experiment starts
- The adaptive selector cannot influence which holdout conditions are tested
- TSR (Transfer Success Rate) measures whether the adaptive selection process affects holdout performance

### TSR (Transfer Success Rate)

```
TSR = (number of holdout evaluations yielding a validated failure) / (total holdout evaluations)
```

TSR near the expected random rate demonstrates that adaptive selection does not leak discovery-time information to held-out test conditions.

## Metamorphic Testing

### Base / Transformation / Relation Evaluation

Metamorphic testing evaluates whether agent output remains consistent under well-defined transformations:

1. **Base Evaluation**: Run the agent with the base prompt/input and record the output.

2. **Transformation**: Apply a valid transformation to the base prompt/input. Valid transformations are well-defined and meaningful (e.g., paraphrasing, removing redundant terms, adding equivalent constraints).

3. **Relation Evaluation**: Run the agent with the transformed prompt/input and compare the output to the base evaluation.

4. **Metamorphic Relation Holds**: If the output satisfies the expected relation (e.g., equality, entailment, paraphrase), the metamorphic relation is supported.

### MCR (Metamorphic Compatibility Rate)

```
MCR = (number of valid transformations where the relation holds) / (total number of valid transformations)
```

### MVR (Metamorphic Validity Rate)

```
MVR = (number of well-defined, meaningful transformations) / (total transformations attempted)
```

MVR ensures that only valid transformations are used in the evaluation, filtering out ill-defined or meaningless transformations.