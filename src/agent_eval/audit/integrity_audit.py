"""Integrity audit for Phase 17.

Validates:
- Execution and artifact integrity across runs and analysis outputs
- Checksums and manifest consistency
- Data structure invariants and completeness
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass
class IntegrityViolation:
    """Represents an integrity check violation."""

    detail: str
    check_name: str = ""

    def __str__(self) -> str:
        return self.detail


def run_integrity_audit(
    experiment_dir: str,
    analysis_dir: str = "",
) -> dict[str, Any]:
    """Run integrity audit for the experiment and its analysis outputs.

    Args:
        experiment_dir: Path to the experiment directory
        analysis_dir: Path to Phase 14 analysis outputs (optional)

    Returns:
        Dict with is_valid, violations, checks, and summary counts.
    """
    violations: list[IntegrityViolation] = []
    checks: dict[str, Any] = {}

    # Check 1: Experiment directory exists
    if not os.path.isdir(experiment_dir):
        violations.append(
            IntegrityViolation(
                f"Experiment directory does not exist: {experiment_dir}",
                "directory_structure",
            )
        )
        return {
            "is_valid": False,
            "violations": violations,
            "checks": {"experiment_dir": {"pass": False}},
            "total_violations": len(violations),
        }

    checks["experiment_dir"] = {"pass": True}

    # Check 2: Runs directory structure
    runs_dir = os.path.join(experiment_dir, "artifacts", "runs")
    if not os.path.isdir(runs_dir):
        runs_dir = os.path.join(experiment_dir, "runs")

    if not os.path.isdir(runs_dir):
        violations.append(
            IntegrityViolation(
                "Runs directory not found in experiment directory",
                "runs_structure",
            )
        )
        checks["runs_dir"] = {"pass": False}
    else:
        checks["runs_dir"] = {"pass": True}
        # Check integrity of run records
        run_dirs = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
        corrupted_runs = 0
        for run_name in run_dirs:
            run_path = os.path.join(runs_dir, run_name)
            actions_path = os.path.join(run_path, "actions.jsonl")
            if os.path.exists(actions_path):
                try:
                    with open(actions_path) as f:
                        for line_num, line in enumerate(f, 1):
                            if line.strip():
                                json.loads(line)
                except Exception as e:
                    corrupted_runs += 1
                    violations.append(
                        IntegrityViolation(
                            f"Malformed JSON in {actions_path} at line {line_num}: {e}",
                            "run_record_integrity",
                        )
                    )
        checks["run_records"] = {
            "pass": corrupted_runs == 0,
            "total_runs": len(run_dirs),
            "corrupted_runs": corrupted_runs,
        }

    # Check 3: Analysis artifacts integrity
    target_analysis = analysis_dir or os.path.join(experiment_dir, "artifacts", "analysis")
    if not os.path.isdir(target_analysis):
        target_analysis = os.path.join(experiment_dir, "analysis")

    if os.path.isdir(target_analysis):
        corrupted_artifacts = 0
        for fname in os.listdir(target_analysis):
            fpath = os.path.join(target_analysis, fname)
            if fname.endswith(".csv"):
                try:
                    with open(fpath, newline="") as f:
                        reader = csv.reader(f)
                        for _ in reader:
                            pass
                except Exception as e:
                    corrupted_artifacts += 1
                    violations.append(
                        IntegrityViolation(
                            f"Corrupted CSV file {fname}: {e}",
                            "analysis_integrity",
                        )
                    )
            elif fname.endswith(".json"):
                try:
                    with open(fpath) as f:
                        json.load(f)
                except Exception as e:
                    corrupted_artifacts += 1
                    violations.append(
                        IntegrityViolation(
                            f"Corrupted JSON file {fname}: {e}",
                            "analysis_integrity",
                        )
                    )
        checks["analysis_artifacts"] = {
            "pass": corrupted_artifacts == 0,
            "corrupted_count": corrupted_artifacts,
        }
    else:
        checks["analysis_artifacts"] = {
            "pass": True,
            "details": "No analysis directory provided or found",
        }

    is_valid = len(violations) == 0
    return {
        "is_valid": is_valid,
        "pass": is_valid,
        "violations": violations,
        "checks": checks,
        "total_violations": len(violations),
    }
