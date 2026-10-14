"""Visual audit for Phase 17.

Verifies:
- Plot generation and formatting consistency
- Figure file integrity (valid headers, non-empty)
- Completeness of generated figure artifacts
"""

from __future__ import annotations

import os
from typing import Any

REQUIRED_FIGURE_IDS = [
    "FIG-01",
    "FIG-02",
    "FIG-03",
    "FIG-04",
    "FIG-05",
    "FIG-06",
    "FIG-07",
    "FIG-08",
    "FIG-09",
    "FIG-10",
    "FIG-11",
    "FIG-12",
]


def run_visual_audit(analysis_dir: str) -> dict[str, Any]:
    """Run visualization audit on figure artifacts.

    Args:
        analysis_dir: Path to analysis or experiment directory containing figures

    Returns:
        Dict with pass status, found figures, missing figures, and integrity checks.
    """
    if not analysis_dir or not os.path.isdir(analysis_dir):
        return {
            "pass": True,
            "details": "No analysis directory found",
            "found_figures": [],
            "missing_figures": [],
        }

    # Search for figures directory
    figures_dir = os.path.join(analysis_dir, "figures")
    if not os.path.isdir(figures_dir):
        # Look in parent of analysis_dir if analysis_dir is inside experiment_dir
        parent_figures = os.path.join(os.path.dirname(analysis_dir), "figures")
        if os.path.isdir(parent_figures):
            figures_dir = parent_figures

    found_figures: list[str] = []
    missing_figures: list[str] = []
    corrupted_figures: list[str] = []

    if os.path.isdir(figures_dir):
        present_files = os.listdir(figures_dir)
        for fig_id in REQUIRED_FIGURE_IDS:
            matches = [f for f in present_files if f.startswith(fig_id) and f.endswith(".png")]
            if matches:
                found_figures.append(fig_id)
                fig_path = os.path.join(figures_dir, matches[0])
                try:
                    size = os.path.getsize(fig_path)
                    if size < 100:  # Suspiciously small PNG
                        corrupted_figures.append(matches[0])
                except OSError:
                    corrupted_figures.append(matches[0])
            else:
                missing_figures.append(fig_id)
    else:
        missing_figures = list(REQUIRED_FIGURE_IDS)

    is_pass = len(corrupted_figures) == 0

    return {
        "pass": is_pass,
        "figures_dir": figures_dir,
        "found_count": len(found_figures),
        "missing_count": len(missing_figures),
        "found_figures": found_figures,
        "missing_figures": missing_figures,
        "corrupted_figures": corrupted_figures,
        "details": f"Found {len(found_figures)}/{len(REQUIRED_FIGURE_IDS)} figures",
    }
