"""Loader for Phase 14 analysis outputs consumed by Phase 15 visualizations.

Reads Phase 14 analysis artifacts from experiments/<experiment_id>/analysis/
and produces validated data structures for visualization consumption.

Key responsibilities:
- Load CSV and JSON outputs from Phase 14 analysis
- Validate data integrity and schema
- Provide normalized access to metric values by method/seed
- Compute presentation-friendly transformations
- Never mutate original analysis data
"""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from typing import Any

from pydantic import BaseModel, Field

from agent_eval.analysis.models import ExclusionRecord


class RunMetric(BaseModel):
    """Normalized run-level metric for visualization."""

    run_id: str = Field(..., description="Run identifier")
    method: str = Field(..., description="Evaluation method")
    seed: str = Field(..., description="Random seed")
    vff: int | None = Field(default=None, description="Validated failure families")
    fde: float | None = Field(default=None, description="Family discovery efficiency")
    cpf: float | None = Field(default=None, description="Cost per family")
    ttff: float | None = Field(default=None, description="Time to first family")
    auf_dc: float | None = Field(default=None, description="AUFDC value")
    tokens_used: int | None = Field(default=None, description="Total tokens used")
    executions: int | None = Field(default=None, description="Execution count")
    pointer_tokens: int | None = Field(
        default=None, description="Prefix tokens"
    )
    branch_tokens: int | None = Field(
        default=None, description="Branch tokens"
    )
    snapshot_tokens: int | None = Field(
        default=None, description="Snapshot tokens"
    )
    holdout_transfer_count: int | None = Field(
        default=None, description="Holdout transfer count"
    )
    branching_efficiency: float | None = Field(
        default=None, description="PTR value"
    )
    redundancy_rate: float | None = Field(
        default=None, description="RTR value"
    )

    @property
    def has_all_metrics(self) -> bool:
        """Check if all primary metrics are present."""
        return all(
            getattr(self, m) is not None
            for m in ["vff", "fde", "cpf", "ttff", "auf_dc"]
        )


class MethodComparison(BaseModel):
    """Result of a pairwise method comparison."""

    method_a: str = Field(..., description="First method")
    method_b: str = Field(..., description="Second method")
    metric: str = Field(..., description="Metric being compared")
    p_value: float | None = Field(default=None, description="Raw p-value")
    adjusted_p_value: float | None = Field(
        default=None, description="Holm-corrected p-value"
    )
    effect_size: float | None = Field(
        default=None, description="Cliff's delta"
    )
    effect_size_measure: str = Field(
        default="Cliff's delta", description="Effect size measure"
    )
    direction: str = Field(
        default="NO_DIFFERENCE",
        description="POSITIVE/NEGATIVE/NO_DIFFERENCE",
    )
    evidence_status: str = Field(
        default="INCONCLUSIVE",
        description="SUPPORTED/NOT_SUPPORTED/INCONCLUSIVE",
    )


class HoldoutResult(BaseModel):
    """Holdout generalization result for a run."""

    run_id: str = Field(..., description="Run identifier")
    families_tested: int | None = Field(default=None, description="Families tested")
    families_transferred: int | None = Field(
        default=None, description="Families transferred"
    )
    tsr: float | None = Field(default=None, description="Transfer success rate")
    successful_transfers: int | None = Field(
        default=None, description="Successful transfers"
    )


class BranchingResult(BaseModel):
    """Branching efficiency result for a run."""

    run_id: str = Field(..., description="Run identifier")
    prefix_tokens: int | None = Field(default=None, description="Prefix tokens")
    branch_tokens: int | None = Field(default=None, description="Branch tokens")
    snapshot_tokens: int | None = Field(default=None, description="Snapshot tokens")
    total_branching_cost: int | None = Field(
        default=None, description="branch_tokens + snapshot_tokens"
    )
    branch_savings: int | None = Field(
        default=None, description="unbranched_prefix_cost - total_branching_cost"
    )
    prefix_token_reduction: float | None = Field(
        default=None, description="PTR value"
    )
    total_branch_cost_reduction: float | None = Field(
        default=None, description="BTCR value"
    )
    redundant_test_rate: float | None = Field(
        default=None, description="RTR value"
    )


class SensitivityPoint(BaseModel):
    """A point in sensitivity analysis."""

    parameter: str = Field(..., description="Parameter name")
    value: Any = Field(..., description="Parameter value")
    metric: str = Field(..., description="Metric name")
    metric_value: Any = Field(..., description="Metric value at this setting")
    status: str = Field(
        default="evaluated", description="evaluated/NOT_RUN"
    )


class VisualizationData(BaseModel):
    """Container for all data needed by visualizations."""

    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis ID")
    runs: dict[str, RunMetric] = Field(
        default_factory=dict, description="Run-level metrics keyed by run_id"
    )
    method_comparisons: dict[str, list[MethodComparison]] = Field(
        default_factory=dict, description="Pairwise comparisons by metric"
    )
    holdout_results: dict[str, HoldoutResult] = Field(
        default_factory=dict, description="Holdout results keyed by run_id"
    )
    branching_results: dict[str, BranchingResult] = Field(
        default_factory=dict, description="Branching results keyed by run_id"
    )
    sensitivity_points: dict[str, list[SensitivityPoint]] = Field(
        default_factory=dict, description="Sensitivity analysis points"
    )
    exclusions: list[ExclusionRecord] = Field(
        default_factory=list, description="Excluded runs"
    )
    raw_data_hash: str = Field(
        "", description="SHA256 hash of raw inputs for integrity checking"
    )


def discover_analysis_artifacts(
    analysis_dir: str,
) -> dict[str, str]:
    """Discover Phase 14 analysis artifacts in the analysis directory.

    Returns a mapping of artifact name to full file path.
    """
    artifacts: dict[str, str] = {}
    if not os.path.isdir(analysis_dir):
        return artifacts

    for fname in os.listdir(analysis_dir):
        fpath = os.path.join(analysis_dir, fname)
        if os.path.isfile(fpath):
            # Categorize by filename patterns
            if fname.startswith("run_metrics"):
                artifacts["run_metrics"] = fpath
            elif fname.startswith("aggregate_metrics"):
                artifacts["aggregate_metrics"] = fpath
            elif fname.startswith("pairwise_comparisons"):
                artifacts["pairwise_comparisons"] = fpath
            elif fname.startswith("hypothesis_results"):
                artifacts["hypothesis_results"] = fpath
            elif fname.startswith("bootstrap_results"):
                artifacts["bootstrap_results"] = fpath
            elif fname.startswith("effect_sizes"):
                artifacts["effect_sizes"] = fpath
            elif fname.startswith("holdout_metrics"):
                artifacts["holdout_metrics"] = fpath
            elif fname.startswith("branching_metrics"):
                artifacts["branching_metrics"] = fpath
            elif fname.startswith("sensitivity_results"):
                artifacts["sensitivity_results"] = fpath
            elif fname.startswith("analysis_exclusions"):
                artifacts["analysis_exclusions"] = fpath
            elif fname == "analysis_manifest.json":
                artifacts["analysis_manifest"] = fpath
            elif fname == "raw_data_hash.txt":
                artifacts["raw_data_hash"] = fpath
            else:
                # Store any other files by basename
                artifacts[fname] = fpath
    return artifacts


def load_run_metrics_csv(csv_path: str) -> dict[str, RunMetric]:
    """Load run-level metrics from CSV.

    Expected columns based on Phase 14 run_metrics.csv output.
    Returns dict keyed by run_id.
    """
    runs: dict[str, RunMetric] = {}
    if not os.path.exists(csv_path):
        return runs

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_id = row.get("run_id", "")
            if not run_id:
                continue

            # Parse method and seed from run_id or columns
            # Format: run:UUID or similar
            method = row.get("method", "")
            seed = row.get("seed", "")

            # Parse metrics
            vff = None
            try:
                vff = int(row.get("VFF", 0)) if row.get("VFF", "").strip() else None
            except (ValueError, TypeError):
                vff = None

            fde = None
            try:
                fde_val = row.get("FDE", "")
                fde = float(fde_val) if fde_val and fde_val.strip() else None
            except (ValueError, TypeError):
                fde = None

            cpf = None
            try:
                cpf_val = row.get("CPF", "")
                cpf = float(cpf_val) if cpf_val and cpf_val.strip() else None
            except (ValueError, TypeError):
                cpf = None

            ttff = None
            try:
                ttff_val = row.get("TTFF", "")
                ttff = float(ttff_val) if ttff_val and ttff_val.strip() else None
            except (ValueError, TypeError):
                ttff = None

            auf_dc = None
            try:
                auf_dc_val = row.get("AUFDC", "")
                auf_dc = float(auf_dc_val) if auf_dc_val and auf_dc_val.strip() else None
            except (ValueError, TypeError):
                auf_dc = None

            tokens_used = None
            try:
                tut_val = row.get("tokens_used", "")
                tokens_used = int(tut_val) if tut_val and tut_val.strip() else None
            except (ValueError, TypeError):
                tokens_used = None

            executions = None
            try:
                exec_val = row.get("executions", "")
                executions = int(exec_val) if exec_val and exec_val.strip() else None
            except (ValueError, TypeError):
                executions = None

            pointer_tokens = None
            try:
                pt_val = row.get("pointer_tokens", "")
                pointer_tokens = int(pt_val) if pt_val and pt_val.strip() else None
            except (ValueError, TypeError):
                pointer_tokens = None

            branch_tokens = None
            try:
                bt_val = row.get("branch_tokens", "")
                branch_tokens = int(bt_val) if bt_val and bt_val.strip() else None
            except (ValueError, TypeError):
                branch_tokens = None

            snapshot_tokens = None
            try:
                st_val = row.get("snapshot_tokens", "")
                snapshot_tokens = int(st_val) if st_val and st_val.strip() else None
            except (ValueError, TypeError):
                snapshot_tokens = None

            holdout_transfer_count = None
            try:
                htc_val = row.get("holdout_transfer_count", "")
                holdout_transfer_count = (
                    int(htc_val) if htc_val and htc_val.strip() else None
                )
            except (ValueError, TypeError):
                holdout_transfer_count = None

            branching_efficiency = None
            try:
                be_val = row.get("branching_efficiency", "")
                branching_efficiency = (
                    float(be_val) if be_val and be_val.strip() else None
                )
            except (ValueError, TypeError):
                branching_efficiency = None

            redundancy_rate = None
            try:
                rr_val = row.get("redundancy_rate", "")
                redundancy_rate = float(rr_val) if rr_val and rr_val.strip() else None
            except (ValueError, TypeError):
                redundancy_rate = None

            run_metric = RunMetric(
                run_id=run_id,
                method=method,
                seed=seed,
                vff=vff,
                fde=fde,
                cpf=cpf,
                ttff=ttff,
                auf_dc=auf_dc,
                tokens_used=tokens_used,
                executions=executions,
                pointer_tokens=pointer_tokens,
                branch_tokens=branch_tokens,
                snapshot_tokens=snapshot_tokens,
                holdout_transfer_count=holdout_transfer_count,
                branching_efficiency=branching_efficiency,
                redundancy_rate=redundancy_rate,
            )

            runs[run_id] = run_metric

    return runs


def load_pairwise_comparisons_csv(
    csv_path: str,
) -> dict[str, list[MethodComparison]]:
    """Load pairwise comparison results from CSV.

    Returns dict keyed by metric name, each containing list of MethodComparison.
    """
    comparisons_by_metric: dict[str, list[MethodComparison]] = defaultdict(list)
    if not os.path.exists(csv_path):
        return comparisons_by_metric

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row.get("metric", "")
            if not metric:
                continue

            comparison = MethodComparison(
                method_a=row.get("method_a", ""),
                method_b=row.get("method_b", ""),
                metric=metric,
                p_value=None if row.get("p_value", "") in ("", "NA", "None")
                else float(row["p_value"]),
                adjusted_p_value=None
                if row.get("adjusted_p_value", "") in ("", "NA", "None")
                else float(row["adjusted_p_value"]),
                effect_size=None
                if row.get("effect_size", "") in ("", "NA", "None")
                else float(row["effect_size"]),
                effect_size_measure=row.get("effect_size_measure", "Cliff's delta"),
                direction=row.get("direction", "NO_DIFFERENCE"),
                evidence_status=row.get("evidence_status", "INCONCLUSIVE"),
            )

            comparisons_by_metric[metric].append(comparison)

    return comparisons_by_metric


def load_hypothesis_results_csv(csv_path: str) -> dict[str, dict]:
    """Load hypothesis test results from CSV.

    Returns dict keyed by hypothesis_id.
    """
    results: dict[str, dict] = {}
    if not os.path.exists(csv_path):
        return results

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hypothesis_id = row.get("hypothesis_id", "")
            if not hypothesis_id:
                continue

            results[hypothesis_id] = {
                "test_name": row.get("test_name", ""),
                "statistic": (
                    float(row["statistic"]) if row.get("statistic", "") not in ("", "NA")
                    else None
                ),
                "p_value": (
                    float(row["p_value"]) if row.get("p_value", "") not in ("", "NA")
                    else None
                ),
                "alpha": float(row["alpha"]) if row.get("alpha", "") not in ("", "NA") else 0.05,
                "effect_size": (
                    float(row["effect_size"]) if row.get("effect_size", "") not in ("", "NA")
                    else None
                ),
                "effect_size_measure": row.get("effect_size_measure", ""),
                "confidence_interval": row.get("confidence_interval", ""),
                "direction": row.get("direction", "NO_DIFFERENCE"),
                "evidence_status": row.get("evidence_status", "INCONCLUSIVE"),
                "adjusted_p_value": (
                    float(row["adjusted_p_value"])
                    if row.get("adjusted_p_value", "") not in ("", "NA")
                    else None
                ),
            }

    return results


def load_holdout_metrics_csv(csv_path: str) -> dict[str, HoldoutResult]:
    """Load holdout generalization metrics from CSV."""
    results: dict[str, HoldoutResult] = {}
    if not os.path.exists(csv_path):
        return results

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_id = row.get("run_id", "")
            if not run_id:
                continue

            holdout_result = HoldoutResult(
                run_id=run_id,
                families_tested=None
                if row.get("families_tested", "") in ("", "NA")
                else int(row["families_tested"]),
                families_transferred=None
                if row.get("families_transferred", "") in ("", "NA")
                else int(row["families_transferred"]),
                tsr=None
                if row.get("tsr", "") in ("", "NA")
                else float(row["tsr"]),
                successful_transfers=None
                if row.get("successful_transfers", "") in ("", "NA")
                else int(row["successful_transfers"]),
            )

            results[run_id] = holdout_result

    return results


def load_branching_metrics_csv(csv_path: str) -> dict[str, BranchingResult]:
    """Load branching metrics from CSV."""
    results: dict[str, BranchingResult] = {}
    if not os.path.exists(csv_path):
        return results

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_id = row.get("run_id", "")
            if not run_id:
                continue

            # Parse pointer_tokens as prefix_tokens
            pointer_tokens = None
            try:
                pt_val = row.get("pointer_tokens", "")
                pointer_tokens = int(pt_val) if pt_val and pt_val.strip() else None
            except (ValueError, TypeError):
                pointer_tokens = None

            branch_tokens = None
            try:
                bt_val = row.get("branch_tokens", "")
                branch_tokens = int(bt_val) if bt_val and bt_val.strip() else None
            except (ValueError, TypeError):
                branch_tokens = None

            snapshot_tokens = None
            try:
                st_val = row.get("snapshot_tokens", "")
                snapshot_tokens = int(st_val) if st_val and st_val.strip() else None
            except (ValueError, TypeError):
                snapshot_tokens = None

            total_branching_cost = None
            try:
                tbc_val = row.get("total_branching_cost", "")
                total_branching_cost = (
                    int(tbc_val) if tbc_val and tbc_val.strip() else None
                )
            except (ValueError, TypeError):
                total_branching_cost = None

            branch_savings = None
            try:
                bs_val = row.get("branch_savings", "")
                branch_savings = (
                    int(bs_val) if bs_val and bs_val.strip() else None
                )
            except (ValueError, TypeError):
                branch_savings = None

            prefix_token_reduction = None
            try:
                ptr_val = row.get("prefix_token_reduction", "")
                prefix_token_reduction = (
                    float(ptr_val) if ptr_val and ptr_val.strip() else None
                )
            except (ValueError, TypeError):
                prefix_token_reduction = None

            total_branch_cost_reduction = None
            try:
                btc_val = row.get("total_branch_cost_reduction", "")
                total_branch_cost_reduction = (
                    float(btc_val) if btc_val and btc_val.strip() else None
                )
            except (ValueError, TypeError):
                total_branch_cost_reduction = None

            redundant_test_rate = None
            try:
                rtr_val = row.get("redundant_test_rate", "")
                redundant_test_rate = (
                    float(rtr_val) if rtr_val and rtr_val.strip() else None
                )
            except (ValueError, TypeError):
                redundant_test_rate = None

            branching_result = BranchingResult(
                run_id=run_id,
                prefix_tokens=pointer_tokens,
                branch_tokens=branch_tokens,
                snapshot_tokens=snapshot_tokens,
                total_branching_cost=total_branching_cost,
                branch_savings=branch_savings,
                prefix_token_reduction=prefix_token_reduction,
                total_branch_cost_reduction=total_branch_cost_reduction,
                redundant_test_rate=redundant_test_rate,
            )

            results[run_id] = branching_result

    return results


def load_sensitivity_results_csv(csv_path: str) -> dict[str, list[SensitivityPoint]]:
    """Load sensitivity analysis results from CSV.

    Returns dict keyed by parameter name, each containing list of SensitivityPoint.
    """
    results: dict[str, list[SensitivityPoint]] = defaultdict(list)
    if not os.path.exists(csv_path):
        return results

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parameter = row.get("parameter", "")
            if not parameter:
                continue

            value = row.get("value", "")
            metric = row.get("metric", "")
            metric_value = row.get("metric_value", "")

            # Try to convert metric_value to appropriate type
            try:
                if "." in str(metric_value):
                    metric_value = float(metric_value)
                else:
                    metric_value = int(metric_value)
            except (ValueError, TypeError):
                pass

            status = row.get("status", "evaluated")

            sensitivity_point = SensitivityPoint(
                parameter=parameter,
                value=value,
                metric=metric,
                metric_value=metric_value,
                status=status,
            )

            results[parameter].append(sensitivity_point)

    # Convert defaultdict to regular dict
    return dict(results)


def load_analysis_manifest(manifest_path: str) -> dict:
    """Load the Phase 14 analysis manifest."""
    if not os.path.exists(manifest_path):
        return {}

    try:
        with open(manifest_path, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def validate_analysis_integrity(
    artifacts: dict[str, str],
) -> tuple[bool, list[str]]:
    """Validate that required Phase 14 analysis artifacts exist and are valid.

    Returns (is_valid, list_of_error_messages).
    Stops visualization if integrity fails.
    """
    errors: list[str] = []

    # Check for required artifacts
    required = ["run_metrics", "aggregate_metrics"]
    for req in required:
        if req not in artifacts:
            errors.append(f"Missing required artifact: {req}")

    # If run_metrics exists, validate it can be loaded
    if "run_metrics" in artifacts:
        try:
            # Basic check - just verify file is readable
            with open(artifacts["run_metrics"], "r") as f:
                header = f.readline().strip()
                if not header:
                    errors.append("run_metrics CSV appears empty")
        except OSError as e:
            errors.append(f"Cannot read run_metrics.csv: {e}")

    # If pairwise_comparisons exists, validate it
    if "pairwise_comparisons" in artifacts:
        try:
            with open(artifacts["pairwise_comparisons"], "r") as f:
                header = f.readline().strip()
                if not header:
                    errors.append("pairwise_comparisons CSV appears empty")
        except OSError as e:
            errors.append(f"Cannot read pairwise_comparisons.csv: {e}")

    # If analysis_manifest exists, validate it has expected fields
    if "analysis_manifest" in artifacts:
        try:
            with open(artifacts["analysis_manifest"], "r", encoding="utf-8") as f:
                manifest = json.load(f)
            if "experiment_id" not in manifest:
                errors.append("analysis_manifest.json missing experiment_id")
        except (json.JSONDecodeError, OSError):
            errors.append("analysis_manifest.json is malformed")

    return len(errors) == 0, errors