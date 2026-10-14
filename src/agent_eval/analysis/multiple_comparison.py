"""Multiple comparison correction for Phase 14 analysis.

When performing multiple pairwise comparisons, adjust p-values
using the Holm correction to control the family-wise error rate.

Do not report raw p-values as though no multiple comparisons occurred.
"""

from __future__ import annotations

from typing import Any

from agent_eval.analysis.hypothesis_tests import (
    holm_correction,
    wilcoxon_signed_rank_test,
)


def adjust_pvalues_holm(
    p_values: list[float],
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Apply Holm correction to a list of p-values.

    Returns a dict with:
    - 'adjusted': list of Holm-adjusted p-values
    - 'rejected': list of booleans indicating which null hypotheses are rejected
    - 'alpha': the overall alpha level used
    - 'method': string identifier ('holm')

    Args:
        p_values: List of raw p-values from multiple comparisons.
        alpha: Family-wise error rate (default 0.05).

    Example:
        >>> adjust_pvalues_holm([0.01, 0.04, 0.06])
        {'adjusted': [0.03, 0.06, 1.0], 'rejected': [True, False, False], 'alpha': 0.05, 'method': 'holm'}
    """
    adjusted, rejected = holm_correction(p_values, alpha)

    return {
        "adjusted": adjusted,
        "rejected": rejected,
        "alpha": alpha,
        "method": "holm",
    }


def pairwise_comparisons(
    method_metrics: dict[str, dict[str, list[float]]],
    metric_name: str,
    alpha: float = 0.05,
    test: str = "wilcoxon",
    paired: bool = True,
) -> dict[str, dict[str, Any]]:
    """Perform all pairwise comparisons between methods for a given metric.

    Compares every method against every other method using the specified
    test procedure.

    Returns a dict keyed by (method_a, method_b) pairs, each containing:
    - test_statistic
    - p_value
    - adjusted_p_value (Holm-corrected)
    - effect_size (Cliff's delta)
    - direction (POSITIVE/NEGATIVE/NO_DIFFERENCE)
    - evidence_status (SUPPORTED/NOT_SUPPORTED/INCONCLUSIVE)

    Args:
        method_metrics: dict keyed by method name, each containing dict
            keyed by metric name, each containing list of run-level values.
        metric_name: Name of the metric to compare (e.g., 'VFF').
        alpha: Significance level for hypothesis testing.
        test: Statistical test to use ('wilcoxon' or 'friedman').
        paired: Whether the comparison is paired (same seeds across methods).

    Important: Do not create arbitrary composite scores or rank orderings.
    Keep pairwise comparisons as independent statements.
    """
    method_names = list(method_metrics.keys())
    n_methods = len(method_names)

    # Perform all pairwise comparisons
    results: dict[str, dict[str, Any]] = {}

    # Collect raw p-values for Holm correction
    raw_pvalues: list[float] = []
    raw_results: dict[str, dict[str, Any]] = {}

    for i in range(n_methods):
        for j in range(i + 1, n_methods):
            method_a = method_names[i]
            method_b = method_names[j]

            a_values = method_metrics[method_a].get(metric_name, [])
            b_values = method_metrics[method_b].get(metric_name, [])

            if not a_values or not b_values:
                # Not enough data
                result_key = f"{method_a}_vs_{method_b}"
                results[result_key] = {
                    "test_statistic": None,
                    "p_value": 1.0,
                    "adjusted_p_value": 1.0,
                    "effect_size": None,
                    "direction": "NO_DIFFERENCE",
                    "evidence_status": "INCONCLUSIVE",
                }
                raw_pvalues.append(1.0)
                raw_results[result_key] = {
                    "p_value": 1.0,
                    "effect_size": None,
                    "direction": "NO_DIFFERENCE",
                }
                continue

            # Perform appropriate test
            test_result = None
            if test == "wilcoxon" and paired:
                test_result = wilcoxon_signed_rank_test(a_values, b_values)
                p = test_result.p_value if test_result.p_value is not None else 1.0
                stat = test_result.statistic
            else:
                # Independent test or friedman
                try:
                    from scipy import stats as scipy_stats
                    if paired:
                        stat, p = scipy_stats.wilcoxon(a_values, b_values,
                                                       alternative="two-sided")
                    else:
                        # Use Mann-Whitney U for independent
                        stat, p = scipy_stats.mannwhitneyu(
                            a_values, b_values, alternative="two-sided"
                        )
                except Exception:
                    p = 1.0
                    stat = None

            # Compute effect size (Cliff's delta)
            delta, delta_dir = cliffs_delta(a_values, b_values)

            # Direction from test statistic
            if test_result and test_result.direction:
                direction = test_result.direction
            elif delta_dir in ("positive", "negative"):
                direction = delta_dir
            else:
                direction = "NO_DIFFERENCE"

            result_key = f"{method_a}_vs_{method_b}"
            raw_pvalues.append(p)

            raw_results[result_key] = {
                "p_value": p,
                "effect_size": delta,
                "direction": direction,
            }

            results[result_key] = {
                "test_statistic": stat,
                "p_value": p,
                "effect_size": delta,
                "direction": direction,
                "evidence_status": (
                    "SUPPORTED" if p < alpha else "NOT_SUPPORTED"
                    if p >= alpha
                    else "INCONCLUSIVE"
                ),
            }

    # Apply Holm correction to all raw p-values
    holm_result = adjust_pvalues_holm(raw_pvalues, alpha)

    # Update results with adjusted p-values
    for idx, (key, r) in enumerate(raw_results.items()):
        if idx < len(holm_result["adjusted"]):
            adj_p = holm_result["adjusted"][idx]
            results[key]["adjusted_p_value"] = adj_p
            results[key]["evidence_status"] = (
                "SUPPORTED"
                if adj_p < alpha
                else "NOT_SUPPORTED"
                if adj_p >= alpha
                else "INCONCLUSIVE"
            )
            results[key]["rejected"] = holm_result["rejected"][idx]
        else:
            results[key]["adjusted_p_value"] = r["p_value"]
            results[key]["evidence_status"] = r["evidence_status"]
            results[key]["rejected"] = r["rejected"]

    return results


def cliffs_delta(
    x: list[float],
    y: list[float],
) -> tuple[float, str]:
    """Compute Cliff's delta for two independent samples.

    See analysis.effect_sizes.cliffs_delta for the full implementation.
    """
    from agent_eval.analysis.effect_sizes import cliffs_delta as cd

    return cd(x, y)