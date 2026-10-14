"""Validated Failure Family distribution visualizations for Phase 15.

Creates figures for VFF (Validated Failure Families) distributions
across evaluation methods.

Possible visualization:
- boxplot + jittered observations

The individual run observations are important because a small number
of seeds can make averages look suspiciously authoritative.

Does not imply that higher VFF automatically means "better" - just
reports the distribution.
"""

from __future__ import annotations

import os
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from agent_eval.visualization.loader import VisualizationData


def plot_vff_distribution(
    data: VisualizationData,
    output_dir: str,
    experiment_id: str,
    figure_id: str = "FIG-04",
    methods: list[str] | None = None,
) -> str:
    """Plot VFF (Validated Failure Families) distribution across methods.

    Uses boxplot + jittered observations to show both the distribution
    and individual run data.

    Args:
        data: Visualization data containing VFF values
        output_dir: Directory to save the figure
        experiment_id: Experiment identifier
        figure_id: Stable figure identifier
        methods: Optional list of method names; None = all

    Returns:
        Path to saved figure file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Collect VFF values by method
    vff_by_method: dict[str, list[int]] = defaultdict(list)
    run_ids_by_method: dict[str, list[str]] = defaultdict(list)

    for run_id, run_metric in data.runs.items():
        if methods is not None and run_metric.method not in methods:
            continue
        vff = run_metric.vff
        if vff is not None:
            vff_by_method[run_metric.method].append(vff)
            run_ids_by_method[run_metric.method].append(run_id)

    # Check if we have data
    methods_with_data = [m for m in vff_by_method if vff_by_method[m]]
    if not methods_with_data:
        figure_path = os.path.join(output_dir, f"{figure_id}.png")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "No VFF data available", ha="center", va="center")
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(figure_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return figure_path

    # Create boxplot + jittered observations
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare data for seaborn
    plot_data = []
    for method in methods_with_data:
        for vff_val in vff_by_method[method]:
            plot_data.append({"method": method, "vff": vff_val})

    # Draw boxplot
    sns.boxplot(
        data=plot_data,
        x="method",
        y="vff",
        ax=ax,
        palette="colorblind",
        showfliers=False,  # We'll add them as jittered points
    )

    # Overlay individual observations as jittered stripplot
    sns.stripplot(
        data=plot_data,
        x="method",
        y="vff",
        ax=ax,
        color="black",
        size=4,
        alpha=0.6,
        jitter=True,
    )

    ax.set_ylabel("Validated Failure Families (VFF)", fontsize=12)
    ax.set_xlabel("Evaluation Method", fontsize=12)
    ax.set_title(
        "Validated Failure Families by Evaluation Method",
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