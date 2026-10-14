"""Event schemas and models for trajectory trace collection.

Every event is a structured, observable execution record.
No private reasoning, chain-of-thought, or evaluator-only data.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from agent_eval.domain.common import DomainMetadata, JSONSerializable
from agent_eval.domain.enums import EventType
from agent_eval.domain.identifiers import StateId, TrajectoryId, is_valid, make_id


class TrajectoryEvent(JSONSerializable):
    """A single observable execution event in a trajectory.

    Every event preserves chronological ordering and stable IDs.
    """

    def __init__(
        self,
        event_id: str,
        trajectory_id: TrajectoryId,
        sequence_number: int,
        timestamp: datetime,
        event_type: EventType,
        state_id: StateId | None = None,
        source: str | None = None,
        payload: dict[str, Any] | None = None,
        metadata: DomainMetadata | None = None,
    ):
        # Validate IDs
        if not is_valid(event_id):
            raise ValueError(f"Invalid event_id: {event_id}")
        if not is_valid(trajectory_id):
            raise ValueError(f"Invalid trajectory_id: {trajectory_id}")

        self.event_id = event_id
        self.trajectory_id = trajectory_id
        self.sequence_number = sequence_number
        self.timestamp = timestamp
        self.event_type = event_type
        self.state_id = state_id
        self.source = source
        self.payload = payload or {}
        self.metadata = metadata or DomainMetadata()

    @property
    def is_valid_sequence(self) -> bool:
        """Check sequence number is non-negative."""
        return self.sequence_number >= 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict."""
        return {
            "event_id": self.event_id,
            "trajectory_id": self.trajectory_id,
            "sequence_number": self.sequence_number,
            "timestamp": self.timestamp.isoformat()
            if isinstance(self.timestamp, datetime)
            else self.timestamp,
            "event_type": self.event_type.name
            if hasattr(self.event_type, "name")
            else str(self.event_type),
            "state_id": self.state_id,
            "source": self.source,
            "payload": self.payload,
            "metadata": self.metadata.to_dict()
            if hasattr(self.metadata, "to_dict")
            else dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TrajectoryEvent:
        """Deserialize from dict."""
        from datetime import datetime

        ts = data.get("timestamp", "")
        timestamp = datetime.fromisoformat(ts) if ts else datetime.now(UTC)

        event_type_str = data.get("event_type", "AGENT_OUTPUT")
        # Try to parse as EventType enum
        try:
            from agent_eval.domain.enums import EventType

            event_type = EventType[event_type_str]
        except (KeyError, ValueError):
            event_type = EventType.AGENT_OUTPUT

        event_id = data.get("event_id", make_id("event"))
        trajectory_id = data.get("trajectory_id", "traj-unknown")
        sequence_number = data.get("sequence_number", 0)

        return cls(
            event_id=event_id,
            trajectory_id=trajectory_id,
            sequence_number=sequence_number,
            timestamp=timestamp,
            event_type=event_type,
            state_id=data.get("state_id"),
            source=data.get("source"),
            payload=data.get("payload"),
            metadata=data.get("metadata"),
        )


# Event payload builders


def build_agent_output_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    agent_id: str,
    action_type: str,
    tool_name: str | None,
    arguments: dict[str, Any],
    state_id: StateId | None = None,
    source: str | None = "agent",
) -> TrajectoryEvent:
    """Build an AGENT_OUTPUT event payload."""
    payload = {
        "agent_id": agent_id,
        "action_type": action_type,
        "tool_name": tool_name,
        "arguments": arguments,
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.AGENT_OUTPUT,
        source=source,
        payload=payload,
    )


def build_tool_request_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    request_id: str,
    tool_name: str,
    arguments: dict[str, Any],
    agent_id: str,
    identity: dict[str, Any] | None = None,
    execution_context: dict[str, Any] | None = None,
    source: str | None = "gateway",
) -> TrajectoryEvent:
    """Build a TOOL_REQUEST event payload."""
    payload = {
        "request_id": request_id,
        "tool_name": tool_name,
        "arguments": arguments,
        "agent_id": agent_id,
        "identity": identity or {},
        "execution_context": execution_context or {},
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.TOOL_REQUEST,
        source=source,
        payload=payload,
    )


def build_policy_decision_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    decision: str,
    identity: str,
    action: str,
    resource_type: str,
    resource_id: str,
    required_capability: str,
    capability_present: bool,
    authorization_result: str,
    matched_rule: str | None = None,
    reason_code: str | None = None,
    source: str | None = "policy_engine",
) -> TrajectoryEvent:
    """Build a POLICY_DECISION event payload."""
    payload = {
        "decision": decision,
        "identity": identity,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "required_capability": required_capability,
        "capability_present": capability_present,
        "authorization_result": authorization_result,
        "matched_rule": matched_rule,
        "reason_code": reason_code,
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.POLICY_DECISION,
        source=source,
        payload=payload,
    )


def build_tool_response_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    request_id: str,
    tool_name: str,
    success: bool,
    result: dict[str, Any] | None = None,
    error_code: str | None = None,
    policy_decision: dict[str, Any] | None = None,
    authorization_result: dict[str, Any] | None = None,
    state_changed: dict[str, Any] | None = None,
    source: str | None = "tool",
) -> TrajectoryEvent:
    """Build a TOOL_RESPONSE event payload."""
    payload = {
        "request_id": request_id,
        "tool_name": tool_name,
        "success": success,
        "result": result or {},
        "error_code": error_code,
        "policy_decision": policy_decision or {},
        "authorization_result": authorization_result or {},
        "state_changed": state_changed or {},
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.TOOL_RESPONSE,
        source=source,
        payload=payload,
    )


def build_state_transition_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    previous_state_id: StateId | None = None,
    new_state_id: StateId | None = None,
    changed_components: list[str] | None = None,
    operation: str | None = None,
    actor: str | None = None,
    source: str | None = "environment",
) -> TrajectoryEvent:
    """Build a STATE_TRANSITION event payload."""
    payload = {
        "previous_state_id": previous_state_id,
        "new_state_id": new_state_id,
        "changed_components": changed_components or [],
        "operation": operation,
        "actor": actor,
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.STATE_TRANSITION,
        state_id=new_state_id,
        source=source,
        payload=payload,
    )


def build_fault_injection_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    fault_type: str,
    target: str,
    parameters: dict[str, Any] | None = None,
    seed: int | None = None,
    activated: bool = True,
    source: str | None = "fault_injector",
) -> TrajectoryEvent:
    """Build a FAULT_INJECTION event payload."""
    payload = {
        "fault_type": fault_type,
        "target": target,
        "parameters": parameters or {},
        "seed": seed,
        "activated": activated,
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.FAULT_INJECTION,
        state_id=None,
        source=source,
        payload=payload,
    )


def build_termination_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    reason: str,
    status: str,
    step_count: int,
    final_state_id: StateId | None = None,
    source: str | None = "execution",
) -> TrajectoryEvent:
    """Build a TERMINATION event payload."""
    payload = {
        "reason": reason,
        "status": status,
        "step_count": step_count,
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.TERMINATION,
        state_id=final_state_id,
        source=source,
        payload=payload,
    )


def build_cost_event(
    event_id: str,
    trajectory_id: TrajectoryId,
    sequence_number: int,
    timestamp: datetime,
    cost_type: str,
    amount: int,
    unit: str = "execution_units",
    component: str | None = None,
    cumulative_cost: int | None = None,
    source: str | None = "execution",
) -> TrajectoryEvent:
    """Build a COST event payload."""
    payload = {
        "cost_type": cost_type,
        "amount": amount,
        "unit": unit,
        "component": component,
        "cumulative_cost": cumulative_cost,
    }
    return TrajectoryEvent(
        event_id=event_id,
        trajectory_id=trajectory_id,
        sequence_number=sequence_number,
        timestamp=timestamp,
        event_type=EventType.COST,
        state_id=None,
        source=source,
        payload=payload,
    )
