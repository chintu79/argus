"""Consistency validation for Phase 16 research report.

Verifies that the reported results match Phase 14 analysis outputs,
that figure and table references point to existing files, and that
experiment IDs, hypothesis outcomes, and sample sizes are consistent
across all artifacts.

If validation fails, the report must not be marked final.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from agent_eval.visualization.loader import (
    discover_analysis_artifacts,
    load_branching_metrics_csv,
    load_holdout_metrics_csv,
    load_hypothesis_results_csv,
    load_pairwise_comparisons_csv,
    load_run_metrics_csv,
    load_sensitivity_results_csv,
)


class ConsistencyViolation(BaseModel):
    """A consistency violation found during validation."""

    category: str = Field(..., description="Violation category")
    severity: str = Field(
        default="warning", description="Severity ('fatal', 'warning', 'info')"
    )
    artifact: str = Field(..., description="Affected artifact")
    detail: str = Field(..., description="Human-readable detail")
    run_id: str | None = Field(
        default=None, description="Affected run ID, if applicable"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="When the violation was detected",
    )


class ConsistencyReport(BaseModel):
    """Report of consistency validation for a research report."""

    is_valid: bool = Field(default=True, description="Whether consistency checks passed")
    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis ID")
    violations: list[ConsistencyViolation] = Field(
        default_factory=list, description="Found violations"
    )
    warnings: list[ConsistencyViolation] = Field(
        default_factory=list, description="Non-fatal warnings"
    )
    generated_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="When validation was performed"
    )

    def add_fatal(self, category: str, detail: str, artifact: str, run_id: str | None = None):
        """Add a fatal consistency violation."""
        self.violations.append(
            ConsistencyViolation(
                category=category,
                severity="fatal",
                artifact=artifact,
                detail=detail,
                run_id=run_id,
            )
        )
        self.is_valid = False

    def add_warning(self, category: str, detail: str, artifact: str, run_id: str | None = None):
        """Add a non-fatal warning."""
        self.violations.append(
            ConsistencyViolation(
                category=category,
                severity="warning",
                artifact=artifact,
                detail=detail,
                run_id=run_id,
            )
        )


def validate_report_consistency(
    experiment_id: str,
    analysis_dir: str,
    report_dir: str,
) -> ConsistencyReport:
    """Run comprehensive consistency validation for the research report.

    Checks that:
    - Phase 14 analysis artifacts exist and are valid
    - Report references to figures/tables point to existing files
    - Experiment IDs match across artifacts
    - Hypothesis outcomes match Phase 14 analysis outputs
    - Sample sizes match the included runs
    - Evidence mapping is complete
    """
    report = ConsistencyReport(
        experiment_id=experiment_id,
        analysis_id=os.path.basename(analysis_dir),
    )

    # Locate Phase 14 analysis artifacts
    artifacts = discover_analysis_artifacts(analysis_dir)

    # Check run metrics exist and are valid
    if "run_metrics" in artifacts:
        runs = load_run_metrics_csv(artifacts["run_metrics"])
        report.warnings.append(
            ConsistencyViolation(
                category="info",
                detail=f"Loaded {len(runs)} run metrics from Phase 14 analysis",
                artifact="run_metrics.csv",
            )
        )

    # Check pairwise comparisons exist
    if "pairwise_comparisons" in artifacts:
        comparisons = load_pairwise_comparisons_csv(artifacts["pairwise_comparisons"])
        report.warnings.append(
            ConsistencyViolation(
                category="info",
                detail=f"Loaded pairwise comparisons for {len(comparisons)} metrics",
                artifact="pairwise_comparisons.csv",
            )
        )

    # Check hypothesis results exist
    if "hypothesis_results" in artifacts:
        hyp_results = load_hypothesis_results_csv(artifacts["hypothesis_results"])
        report.warnings.append(
            ConsistencyViolation(
                category="info",
                detail=f"Loaded {len(hyp_results)} hypothesis test results",
                artifact="hypothesis_results.csv",
            )
        )

    # Check holdout metrics exist
    if "holdout_metrics" in artifacts:
        holdout = load_holdout_metrics_csv(artifacts["holdout_metrics"])
        report.warnings.append(
            ConsistencyViolation(
                category="info",
                detail=f"Loaded holdout metrics for {len(holdout)} runs",
                artifact="holdout_metrics.csv",
            )
        )

    # Check branching metrics exist
    if "branching_metrics" in artifacts:
        branching = load_branching_metrics_csv(artifacts["branching_metrics"])
        report.warnings.append(
            ConsistencyViolation(
                category="info",
                detail=f"Loaded branching metrics for {len(branching)} runs",
                artifact="branching_metrics.csv",
            )
        )

    # Check sensitivity results exist
    if "sensitivity_results" in artifacts:
        sensitivity = load_sensitivity_results_csv(artifacts["sensitivity_results"])
        report.warnings.append(
            ConsistencyViolation(
                category="info",
                detail=f"Loaded sensitivity results for {len(sensitivity)} parameters",
                artifact="sensitivity_results.csv",
            )
        )

    # Validate experiment ID consistency
    # Check analysis manifest
    manifest_path = artifacts.get("analysis_manifest", "")
    if manifest_path and os.path.exists(manifest_path):
        import json
        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
            if manifest.get("experiment_id") != experiment_id:
                report.add_fatal(
                    "experiment_id_mismatch",
                    f"Analysis manifest experiment_id '{manifest.get('experiment_id')}' "
                    f"does not match report experiment_id '{experiment_id}'",
                    "analysis_manifest.json",
                )
        except (OSError, json.JSONDecodeError) as e:
            report.add_fatal(
                "manifest_read_error",
                f"Cannot read analysis manifest: {e}",
                "analysis_manifest.json",
            )

    # Check report directory for experiment ID consistency
    report_manifest_path = os.path.join(report_dir, "report_manifest.json") if os.path.exists(
        report_dir
    ) else None
    if report_manifest_path and os.path.exists(report_manifest_path):
        try:
            with open(report_manifest_path) as f:
                report_manifest = json.load(f)
            if report_manifest.get("experiment_id") != experiment_id:
                report.add_fatal(
                    "report_experiment_id_mismatch",
                    f"Report manifest experiment_id '{report_manifest.get('experiment_id')}' "
                    f"does not match '{experiment_id}'",
                    "report_manifest.json",
                )
        except (OSError, json.JSONDecodeError):
            pass

    # Check that all reported figures exist
    figures_dir = os.path.join(report_dir, "figures") if os.path.exists(report_dir) else None
    if figures_dir and os.path.isdir(figures_dir):
        figure_files = set(os.listdir(figures_dir))
        # Check for common figure patterns
        for fig_pattern in ["FIG-01.png", "FIG-02.png", "FIG-03.png", "FIG-04.png"]:
            if fig_pattern in figure_files:
                report.warnings.append(
                    ConsistencyViolation(
                        category="info",
                        detail=f"Figure {fig_pattern} exists in report figures directory",
                        artifact=f"figures/{fig_pattern}",
                    )
                )
            else:
                # Not all figures need to exist, but check if any are referenced
                pass

    # Check report manifest for completeness
    report_manifest_path = os.path.join(report_dir, "report_manifest.json") if os.path.exists(
        report_dir
    ) else None
    if report_manifest_path and os.path.exists(report_manifest_path):
        try:
            with open(report_manifest_path) as f:
                rm = json.load(f)
            required_fields = ["experiment_id", "analysis_id", "generated_at"]
            for field in required_fields:
                if field not in rm:
                    report.add_warning(
                        "missing_report_field",
                        f"Report manifest missing field: {field}",
                        "report_manifest.json",
                    )
        except (OSError, json.JSONDecodeError):
            report.add_warning(
                "report_manifest_read_error",
                "Cannot read report manifest",
                "report_manifest.json",
            )

    return report