"""Load frozen raw experimental data for Phase 14 analysis.

Reads from experiments/<experiment_id>/raw/ and produces validated
run-level data structures. Does not mutate underlying data.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class RawDataHash(BaseModel):
    """Hash of raw data inputs for integrity verification."""

    hash: str = Field(..., description="SHA256 hash of concatenated raw inputs")
    components: dict[str, str] = Field(
        ..., description="Per-component hashes"
    )
    generated_at: str = Field(
        ..., description="ISO timestamp when hash was generated"
    )


class ExclusionRecord(BaseModel):
    """Record of an excluded run."""

    run_id: str = Field(..., description="Run identifier")
    reason: str = Field(..., description="Exclusion reason")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO timestamp of exclusion decision",
    )


class RawExperimentData(BaseModel):
    """Validated raw experiment data container."""

    experiment_id: str = Field(..., description="Experiment identifier")
    run_records: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Run records keyed by run_id",
    )
    failure_records: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Failure records keyed by failure_id",
    )
    family_records: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Failure family records keyed by family_id",
    )
    reproducibility_records: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Reproducibility records keyed by run_id",
    )
    holdout_results: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Holdout test results keyed by run_id",
    )
    branch_accounting: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Branch accounting records keyed by run_id",
    )
    discovery_curves: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Discovery curve data keyed by run_id",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Experiment metadata",
    )

    @field_validator(
        "run_records",
        "failure_records",
        "family_records",
        "reproducibility_records",
        "holdout_results",
        "branch_accounting",
        "discovery_curves",
        mode="before",
    )
    @classmethod
    def _ensure_dict(cls, v):
        return v if isinstance(v, dict) else {}


def compute_raw_data_hash(
    raw_dir: str,
    filenames: tuple[str, ...] = (
        "runs.csv",
        "failures.csv",
        "families.csv",
        "reproducibility.csv",
        "discovery_curves.csv",
        "branch_accounting.csv",
        "holdout_results.csv",
    ),
) -> RawDataHash:
    """Compute SHA256 hash across raw CSV/JSONL inputs.

    Hashes actual content, not file paths.
    """
    hasher = hashlib.sha256()
    components: dict[str, str] = {}

    for fname in filenames:
        fpath = os.path.join(raw_dir, fname)
        if os.path.exists(fpath):
            m = hashlib.sha256()
            with open(fpath, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    m.update(chunk)
            components[fname] = m.hexdigest()
            hasher.update(m.digest() + fname.encode())
        else:
            components[fname] = ""

    return RawDataHash(
        hash=hasher.hexdigest(),
        components=components,
        generated_at=datetime.now(UTC).isoformat(),
    )


def discover_raw_files(raw_dir: str) -> dict[str, str]:
    """Discover and categorize raw data files in the raw directory.

    Returns a mapping of file basename to full path.
    """
    result: dict[str, str] = {}
    if not os.path.isdir(raw_dir):
        return result

    for fname in os.listdir(raw_dir):
        fpath = os.path.join(raw_dir, fname)
        if os.path.isfile(fpath):
            result[fname] = fpath
    return result


def load_runs_from_csv(csv_path: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Load run records from a CSV file.

    Expected columns based on ExperimentRun serialization.
    Returns (dict keyed by run_id, list of duplicate run_ids).
    """
    runs: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    if not os.path.exists(csv_path):
        return runs, duplicates

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_id = row.get("run_id", "")
            if run_id:
                if run_id in runs:
                    duplicates.append(run_id)
                runs[run_id] = dict(row)
    return runs, duplicates


def load_jsonl_records(jsonl_path: str) -> dict[str, dict[str, Any]]:
    """Load records from a JSONL file.

    Returns dict keyed by the record's internal id field.
    """
    records: dict[str, dict[str, Any]] = {}
    if not os.path.exists(jsonl_path):
        return records

    with open(jsonl_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                # Use the first meaningful id field
                for id_key in ("failure_id", "family_id", "run_id", "candidate_id"):
                    if id_key in record:
                        records[record[id_key]] = record
                        break
                else:
                    # Use line number as fallback key
                    records[f"line_{len(records)}"] = record
            except json.JSONDecodeError:
                continue
    return records


def validate_run_id_uniqueness(duplicates: list[str]) -> tuple[bool, list[str]]:
    """Check for duplicate run IDs.

    Returns (is_valid, list_of_duplicate_ids).
    """
    return len(duplicates) == 0, duplicates


def load_experiment_data(raw_dir: str) -> RawExperimentData:
    """Load and validate raw experiment data from the standard directory.

    Reads from: experiments/<experiment_id>/raw/
    """
    runs: dict[str, dict[str, Any]] = {}
    failures: dict[str, dict[str, Any]] = {}
    families: dict[str, dict[str, Any]] = {}
    reproducibility: dict[str, dict[str, Any]] = {}
    holdout: dict[str, dict[str, Any]] = {}
    branch_acct: dict[str, dict[str, Any]] = {}
    discovery_curves: dict[str, dict[str, Any]] = {}
    metadata: dict[str, Any] = {}

    # Load runs.csv
    runs_csv = os.path.join(raw_dir, "runs.csv")
    runs, duplicates = load_runs_from_csv(runs_csv)

    # Load other JSONL files
    failures_jsonl = os.path.join(raw_dir, "failures.csv")
    failures = load_jsonl_records(failures_jsonl)

    families_jsonl = os.path.join(raw_dir, "families.csv")
    families = load_jsonl_records(families_jsonl)

    repro_jsonl = os.path.join(raw_dir, "reproducibility.csv")
    reproducibility = load_jsonl_records(repro_jsonl)

    holdout_jsonl = os.path.join(raw_dir, "holdout_results.csv")
    holdout = load_jsonl_records(holdout_jsonl)

    branch_jsonl = os.path.join(raw_dir, "branch_accounting.csv")
    branch_acct = load_jsonl_records(branch_jsonl)

    curves_jsonl = os.path.join(raw_dir, "discovery_curves.csv")
    discovery_curves = load_jsonl_records(curves_jsonl)

    # Load metadata if exists
    metadata_path = os.path.join(raw_dir, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    # Validate run ID uniqueness
    is_valid_uniqueness, dup_list = validate_run_id_uniqueness(duplicates)
    if not is_valid_uniqueness:
        import warnings
        warnings.warn(
            f"Duplicate run IDs found: {dup_list}",
            stacklevel=2,
        )

    return RawExperimentData(
        experiment_id=os.path.basename(raw_dir),
        run_records=runs,
        failure_records=failures,
        family_records=families,
        reproducibility_records=reproducibility,
        holdout_results=holdout,
        branch_accounting=branch_acct,
        discovery_curves=discovery_curves,
        metadata=metadata,
    )