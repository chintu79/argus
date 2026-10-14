"""Failure detection rules mapping invariant violations to failure candidates.

Each rule maps a specific invariant violation (I1–I8) to a failure candidate
with a corresponding reason code and deterministic description.
"""

from __future__ import annotations

from typing import Any

from agent_eval.domain.enums import InvariantOutcome
from agent_eval.failures.detector import FailureDetector
from agent_eval.failures.models import FailureCandidate


def applies_invariant(invariant_id: str) -> bool:
    """Check if this rule applies to the given invariant ID."""
    return invariant_id in {"I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"}


def detect_from_invariant_result(
    invariant_result: Any,
    trajectory: Any,
    relevant_events: list[Any],
    relevant_states: list[Any],
    scenario: Any | None = None,
    environment_metadata: dict[str, Any] | None = None,
) -> FailureCandidate | None:
    """Detect failure candidate from an invariant result.

    Only VIOLATED results produce candidates. Other statuses return None.
    """
    if not hasattr(invariant_result, "status"):
        return None
    if (
        invariant_result.status != InvariantOutcome.VIOLATED
        and getattr(invariant_result.status, "name", "") != "VIOLATED"
    ):
        return None

    return FailureDetector.detect(
        invariant_result=invariant_result,
        trajectory=trajectory,
        relevant_events=relevant_events,
        relevant_states=relevant_states,
        scenario=scenario,
        environment_metadata=environment_metadata,
    )


# Rule aliases for I1–I8 mapping to the unified detection pipeline
rule_i1 = detect_from_invariant_result
rule_i2 = detect_from_invariant_result
rule_i3 = detect_from_invariant_result
rule_i4 = detect_from_invariant_result
rule_i5 = detect_from_invariant_result
rule_i6 = detect_from_invariant_result
rule_i7 = detect_from_invariant_result
rule_i8 = detect_from_invariant_result
