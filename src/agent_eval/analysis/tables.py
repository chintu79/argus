"""Result tables for Phase 14 analysis.

Generate machine-readable CSV tables and human-readable report structures.

Machine-readable outputs:
- run_metrics.csv
- aggregate_metrics.csv
- pairwise_comparisons.csv
- hypothesis_results.csv
- bootstrap_results.csv
- effect_sizes.csv
- holdout_metrics.csv
- branching_metrics.csv
- sensitivity_results.csv
- analysis_exclusions.csv

Human-readable report:
- analysis/results.md

All outputs use neutral language and avoid ranking or composite scores.
"""

from __future__ import annotations

import csv
import os
from typing import Any

from agent_eval.analysis.hypothesis_tests import HypothesisTestResult


def write_run_metrics_csv(
    run_metrics: dict[str, dict[str, Any]],
    output_path: str,
) -> None:
    """Write run-level metrics to CSV.

    Format:
    run_id,method,seed,VFF,FDE,CPF,TTFF,AUFDC,tokens_used,executions

    Preserves per-run values without aggregation.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    fieldnames = [
        "run_id",
        "method",
        "seed",
        "VFF",
        "FDE",
        "CPF",
        "TTFF",
        "AUFDC",
        "tokens_used",
        "executions",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for run_id, metrics in run_metrics.items():
            row: dict[str, Any] = {
                "run_id": run_id,
                "method": metrics.get("method", ""),
                "seed": metrics.get("seed", ""),
                "VFF": metrics.get("vff", ""),
                "FDE": metrics.get("fde", ""),
                "CPF": metrics.get("cpf", ""),
                "TTFF": metrics.get("ttff", ""),
                "AUFDC": metrics.get("aufdc", ""),
                "tokens_used": metrics.get("tokens_used", ""),
                "executions": metrics.get("executions", ""),
            }
            writer.writerow(row)


def write_aggregate_metrics_csv(
    aggregate_stats: dict[str, dict[str, Any]],
    output_path: str,
) -> None:
    """Write aggregate statistics to CSV.

    Format:
    metric,n,mean,median,stdev,variance,min,max,iqr,mad

    One row per metric with both parametric and robust statistics.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    fieldnames = [
        "metric",
        "n",
        "mean",
        "median",
        "stdev",
        "variance",
        "min",
        "max",
        "iqr",
        "mad",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for metric_name, stats_dict in aggregate_stats.items():
            row: dict[str, Any] = {
                "metric": metric_name,
                "n": stats_dict.get("n", 0),
                "mean": stats_dict.get("mean"),
                "median": stats_dict.get("median"),
                "stdev": stats_dict.get("stdev"),
                "variance": stats_dict.get("variance"),
                "min": stats_dict.get("min"),
                "max": stats_dict.get("max"),
                "iqr": stats_dict.get("iqr"),
                "mad": stats_dict.get("mad"),
            }
            writer.writerow(row)


def write_pairwise_comparisons_csv(
    comparison_results: dict[str, dict[str, dict[str, Any]]],
    output_path: str,
) -> None:
    """Write pairwise comparison results to CSV.

    Format per metric:
    comparison,method_a,method_b,p_value,adjusted_p_value,effect_size,
    direction,evidence_status

    Do not report raw p-values as though no multiple comparisons occurred.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Flatten all comparisons across metrics
    rows: list[dict[str, Any]] = []

    for metric_name, comparisons in comparison_results.items():
        for comparison_key, result in comparisons.items():
            # Parse method names from comparison key
            parts = comparison_key.replace("vs", "_vs_").split("_vs_")
            method_a = parts[0] if len(parts) > 1 else comparison_key
            method_b = parts[1] if len(parts) > 1 else ""

            row: dict[str, Any] = {
                "comparison": comparison_key,
                "method_a": method_a,
                "method_b": method_b,
                "p_value": result.get("p_value"),
                "adjusted_p_value": result.get("adjusted_p_value"),
                "effect_size": result.get("effect_size"),
                "effect_size_measure": "Cliff's delta",
                "direction": result.get("direction"),
                "evidence_status": result.get("evidence_status"),
                "metric": metric_name,
            }
            rows.append(row)

    with open(output_path, "w", newline="") as f:
        fieldnames = [
            "comparison",
            "method_a",
            "method_b",
            "p_value",
            "adjusted_p_value",
            "effect_size",
            "effect_size_measure",
            "direction",
            "evidence_status",
            "metric",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_hypothesis_results_csv(
    hypothesis_results: dict[str, HypothesisTestResult],
    output_path: str,
) -> None:
    """Write hypothesis test results to CSV.

    Format:
    hypothesis_id,test_name,statistic,p_value,alpha,effect_size,
    effect_size_measure,confidence_interval,direction,evidence_status

    Use neutral language - no 'winner' or 'best'.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    fieldnames = [
        "hypothesis_id",
        "test_name",
        "statistic",
        "p_value",
        "alpha",
        "effect_size",
        "effect_size_measure",
        "confidence_interval",
        "direction",
        "evidence_status",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for hypothesis_id, result in hypothesis_results.items():
            # Format confidence interval
            ci_str = ""
            if result.confidence_interval:
                ci_str = f"[{result.confidence_interval[0]:.4f}, {result.confidence_interval[1]:.4f}]"

            row: dict[str, Any] = {
                "hypothesis_id": hypothesis_id,
                "test_name": result.test_name,
                "statistic": result.statistic,
                "p_value": result.p_value,
                "alpha": result.alpha,
                "effect_size": result.effect_size,
                "effect_size_measure": result.effect_size_measure or "",
                "confidence_interval": ci_str,
                "direction": result.direction,
                "evidence_status": result.evidence_status,
            }
            writer.writerow(row)


def write_bootstrap_results_csv(
    bootstrap_results: dict[str, dict[str, dict[str, float]]],
    output_path: str,
) -> None:
    """Write bootstrap confidence interval results to CSV.

    Format:
    method,metric,mean_bootstrap,ci_lower,ci_upper,ci_width

    One row per method-per-metric combination.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    rows: list[dict[str, Any]] = []

    for method, metrics in bootstrap_results.items():
        for metric_name, ci in metrics.items():
            row: dict[str, Any] = {
                "method": method,
                "metric": metric_name,
                "mean_bootstrap": ci.get("mean_bootstrap", 0.0),
                "ci_lower": ci.get("ci_lower", 0.0),
                "ci_upper": ci.get("ci_upper", 0.0),
                "ci_width": ci.get("ci_width", 0.0),
            }
            rows.append(row)

    fieldnames = ["method", "metric", "mean_bootstrap", "ci_lower", "ci_upper", "ci_width"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_exclusion_csv(
    exclusions: list[dict[str, str]],
    output_path: str,
) -> None:
    """Write analysis exclusions to CSV.

    Format:
    run_id,reason,timestamp

    Records every run excluded from analysis with the reason.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    fieldnames = ["run_id", "reason", "timestamp"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for exclusion in exclusions:
            row: dict[str, Any] = {
                "run_id": exclusion.get("run_id", ""),
                "reason": exclusion.get("reason", ""),
                "timestamp": exclusion.get("timestamp", ""),
            }
            writer.writerow(row)


def write_results_markdown(
    analysis_config: dict[str, Any],
    dataset_summary: dict[str, Any],
    metric_coverage: dict[str, str],
    hypothesis_table: list[dict[str, Any]],
    integrity: dict[str, str],
    warnings: list[str],
    output_path: str,
) -> None:
    """Write the human-readable analysis results report.

    Structure (all neutral language, no ranking):
    1. Analysis Protocol
    2. Dataset Integrity
    3. Experimental Population
    4. Discovery Metrics
    5. Reproducibility Metrics
    6. Branching Metrics
    7. Holdout Generalization
    8. Statistical Comparisons
    9. Effect Sizes
    10. Hypothesis Results
    11. Sensitivity Analysis
    12. Limitations
    13. Raw Result References

    Do not use ranking language ('winner', 'best', 'superior').
    Do not create composite scores or overall rankings.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Determine warnings section
    warnings_section = ""
    if warnings:
        warnings_section = "### Warnings\\n\\n"
        for warning in warnings:
            warnings_section += f"- {warning}\\n"
    else:
        warnings_section = "### No warnings\\n\\n"

    # Format hypothesis table
    hypothesis_rows = ""
    for hyp in hypothesis_table:
        hyp_row = f"| {hyp.get('hypothesis_id', '')} | {hyp.get('metric', '')} | {hyp.get('comparison', '')} | {hyp.get('effect_size', ''):.4f if hyp.get('effect_size') else 'N/A'} | {hyp.get('adjusted_p_value', ''):.4f if hyp.get('adjusted_p_value') else 'N/A'} | {hyp.get('confidence_interval', '')} | {hyp.get('status', '')} |"
        hypothesis_rows += hyp_row + "\\n"

    markdown = f"""# Analysis Results Report

## Analysis Protocol

- **Experiment**: {analysis_config.get('experiment_id', '')}
- **Analysis ID**: {analysis_config.get('analysis_id', '')}
- **Raw Data Hash**: {analysis_config.get('raw_data_hash', '')}
- **Bootstrap Resamples**: {analysis_config.get('bootstrap_resamples', 10000)}
- **Bootstrap Seed**: {analysis_config.get('bootstrap_seed', 42)}
- **Alpha**: {analysis_config.get('alpha', 0.05)}
- **Confidence Level**: {analysis_config.get('confidence_level', 0.95)}

## Dataset

- **Completed runs**: {dataset_summary.get('completed_runs', 0)}
- **Excluded runs**: {dataset_summary.get('excluded_runs', 0)}
- **Methods**: {', '.join(dataset_summary.get('methods', []))}
- **Seeds**: {', '.join(dataset_summary.get('seeds', []))}

## Metric Coverage

| Metric | Status |
|--------|--------|
{chr(10).join([f"| {m} | {s} |" for m, s in metric_coverage.items()])}

## Hypothesis Results

| Hypothesis | Metric | Comparison | Effect Size | Adjusted p | CI | Status |
|-----------|--------|------------|-------------|------------|----|--------|
{hypothesis_rows.strip() if hypothesis_rows else "| — | — | — | — | — | — |"} |

## Integrity

- **Raw data immutable**: {integrity.get('raw_data_immutable', 'unknown')}
- **Analysis deterministic**: {integrity.get('analysis_deterministic', 'unknown')}
- **Holdout isolation**: {integrity.get('holdout_isolation', 'unknown')}
- **Budget integrity**: {integrity.get('budget_integrity', 'unknown')}
- **Seed integrity**: {integrity.get('seed_integrity', 'unknown')}

{warnings_section}

## Raw Result References

- Run-level metrics: analysis/run_metrics.csv
- Aggregate metrics: analysis/aggregate_metrics.csv
- Pairwise comparisons: analysis/pairwise_comparisons.csv
- Hypothesis results: analysis/hypothesis_results.csv
- Bootstrap CIs: analysis/bootstrap_results.csv

"""

    with open(output_path, "w") as f:
        f.write(markdown)