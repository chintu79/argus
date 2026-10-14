"""Data validation for Phase 14 analysis.

Validates frozen raw experimental data before metric calculation.
Stops analysis if validation fails - does not silently drop invalid data.

Data flow principle: validate before transforming.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from agent_eval.analysis.loader import (
    ExclusionRecord,
    RawExperimentData,
    validate_run_id_uniqueness,
)


class ValidationError(BaseModel):
    """A validation error found in the data."""

    category: str = Field(..., description="Error category (e.g., 'integrity', 'structure')")
    severity: str = Field(
        default="fatal", description="Severity ('fatal', 'warning', 'info')"
    )
    run_id: str | None = Field(
        default=None, description="Affected run ID, if applicable"
    )
    detail: str = Field(..., description="Human-readable error detail")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="When the error was detected",
    )


class ValidationResult(BaseModel):
    """Result of data validation."""

    is_valid: bool = Field(
        ..., description="Whether data passes all validation checks"
    )
    errors: list[ValidationError] = Field(
        default_factory=list, description="List of validation errors found"
    )
    warnings: list[ValidationError] = Field(
        default_factory=list,
        description="Non-fatal warnings that don't stop analysis",
    )
    excluded_runs: list[ExclusionRecord] = Field(
        default_factory=list,
        description="Runs excluded from analysis",
    )
    raw_data_hash: str = Field(
        "", description="Hash of raw inputs for integrity checking"
    )

    def add_error(self, category: str, detail: str, run_id: str | None = None):
        """Add a fatal validation error."""
        self.errors.append(
            ValidationError(
                category=category,
                severity="fatal",
                run_id=run_id,
                detail=detail,
            )
        )
        self.is_valid = False

    def add_warning(self, category: str, detail: str, run_id: str | None = None):
        """Add a non-fatal warning."""
        self.warnings.append(
            ValidationError(
                category=category,
                severity="warning",
                run_id=run_id,
                detail=detail,
            )
        )

    def add_exclusion(self, run_id: str, reason: str):
        """Record a run exclusion."""
        self.excluded_runs.append(
            ExclusionRecord(run_id=run_id, reason=reason)
        )
        self.add_warning("exclusion", f"Run {run_id} excluded: {reason}")


class DataIntegrityChecker:
    """Checks various aspects of data integrity for analysis."""

    @staticmethod
    def check_run_id_uniqueness(
        runs: dict[str, dict[str, Any]] | list[str],
    ) -> tuple[bool, list[str]]:
        """Check for duplicate run IDs."""
        if isinstance(runs, list):
            return validate_run_id_uniqueness(runs)
        return True, []

    @staticmethod
    def check_budget_integrity(
        runs: dict[str, dict[str, Any]],
    ) -> tuple[bool, list[ValidationError]]:
        """Check that all completed runs have valid budget info.

        Returns (is_valid, list_of_errors).
        """
        errors: list[ValidationError] = []

        for run_id, run_data in runs.items():
            status = run_data.get("status", "")
            if status in ("COMPLETED",):
                budget = run_data.get("budget_total_tokens")
                if budget is None or str(budget).strip() == "":
                    errors.append(
                        ValidationError(
                            category="budget_integrity",
                            detail=f"Run {run_id}: COMPLETED but missing budget_total_tokens",
                            run_id=run_id,
                        )
                    )

        return len(errors) == 0, errors

    @staticmethod
    def check_seed_integrity(
        runs: dict[str, dict[str, Any]],
    ) -> tuple[bool, list[ValidationError]]:
        """Check that runs have valid seed information."""
        errors: list[ValidationError] = []

        for run_id, run_data in runs.items():
            seed = run_data.get("seed", None)
            if seed is None:
                errors.append(
                    ValidationError(
                        category="seed_integrity",
                        detail=f"Run {run_id}: missing seed",
                        run_id=run_id,
                    )
                )

        return len(errors) == 0, errors

    @staticmethod
    def check_failure_references(
        runs: dict[str, dict[str, Any]],
        failures: dict[str, dict[str, Any]],
    ) -> tuple[bool, list[ValidationError]]:
        """Check that all failures reference valid runs."""
        errors: list[ValidationError] = []

        for failure_id, failure_data in failures.items():
            ref_run_id = failure_data.get("run_id", "")
            if ref_run_id and ref_run_id not in runs:
                errors.append(
                    ValidationError(
                        category="failure_reference",
                        detail=f"Failure {failure_id}: references unknown run {ref_run_id}",
                        run_id=failure_id,
                    )
                )

        return len(errors) == 0, errors

    @staticmethod
    def check_family_references(
        families: dict[str, dict[str, Any]],
        failures: dict[str, dict[str, Any]],
    ) -> tuple[bool, list[ValidationError]]:
        """Check that all families reference valid failures."""
        errors: list[ValidationError] = []

        for family_id, family_data in families.items():
            ref_failure_id = family_data.get("failure_id", "")
            if ref_failure_id and ref_failure_id not in failures:
                errors.append(
                    ValidationError(
                        category="family_reference",
                        detail=f"Family {family_id}: references unknown failure {ref_failure_id}",
                        run_id=family_id,
                    )
                )

        return len(errors) == 0, errors

    @staticmethod
    def check_holdout_references(
        holdout: dict[str, dict[str, Any]],
        families: dict[str, dict[str, Any]],
    ) -> tuple[bool, list[ValidationError]]:
        """Check that holdout results reference valid families."""
        errors: list[ValidationError] = []

        for run_id, run_holdout in holdout.items():
            for family_id in run_holdout.get("families_tested", []):
                if family_id and family_id not in families:
                    errors.append(
                        ValidationError(
                            category="holdout_reference",
                            detail=f"Holdout run {run_id}: tests family {family_id} not found in families",
                            run_id=run_id,
                        )
                    )

        return len(errors) == 0, errors

    @staticmethod
    def check_branch_accounting(
        branch_acct: dict[str, dict[str, Any]],
        runs: dict[str, dict[str, Any]],
    ) -> tuple[bool, list[ValidationError]]:
        """Check branch accounting references valid runs."""
        errors: list[ValidationError] = []

        for run_id in branch_acct:
            if run_id and run_id not in runs:
                errors.append(
                    ValidationError(
                        category="branch_reference",
                        detail=f"Branch accounting run {run_id}: run not found",
                        run_id=run_id,
                    )
                )

        return len(errors) == 0, errors

    @staticmethod
    def run_all_checks(
        data: RawExperimentData,
    ) -> ValidationResult:
        """Run all integrity checks on raw experiment data.

        Returns a ValidationResult that stops analysis if fatal errors found.
        """
        result = ValidationResult(
            is_valid=True,
            raw_data_hash=data.metadata.get("raw_data_hash", ""),
        )

        runs = data.run_records
        failures = data.failure_records
        families = data.family_records

        # 1. Run ID uniqueness
        is_valid, duplicates = DataIntegrityChecker.check_run_id_uniqueness(runs)
        if not is_valid:
            result.add_error(
                "integrity",
                f"Duplicate run IDs found: {duplicates}",
            )

        # 2. Budget integrity
        is_valid, budget_errors = DataIntegrityChecker.check_budget_integrity(runs)
        if not is_valid:
            for e in budget_errors:
                result.add_error(e.category, e.detail, e.run_id)

        # 3. Seed integrity
        is_valid, seed_errors = DataIntegrityChecker.check_seed_integrity(runs)
        if not is_valid:
            for e in seed_errors:
                result.add_error(e.category, e.detail, e.run_id)

        # 4. Failure-reference integrity
        is_valid, fail_errors = DataIntegrityChecker.check_failure_references(
            runs, failures
        )
        if not is_valid:
            for e in fail_errors:
                result.add_error(e.category, e.detail, e.run_id)

        # 5. Family-reference integrity
        is_valid, family_errors = DataIntegrityChecker.check_family_references(
            families, failures
        )
        if not is_valid:
            for e in family_errors:
                result.add_error(e.category, e.detail, e.run_id)

        # 6. Holdout-reference integrity
        is_valid, holdout_errors = DataIntegrityChecker.check_holdout_references(
            data.holdout_results, families
        )
        if not is_valid:
            for e in holdout_errors:
                result.add_error(e.category, e.detail, e.run_id)

        # 7. Branch-accounting reference integrity
        is_valid, branch_errors = DataIntegrityChecker.check_branch_accounting(
            data.branch_accounting, runs
        )
        if not is_valid:
            for e in branch_errors:
                result.add_error(e.category, e.detail, e.run_id)

        # Record exclusions
        for exc in result.excluded_runs:
            result.add_exclusion(exc.run_id, exc.reason)

        return result