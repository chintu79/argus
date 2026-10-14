# Demonstration Package

## Overview

This demonstration shows the BCADE-AI pipeline for budget-constrained adaptive security evaluation of AI agents. The demo is designed to run on a clean environment with minimal configuration.

## Prerequisites

- Python 3.11+
- Project dependencies installed (`uv pip install -e .` or `pip install -e .`)
- Access to the project source code

## Demonstration Flow

The demonstration follows these steps:

1. **Initialize project** - Set up the project environment and validate configuration
2. **Create controlled environment** - Initialize the mock agent and evaluation environment
3. **Run mock agent** - Execute a baseline evaluation run
4. **Execute adaptive selection** - Run the adaptive candidate selector
5. **Create state snapshot** - Snapshot the execution state for branching
6. **Create branch** - Create an isolated branch from the snapshot
7. **Inject controlled perturbation** - Apply a controlled perturbation to the branched state
8. **Evaluate invariant** - Check invariants during branched execution
9. **Detect failure** - Identify and classify a failure candidate
10. **Reproduce failure** - Independently replay the failure to validate
11. **Generate failure signature** - Create a signature for the validated failure
12. **Assign failure family** - Classify the failure into a failure family
13. **Generate metrics** - Compute evaluation metrics (FDE, CPF, TTFF, etc.)
14. **Generate visualization** - Create a discovery curve or metric visualization
15. **Generate evidence artifact** - Persist the evidence for the run

## Demo Commands

```bash
# Step 1: Initialize project
cd /path/to/project
python -m agent_eval experiment init --config configs/experiments/smoke.yaml

# Step 2: Validate configuration
python -m agent_eval config validate --config configs/experiments/smoke.yaml

# Step 3: Create controlled environment
python -m agent_eval environment create --config configs/experiments/smoke.yaml

# Step 4: Run mock agent baseline
python -m agent_eval experiment run --config configs/experiments/smoke.yaml --phase 1

# Step 5: Execute adaptive selection
python -m agent_eval selector run --config configs/experiments/smoke.yaml --budget 50000

# Step 6: Create state snapshot
python -m agent_eval snapshot create --run-id <run_id> --snapshot-id snap_001

# Step 7: Create branch
python -m agent_eval branch create --snapshot-id snap_001 --branch-id branch_001

# Step 8: Inject controlled perturbation
python -m agent_eval perturbation inject --branch-id branch_001 --perturbation "prompt_injection_attempt"

# Step 9: Evaluate invariant
python -m agent_eval invariant evaluate --branch-id branch_001

# Step 10: Detect failure
python -m agent_eval failure detect --branch-id branch_001 --candidate

# Step 11: Reproduce failure
python -m agent_eval failure reproduce --candidate-id <candidate_id> --seed 42

# Step 12: Generate failure signature
python -m agent_eval failure signature --validated-id <validated_id>

# Step 13: Assign failure family
python -m agent_eval failure family --validated-id <validated_id>

# Step 14: Generate metrics
python -m agent_eval metrics compute --experiment-id smoke_test

# Step 15: Generate visualization
python -m agent_eval visualization generate --experiment-id smoke_test --type discovery_curve

# Step 16: Generate evidence artifact
python -m agent_eval evidence package --experiment-id smoke_test
```

## Expected Output

The demonstration should produce:

- A validated failure with family assignment
- Metrics including FDE, CPF, and TTFF
- A discovery curve visualization
- Persistence of all evidence artifacts in the experiment directory
- Budget accounting showing total cost within configured budget

## Safety

The demonstration uses:
- Deterministic mock components
- Simulated services
- Non-sensitive data
- Bounded budgets (default: 50,000 tokens)
- Isolated filesystem paths
- Fixed seeds for reproducibility