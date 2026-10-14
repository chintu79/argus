"""Validation functions for Phase 17 audit module.

Provides utility functions for computing costs, validating experiment integrity,
and supporting audit checks across the evaluation pipeline.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from typing import Any


def compute_total_cost(experiment_dir: str) -> tuple[float, dict[str, float]]:
    """Recalculate total evaluation cost from persisted records.
    
    Traverses the experiment directory structure and sums costs from:
    - Action execution records (actions.jsonl)
    - Budget ledger files (budget_ledger.json)
    - Verification and reproduction records
    
    Args:
        experiment_dir: Path to the experiment directory
        
    Returns:
        Tuple of (total_cost, breakdown_dict) where breakdown_dict contains
        costs per category (execution, snapshot, restore, verification, etc.)
    """
    total: float = 0.0
    breakdown: dict[str, float] = defaultdict(float)
    
    # Try to load action records from all runs
    runs_dir = os.path.join(experiment_dir, "artifacts", "runs")
    if not os.path.isdir(runs_dir):
        return 0.0, dict(breakdown)
    
    for run_name in os.listdir(runs_dir):
        run_path = os.path.join(runs_dir, run_name)
        if not os.path.isdir(run_path):
            continue
        
        # Load action records
        actions_path = os.path.join(run_path, "actions.jsonl")
        if os.path.exists(actions_path):
            try:
                with open(actions_path) as f:
                    for line in f:
                        try:
                            action = json.loads(line.strip())
                            # Extract cost from action metadata
                            cost = action.get("metadata", {}).get("cost", 0)
                            if cost is None:
                                cost = action.get("cost", 0)
                            if cost is None:
                                cost = 1  # default default
                            total += cost
                            breakdown["execution"] += cost
                        except (json.JSONDecodeError, KeyError):
                            continue
            except OSError:
                pass
        
        # Load budget ledger if available
        budget_path = os.path.join(run_path, "budget_ledger.json")
        if os.path.exists(budget_path):
            try:
                with open(budget_path) as f:
                    ledger = json.load(f)
                for category, cost in ledger.items():
                    if isinstance(cost, (int, float)):
                        total += cost
                        breakdown[category] += cost
            except (OSError, json.JSONDecodeError):
                pass
    
    return total, dict(breakdown)


def compute_budget_discrepancy(
    experiment_dir: str,
    configured_budget: int | None = None,
) -> dict[str, Any]:
    """Compute budget discrepancy between recalculated and configured budgets.
    
    Args:
        experiment_dir: Path to the experiment directory
        configured_budget: Override for the configured budget (loaded from config if not provided)
        
    Returns:
        Dict with total_cost, configured_budget, discrepancy, and pass status
    """
    total_cost, breakdown = compute_total_cost(experiment_dir)
    
    if configured_budget is None:
        # Try to load from config
        config_path = os.path.join(experiment_dir, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                configured_budget = config.get("budget", {}).get("total_tokens", 0)
            except (OSError, json.JSONDecodeError):
                configured_budget = 0
        else:
            configured_budget = 0

    if configured_budget is None:
        configured_budget = 0

    discrepancy = total_cost - configured_budget

    pass_check = discrepancy <= 0 or (configured_budget > 0 and abs(discrepancy) / configured_budget < 0.05)
    
    return {
        "total_cost": total_cost,
        "configured_budget": configured_budget,
        "discrepancy": discrepancy,
        "pass": pass_check,
        "breakdown": breakdown,
    }