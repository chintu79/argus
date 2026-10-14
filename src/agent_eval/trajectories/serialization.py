"""Trace serialization and hashing for reproducibility and integrity.

Provides deterministic canonical hashing and JSONL export/import.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from agent_eval.domain.enums import EventType
from agent_eval.domain.identifiers import is_valid, make_id

TRACE_SCHEMA_VERSION = "1.0"


def canonical_event_hash(event_dict: dict[str, Any]) -> str:
    """Compute a deterministic canonical hash for a single event.

    Only includes fields that are stable across executions.
    Excludes execution-specific timestamps, secrets, and transient metadata.
    """
    # Fields to include in the canonical representation
    canonical_fields = [
        "event_id",
        "trajectory_id",
        "sequence_number",
        "event_type",
        "state_id",
        "source",
    ]

    # Build canonical representation
    canonical_parts = []
    for field in canonical_fields:
        if field in event_dict:
            value = event_dict[field]
            # Normalize enums
            if hasattr(value, "name"):
                value = value.name
            # Normalize identifiers
            if isinstance(value, str) and ":" in value:
                # Keep as-is for stable hashing
                pass
            canonical_parts.append(f"{field}:{json.dumps(value, sort_keys=True)}")

    canonical_string = "|".join(canonical_fields) + "|" + "|".join(canonical_parts)
    return hashlib.sha256(canonical_string.encode("utf-8")).hexdigest()


def trace_hash(trace_events: list[dict[str, Any]]) -> str:
    """Compute a deterministic hash for an entire trace.

    The hash is computed from canonical event representations in sequence order.
    Does NOT include execution timestamps or seed - those are execution-specific.
    """
    # Sort events by sequence number
    sorted_events = sorted(trace_events, key=lambda e: e.get("sequence_number", 0))

    # Hash each event and concatenate
    event_hashes = [canonical_event_hash(event) for event in sorted_events]
    combined = "|".join(event_hashes)

    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def trace_to_dict(trace: dict[str, Any]) -> dict[str, Any]:
    """Convert trace to a fully JSON-serializable dict.

    Ensures all nested structures are serializable.
    """
    result: dict[str, Any] = {}
    for key, value in trace.items():
        if key == "events":
            # Serialize events
            serialized_events: list[Any] = []
            for event in value:
                serialized_event: dict[str, Any] = {}
                for ek, ev in event.items():
                    if isinstance(ev, (str, int, float, bool, type(None))):
                        serialized_event[ek] = ev
                    elif isinstance(ev, list):
                        # Try to serialize list items
                        serialized_list = []
                        for item in ev:
                            if isinstance(item, (str, int, float, bool, type(None))):
                                serialized_list.append(item)
                            else:
                                serialized_list.append(str(item))
                        serialized_event[ek] = serialized_list
                    elif isinstance(ev, dict):
                        # Recursively serialize
                        serialized_dict = {}
                        for dk, dv in ev.items():
                            if isinstance(dv, (str, int, float, bool, type(None))):
                                serialized_dict[dk] = dv
                            else:
                                serialized_dict[dk] = str(dv)
                        serialized_event[ek] = serialized_dict
                    else:
                        serialized_event[ek] = str(ev)
                serialized_events.append(serialized_event)
            result[key] = serialized_events
        elif isinstance(value, (str, int, float, bool, type(None))):
            result[key] = value
        elif isinstance(value, list):
            serialized_list = []
            for item in value:
                if isinstance(item, (str, int, float, bool, type(None))):
                    serialized_list.append(item)
                else:
                    serialized_list.append(str(item))
            result[key] = serialized_list
        elif isinstance(value, dict):
            serialized_dict = {}
            for dk, dv in value.items():
                if isinstance(dv, (str, int, float, bool, type(None))):
                    serialized_dict[dk] = dv
                else:
                    serialized_dict[dk] = str(dv)
            result[key] = serialized_dict
        else:
            result[key] = str(value)
    return result


def dict_to_trace(data: dict[str, Any]) -> dict[str, Any]:
    """Convert a dict to trace structure, ensuring schema version."""

    # Ensure schema version
    if "trace_schema_version" not in data:
        data["trace_schema_version"] = TRACE_SCHEMA_VERSION

    # Ensure events is present
    if "events" not in data:
        data["events"] = []

    # Ensure metadata is present
    if "metadata" not in data:
        data["metadata"] = {"source": "imported"}

    # Ensure event IDs are valid
    for event in data.get("events", []):
        if "event_id" not in event or not is_valid(event.get("event_id")):
            event["event_id"] = event.get("event_id", make_id("event"))

    # Ensure sequence numbers are valid
    for event in data.get("events", []):
        if "sequence_number" not in event:
            event["sequence_number"] = 0

    return data


def verify_trace_integrity(trace_dict: dict[str, Any]) -> bool:
    """Verify the integrity of a trace dict.

    Checks:
    - Schema version
    - Event ordering
    - Unique event IDs
    - Valid event types
    - Trajectory ID consistency
    """
    # Check schema version
    if trace_dict.get("trace_schema_version") != TRACE_SCHEMA_VERSION:
        return False

    events = trace_dict.get("events", [])
    seen_ids = set()
    last_seq = -1

    for event in events:
        # Check sequence is monotonically increasing
        seq = event.get("sequence_number", 0)
        if seq <= last_seq:
            return False
        last_seq = seq

        # Check unique event IDs
        eid = event.get("event_id", "")
        if eid in seen_ids:
            return False
        seen_ids.add(eid)

        # Check valid event type
        etype = event.get("event_type", "")
        if etype not in [et.name for et in EventType]:
            return False

        # Check trajectory ID consistency
        tid = event.get("trajectory_id", "")
        if trace_dict.get("trajectory_id") and tid != trace_dict["trajectory_id"]:
            return False

    return True
