"""Integrity validation for Phase 15 visualization layer.

Ensures that visualization data originates from valid Phase 14 analysis
outputs and experiment artifacts. Prevents generating polished visualizations
from corrupted or inconsistent analysis data.

Principles:
- Validate before visualizing
- Fail fast with clear errors
- Never silently drop invalid data
- Preserve data lineage for auditability
"""

from __future__ import annotations

import hashlib
import os
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from agent_eval.visualization.loader import (
    discover_analysis_artifacts,
    load_analysis_manifest,
    load_branching_metrics_csv,
    load_holdout_metrics_csv,
    load_hypothesis_results_csv,
    load_pairwise_comparisons_csv,
    load_run_metrics_csv,
    load_sensitivity_results_csv,
)


class IntegrityViolation(BaseModel):
    """A detected integrity violation."""

    category: str = Field(..., description="Violation category")
    severity: str = Field(
        ..., description="Severity ('fatal', 'warning', 'info')"
    )
    artifact: str = Field(
        ..., description="Affected artifact name"
    )
    detail: str = Field(..., description="Human-readable detail")
    run_id: str | None = Field(
        default=None, description="Affected run ID, if applicable"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="When the violation was detected",
    )


class IntegrityReport(BaseModel):
    """Report of integrity validation for a visualization run."""

    is_valid: bool = Field(default=True, description="Whether validation passed")
    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis ID")
    violations: list[IntegrityViolation] = Field(
        default_factory=list, description="Detected violations"
    )
    warnings: list[IntegrityViolation] = Field(
        default_factory=list, description="Non-fatal warnings"
    )
    hash_verified: bool = Field(
        default=False, description="Raw-data hash verified"
    )
    manifest_verified: bool = Field(
        default=False, description="Analysis manifest verified"
    )
    generated_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="When validation was performed"
    )

    def add_fatal(self, category: str, detail: str, artifact: str, run_id: str | None = None):
        """Add a fatal integrity violation."""
        self.violations.append(
            IntegrityViolation(
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
            IntegrityViolation(
                category=category,
                severity="warning",
                artifact=artifact,
                detail=detail,
                run_id=run_id,
            )
        )


def compute_sha256(filepath: str) -> str:
    """Compute SHA256 hash of a file's contents."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_data_hash(
    artifacts: dict[str, str],
    expected_hash: str,
) -> bool:
    """Verify that raw data hash matches analyzed outputs.

    Compares the hash recorded in the analysis manifest against
    recomputed hashes of the raw input files.
    """
    if not expected_hash:
        return False

    # Check common raw data files
    raw_files = [
        "runs.csv",
        "failures.csv",
        "families.csv",
        "reproducibility.csv",
        "discovery_curves.csv",
        "branch_accounting.csv",
        "holdout_results.csv",
    ]

    for fname in raw_files:
        fpath = os.path.join(
            os.path.dirname(next(iter(artifacts.values())) if artifacts else ""),
            fname,
        )
        if os.path.exists(fpath):
            actual_hash = compute_sha256(fpath)
            if actual_hash != expected_hash:
                return False
    return True


def _get_val(obj: Any, key: str) -> Any:
    """Helper to get a value from either a dict or an object attribute."""
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _has_val(obj: Any, key: str) -> bool:
    """Helper to check if a key exists in a dict or as an attribute."""
    if isinstance(obj, dict):
        return key in obj
    return hasattr(obj, key)


def validate_run_metrics_schema(
    runs: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate the schema of run metrics data.

    Checks for required columns, valid values, and consistency.
    """
    errors: list[str] = []

    if not runs:
        errors.append("No run metrics data found")
        return False, errors

    # Check for required fields in first run
    first_run_id = next(iter(runs))
    first_run = runs[first_run_id]

    required_fields = ["run_id", "method", "seed", "tokens_used"]
    for field in required_fields:
        if not _has_val(first_run, field):
            errors.append(f"Missing required field '{field}' in run metrics")

    # Validate values
    for run_id, run_data in runs.items():
        # tokens_used should be non-negative
        tokens = _get_val(run_data, "tokens_used")
        if tokens is not None and tokens < 0:
            errors.append(f"Run {run_id}: tokens_used ({tokens}) is negative")

        # VFF should be non-negative if present
        vff = _get_val(run_data, "vff")
        if vff is not None and vff < 0:
            errors.append(f"Run {run_id}: VFF ({vff}) is negative")

        # FDE should be non-negative if present
        fde = _get_val(run_data, "fde")
        if fde is not None and fde < 0:
            errors.append(f"Run {run_id}: FDE ({fde}) is negative")

        # CPF should be non-negative if present
        cpf = _get_val(run_data, "cpf")
        if cpf is not None and cpf < 0:
            errors.append(f"Run {run_id}: CPF ({cpf}) is negative")

    return len(errors) == 0, errors


def validate_pairwise_comparisons_schema(
    comparisons_by_metric: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate pairwise comparisons schema."""
    errors: list[str] = []

    for metric_name, comparisons in comparisons_by_metric.items():
        if not comparisons:
            errors.append(f"No comparisons found for metric '{metric_name}'")
            continue

        for i, comp in enumerate(comparisons):
            # Check required fields
            required = ["method_a", "method_b", "p_value", "effect_size"]
            for field in required:
                val = _get_val(comp, field)
                if val is None:
                    errors.append(
                        f"Comparison {i} for metric '{metric_name}': missing '{field}'"
                    )

            # p_value should be in [0, 1]
            p_val = _get_val(comp, "p_value")
            if p_val is not None and (p_val < 0 or p_val > 1):
                errors.append(
                    f"Comparison {i} for metric '{metric_name}': p_value "
                    f"({p_val}) out of [0,1] range"
                )

            # effect_size should be in [-1, 1] for Cliff's delta
            es = _get_val(comp, "effect_size")
            if es is not None and (es < -1 or es > 1):
                errors.append(
                    f"Comparison {i} for metric '{metric_name}': effect_size "
                    f"({es}) out of [-1,1] range"
                )

    return len(errors) == 0, errors


def validate_hypothesis_results_schema(
    hypothesis_results: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate hypothesis test results schema."""
    errors: list[str] = []

    for hyp_id, result in hypothesis_results.items():
        # required fields
        required = ["test_name", "p_value", "direction", "evidence_status"]
        for field in required:
            if not _has_val(result, field):
                errors.append(f"Hypothesis {hyp_id}: missing '{field}'")

        # evidence_status must be in vocabulary
        ev_status = _get_val(result, "evidence_status") or ""
        if ev_status not in ("SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"):
            errors.append(
                f"Hypothesis {hyp_id}: invalid evidence_status "
                f"'{ev_status}'"
            )

        # direction must be valid
        direction = _get_val(result, "direction") or ""
        if direction not in ("POSITIVE", "NEGATIVE", "NO_DIFFERENCE"):
            errors.append(
                f"Hypothesis {hyp_id}: invalid direction "
                f"'{direction}'"
            )

    return len(errors) == 0, errors


def validate_holdout_metrics_schema(
    holdout_results: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate holdout metrics schema."""
    errors: list[str] = []

    for run_id, result in holdout_results.items():
        # TSR should be in [0, 1] if present
        tsr = _get_val(result, "tsr")
        if tsr is not None and (tsr < 0 or tsr > 1):
            errors.append(
                f"Holdout run {run_id}: TSR ({tsr}) out of [0,1] range"
            )

        # families_tested and families_transferred should be non-negative
        ft = _get_val(result, "families_tested")
        if ft is not None and ft < 0:
            errors.append(f"Holdout run {run_id}: families_tested ({ft}) negative")

        ft2 = _get_val(result, "families_transferred")
        if ft2 is not None and ft2 < 0:
            errors.append(f"Holdout run {run_id}: families_transferred ({ft2}) negative")

    return len(errors) == 0, errors


def validate_branching_metrics_schema(
    branching_results: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate branching metrics schema."""
    errors: list[str] = []

    for run_id, result in branching_results.items():
        # total_branching_cost = branch_tokens + snapshot_tokens
        bc = _get_val(result, "total_branching_cost")
        bp = _get_val(result, "branch_tokens")
        sp = _get_val(result, "snapshot_tokens")

        # If all three are present, verify consistency
        if bc is not None and bp is not None and sp is not None and bc != bp + sp:
            errors.append(
                f"Branching run {run_id}: total_branching_cost ({bc}) "
                f"!= branch_tokens ({bp}) + snapshot_tokens ({sp})"
            )

        # PTR should be in [0, 1] if present
        ptr = _get_val(result, "prefix_token_reduction")
        if ptr is not None and (ptr < 0 or ptr > 1):
            errors.append(
                f"Branching run {run_id}: prefix_token_reduction ({ptr}) "
                f"out of [0,1] range"
            )

        # BTCR has no explicit range constraint but should be reasonable
        btc = _get_val(result, "total_branch_cost_reduction")
        if btc is not None and abs(btc) > 100:
            errors.append(
                f"Branching run {run_id}: total_branch_cost_reduction ({btc}) "
                f"appears unreasonably large"
            )

        # RTR should be in [0, 1] if present
        rtr = _get_val(result, "redundant_test_rate")
        if rtr is not None and (rtr < 0 or rtr > 1):
            errors.append(
                f"Branching run {run_id}: redundant_test_rate ({rtr}) "
                f"out of [0,1] range"
            )

    return len(errors) == 0, errors


def run_visualization_integrity_check(
    experiment_id: str,
    analysis_dir: str,
    raw_data_hash: str | None = None,
) -> IntegrityReport:
    """Run complete integrity validation for visualization layer.

    This is the gatekeeper - if fatal errors are found, visualization
    must STOP and report the integrity report.

    Args:
        experiment_id: The experiment identifier
        analysis_dir: Path to Phase 14 analysis outputs
        raw_data_hash: Expected SHA256 hash of raw inputs (from manifest)

    Returns:
        IntegrityReport - must be checked.is_valid before proceeding
    """
    report = IntegrityReport(
        experiment_id=experiment_id,
        analysis_id=os.path.basename(analysis_dir),
    )

    # Locate artifacts
    artifacts = discover_analysis_artifacts(analysis_dir)

    # Verify analysis manifest
    manifest_path = artifacts.get("analysis_manifest", "")
    if manifest_path and os.path.exists(manifest_path):
        manifest = load_analysis_manifest(manifest_path)
        report.manifest_verified = (
            manifest.get("experiment_id") == experiment_id
        )
        if not report.manifest_verified:
            report.add_warning(
                "manifest_mismatch",
                "Analysis manifest experiment_id does not match",
                "analysis_manifest",
            )

    # Verify raw data hash
    if raw_data_hash:
        report.hash_verified = verify_data_hash(artifacts, raw_data_hash)
        if not report.hash_verified:
            report.add_warning(
                "data_hash_mismatch",
                "Raw data hash does not match analyzed outputs",
                "raw_data",
            )

    # Validate run metrics
    if "run_metrics" in artifacts:
        runs = load_run_metrics_csv(artifacts["run_metrics"])
        schema_valid, schema_errors = validate_run_metrics_schema(runs)
        if not schema_valid:
            for err in schema_errors:
                report.add_fatal("run_metrics_schema", err, "run_metrics.csv")

        # If valid, add runs to report data (for later use)
        # Note: we don't store the runs in the report, just validate

    # Validate pairwise comparisons
    if "pairwise_comparisons" in artifacts:
        comparisons = load_pairwise_comparisons_csv(artifacts["pairwise_comparisons"])
        schema_valid, schema_errors = validate_pairwise_comparisons_schema(comparisons)
        if not schema_valid:
            for err in schema_errors:
                report.add_fatal("pairwise_comparisons_schema", err, "pairwise_comparisons.csv")

    # Validate hypothesis results
    if "hypothesis_results" in artifacts:
        hyp_results = load_hypothesis_results_csv(artifacts["hypothesis_results"])
        schema_valid, schema_errors = validate_hypothesis_results_schema(hyp_results)
        if not schema_valid:
            for err in schema_errors:
                report.add_fatal("hypothesis_results_schema", err, "hypothesis_results.csv")

    # Validate holdout metrics
    if "holdout_metrics" in artifacts:
        holdout = load_holdout_metrics_csv(artifacts["holdout_metrics"])
        schema_valid, schema_errors = validate_holdout_metrics_schema(holdout)
        if not schema_valid:
            for err in schema_errors:
                report.add_fatal("holdout_metrics_schema", err, "holdout_metrics.csv")

    # Validate branching metrics
    if "branching_metrics" in artifacts:
        branching = load_branching_metrics_csv(artifacts["branching_metrics"])
        schema_valid, schema_errors = validate_branching_metrics_schema(branching)
        if not schema_valid:
            for err in schema_errors:
                report.add_fatal("branching_metrics_schema", err, "branching_metrics.csv")

    # Validate sensitivity results
    if "sensitivity_results" in artifacts:
        sensitivity = load_sensitivity_results_csv(artifacts["sensitivity_results"])
        # Basic check: ensure we can load it
        for param, points in sensitivity.items():
            if not points:
                report.add_warning(
                    "empty_sensitivity",
                    f"Sensitivity parameter '{param}' has no data points",
                    "sensitivity_results.csv",
                )

    # Check for duplicate run IDs
    if "run_metrics" in artifacts:
        runs = load_run_metrics_csv(artifacts["run_metrics"])
        run_ids = list(runs.keys())
        if len(run_ids) != len(set(run_ids)):
            report.add_fatal(
                "duplicate_run_ids",
                "Duplicate run IDs found in run_metrics.csv",
                "run_metrics.csv",
            )

    return report