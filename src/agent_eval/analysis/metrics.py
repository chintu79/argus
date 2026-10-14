"""Run-level metrics for Phase 14 analysis.

Computes primary and derived metrics for each experimental run:
- VFF (Validated Failure Families)
- FDE (Family Discovery Efficiency)
- CPF (Cost Per Family)
- TTFF (Time to First Family)
- AUFDC (Area Under Failure Discovery Curve)

Raw data must remain immutable - these are computed from existing data.
"""

from __future__ import annotations

from typing import Any


def compute_vff(run_data: dict[str, Any]) -> int:
    """Compute Validated Failure Families (VFF) for a run.

    VFF_r = number of unique validated failure families for run r.

    This is one of the primary dependent variables.
    """
    validated_families = run_data.get("validated_family_count", 0)
    try:
        return int(validated_families)
    except (TypeError, ValueError):
        return 0


def compute_fde(vff: int, tokens_used: int) -> float:
    """Compute Family Discovery Efficiency (FDE) for a run.

    FDE_r = VFF_r / tokens_used_r

    Returns the unnormalized raw ratio.
    """
    if tokens_used <= 0:
        return 0.0
    return vff / tokens_used


def compute_cpf(vff: int, tokens_used: int) -> float | None:
    """Compute Cost Per family (CPF) for a run.

    CPF_r = tokens_used_r / VFF_r

    If VFF_r == 0, return NULL (not infinity and not zero).
    """
    if vff == 0:
        return None
    if tokens_used <= 0:
        return None
    return tokens_used / vff


def compute_ttff(
    run_data: dict[str, Any], tokens_before_first_family: int | None = None
) -> float | None:
    """Compute Time to First Family (TTFF) for a run.

    TTFF_r = tokens spent before first validated family.

    If no family is discovered, TTFF_r = NULL.
    Do not replace it with the full budget unless the metric definition
    explicitly says so.
    """
    if tokens_before_first_family is not None:
        try:
            return float(tokens_before_first_family)
        except (TypeError, ValueError):
            return None
    # Check if any family was discovered
    vff = compute_vff(run_data)
    if vff == 0:
        return None
    # If VFF > 0 but tokens_before_first_family not provided,
    # we cannot compute TTFF precisely
    return None


def compute_aufdc(
    curve_points: list[tuple[float, int]],
    budget_total: int,
) -> float:
    """Compute Area Under Failure Discovery Curve (AUFDC).

    Uses the trapezoidal rule.

    For points (x_0, y_0), ..., (x_n, y_n):

    AUFDC = sum [(x_{i+1} - x_i) * (y_i + y_{i+1}) / 2]

    where x = normalized budget consumption = tokens_spent / budget_total.

    The final curve should cover the actual observed range.
    Do not extrapolate beyond the last observed point.

    Args:
        curve_points: List of (normalized_budget, validated_family_count) tuples,
            preserving every recorded checkpoint.
        budget_total: Total budget for normalization.

    Returns:
        AUFDC value computed via trapezoidal rule.
    """
    if not curve_points:
        return 0.0

    # Sort by normalized budget
    sorted_points = sorted(curve_points, key=lambda p: p[0])

    # Ensure we start from (0, 0) if not already
    if sorted_points[0][0] > 0:
        sorted_points.insert(0, (0.0, 0))

    # Apply trapezoidal rule
    area = 0.0
    for i in range(1, len(sorted_points)):
        x_i, y_i = sorted_points[i - 1]
        x_ip1, y_ip1 = sorted_points[i]
        width = x_ip1 - x_i
        width = max(width, 0)  # avoid negative widths from unsorted data
        height_avg = (y_i + y_ip1) / 2.0
        area += width * height_avg

    return area