"""Failure candidate domain models for the research prototype."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator

from agent_eval.domain.enums import InvariantSeverity


class FailureCandidateStatus(str, Enum):
    """Status of a failure candidate."""

    CANDIDATE = "CANDIDATE"
    # Future phases may add: CONFIRMED, REPRODUCIBLE, GENERALIZED, FAMILY


class FailureReasonCode(str, Enum):
    """Machine-readable reason codes for failure candidates."""

    UNAUTHORIZED_SENSITIVE_ACTION = "UNAUTHORIZED_SENSITIVE_ACTION"
    DENIED_ACTION_MUTATED_STATE = "DENIED_ACTION_MUTATED_STATE"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    MISSING_REQUIRED_CAPABILITY = "MISSING_REQUIRED_CAPABILITY"
    POLICY_EXECUTION_CONTRADICTION = "POLICY_EXECUTION_CONTRADICTION"
    RESOURCE_BOUNDARY_VIOLATION = "RESOURCE_BOUNDARY_VIOLATION"
    SENSITIVE_DATA_EXPOSURE = "SENSITIVE_DATA_EXPOSURE"
    PROCESS_ORDER_VIOLATION = "PROCESS_ORDER_VIOLATION"


class FailureCandidateBase(BaseModel):
    """Base failure candidate model with required fields."""

    failure_id: str = Field(..., description="Unique failure candidate identifier")
    trajectory_id: str = Field(..., description="Referenced trajectory")
    invariant_result_id: str = Field(
        ..., description="Referenced invariant evaluation result"
    )
    invariant_id: str = Field(..., description="Referenced invariant")
    status: FailureCandidateStatus = Field(
        default=FailureCandidateStatus.CANDIDATE,
        description="Candidate status",
    )
    severity: InvariantSeverity = Field(
        ..., description="Severity level inherited from invariant result"
    )
    reason_code: FailureReasonCode = Field(
        ..., description="Machine-readable reason code"
    )
    description: str = Field(
        ..., description="Deterministic description of the violation"
    )
    evidence: dict[str, Any] = Field(
        ..., description="Referenced evidence (event_ids, state_ids)"
    )
    detected_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Detection timestamp",
    )
    detector_version: str = Field(default="1.0", description="Detector version")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    @validator("failure_id")
    def failure_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("failure_id must not be empty")
        return v

    @validator("trajectory_id")
    def trajectory_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("trajectory_id must not be empty")
        return v

    @validator("invariant_result_id")
    def invariant_result_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("invariant_result_id must not be empty")
        return v

    @validator("invariant_id")
    def invariant_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("invariant_id must not be empty")
        return v


class FailureCandidate(FailureCandidateBase):
    """Full failure candidate model."""

    event_ids: list[str] = Field(
        default_factory=list,
        description="Referenced event IDs from trajectory",
    )
    state_ids: list[str] = Field(
        default_factory=list,
        description="Referenced state IDs from trajectory",
    )
    scenario_id: str | None = Field(default=None, description="Optional scenario ID")
    agent_id: str | None = Field(default=None, description="Optional agent ID")
    environment_id: str | None = Field(default=None, description="Optional environment ID")


class FailureDetectionContext:
    """Read-only context for failure detector evaluation.

    The detector must not mutate any of these objects.
    """

    def __init__(
        self,
        trajectory: Any,
        invariant_result: Any,
        relevant_events: list[Any],
        relevant_states: list[Any],
        scenario: Any | None = None,
        environment_metadata: dict[str, Any] | None = None,
    ):
        self._trajectory = trajectory
        self._invariant_result = invariant_result
        self._relevant_events = relevant_events
        self._relevant_states = relevant_states
        self._scenario = scenario
        self._environment_metadata = environment_metadata or {}

    @property
    def trajectory(self) -> Any:
        return self._trajectory

    @property
    def invariant_result(self) -> Any:
        return self._invariant_result

    @property
    def relevant_events(self) -> list[Any]:
        return self._relevant_events

    @property
    def relevant_states(self) -> list[Any]:
        return self._relevant_states

    @property
    def scenario(self) -> Any | None:
        return self._scenario

    @property
    def environment_metadata(self) -> dict[str, Any]:
        return self._environment_metadata

    def find_event(self, event_id: str) -> Any | None:
        """Find an event by ID in the relevant events."""
        for event in self._relevant_events:
            if hasattr(event, "event_id") and event.event_id == event_id:
                return event
        return None

    def find_state(self, state_id: str) -> Any | None:
        """Find a state by ID in the relevant states."""
        for state in self._relevant_states:
            if hasattr(state, "state_id") and state.state_id == state_id:
                return state
        return None
