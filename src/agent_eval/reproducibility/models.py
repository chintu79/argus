"""Reproducibility and verification domain models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator


class ReproducibilityStatus(str, Enum):
    """Status of a reproducibility verification."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    REPRODUCIBLE = "REPRODUCIBLE"
    PARTIAL = "PARTIAL"
    NOT_REPRODUCIBLE = "NOT_REPRODUCIBLE"
    INCONCLUSIVE = "INCONCLUSIVE"
    ERROR = "ERROR"


class SignatureMatchResult(str, Enum):
    """Result of comparing a target signature with observed signatures."""

    MATCH = "MATCH"
    NO_MATCH = "NO_MATCH"
    INCONCLUSIVE = "INCONCLUSIVE"


class VerificationRunStatus(str, Enum):
    """Status of an individual verification run."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ReproducibilityRequest(BaseModel):
    """Request to verify a failure candidate across multiple seeds."""

    verification_id: str | None = Field(default=None, description="Unique verification ID")
    failure_id: str = Field(..., description="Target failure candidate ID")
    trajectory_id: str = Field(..., description="Original trajectory ID")
    scenario_id: str = Field(..., description="Scenario to rerun")
    verification_seeds: list[int] = Field(
        default_factory=lambda: [101, 202, 303],
        description="Seeds for independent verification runs",
    )
    k: int = Field(
        default=3,
        description="Number of verification runs (must equal len(verification_seeds))",
    )
    temperature: float | None = Field(
        default=0.7,
        description="Agent temperature (if supported by agent)",
    )
    max_attempts: int = Field(
        default=3,
        description="Maximum attempts per run",
    )
    timeout: int | None = Field(
        default=300,
        description="Timeout per run in seconds",
    )
    threshold: float = Field(
        default=0.75,
        description="Reproducibility threshold (default 0.75)",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    @validator("verification_seeds")
    def validate_seeds(cls, v):
        if len(v) == 0:
            raise ValueError("At least one verification seed required")
        if len(set(v)) != len(v):
            raise ValueError("Verification seeds must be unique")
        return v

    @validator("k")
    def validate_k(cls, v, values):
        if "verification_seeds" in values and v != len(values["verification_seeds"]):
            raise ValueError("k must equal number of verification_seeds")
        return v


class FailureSignature(BaseModel):
    """Deterministic signature of a failure for reproducibility comparison.

    Does NOT include trajectory IDs, timestamps, or execution-specific IDs.
    """

    invariant_id: str = Field(..., description="Invariant that was violated")
    reason_code: str = Field(..., description="Machine-readable reason code")
    action: str | None = Field(default=None, description="Action that triggered the violation")
    resource: str | None = Field(default=None, description="Resource involved in the violation")
    state_transition: str | None = Field(
        default=None, description="Observed state transition pattern"
    )
    resource_type: str | None = Field(
        default=None, description="Type of resource (customer, account, etc.)"
    )
    policy_decision: str | None = Field(
        default=None, description="Policy decision that occurred (ALLOW/DENY/REVIEW/ERROR)"
    )

    def to_canonical_string(self) -> str:
        """Create a canonical string representation for comparison."""
        parts = [
            f"inv:{self.invariant_id}",
            f"rc:{self.reason_code}",
        ]
        if self.action:
            parts.append(f"act:{self.action}")
        if self.resource:
            parts.append(f"res:{self.resource}")
        if self.state_transition:
            parts.append(f"trans:{self.state_transition}")
        if self.resource_type:
            parts.append(f"rtype:{self.resource_type}")
        if self.policy_decision:
            parts.append(f"policy:{self.policy_decision}")
        return "|".join(parts)


class VerificationRun(BaseModel):
    """Record of a single verification run."""

    run_id: str = Field(..., description="Unique run identifier")
    verification_id: str = Field(..., description="Parent verification ID")
    seed: int = Field(..., description="Seed used for this run")
    status: VerificationRunStatus = Field(
        default=VerificationRunStatus.PENDING,
        description="Run status",
    )
    started_at: datetime | None = Field(default=None, description="Run start time")
    completed_at: datetime | None = Field(default=None, description="Run completion time")
    trajectory_id: str | None = Field(default=None, description="Resulting trajectory ID")
    target_matched: SignatureMatchResult | None = Field(
        default=None, description="Whether target signature was matched"
    )
    observed_signature: FailureSignature | None = Field(
        default=None, description="Signature observed in this run"
    )
    invariant_results: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Invariant evaluation results from this run",
    )
    token_count: int | None = Field(default=None, description="Tokens consumed in this run")
    error: str | None = Field(default=None, description="Error message if run failed")


class ReproducibilityResult(BaseModel):
    """Aggregated result of a reproducibility verification."""

    failure_id: str = Field(..., description="Original failure candidate ID")
    verification_id: str = Field(..., description="Unique verification ID")
    k: int = Field(..., description="Number of verification runs")
    successful_replications: int = Field(
        default=0,
        description="Number of runs that reproduced the failure",
    )
    rep_k: float = Field(
        default=0.0,
        description="Reproducibility rate (successful_replications / k)",
    )
    threshold: float = Field(
        default=0.75,
        description="Reproducibility threshold",
    )
    status: ReproducibilityStatus = Field(
        default=ReproducibilityStatus.PENDING,
        description="Overall verification status",
    )
    runs: list[VerificationRun] = Field(
        default_factory=list,
        description="Individual run records",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Verification creation time",
    )
    completed_at: datetime | None = Field(
        default=None, description="Verification completion time"
    )
    verifier_version: str = Field(
        default="1.0",
        description="Verifier version",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )


class ReproducibilityPolicy(BaseModel):
    """Configuration policy for reproducibility verification."""

    default_k: int = Field(default=3, description="Default number of runs")
    default_seeds: list[int] = Field(
        default_factory=lambda: [101, 202, 303],
        description="Default verification seeds",
    )
    default_threshold: float = Field(
        default=0.75,
        description="Default reproducibility threshold",
    )
    default_temperature: float = Field(
        default=0.7,
        description="Default agent temperature",
    )
    early_stopping: bool = Field(
        default=False,
        description="Whether to stop early on threshold reached",
    )
    max_run_time_seconds: int = Field(
        default=300,
        description="Maximum time per verification run",
    )
