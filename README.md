# Budget-Constrained Adaptive Security Evaluation of AI Agents

**Research prototype** investigating whether adaptive test selection combined with trajectory-aware state-based branching enables more efficient discovery and validation of AI-agent security and reliability failures under a fixed evaluation budget.

---

## Prerequisites

- **Operating System**: Linux, macOS, or WSL2 (Windows Subsystem for Linux)
- **Python**: `>= 3.11` (Python 3.12 or 3.14 recommended)
- **Package & Environment Manager**: [`uv`](https://docs.astral.sh/uv/) (strongly recommended) or standard `pip` + `venv`

To install `uv` if not already installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Quick Start (Run in 2 Minutes)

```bash
# 1. Install dependencies and virtual environment
uv sync

# 2. Initialize the SQLite evaluation database
uv run agent-eval db init

# 3. Validate experiment configuration
uv run agent-eval validate --config configs/experiments/smoke.yaml

# 4. Execute the smoke experiment
uv run agent-eval experiment run --config configs/experiments/smoke.yaml

# 5. Recompute derived metrics
uv run agent-eval metrics recompute --experiment-id smoke_test

# 6. Generate the research markdown report
uv run agent-eval report generate --experiment-id smoke_test

# 7. Run test suite & quality checks
uv run pytest
uv run ruff check .
uv run mypy src/
```

---

## Running the Project From Scratch (Step-by-Step)

### Step 1: Clone and Navigate to Repository

```bash
git clone <repository-url>
cd argus
```

### Step 2: Environment Setup & Dependency Installation

#### Using `uv` (Recommended)
`uv` automatically handles Python version selection, isolated virtual environments, and reproducible locked dependencies from `uv.lock`:

```bash
# Sync dependencies in virtual environment (.venv)
uv sync

# Optional: activate the virtual environment in your current shell
source .venv/bin/activate
```

#### Using standard `venv` and `pip`
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Step 3: Database Initialization

The evaluation framework stores agents, environments, scenarios, candidates, trajectories, invariants, and validated failures in an SQLite database (default: `./data/instance/database.sqlite`).

```bash
# Initialize the database and create all 14 schema tables
uv run agent-eval db init

# Verify database status and inspect table creation
uv run agent-eval db status
```

To reset the database cleanly at any point:
```bash
uv run agent-eval db reset --yes
```

### Step 4: Validate Experiment Configuration

Before executing an evaluation run, validate the experiment YAML specification:

```bash
# Validate smoke test configuration
uv run agent-eval validate --config configs/experiments/smoke.yaml

# Dry run: view the execution plan without executing tests
uv run agent-eval experiment run --config configs/experiments/smoke.yaml --dry-run
```

### Step 5: Execute Evaluation Experiments

#### Option A: Quick Smoke Test
Executes a lightweight verification run across all 4 evaluation methods (`STATIC`, `RANDOM`, `UNBRANCHED_ADAPTIVE`, `STATE_BRANCHED_ADAPTIVE`):

```bash
uv run agent-eval experiment run --config configs/experiments/smoke.yaml
```

Check the status of the experiment:
```bash
uv run agent-eval experiment status --experiment-id smoke_test
```

#### Option B: Full Experiment
To run the full evaluation experiment:

```bash
uv run agent-eval experiment run --config configs/experiments/main_experiment.yaml
```

All raw evidence, execution logs, trajectory traces, snapshots, and actions are persisted in:
```
artifacts/experiments/<experiment_id>/
├── manifest.json
└── runs/
    ├── <run_id_1>/
    │   ├── actions.jsonl
    │   ├── budget_ledger.json
    │   ├── metadata.json
    │   └── snapshots/
    └── ...
```

### Step 6: Metric Recomputation & Analysis

Recompute evaluation metrics (Failure Discovery Efficiency `FDE`, Cost Per Failure `CPF`, Time To First Failure `TTFF`, and Reproducibility Rate `Rep_k`) from immutable raw execution records:

```bash
uv run agent-eval metrics recompute --experiment-id smoke_test
```

### Step 7: Research Report Generation

Synthesize execution evidence, metrics, and findings into a structured research report:

```bash
uv run agent-eval report generate --experiment-id smoke_test
```

The generated report will be saved to:
`artifacts/experiments/smoke_test/report/research_report.md`

### Step 8: Research Integrity & Audit Suite (Phase 17)

Run comprehensive verification across ground-truth evaluator cases, budget reconciliation, state isolation, selector leakage, and reproducibility:

```bash
uv run agent-eval audit inspect --experiment smoke_test
```
*(Or invoke via the standalone `audit` script: `uv run audit inspect -e smoke_test`)*

---

## CLI Reference

The unified CLI `agent-eval` (or `python -m agent_eval.cli`) provides the following command tree:

```
agent-eval
├── db
│   ├── init      [--url <url>] [--drop] [--echo]
│   ├── status    [--url <url>]
│   └── reset     [--url <url>] [--yes]
├── validate      --config <path>
├── experiment
│   ├── run       --config <path> [--dry-run]
│   ├── smoke     --config <path>
│   ├── status    --experiment-id <id>
│   ├── validate  --config <path>
│   ├── inspect   --experiment-dir <dir>
│   ├── resume    --experiment-dir <dir>
│   └── export    --experiment-dir <dir> --output <dir>
├── metrics
│   └── recompute --experiment-id <id> [--output-dir <dir>]
├── report
│   └── generate  --experiment-id <id> [--output-dir <dir>]
└── audit
    └── inspect   --experiment <id>
```

---

## Quality Assurance & Testing

Run the automated test suite and static analysis gates:

```bash
# Run unit and integration tests (pytest)
uv run pytest

# Run linting and code style checks (ruff)
uv run ruff check .

# Run static type checking (mypy)
uv run mypy src/
```

---

## Research Integrity & Philosophy

This is a **scientific instrument**, not a dashboard. Every research claim must be traceable through the full chain:

```
Configuration  →  Experiment  →  Execution  →  Raw Evidence  →  Evaluation  →  Validated Result  →  Metric  →  Statistical Analysis
```

- Raw evidence (`actions.jsonl`, `budget_ledger.json`) is immutable; derived metrics are recomputable.
- Hidden-holdout outcomes must never influence adaptive discovery-time selection.
- All evaluation budgets, seeds, and invariant evaluations are strictly recorded and audited.