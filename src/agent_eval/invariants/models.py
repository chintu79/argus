"""Invariant data models for the research prototype."""

from __future__ import annotations

import builtins
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator


class InvariantStatus(str, Enum):
    """Status of an invariant evaluation."""

    SATISFIED = "SATISFIED"
    VIOLATED = "VIOLATED"
    INCONCLUSIVE = "INCONCLUSIVE"
    INVALID = "INVALID"
    ERROR = "ERROR"


class InvariantSeverity(str, Enum):
    """Severity classification for invariants."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class InvariantBase(BaseModel):
    """Base invariant model with required fields."""

    invariant_id: str = Field(..., description="Unique invariant identifier")
    name: str = Field(..., description="Human-readable invariant name")
    description: str = Field(..., description="Detailed invariant description")
    version: str = Field(default="1.0.0", description="Invariant version")
    severity: InvariantSeverity = Field(
        default=InvariantSeverity.MEDIUM,
        description="Impact severity level",
    )
    enabled: bool = Field(default=True, description="Whether invariant is active")

    @validator("invariant_id")
    def invariant_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("invariant_id must not be empty")
        return v


class Invariant(InvariantBase):
    """Full invariant model with type and parameters."""

    invariant_type: str = Field(..., description="Type/category of invariant")
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Invariant-specific parameters",
    )


class InvariantResultBase(BaseModel):
    """Base invariant result model."""

    result_id: str = Field(..., description="Unique result identifier")
    invariant_id: str = Field(..., description="Referenced invariant")
    trajectory_id: str = Field(..., description="Referenced trajectory")
    status: InvariantStatus = Field(..., description="Evaluation status")
    severity: InvariantSeverity = Field(..., description="Severity level")
    evaluated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Evaluation timestamp",
    )
    reason_code: str | None = Field(default=None, description="Machine-readable reason code")
    message: str | None = Field(default=None, description="Human-readable explanation")
    evidence: dict[str, Any] = Field(
        default_factory=dict,
        description="Traceable evidence references",
    )
    engine_version: str = Field(default="1.0", description="Engine version")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    @validator("result_id")
    def result_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("result_id must not be empty")
        return v


class InvariantResult(InvariantResultBase):
    """Full invariant result model."""

    event_ids: list[str] = Field(
        default_factory=list,
        description="Referenced event IDs from trajectory",
    )
    state_ids: list[str] = Field(
        default_factory=list,
        description="Referenced state IDs from trajectory",
    )


class InvariantRegistry:
    """Registry for managing invariants."""

    def __init__(self):
        self._invariants: dict[str, Invariant] = {}
        self._evaluators: dict[str, type] = {}

    def register(self, invariant: Invariant, evaluator: type) -> None:
        """Register an invariant with its evaluator class."""
        if invariant.invariant_id in self._invariants:
            raise ValueError(
                f"Invariant ID already registered: {invariant.invariant_id}"
            )
        self._invariants[invariant.invariant_id] = invariant
        self._evaluators[invariant.invariant_id] = evaluator

    def get(self, invariant_id: str) -> Invariant | None:
        """Get an invariant by ID."""
        return self._invariants.get(invariant_id)

    def list(self) -> builtins.list[Invariant]:
        """List all registered invariants."""
        return list(self._invariants.values())

    def enable(self, invariant_id: str) -> None:
        """Enable an invariant."""
        if invariant_id in self._invariants:
            self._invariants[invariant_id].enabled = True

    def disable(self, invariant_id: str) -> None:
        """Disable an invariant."""
        if invariant_id in self._invariants:
            self._invariants[invariant_id].enabled = False


class Predicate:
    """Base predicate for invariant evaluation logic."""

    def evaluate(
        self,
        trajectory: Any,
        evidence: dict[str, Any],
    ) -> tuple[InvariantStatus, dict[str, Any]]:
        """Evaluate the predicate against the trajectory and evidence."""
        raise NotImplementedError()


def result_status(
    satisfied: bool,
    violated: bool,
    inconclusive: bool,
    invalid: bool,
    error: bool,
) -> InvariantStatus:
    """Determine the invariant status from boolean flags.

    Priority: invalid > error > violated > satisfied > inconclusive
    """
    if invalid:
        return InvariantStatus.INVALID
    if error:
        return InvariantStatus.ERROR
    if violated:
        return InvariantStatus.VIOLATED
    if satisfied:
        return InvariantStatus.SATISFIED
    if inconclusive:
        return InvariantStatus.INCONCLUSIVE
    return InvariantStatus.INCONCLUSIVE
