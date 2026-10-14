"""Trace validation functions for the Budget-Constrained Adaptive Security Evaluation prototype.

Validates traces, events, and ensures integrity constraints are met.
"""

from __future__ import annotations

from typing import Any

from agent_eval.domain.enums import EventType
from agent_eval.domain.identifiers import is_valid


def validate_event(event_data: dict[str, Any]) -> tuple[bool, str | None]:
    """Validate a single event dict.

    Returns (is_valid, error_message).
    """
    # Check required fields
    required_fields = [
        "event_id",
        "trajectory_id",
        "sequence_number",
        "event_type",
        "timestamp",
        "payload",
    ]
    for field in required_fields:
        if field not in event_data:
            return False, f"Missing required field: {field}"

    # Check event_id is valid
    if not is_valid(event_data.get("event_id")):
        return False, f"Invalid event_id: {event_data.get('event_id')}"

    # Check trajectory_id is valid
    if not is_valid(event_data.get("trajectory_id")):
        return False, f"Invalid trajectory_id: {event_data.get('trajectory_id')}"

    # Check sequence_number is non-negative
    seq = event_data.get("sequence_number", 0)
    if not isinstance(seq, int) or seq < 0:
        return False, f"Invalid sequence_number: {seq} (must be non-negative integer)"

    # Check event_type is valid
    etype = event_data.get("event_type", "")
    try:
        from agent_eval.domain.enums import EventType

        EventType[etype]
    except (KeyError, ValueError):
        return False, f"Invalid event_type: {etype}"

    # Check payload is a dict
    payload = event_data.get("payload")
    if payload is not None and not isinstance(payload, dict):
        return False, f"payload must be a dict, got {type(payload).__name__}"

    return True, None


def validate_trajectory_events(
    events: list[dict[str, Any]],
    trajectory_id: str,
) -> tuple[bool, list[str]]:
    """Validate a list of events belonging to a trajectory.

    Returns (is_valid, list_of_errors).
    """
    errors: list[str] = []
    seen_ids: set[str] = set()
    last_seq = -1

    for i, event_data in enumerate(events):
        # Validate individual event
        is_valid_event, error = validate_event(event_data)
        if not is_valid_event:
            errors.append(f"Event {i}: {error}")

        # Check trajectory ID consistency
        event_trajectory = event_data.get("trajectory_id", "")
        if event_trajectory != trajectory_id:
            errors.append(
                f"Event {i}: trajectory_id mismatch: expected {trajectory_id}, "
                f"got {event_trajectory}"
            )

        # Check monotonically increasing sequence
        seq = event_data.get("sequence_number", 0)
        if seq <= last_seq:
            errors.append(
                f"Event {i}: sequence_number {seq} is not greater than previous {last_seq}"
            )
        last_seq = seq

        # Check unique event IDs
        eid = event_data.get("event_id", "")
        if eid in seen_ids:
            errors.append(f"Event {i}: duplicate event_id {eid}")
        seen_ids.add(eid)

        # Check valid event type
        etype = event_data.get("event_type", "")
        if etype not in [et.name for et in EventType]:
            errors.append(f"Event {i}: invalid event_type {etype}")

    return len(errors) == 0, errors


def validate_trace_dict(trace_dict: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate a complete trace dict.

    Returns (is_valid, list_of_errors).
    """
    errors: list[str] = []

    # Check schema version
    if trace_dict.get("trace_schema_version") != "1.0":
        errors.append("Invalid or missing trace_schema_version")

    # Check events list
    events = trace_dict.get("events", [])
    if not isinstance(events, list):
        errors.append("events must be a list")
        return len(errors) > 0, errors

    # Validate all events
    trajectory_id = trace_dict.get("trajectory_id", "")
    is_valid, event_errors = validate_trajectory_events(events, trajectory_id)
    if not is_valid:
        errors.extend(event_errors)

    # Check event count
    if len(events) == 0:
        errors.append("Trace must contain at least one event")

    # Check required metadata
    if "execution_id" not in trace_dict:
        errors.append("Missing execution_id in trace")

    if "agent_id" not in trace_dict:
        errors.append("Missing agent_id in trace")

    return len(errors) == 0, errors
