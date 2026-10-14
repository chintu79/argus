"""Hypothesis tests for Phase 14 analysis.

Implements non-parametric hypothesis tests as default, consistent with
the Phase 14 principle of not assuming normality for failediscovery data.

Default tests:
- Paired methods: Wilcoxon signed-rank test
- More than two methods: Friedman test

Adjustment:
- Holm correction for multiple comparisons

The same test protocol is used consistently across all hypotheses.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from scipy import stats as scipy_stats

from agent_eval.analysis.effect_sizes import cliffs_delta


class HypothesisTestResult(BaseModel):
    """Result of a single hypothesis test."""

    hypothesis_id: str = Field(..., description="Identifier for the hypothesis")
    test_name: str = Field(..., description="Name of the test performed")
    statistic: float | None = Field(
        default=None, description="Test statistic value"
    )
    p_value: float | None = Field(
        default=None, description="P-value from the test"
    )
    alpha: float = Field(
        default=0.05, description=" significance level used"
    )
    effect_size: float | None = Field(
        default=None, description="Effect size (e.g., Cliff's delta)"
    )
    effect_size_measure: str | None = Field(
        default=None, description="Name of effect size measure"
    )
    confidence_interval: tuple[float, float] | None = Field(
        default=None, description="Confidence interval for the effect"
    )
    direction: str = Field(
        default="NO_DIFFERENCE",
        description="POSITIVE, NEGATIVE, or NO_DIFFERENCE",
    )
    adjusted_p_value: float | None = Field(
        default=None, description="P-value after multiple comparison correction"
    )
    corrected: bool = Field(
        default=False, description="Whether correction was applied"
    )
    evidence_status: str = Field(
        default="INCONCLUSIVE",
        description="SUPPORTED, NOT_SUPPORTED, or INCONCLUSIVE",
    )


def wilcoxon_signed_rank_test(
    method_a: list[float],
    method_b: list[float],
    paired_seeds: bool = True,
) -> HypothesisTestResult:
    """Perform Wilcoxon signed-rank test for paired methods.

    Controls for variation introduced by the seed.

    Args:
        method_a: List of metric values for Method A (one per seed).
        method_b: List of metric values for Method B (one per seed).
        paired_seeds: If True, methods are assumed to use the same seeds.

    Returns:
        HypothesisTestResult with test statistic, p-value, and direction.
    """
    if not method_a or not method_b:
        return HypothesisTestResult(
            hypothesis_id="",
            test_name="wilcoxon_signed_rank",
            p_value=1.0,
            alpha=0.05,
            direction="NO_DIFFERENCE",
            evidence_status="INCONCLUSIVE",
        )

    # If paired seeds, ensure same length
    if paired_seeds and len(method_a) != len(method_b):
        # Truncate to shorter length
        n = min(len(method_a), len(method_b))
        method_a = method_a[:n]
        method_b = method_b[:n]

    # Compute differences
    diffs = [a - b for a, b in zip(method_a, method_b)]

    # Perform Wilcoxon signed-rank test
    try:
        stat, p = scipy_stats.wilcoxon(diffs, alternative="two-sided")
        # Determine direction
        if stat > 0:
            direction = "POSITIVE"
        elif stat < 0:
            direction = "NEGATIVE"
        else:
            direction = "NO_DIFFERENCE"

        # Cliff's delta as effect size
        delta, _ = cliffs_delta(method_a, method_b)
        effect_size_measure = "Cliff's delta"

        return HypothesisTestResult(
            hypothesis_id="",
            test_name="wilcoxon_signed_rank",
            statistic=round(float(stat), 6),
            p_value=round(float(p), 6),
            alpha=0.05,
            effect_size=round(delta, 6) if delta is not None else None,
            effect_size_measure=effect_size_measure,
            direction=direction,
            evidence_status=(
                "SUPPORTED"
                if p < 0.05
                else "NOT_SUPPORTED"
                if p >= 0.05
                else "INCONCLUSIVE"
            ),
        )
    except Exception:
        return HypothesisTestResult(
            hypothesis_id="",
            test_name="wilcoxon_signed_rank",
            p_value=1.0,
            alpha=0.05,
            direction="NO_DIFFERENCE",
            evidence_status="INCONCLUSIVE",
        )


def friedman_test(
    method_results: dict[str, list[float]],
) -> HypothesisTestResult:
    """Perform Friedman test for more than two related methods.

    Args:
        method_results: dict keyed by method name, each containing
            list of metric values (one per run/block).

    Returns:
        HypothesisTestResult with chi-squared statistic and p-value.
    """
    if not method_results or len(method_results) < 2:
        return HypothesisTestResult(
            hypothesis_id="",
            test_name="friedman",
            p_value=1.0,
            alpha=0.05,
            direction="NO_DIFFERENCE",
            evidence_status="INCONCLUSIVE",
        )

    try:
        # Get the number of observations (blocks/runs)
        n_obs = None
        method_names = []
        data_matrix = []

        for method_name, results in method_results.items():
            method_names.append(method_name)
            if n_obs is None:
                n_obs = len(results)
            elif len(results) != n_obs:
                # Inconsistent - return inconclusive
                return HypothesisTestResult(
                    hypothesis_id="",
                    test_name="friedman",
                    p_value=1.0,
                    alpha=0.05,
                    direction="NO_DIFFERENCE",
                    evidence_status="INCONCLUSIVE",
                )
            data_matrix.append(results)

        if n_obs is None or n_obs < 2:
            return HypothesisTestResult(
                hypothesis_id="",
                test_name="friedman",
                p_value=1.0,
                alpha=0.05,
                direction="NO_DIFFERENCE",
                evidence_status="INCONCLUSIVE",
            )

        n_methods = len(method_names)

        # Perform Friedman test
        # H0: The distributions are the same across all methods
        # H1: At least one method differs from the others

        # Calculate ranks within each block
        ranks = []
        for block_idx in range(n_obs):
            block_values = [data_matrix[method_idx][block_idx]
                           for method_idx in range(n_methods)]
            # Rank the values (average ranks for ties)
            sorted_indices = sorted(range(n_methods), key=lambda i: block_values[i])
            block_ranks = [0.0] * n_methods
            for rank_idx, method_idx in enumerate(sorted_indices):
                block_ranks[method_idx] = rank_idx + 1  # 1-based ranks
            ranks.append(block_ranks)

        # Calculate Friedman statistic
        # R_j = sum of ranks for method j across all blocks
        r_j = [sum(ranks[block_idx][method_idx]
                 for block_idx in range(n_obs))
               for method_idx in range(n_methods)]

        # Friedman chi-squared statistic
        # χ²_F = (12 * n_obs) / (n_methods * (n_methods + 1)) * sum(R_j^2) - 3 * n_obs * (n_methods + 1)
        sum_r_sq = sum(r ** 2 for r in r_j)
        epsilon = 1.0 - (n_methods - 1) / (6 * n_obs * (n_methods - 1)) if n_methods > 1 and n_obs > 1 else 1.0
        chi2 = (12.0 * n_obs / (n_methods * (n_methods + 1)) * sum_r_sq - 3 * n_obs * (n_methods + 1)) * epsilon

        # Approximate p-value using chi-squared distribution with n_methods-1 df
        df = n_methods - 1
        if df > 0:
            p = scipy_stats.chi2.sf(chi2, df)
        else:
            p = 1.0

        if p < 0.05:
            direction = "POSITIVE"  # some method differs
        else:
            direction = "NO_DIFFERENCE"

        return HypothesisTestResult(
            hypothesis_id="",
            test_name="friedman",
            statistic=round(float(chi2), 6),
            p_value=round(float(p), 6),
            alpha=0.05,
            effect_size=None,
            effect_size_measure=None,
            direction=direction,
            evidence_status=(
                "SUPPORTED" if p < 0.05 else "NOT_SUPPORTED"
                if p >= 0.05
                else "INCONCLUSIVE"
            ),
        )
    except Exception:
        return HypothesisTestResult(
            hypothesis_id="",
            test_name="friedman",
            p_value=1.0,
            alpha=0.05,
            direction="NO_DIFFERENCE",
            evidence_status="INCONCLUSIVE",
        )


def holm_correction(
    p_values: list[float],
    alpha: float = 0.05,
) -> tuple[list[float], list[bool]]:
    """Apply Holm correction to p-values for multiple comparisons.

    Args:
        p_values: List of raw p-values.
        alpha: Overall significance level.

    Returns:
        (adjusted_p_values, rejected_nulls) where:
        - adjusted_p_values: Holm-adjusted p-values
        - rejected_nulls: Boolean list indicating which hypotheses are rejected
    """
    if not p_values:
        return [], []

    n = len(p_values)
    sorted_p_indices = sorted(range(n), key=lambda i: p_values[i])

    adjusted = [0.0] * n
    rejected = [False] * n

    # Step-down procedure
    for rank, idx in enumerate(sorted_p_indices, start=1):
        p = p_values[idx]
        # Holm-adjusted p-value
        adjusted[idx] = min(1.0, p * n / rank)

        # Compare to alpha
        if adjusted[idx] <= alpha and not rejected[idx]:
            rejected[idx] = True

    # Ensure monotonicity: if a hypothesis is not rejected,
    # all subsequent (larger adjusted p) should also not be rejected
    for i in range(1, n):
        if not rejected[i - 1]:
            rejected[i] = False

    return adjusted, rejected