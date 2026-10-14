#!/usr/bin/env bash
# Demo execution script for BCADE-AI

set -euo pipefail

PROJECT_DIR="/home/krishna/Desktop/argus"
DEMO_CONFIG="final_submission/demo/demo_config.yaml"

echo "=== BCADE-AI Demonstration ==="
echo ""

# Step 1: Initialize
echo "Step 1: Initialize project..."
cd "$PROJECT_DIR"
python -m agent_eval experiment init --config configs/experiments/smoke.yaml

# Step 2: Validate configuration
echo "Step 2: Validate configuration..."
python -m agent_eval config validate --config "$DEMO_CONFIG"

# Step 3: Create controlled environment
echo "Step 3: Create controlled environment..."
python -m agent_eval environment create --config "$DEMO_CONFIG"

# Step 4: Run mock agent baseline
echo "Step 4: Run mock agent baseline..."
python -m agent_eval experiment run --config "$DEMO_CONFIG" --phase 1

# Step 5: Execute adaptive selection
echo "Step 5: Execute adaptive selection..."
python -m agent_eval selector run --config "$DEMO_CONFIG" --budget 50000

# Step 6: Create state snapshot
echo "Step 6: Create state snapshot..."
python -m agent_eval snapshot create --run-id smoke_test --snapshot-id snap_001

# Step 7: Create branch
echo "Step 7: Create branch..."
python -m agent_eval branch create --snapshot-id snap_001 --branch-id branch_001

# Step 8: Inject controlled perturbation
echo "Step 8: Inject controlled perturbation..."
python -m agent_eval perturbation inject --branch-id branch_001 --perturbation "prompt_injection_attempt"

# Step 9: Evaluate invariant
echo "Step 9: Evaluate invariant..."
python -m agent_eval invariant evaluate --branch-id branch_001

# Step 10: Detect failure
echo "Step 10: Detect failure..."
python -m agent_eval failure detect --branch-id branch_001 --candidate

# Step 11: Reproduce failure
echo "Step 11: Reproduce failure..."
python -m agent_eval failure reproduce --candidate-id candidate_001 --seed 42

# Step 12: Generate failure signature
echo "Step 12: Generate failure signature..."
python -m agent_eval failure signature --validated-id validated_001

# Step 13: Assign failure family
echo "Step 13: Assign failure family..."
python -m agent_eval failure family --validated-id validated_001

# Step 14: Generate metrics
echo "Step 14: Generate metrics..."
python -m agent_eval metrics compute --experiment-id smoke_test

# Step 15: Generate visualization
echo "Step 15: Generate visualization..."
python -m agent_eval visualization generate --experiment-id smoke_test --type discovery_curve

# Step 16: Generate evidence artifact
echo "Step 16: Generate evidence artifact..."
python -m agent_eval evidence package --experiment-id smoke_test

echo ""
echo "=== Demonstration Complete ==="