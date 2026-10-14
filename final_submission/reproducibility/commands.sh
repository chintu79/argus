#!/usr/bin/env bash
# Reproducibility commands for BCADE-AI

set -euo pipefail

PROJECT_DIR="/home/krishna/Desktop/argus"

echo "=== BCADE-AI Reproducibility Commands ==="
echo ""

# Environment setup
echo "1. Install dependencies..."
cd "$PROJECT_DIR"
uv sync --extra dev --extra test

# Configuration validation
echo "2. Validate configuration..."
python -m agent_eval config validate --config configs/experiments/smoke.yaml

# Smoke test
echo "3. Run smoke test (Phase 1)..."
python -m agent_eval experiment run --config configs/experiments/smoke.yaml --phase 1

# Full experiment
echo "4. Run full experiment (phases 1-25)..."
for phase in $(seq 1 25); do
    python -m agent_eval experiment run --config configs/experiments/smoke.yaml --phase $phase
done

# Analysis
echo "5. Compute analysis..."
python -m agent_eval analysis compute --experiment-id smoke_test

# Visualization
echo "6. Generate visualizations..."
python -m agent_eval visualization generate --experiment-id smoke_test --type all

# Report generation
echo "7. Generate research report..."
python -m agent_eval research_report generate --experiment-id smoke_test

# Audit and validation
echo "8. Run release audit..."
python -m agent_eval audit release --experiment-id smoke_test

# Final validation
echo "9. Run final validation..."
python -m agent_eval final validate --experiment-id smoke_test

echo ""
echo "=== Reproducibility Complete ==="