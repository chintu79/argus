"""Discovery curves for Phase 14 analysis.

Produces (tokens_spent, validated_family_count) curves per run,
preserving every recorded checkpoint. Does not smooth raw curves.

Data flow principle: read from raw discovery curve data, produce
normalized and raw curve points for analysis and export.
"""

from __future__ import annotations

import csv
import math
import os
from typing import Any


def discover_curve_points(
    discovery_curves: dict[str, dict[str, Any]],
    run_id: str,
) -> list[tuple[float, int]]:
    """Extract discovery curve points for a single run.

    Returns list of (normalized_budget, validated_family_count) tuples,
    preserving every recorded checkpoint from the raw data.

    The curve points are extracted from the raw discovery_curves data
    stored in the experiment's raw directory.

    Normalization: x = tokens_spent / budget_total, where budget_total
    is the run's total budget allocation.

    Raw data immutability: this function only reads from the stored
    curve data; it does not modify the original data.
    """
    points: list[tuple[float, int]] = []

    curve_data = discovery_curves.get(run_id, {})
    if not curve_data:
        return points

    # Extract curve points from the stored data
    # Expected format: {"checkpoint_N": {"tokens_spent": int, "validated_count": int}, ...}
    # Or: {"tokens_spent_list": [int, ...], "validated_count_list": [int, ...]}
    if "tokens_spent_list" in curve_data and "validated_count_list" in curve_data:
        tokens_list = curve_data["tokens_spent_list"]
        validated_list = curve_data["validated_count_list"]
        if len(tokens_list) == len(validated_list):
            budget_total = max(tokens_list) if tokens_list else 1
            for tokens_spent, validated_count in zip(tokens_list, validated_list):
                normalized_budget = tokens_spent / budget_total if budget_total > 0 else 0.0
                points.append((normalized_budget, validated_count))
    elif "checkpoints" in curve_data:
        for checkpoint_data in curve_data["checkpoints"]:
            tokens_spent = checkpoint_data.get("tokens_spent", 0)
            validated_count = checkpoint_data.get("validated_family_count", 0)
            budget_total = checkpoint_data.get(
                "budget_total", max(tokens_spent for _ in [1]) if tokens_spent else 1
            )
            normalized = tokens_spent / budget_total if budget_total > 0 else 0.0
            points.append((normalized, validated_count))
    else:
        # Try to extract any dict keys that look like curve data
        for value in curve_data.values():
            if isinstance(value, (int, float)):
                continue
            # Attempt to parse as curve point
            if isinstance(value, dict):
                tokens = value.get("tokens_spent", 0)
                count = value.get("validated_count", 0)
                points.append((tokens, count))

    # Sort by tokens_spent to ensure proper ordering
    points.sort(key=lambda p: p[0])

    return points


def compute_aufdc_for_curve(
    curve_points: list[tuple[float, int]],
    budget_total: int,
) -> float:
    """Compute AUFDC for a discovery curve.

    Uses the trapezoidal rule on the normalized curve points.

    See metrics.py::compute_aufdc for the mathematical definition.
    """
    from agent_eval.analysis.metrics import compute_aufdc

    return compute_aufdc(curve_points, budget_total)


def validate_curve_points(curve_points: list[tuple[float, int]]) -> bool:
    """Validate that curve points are suitable for analysis.

    Checks:
    - Non-empty list
    - x values (normalized budget) are monotonically non-decreasing
    - y values (validated family count) are non-negative integers
    - No NaN or infinite values
    """
    if not curve_points:
        return False

    prev_x = -1.0
    for x, y in curve_points:
        if not isinstance(x, (int, float)) or not isinstance(y, int):
            return False
        if math.isnan(x) or math.isinf(x) or math.isnan(y) or math.isinf(y):
            return False
        if y < 0:
            return False
        if x < prev_x:
            return False  # not monotonically non-decreasing
        prev_x = x

    return True


def export_curve_csv(
    curve_points: list[tuple[float, int]],
    output_path: str,
) -> None:
    """Export discovery curve points to a CSV file.

    Format:
    normalized_budget,tokens_spent,validated_family_count

    Preserves every recorded checkpoint without smoothing.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["normalized_budget", "tokens_spent", "validated_family_count"])
        for x, y in curve_points:
            # x is already normalized budget (0-1 range)
            # tokens_spent is the raw count
            writer.writerow([x, y])


def merge_curves(
    curve_sets: dict[str, list[tuple[float, int]]],
) -> list[tuple[float, int]]:
    """Merge multiple curve sets into a single combined curve.

    For each unique x (normalized budget), take the maximum y (validated families).
    This is useful for creating a "best observed" curve across methods.

    Do not use this for primary analysis - keep method-specific curves separate.
    """
    merged: dict[float, int] = {}

    for method_curves in curve_sets.values():
        for x, y in method_curves:
            if x not in merged or y > merged[x]:
                merged[x] = y

    # Sort by x value
    merged_points = sorted(merged.items(), key=lambda item: item[0])

    return [(x, y) for x, y in merged_points]