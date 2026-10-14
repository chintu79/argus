"""AUFDC distribution visualizations for Phase 15.

Creates figures for Area Under Failure Discovery Curve distributions
across evaluation methods.

Recommended presentation:
- boxplot or violin + individual observations

Uses actual run-level AUFDC values.
Does not replace distributions with only means.

Does not label one method as "best".
Neutral title: "Area Under Failure Discovery Curves by Evaluation Method"
"""

from __future__ import annotations

import os
import statistics
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from agent_eval.visualization.loader import VisualizationData


def plot_aufdc_distribution(
    data: VisualizationData,
    output_dir: str,
    experiment_id: str,
    figure_id: str = "FIG-03",
    methods: list[str] | None = None,
) -> str:
    """Plot AUFDC distribution across evaluation methods.

    Shows run-level AUFDC values as a violin plot with individual
    observations overlaid, as recommended by the specification.

    Does not replace the distribution with only the mean.

    Args:
        data: Visualization data containing AUFDC values
        output_dir: Directory to save the figure
        experiment_id: Experiment identifier
        figure_id: Stable figure identifier
        methods: Optional list of method names; None = all

    Returns:
        Path to saved figure file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Collect AUFDC values by method
    aufdc_by_method: dict[str, list[float]] = defaultdict(list)
    run_ids_by_method: dict[str, list[str]] = defaultdict(list)

    for run_id, run_metric in data.runs.items():
        if methods is not None and run_metric.method not in methods:
            continue
        aufdc = run_metric.auf_dc
        if aufdc is not None:
            aufdc_by_method[run_metric.method].append(aufdc)
            run_ids_by_method[run_metric.method].append(run_id)

    if not any(v for v in aufdc_by_method.values()):
        # No AUFDC data found
        figure_path = os.path.join(output_dir, f"{figure_id}.png")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "No AUFDC data available", ha="center", va="center")
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(figure_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return figure_path

    # Set up the plot
    methods_with_data = [m for m in aufdc_by_method if aufdc_by_method[m]]
    
    if not methods_with_data:
        figure_path = os.path.join(output_dir, f"{figure_id}.png")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "No AUFDC data for selected methods", ha="center", va="center")
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(figure_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return figure_path

    # Create violin plot with individual observations
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare data for seaborn violin plot
    plot_data = []
    for method in methods_with_data:
        for val in aufdc_by_method[method]:
            plot_data.append({"method": method, "aufdc": val})

    # Draw violin plot
    sns.violinplot(
        data=plot_data,
        x="method",
        y="aufdc",
        ax=ax,
        inner=None,  # We'll add points separately
        palette="colorblind",
    )

    # Overlay individual observations as stripplot
    sns.stripplot(
        data=plot_data,
        x="method",
        y="aufdc",
        ax=ax,
        color="black",
        size=4,
        alpha=0.6,
        jitter=True,
    )

    # Add median markers
    for method in methods_with_data:
        vals = aufdc_by_method[method]
        if vals:
            median_val = statistics.median(vals)
            ax.plot(
                method, median_val,
                "s", color="white", markeredgewidth=2,
                markersize=8, label=f"{method} median"
            )

    ax.set_ylabel("AUFDC (Area Under Failure Discovery Curve)", fontsize=12)
    ax.set_xlabel("Evaluation Method", fontsize=12)
    ax.set_title(
        "Area Under Failure Discovery Curves by Evaluation Method",
        fontsize=14,
    )
    ax.grid(True, alpha=0.3, axis="y")
    ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()

    figure_path = os.path.join(output_dir, f"{figure_id}.png")
    plt.savefig(figure_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Also save SVG and PDF
    base = figure_path.replace(".png", "")
    plt.savefig(f"{base}.svg", bbox_inches="tight")
    plt.savefig(f"{base}.pdf", bbox_inches="tight")

    return figure_path