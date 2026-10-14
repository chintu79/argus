"""Bootstrap confidence intervals for Phase 14 analysis.

Implements bootstrap resampling at the experimental unit (independent run) level.

The experimental unit is an independent experiment run. Therefore bootstrap
at the run level, NOT at the individual tool call, event, failure, or
trajectory step level.

Default:
- bootstrap_resamples = 10_000
- confidence_level = 0.95

Both are configurable.

Result determinism: given the same raw data, same analysis configuration,
same bootstrap seed, and same code version, the bootstrap results must
be deterministic.
"""

from __future__ import annotations

import random
import statistics

from pydantic import BaseModel, Field


class BootstrapResult(BaseModel):
    """Result of bootstrap resampling for a single metric and method."""

    statistic_name: str = Field(..., description="Name of the statistic (e.g., 'mean_VFF')")
    method: str = Field(..., description="Method name")
    resamples: int = Field(..., description="Number of bootstrap resamples")
    confidence_level: float = Field(
        ..., description="Confidence level (e.g., 0.95)"
    )
    bootstrap_samples: list[float] = Field(
        ..., description="List of bootstrap statistic values"
    )
    mean_bootstrap: float = Field(
        ..., description="Mean of the bootstrap distribution"
    )
    ci_lower: float = Field(
        ..., description="Lower bound of confidence interval"
    )
    ci_upper: float = Field(
        ..., description="Upper bound of confidence interval"
    )
    percentile_method: bool = Field(
        ..., description="Whether percentile method was used"
    )
    bca_adjusted: float | None = Field(
        default=None, description="BCa-adjusted interval boundary"
    )

    @property
    def ci_width(self) -> float:
        """Width of the confidence interval."""
        return self.ci_upper - self.ci_lower


def bootstrap_resample(
    data: list[float],
    resamples: int = 10_000,
    seed: int | None = None,
    statistic: str = "mean",
) -> list[float]:
    """Perform bootstrap resampling at the run level.

    Args:
        data: List of run-level metric values (e.g., VFF values across runs).
        resamples: Number of bootstrap resamples to draw.
        seed: Random seed for reproducibility. Default None uses system random.
        statistic: Which statistic to compute per resample.
            Supported: "mean", "median", "sum".

    Returns:
        List of bootstrap statistic values (length = resamples).
    """
    if seed is not None:
        random.seed(seed)

    n = len(data)
    if n == 0:
        return []

    if resamples <= 0:
        return []

    samples: list[float] = []

    for _ in range(resamples):
        # Resample with replacement at the run level
        resampled = [random.choice(data) for _ in range(n)]

        # Compute the statistic
        if statistic == "mean":
            if resampled:
                s = sum(resampled) / len(resampled)
            else:
                s = 0.0
        elif statistic == "median":
            if resampled:
                s = statistics.median(resampled)
            else:
                s = 0.0
        elif statistic == "sum":
            s = sum(resampled) if resampled else 0.0
        else:
            s = sum(resampled) / len(resampled) if resampled else 0.0

        samples.append(s)

    return samples


def compute_bootstrap_ci(
    data: list[float],
    resamples: int = 10_000,
    confidence_level: float = 0.95,
    seed: int | None = None,
    statistic: str = "mean",
) -> dict[str, float]:
    """Compute bootstrap confidence interval for a metric.

    Args:
        data: List of run-level metric values.
        resamples: Number of bootstrap resamples.
        confidence_level: Confidence level (e.g., 0.95 for 95% CI).
        seed: Random seed for reproducibility.
        statistic: Which statistic to bootstrap ("mean", "median", "sum").

    Returns:
        Dict with keys:
        - "mean_bootstrap": mean of bootstrap distribution
        - "ci_lower": lower confidence interval boundary
        - "ci_upper": upper confidence interval boundary
        - "ci_width": width of the confidence interval
    """
    if not data:
        return {
            "mean_bootstrap": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "ci_width": 0.0,
        }

    # Generate bootstrap samples
    samples = bootstrap_resample(data, resamples=resamples, seed=seed, statistic=statistic)

    if not samples:
        return {
            "mean_bootstrap": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "ci_width": 0.0,
        }

    # Compute mean of bootstrap distribution
    mean_bootstrap = sum(samples) / len(samples) if samples else 0.0

    # Compute confidence interval using percentile method
    sorted_samples = sorted(samples)
    alpha = 1.0 - confidence_level
    lower_idx = int(alpha / 2 * resamples)
    upper_idx = int((1 - alpha / 2) * resamples) - 1

    # Clamp indices to valid range
    lower_idx = max(0, min(lower_idx, resamples - 1))
    upper_idx = max(0, min(upper_idx, resamples - 1))

    ci_lower = sorted_samples[lower_idx]
    ci_upper = sorted_samples[upper_idx]

    return {
        "mean_bootstrap": round(mean_bootstrap, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "ci_width": round(ci_upper - ci_lower, 4),
    }


def run_bootstrap_across_methods(
    method_metrics: dict[str, dict[str, list[float]]],
    resamples: int = 10_000,
    confidence_level: float = 0.95,
    seed: int = 42,
    statistic: str = "mean",
) -> dict[str, dict[str, dict[str, float]]]:
    """Run bootstrap CI computation across multiple methods and metrics.

    Args:
        method_metrics: dict keyed by method name, each containing dict
            keyed by metric name, each containing list of run-level values.
        resamples: Number of bootstrap resamples.
        confidence_level: Confidence level.
        seed: Random seed for reproducibility.
        statistic: Which statistic to bootstrap.

    Returns:
        dict keyed by method, then by metric, then by CI component.
    """
    results: dict[str, dict[str, dict[str, float]]] = {}

    for method, metrics in method_metrics.items():
        results[method] = {}
        for metric_name, values in metrics.items():
            if values:
                ci_result = compute_bootstrap_ci(
                    values,
                    resamples=resamples,
                    confidence_level=confidence_level,
                    seed=seed,
                    statistic=statistic,
                )
                results[method][metric_name] = ci_result
            else:
                results[method][metric_name] = {
                    "mean_bootstrap": 0.0,
                    "ci_lower": 0.0,
                    "ci_upper": 0.0,
                    "ci_width": 0.0,
                }

    return results