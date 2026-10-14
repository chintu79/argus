# Reproducibility Package

## Overview

This package documents how to reproduce the entire BCADE-AI research project from a clean environment. It includes environment setup, dependency installation, experiment execution, analysis, visualization, report generation, and integrity verification.

## Environment Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd argus
```

### 2. Install dependencies

Using `uv` (recommended):

```bash
uv sync --extra dev --extra test
```

Or using `pip`:

```bash
pip install -e ".[dev,test]"
```

### 3. Install the project in development mode

```bash
uv pip install -e .
```

### 4. Verify installation

```bash
python -m agent_eval --help
```

## Dependency Installation

### environment.yml

Create the Conda environment:

```bash
conda env create -f environment.yml
conda activate agent-eval
```

### requirements.txt

```bash
pip install -r requirements.txt
```

### lockfile

The `uv.lock` file ensures reproducible dependency versions. Use `uv sync` to restore the exact lockfile state.

## Configuration Validation

```bash
python -m agent_eval config validate --config configs/experiments/smoke.yaml
```

The configuration must pass validation before the experiment can be run.

## Smoke Test

```bash
python -m agent_eval experiment run --config configs/experiments/smoke.yaml --phase 1
```

The smoke test runs a single phase with the mock agent. Full experiment execution runs all 25 phases.

## Full Experiment Execution

```bash
python -m agent_eval experiment run --config configs/experiments/smoke.yaml --phases 1-25
```

Or using a loop:

```bash
for phase in $(seq 1 25); do
    python -m agent_eval experiment run --config configs/experiments/smoke.yaml --phase $phase
done
```

## Analysis

```bash
python -m agent_eval analysis compute --experiment-id smoke_test
python -m agent_eval analysis validate --experiment-id smoke_test
```

## Visualization

```bash
python -m agent_eval visualization generate --experiment-id smoke_test --type all
```

Individual visualization types can be generated selectively:

- discovery_curves
- aufdc
- efficiency_metrics
- reproducibility
- metamorphic
- holdout
- branching
- taxonomy
- effect_sizes
- sensitivity

## Report Generation

```bash
python -m agent_eval research_report generate --experiment-id smoke_test
python -m agent_eval research_report export --experiment-id smoke_test --format pdf
python -m agent_eval research_report export --experiment-id smoke_test --format md
```

## Audit and Validation

```bash
python -m agent_eval audit release --experiment-id smoke_test
python -m agent_eval audit inspect --experiment-id smoke_test
python -m agent_eval final validate --experiment-id smoke_test
```

## Checksums

```bash
sha256sum -c SHA256SUMS
```

## Expected Outputs

After full execution, the following artifacts should exist:

```
artifacts/experiments/smoke_test/
├── run_metrics.csv          # Per-run metrics
├── aggregate_metrics.csv    # Summary statistics
├── hypothesis_results.csv   # Phase 14 hypothesis test results
├── failure_families.csv     # Failure family assignments
├── branching_metrics.csv    # PTR, BTCR, RTR results
├── holdout_metrics.csv      # TSR and hidden-holdout results
├── discovery_curve.png      # FIG-01
├── failure_families.png     # FIG-02
├── aufdc.png                # FIG-03
├── efficiency_metrics.png   # FIG-04
├── reproducibility.png      # FIG-05
├── metamorphic.png          # FIG-06
├── holdout.png              # FIG-07
├── branching.png            # FIG-08
├── taxonomy.png             # FIG-09
├── effect_sizes.png         # FIG-10
├── sensitivity.png          # FIG-11
├── holdout_metrics.png      # FIG-12
├── evidence/                # Persisted evidence artifacts
└── analysis/                # Computed analysis outputs
```

## Commands Script

```bash
bash final_submission/demo/demo_commands.sh
```

This script runs the full demonstration flow on a clean environment.

## Checklist

- [ ] Environment setup (Python 3.11+, dependencies)
- [ ] Configuration validation
- [ ] Smoke test execution
- [ ] Full experiment execution (25 phases)
- [ ] Analysis computation
- [ ] Visualization generation
- [ ] Research report generation
- [ ] Audit and validation
- [ ] Checksum verification
- [ ] Reproducibility verification