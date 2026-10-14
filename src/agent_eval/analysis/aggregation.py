"""Aggregate statistics for Phase 14 analysis.

For each metric and method calculate:
- n (count)
- mean
- median
- standard_deviation
- variance
- minimum
- maximum

Also calculate robust statistics because failure-discovery data may be skewed:
- median
- IQR (interquartile range)
- MAD (median absolute deviation)

Do not assume normality. Report both parametric and robust statistics.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any


def compute_aggregate_stats(
    metric_values: dict[str, list[float]],
) -> dict[str, dict[str, Any]]:
    """Compute aggregate statistics for each metric across methods.

    For each metric and method compute:
    - n (count)
    - mean
    - median
    - standard_deviation
    - variance
    - minimum
    - maximum

    Also compute robust statistics because failure-discovery data may be skewed:
    - median (already included)
    - IQR (interquartile range)
    - MAD (median absolute deviation)

    Do not assume normality. Report both parametric and robust statistics.
    """
    aggregates: dict[str, dict[str, Any]] = {}

    for metric_name, values in metric_values.items():
        if not values:
            aggregates[metric_name] = {
                "n": 0,
                "mean": None,
                "median": None,
                "stdev": None,
                "variance": None,
                "min": None,
                "max": None,
                "iqr": None,
                "mad": None,
            }
            continue

        n = len(values)

        # Parametric statistics
        mean_val = statistics.mean(values)
        median_val = statistics.median(values)
        stdev_val = statistics.stdev(values) if n > 1 else 0.0
        variance_val = statistics.variance(values) if n > 1 else 0.0
        min_val = min(values)
        max_val = max(values)

        # Robust statistics
        # IQR = Q3 - Q1
        q1 = statistics.quantiles(values, n=4)[0] if n >= 4 else median_val
        q3 = statistics.quantiles(values, n=4)[2] if n >= 4 else median_val
        iqr_val = q3 - q1

        # MAD = median(|x - median(x)|)
        median_val_for_mad = statistics.median(values)
        deviations = [abs(v - median_val_for_mad) for v in values]
        mad_val = statistics.median(deviations) if deviations else 0.0

        aggregates[metric_name] = {
            "n": n,
            "mean": round(mean_val, 4) if mean_val is not None else None,
            "median": round(median_val, 4) if median_val is not None else None,
            "stdev": round(stdev_val, 4) if stdev_val is not None else None,
            "variance": round(variance_val, 4) if variance_val is not None else None,
            "min": round(min_val, 4) if min_val is not None else None,
            "max": round(max_val, 4) if max_val is not None else None,
            "iqr": round(iqr_val, 4) if iqr_val is not None else None,
            "mad": round(mad_val, 4) if mad_val is not None else None,
        }

    return aggregates


def compute_metric_aggregates(
    method_metrics: dict[str, dict[str, dict[str, Any]]],
    metric_names: tuple[str, ...] = (
        "VFF",
        "FDE",
        "CPF",
        "AUFDC",
    ),
) -> dict[str, dict[str, Any]]:
    """Compute aggregate statistics across runs for each method and metric.

    method_metrics: dict keyed by method name, each containing dict keyed
    by metric name, each containing list of run-level values.

    Returns dict keyed by metric name, each containing aggregate statistics.
    """
    aggregates: dict[str, dict[str, Any]] = {}

    for metric_name in metric_names:
        metric_values_by_method: dict[str, list[float]] = defaultdict(list)

        for method, metrics in method_metrics.items():
            if metric_name in metrics:
                values = metrics[metric_name]
                if isinstance(values, list):
                    metric_values_by_method[method] = values
                elif isinstance(values, (int, float)):
                    metric_values_by_method[method] = [values]

        if metric_values_by_method:
            aggregates[metric_name] = compute_aggregate_stats(metric_values_by_method)
        else:
            aggregates[metric_name] = {
                "n": 0,
                "mean": None,
                "median": None,
                "stdev": None,
                "variance": None,
                "min": None,
                "max": None,
                "iqr": None,
                "mad": None,
            }

    return aggregates