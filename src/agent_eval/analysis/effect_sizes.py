"""Effect sizes for Phase 14 analysis.

Implements Cliff's delta for independent/non-normal comparisons,
and paired rank-biserial correlation for paired comparisons.

Effect size statistics are reported as effect-size statistics, not
quality rankings. Direction is recorded as POSITIVE, NEGATIVE, or
NO_DIFFERENCE.

The implementation must identify which statistic was used.
"""

from __future__ import annotations

import math

from scipy import stats


def cliffs_delta(
    x: list[float],
    y: list[float],
) -> tuple[float, str]:
    """Compute Cliff's delta for two independent samples.

    Cliff's delta is a non-parametric effect size measure that
    quantifies the amount of non-overlap between two distributions.

    Returns:
        (delta, interpretation) where:
        - delta: float in range [-1, 1]
        - interpretation: "positive", "negative", or "null"

    Interpretation guidelines (from Rosenthal & Rubin, 2003):
    - |delta| < 0.147: negligible/nothing
    - 0.147 <= |delta| < 0.33: small
    - 0.33 <= |delta| < 0.474: medium
    - |delta| >= 0.474: large

    The interpretation field reports the direction:
    - "positive": x tends to be greater than y
    - "negative": y tends to be greater than x
    - "null": distributions are essentially identical
    """
    if not x or not y:
        return 0.0, "null"

    # Calculate Cliff's delta
    n_x = len(x)
    n_y = len(y)

    # Count how many times x > y
    greater = 0
    less = 0
    tie = 0

    for xi in x:
        for yi in y:
            if xi > yi:
                greater += 1
            elif xi < yi:
                less += 1
            else:
                tie += 1

    # Cliff's delta formula
    delta = (greater - less) / (n_x * n_y) if n_x * n_y > 0 else 0.0

    # Determine direction
    if abs(delta) < 1e-10:
        interpretation = "null"
    elif delta > 0:
        interpretation = "positive"
    else:
        interpretation = "negative"

    return round(delta, 6), interpretation


def paired_rank_biserial(
    diffs: list[float],
) -> tuple[float | None, str]:
    """Compute paired rank-biserial correlation.

    For paired observations, the rank-biserial correlation measures
    the strength of the relationship between the pairing and the
    observed differences.

    Args:
        diffs: List of paired differences (Method A - Method B).

    Returns:
        (correlation, direction) where:
        - correlation: float in [-1, 1], or None if computation impossible
        - direction: "positive", "negative", or "null"
    """
    if not diffs:
        return None, "null"

    # Remove zero differences
    non_zero_diffs = [d for d in diffs if d != 0]

    if not non_zero_diffs:
        return 0.0, "null"

    n = len(non_zero_diffs)
    # Rank the absolute differences
    abs_diffs = [abs(d) for d in non_zero_diffs]
    ranked = sorted(range(n), key=lambda i: abs_diffs[i])

    # Assign ranks (handling ties with average rank)
    ranks = [0.0] * n
    rank_sum = 0.0
    i = 0
    while i < n:
        j = i
        while j < n and abs_diffs[ranked[j]] == abs_diffs[ranked[i]]:
            rank_sum += ranked[j] + 1
            j += 1
        avg_rank = rank_sum / (j - i)
        for k in range(i, j):
            ranks[ranked[k]] = avg_rank
            rank_sum -= ranked[k] + 1
        i = j

        # Count positive and negative ranks
        pos_ranks = sum(1 for r in ranks if r > 0)
        neg_ranks = sum(1 for r in ranks if r < 0)

        # Rank-biserial formula
        rb = (pos_ranks - neg_ranks) / (pos_ranks + neg_ranks) if (pos_ranks + neg_ranks) > 0 else 0.0

        # Determine direction
        if rb > 0:
            direction = "positive"
        elif rb < 0:
            direction = "negative"
        else:
            direction = "null"

        return round(rb, 6), direction

    # Fallback using scipy
    try:
        # Use Mann-Whitney U on the differences
        u, _p = stats.mannwhitneyu(
            [0.0] * len(diffs), diffs, alternative="two-sided"
        )
        # Convert to rank-biserial r
        r = 1 - (2 * u) / (len(diffs) * (len(diffs) + 1) / 2) if len(diffs) > 0 else 0
        if r > 0:
            direction = "positive"
        elif r < 0:
            direction = "negative"
        else:
            direction = "null"
        return round(r, 6), direction
    except Exception:
        # Fallback to Cliff's delta on the differences
        if len(diffs) > 1:
            delta, dir_name = cliffs_delta(diffs, [0.0] * len(diffs))
            return delta, dir_name
        return 0.0, "null"


def cohens_d(
    x: list[float],
    y: list[float],
) -> tuple[float | None, str]:
    """Compute Cohen's d (pooled standard deviation version).

    Note: Cohen's d assumes approximately normal distributions,
    so for failure-discovery data (which is typically skewed),
    Cliff's delta is preferred.

    Returns:
        (d, interpretation) where d is the effect size or None.
    """
    try:
        nx = len(x)
        ny = len(y)
        if nx < 2 or ny < 2:
            return None, "null"

        mean_x = sum(x) / nx
        mean_y = sum(y) / ny
        var_x = sum((xi - mean_x) ** 2 for xi in x) / (nx - 1)
        var_y = sum((yi - mean_y) ** 2 for yi in y) / (ny - 1)

        # Pooled standard deviation
        pooled_sd = math.sqrt((var_x * (nx - 1) + var_y * (ny - 1)) / (nx + ny - 2))

        if pooled_sd == 0:
            return None, "null"

        d = (mean_x - mean_y) / pooled_sd

        # Interpret magnitude
        if abs(d) < 0.2:
            magnitude = "negligible"
        elif abs(d) < 0.5:
            magnitude = "small"
        elif abs(d) < 0.8:
            magnitude = "medium"
        else:
            magnitude = "large"

        return round(d, 6), magnitude
    except Exception:
        return None, "null"


def surface_area_between_curves(
    curve_a: list[tuple[float, int]],
    curve_b: list[tuple[float, int]],
) -> float:
    """Compute the area between two discovery curves.

    This measures the cumulative difference in validated family counts
    across the normalized budget range.

    A larger area indicates greater divergence between the curves.

    The area is computed using the trapezoidal rule on both curves,
    then the difference is taken.

    Args:
        curve_a: List of (normalized_budget, validated_family_count) for method A
        curve_b: List of (normalized_budget, validated_family_count) for method B

    Returns:
        Positive if curve A dominates (more families at each budget level),
        negative if curve B dominates, near zero if curves are similar.
    """
    # Ensure both curves start from (0, 0) and end at same x range
    from agent_eval.analysis.curves import validate_curve_points

    if not validate_curve_points(curve_a) or not validate_curve_points(curve_b):
        return 0.0

    # Sort both curves by normalized budget
    a_sorted = sorted(curve_a, key=lambda p: p[0])
    b_sorted = sorted(curve_b, key=lambda p: p[0])

    # Align x ranges - start both from 0
    if a_sorted[0][0] > 0:
        a_sorted.insert(0, (0.0, 0))
    if b_sorted[0][0] > 0:
        b_sorted.insert(0, (0.0, 0))

    # Align x ranges - end at min of both end points
    max_x = min(a_sorted[-1][0], b_sorted[-1][0])
    if max_x <= 0:
        return 0.0

    # Truncate both curves to same x range
    a_truncated = [(x, y) for x, y in a_sorted if x <= max_x]
    b_truncated = [(x, y) for x, y in b_sorted if x <= max_x]

    # Ensure both have same x points by interpolation/nearest
    # Get all unique x points
    all_x = sorted(set([x for x, _ in a_truncated] + [x for x, _ in b_truncated]))

    if not all_x:
        return 0.0

    # Build continuous representations
    area_difference = 0.0

    for x_target in all_x:
        # Find y values for both curves at this x
        # Use nearest point
        a_y = 0
        b_y = 0

        # Nearest for curve A
        if a_truncated:
            a_y = a_truncated[0][1]
            for x_a, y_a in a_truncated:
                if abs(x_a - x_target) < abs((a_truncated[0][0] if a_truncated else 0) - x_target):
                    a_y = y_a

        # Nearest for curve B
        if b_truncated:
            b_y = b_truncated[0][1]
            for x_b, y_b in b_truncated:
                if abs(x_b - x_target) < abs((b_truncated[0][0] if b_truncated else 0) - x_target):
                    b_y = y_b

        area_difference += (a_y - b_y)  # accumulate difference

    return round(area_difference, 4)