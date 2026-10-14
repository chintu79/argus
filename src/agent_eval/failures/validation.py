"""Failure candidate validation.

Validates failure candidates at creation time and during persistence,
ensuring evidence integrity and schema compliance.
"""

from __future__ import annotations

from typing import Any

from agent_eval.domain.identifiers import is_valid
from agent_eval.failures.evidence import EvidenceValidator
from agent_eval.failures.models import FailureCandidate, FailureCandidateStatus


def validate_failure_candidate(
    candidate: FailureCandidate,
    available_events: list[Any] | None = None,
    available_states: list[Any] | None = None,
    available_trajectories: list[Any] | None = None,
) -> tuple[bool, list[str]]:
    """Validate a failure candidate's fields and evidence references.

    Returns (is_valid, list_of_errors).
    """
    errors: list[str] = []

    # Check required fields are non-empty
    if not candidate.failure_id or not is_valid(candidate.failure_id):
        errors.append("failure_id must be a non-empty valid string")

    if not candidate.trajectory_id or not is_valid(candidate.trajectory_id):
        errors.append("trajectory_id must be a non-empty valid string")

    if not candidate.invariant_result_id or not is_valid(candidate.invariant_result_id):
        errors.append("invariant_result_id must be a non-empty valid string")

    if not candidate.invariant_id or not is_valid(candidate.invariant_id):
        errors.append("invariant_id must be a non-empty valid string")

    # Check status is a valid enum value
    if not hasattr(candidate.status, "value"):
        errors.append("status must be a valid FailureCandidateStatus enum")
    elif candidate.status not in [
        FailureCandidateStatus.CANDIDATE,
    ]:
        # Allow other statuses for future phases
        pass

    # Check severity is valid
    if not hasattr(candidate.severity, "value"):
        errors.append("severity must be a valid InvariantSeverity enum")

    # Check reason_code is valid
    if not hasattr(candidate.reason_code, "value"):
        errors.append("reason_code must be a valid FailureReasonCode enum")

    # Validate event references if available events are provided
    if available_events is not None:
        ev_valid, missing = EvidenceValidator.validate_event_references(
            candidate.evidence.get("event_ids", []), available_events
        )
        if not ev_valid:
            for m in missing:
                errors.append(f"event_reference: {m}")

    # Validate state references if available states are provided
    if available_states is not None:
        st_valid, missing = EvidenceValidator.validate_state_references(
            candidate.evidence.get("state_ids", []), available_states
        )
        if not st_valid:
            for m in missing:
                errors.append(f"state_reference: {m}")

    # Check evidence dict has required keys
    evidence = candidate.evidence
    if not isinstance(evidence, dict):
        errors.append("evidence must be a dict")
    elif "event_ids" not in evidence:
        errors.append("evidence must contain event_ids key")
    elif "state_ids" not in evidence:
        errors.append("evidence must contain state_ids key")

    return len(errors) == 0, errors


def validate_candidate_creation(
    candidate: FailureCandidate,
    invariant_result: Any,
    trajectory: Any,
) -> tuple[bool, list[str]]:
    """Validate a failure candidate against its source invariant result and trajectory.

    Ensures the candidate correctly references a real invariant result
    and a real trajectory.
    """
    errors: list[str] = []

    # Check invariant result exists and was VIOLATED
    if not hasattr(invariant_result, "status"):
        errors.append("invariant_result must have a status field")
    else:
        status_name = getattr(invariant_result.status, "name", str(invariant_result.status))
        if status_name == "SATISFIED":
            errors.append(
                "SATISFIED invariant results do not produce failure candidates"
            )

    # Check trajectory reference is valid
    trajectory_id = getattr(trajectory, "trajectory_id", None)
    if not trajectory_id or not is_valid(trajectory_id):
        errors.append("trajectory must have a valid trajectory_id")

    # Check invariant ID matches
    invariant_id = getattr(invariant_result, "invariant_id", None)
    if not invariant_id or not is_valid(invariant_id):
        errors.append("invariant_result must have a valid invariant_id")

    # Check candidate invariant_id matches invariant_result invariant_id
    if candidate.invariant_id != invariant_id:
        errors.append(
            f"candidate.invariant_id ({candidate.invariant_id}) "
            f"must match invariant_result.invariant_id ({invariant_id})"
        )

    return len(errors) == 0, errors
