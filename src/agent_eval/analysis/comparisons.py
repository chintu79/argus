"""Pairwise comparisons for Phase 14 analysis.

Perform pairwise statistical comparisons between methods for all
primary metrics, with proper correction for multiple comparisons.

Do not reorder methods into a "best to worst" ranking.
The analysis should present method-specific measurements and
statistical comparisons as independent statements.
"""

from __future__ import annotations

from typing import Any

from agent_eval.analysis.hypothesis_tests import (
    HypothesisTestResult,
    wilcoxon_signed_rank_test,
)
from agent_eval.analysis.multiple_comparison import (
    adjust_pvalues_holm,
    cliffs_delta,
)


def run_pairwise_comparisons(
    method_metrics: dict[str, dict[str, list[float]]],
    metric_names: tuple[str, ...] = ("VFF", "FDE", "CPF", "AUFDC"),
    alpha: float = 0.05,
    paired: bool = True,
) -> dict[str, dict[str, dict[str, Any]]]:
    """Run pairwise comparisons between all methods for each metric.

    Compares every method against every other method using the specified
    test procedure, with Holm correction for multiple comparisons.

    Returns a nested dict:
    results[metric_name][comparison_key] = test_result_dict

    where comparison_key is "method_a_vs_method_b".

    Do not create arbitrary composite scores or rank orderings.
    Keep pairwise comparisons as independent statements.
    """
    method_names = list(method_metrics.keys())
    n_methods = len(method_names)

    results: dict[str, dict[str, dict[str, Any]]] = {}

    for metric_name in metric_names:
        metric_results: dict[str, dict[str, Any]] = {}

        # Collect all pairwise comparisons
        raw_pvalues: list[float] = []
        all_comparison_keys: list[str] = []

        for i in range(n_methods):
            for j in range(i + 1, n_methods):
                method_a = method_names[i]
                method_b = method_names[j]

                a_values = method_metrics[method_a].get(metric_name, [])
                b_values = method_metrics[method_b].get(metric_name, [])

                comparison_key = f"{method_a}_vs_{method_b}"
                all_comparison_keys.append(comparison_key)

                if not a_values or not b_values:
                    # Not enough data
                    metric_results[comparison_key] = {
                        "test_statistic": None,
                        "p_value": 1.0,
                        "effect_size": None,
                        "direction": "NO_DIFFERENCE",
                        "evidence_status": "INCONCLUSIVE",
                        "adjusted_p_value": 1.0,
                    }
                    raw_pvalues.append(1.0)
                    continue

                # Perform appropriate test
                if paired and len(a_values) == len(b_values):
                    test_result = wilcoxon_signed_rank_test(a_values, b_values)
                else:
                    # Independent groups test
                    try:
                        from scipy import stats as scipy_stats
                        stat, p = scipy_stats.mannwhitneyu(
                            a_values, b_values, alternative="two-sided"
                        )
                        # Create a minimal result object
                        test_result = HypothesisTestResult(
                            hypothesis_id="",
                            test_name="mann_whitney_u",
                            statistic=stat,
                            p_value=p,
                            alpha=alpha,
                        )
                    except Exception:
                        test_result = HypothesisTestResult(
                            hypothesis_id="",
                            test_name="mann_whitney_u",
                            p_value=1.0,
                            alpha=alpha,
                        )

                # Compute effect size (Cliff's delta)
                delta, delta_dir = cliffs_delta(a_values, b_values)

                # Determine direction
                if test_result and test_result.direction:
                    direction = test_result.direction
                elif delta_dir in ("positive", "negative"):
                    direction = delta_dir
                else:
                    direction = "NO_DIFFERENCE"

                # Build result dict
                result: dict[str, Any] = {
                    "test_statistic": test_result.statistic
                    if test_result
                    else None,
                    "p_value": test_result.p_value
                    if test_result
                    else 1.0,
                    "effect_size": delta,
                    "direction": direction,
                    "evidence_status": (
                        "SUPPORTED"
                        if (test_result and test_result.p_value is not None and test_result.p_value < alpha)
                        else "NOT_SUPPORTED"
                        if (test_result and test_result.p_value is not None and test_result.p_value >= alpha)
                        else "INCONCLUSIVE"
                    ),
                }

                metric_results[comparison_key] = result
                raw_pvalues.append(test_result.p_value if (test_result and test_result.p_value is not None) else 1.0)

        # Apply Holm correction to all p-values for this metric
        if raw_pvalues:
            holm_result = adjust_pvalues_holm(raw_pvalues, alpha)

            # Map adjusted p-values back to comparisons
            # Sort by p-value to match Holm ordering
            p_to_key: list[tuple[float, str]] = []
            for key, p in zip(all_comparison_keys, raw_pvalues):
                p_to_key.append((p, key))

            p_to_key.sort(key=lambda x: x[0])

            # Assign adjusted p-values
            for rank, (p, key) in enumerate(p_to_key, start=1):
                if key in metric_results:
                    metric_results[key]["adjusted_p_value"] = holm_result["adjusted"][
                        rank - 1
                    ]
                    # Update evidence status based on adjusted p-value
                    if holm_result["adjusted"][rank - 1] < alpha:
                        metric_results[key]["evidence_status"] = "SUPPORTED"
                    elif holm_result["adjusted"][rank - 1] >= alpha:
                        metric_results[key]["evidence_status"] = "NOT_SUPPORTED"
                    else:
                        metric_results[key]["evidence_status"] = "INCONCLUSIVE"

        results[metric_name] = metric_results

    return results


def summarize_comparisons(
    comparison_results: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Summarize pairwise comparison results in neutral language.

    Returns a dict keyed by metric name, each containing a list of
    comparison summaries with neutral language.

    Do not convert direction into "winner/ best/ worst".
    Do not create an overall score or leaderboard.
    """
    summaries: dict[str, list[dict[str, Any]]] = {}

    for metric_name, comparisons in comparison_results.items():
        metric_summaries: list[dict[str, Any]] = []

        for comparison_key, result in comparisons.items():
            summary: dict[str, Any] = {
                "comparison": comparison_key,
                "p_value": result.get("p_value"),
                "adjusted_p_value": result.get("adjusted_p_value"),
                "effect_size": result.get("effect_size"),
                "effect_size_measure": "Cliff's delta",
                "direction": result.get("direction"),
                "evidence_status": result.get("evidence_status"),
            }
            metric_summaries.append(summary)

        summaries[metric_name] = metric_summaries

    return summaries