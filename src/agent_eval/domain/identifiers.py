"""
Stable Identifiers for the Budget-Constrained Adaptive Security Evaluation prototype.

All identifiers are represented as simple strings for serialization compatibility.
No UUID database dependencies.
"""

from __future__ import annotations

from typing import TypeGuard

ExperimentId = str
RunId = str
ScenarioId = str
CandidateId = str
AgentId = str
EnvironmentId = str
ExecutionId = str
TrajectoryId = str
EventId = str
StateId = str
SnapshotId = str
BranchId = str
InvariantId = str
InvariantEvaluationId = str
FailureId = str
FailureFamilyId = str
BudgetId = str


def make_id(prefix: str, value: str | None = None) -> str:
    """Generate a deterministic ID from a prefix and optional value."""
    if value:
        return f"{prefix}:{value}"
    import uuid

    return f"{prefix}:{uuid.uuid4()}"


def is_valid(id_str: str | None) -> TypeGuard[str]:
    """Check if an ID string is valid (non-empty, non-None)."""
    return id_str is not None and isinstance(id_str, str) and len(id_str.strip()) > 0


def validate_id(id_str: str | None, expected_prefix: str | None = None) -> bool:
    """Validate an ID has the expected prefix and format."""
    if not is_valid(id_str):
        return False
    return not (expected_prefix and not id_str.startswith(expected_prefix))


def is_safe_identifier(id_str: str | None) -> bool:
    """Check if an ID is valid and safe against path traversal."""
    if not is_valid(id_str):
        return False
    if ".." in id_str or "/" in id_str or "\\" in id_str or "\0" in id_str:
        return False
    import re
    return bool(re.match(r"^[a-zA-Z0-9_\-.:]+$", id_str))


def sanitize_id_for_path(id_str: str) -> str:
    """Convert an identifier into a safe filename/directory component."""
    if not is_valid(id_str):
        raise ValueError(f"Invalid identifier: {id_str!r}")
    import re
    cleaned = id_str.replace("..", "_").replace("/", "_").replace("\\", "_").replace(":", "_")
    return re.sub(r"[^a-zA-Z0-9_\-.]", "_", cleaned)

