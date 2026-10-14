"""Invariant evaluation engine.

The engine consumes finalized trajectory evidence and evaluates predefined
invariants against observed execution behavior. It produces structured
results but does NOT classify failures or infer root causes.

Conceptual flow:
    Scenario → Agent Execution → Trajectory → Invariant Engine → Invariant Result
"""

from __future__ import annotations

from typing import Any

from agent_eval.domain.identifiers import make_id
from agent_eval.invariants.models import (
    Invariant,
    InvariantRegistry,
    InvariantResult,
    InvariantSeverity,
    InvariantStatus,
)


class InvariantEvaluationContext:
    """Read-only context for invariant evaluation.

    The engine must NOT mutate this context or the underlying trajectory.
    """

    def __init__(
        self,
        trajectory: Any,
        invariant: Invariant,
        events: list[Any],
        states: list[Any],
        metadata: dict[str, Any],
    ):
        self._trajectory = trajectory
        self._invariant = invariant
        self._events = events
        self._states = states
        self._metadata = metadata

    @property
    def trajectory(self) -> Any:
        return self._trajectory

    @property
    def invariant(self) -> Invariant:
        return self._invariant

    @property
    def events(self) -> list[Any]:
        return self._events

    @property
    def states(self) -> list[Any]:
        return self._states

    @property
    def metadata(self) -> dict[str, Any]:
        return self._metadata

    def find_event(self, event_id: str) -> Any | None:
        """Find an event by ID in the trajectory."""
        for event in self._events:
            if hasattr(event, "event_id") and event.event_id == event_id:
                return event
        return None

    def find_events_by_type(self, event_type: str) -> list[Any]:
        """Find all events of a given type."""
        result = []
        for event in self._events:
            if hasattr(event, "event_type") and event.event_type == event_type:
                result.append(event)
        return result

    def find_state(self, state_id: str) -> Any | None:
        """Find a state by ID."""
        for state in self._states:
            if hasattr(state, "state_id") and state.state_id == state_id:
                return state
        return None


class InvariantEngine:
    """Core invariant evaluation engine.

    Evaluates invariants against finalized trajectory evidence and produces
    structured results. Does NOT classify failures, assign families, or infer
    root causes.
    """

    def __init__(self, registry: InvariantRegistry):
        self._registry = registry

    def evaluate(
        self,
        invariant_id: str,
        trajectory: Any,
        events: list[Any],
        states: list[Any],
        metadata: dict[str, Any] | None = None,
    ) -> InvariantResult | None:
        """Evaluate a single invariant against trajectory evidence.

        Returns None if the invariant is not found in the registry.
        """
        # Look up the invariant
        invariant = self._registry.get(invariant_id)
        if invariant is None:
            return None

        # If invariant is not enabled, return SATISFIED by convention
        # (or we could return INVALID - but per spec we just skip)
        if not invariant.enabled:
            return None

        # Get the evaluator class for this invariant
        evaluator_class = self._registry._evaluators.get(invariant_id)
        if evaluator_class is None:
            # Try to find by name matching
            from agent_eval.invariants.engine import (
                _get_evaluator_by_name,
            )

            evaluator_class = _get_evaluator_by_name(invariant_id)

        if evaluator_class is None:
            # No evaluator registered - return ERROR
            return InvariantResult(
                result_id=make_id("result"),
                invariant_id=invariant_id,
                trajectory_id=getattr(trajectory, "trajectory_id", "unknown"),
                status=InvariantStatus.ERROR,
                severity=InvariantSeverity.HIGH,
                message=f"No evaluator found for invariant {invariant_id}",
                evidence={},
                engine_version="1.0",
            )

        # Create evaluation context
        context = InvariantEvaluationContext(
            trajectory=trajectory,
            invariant=invariant,
            events=events,
            states=states,
            metadata=metadata or {},
        )

        # Execute the evaluator
        try:
            evaluator = evaluator_class(invariant, context)
            result = evaluator.evaluate()
            # Ensure result has required fields
            if not hasattr(result, "status"):
                result.status = InvariantStatus.INCONCLUSIVE
            if not hasattr(result, "result_id"):
                result.result_id = make_id("result")
            return result
        except Exception as e:
            # Return ERROR for unexpected evaluator exceptions
            return InvariantResult(
                result_id=make_id("result"),
                invariant_id=invariant_id,
                trajectory_id=getattr(trajectory, "trajectory_id", "unknown"),
                status=InvariantStatus.ERROR,
                severity=InvariantSeverity.HIGH,
                message=f"Evaluator exception: {e!s}",
                evidence={},
                engine_version="1.0",
            )

    def evaluate_all(
        self,
        trajectory: Any,
        events: list[Any],
        states: list[Any],
        metadata: dict[str, Any] | None = None,
    ) -> list[InvariantResult]:
        """Evaluate all enabled invariants against a trajectory.

        Results preserve trajectory_id and invariant_id for traceability.
        """
        results = []
        for invariant_id, invariant in self._registry._invariants.items():
            if not invariant.enabled:
                continue

            result = self.evaluate(
                invariant_id=invariant_id,
                trajectory=trajectory,
                events=events,
                states=states,
                metadata=metadata,
            )
            if result is not None:
                results.append(result)

        # Sort by invariant_id for deterministic output
        results.sort(key=lambda r: r.invariant_id)
        return results


def _get_evaluator_by_name(invariant_id: str) -> type | None:
    """Try to find an evaluator by invariant ID name matching.

    Maps invariant IDs like "I1", "I2", etc. to evaluator classes.
    """
    return None
