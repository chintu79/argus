"""Failure candidate detector.

Converts invariant evaluation results into structured failure candidates
while preserving strict evidence traceability.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar

from agent_eval.domain.enums import InvariantOutcome, InvariantSeverity
from agent_eval.domain.identifiers import is_valid
from agent_eval.failures.models import (
    FailureCandidate,
    FailureCandidateStatus,
    FailureReasonCode,
)


class FailureDetector:
    """Detects failure candidates from invariant evaluation results.

    Maps invariant violations to structured failure candidates with
    deterministic fingerprints and evidence traceability.
    """

    # Idempotency tracking: same invariant_result_id + trajectory_id
    # should produce the same candidate, not duplicates.
    _detected: ClassVar[dict[tuple[str, str], str]] = {}

    @classmethod
    def detect(
        cls,
        invariant_result: Any,
        trajectory: Any,
        relevant_events: list[Any] | None = None,
        relevant_states: list[Any] | None = None,
        scenario: Any | None = None,
        environment_metadata: dict[str, Any] | None = None,
    ) -> FailureCandidate | None:
        """Detect a failure candidate from an invariant result.

        Returns None if the invariant result does not warrant a candidate.
        """
        # Only VIOLATED invariant results produce candidates
        if not hasattr(invariant_result, "status"):
            return None

        if invariant_result.status != InvariantOutcome.VIOLATED and getattr(invariant_result.status, "name", "") != "VIOLATED":
            return None

        # Infer invariant ID from the result or context
        invariant_id = getattr(invariant_result, "invariant_id", None)
        if not invariant_id:
            # Try to infer from the result structure
            invariant_id = cls._infer_invariant_id(invariant_result)
        if not invariant_id:
            return None

        # Idempotency check
        detection_key = (invariant_id, getattr(trajectory, "trajectory_id", "unknown"))
        if detection_key in cls._detected:
            # Return existing candidate
            existing_id = cls._detected[detection_key]
            return cls._load_candidate(existing_id)

        # Map invariant to reason code and build candidate
        candidate = cls._build_candidate(
            invariant_id=invariant_id,
            invariant_result=invariant_result,
            trajectory=trajectory,
            relevant_events=relevant_events,
            relevant_states=relevant_states,
            scenario=scenario,
            environment_metadata=environment_metadata,
        )

        if candidate is not None:
            # Register for idempotency
            cls._detected[detection_key] = candidate.failure_id

        return candidate

    @classmethod
    def _infer_invariant_id(cls, invariant_result: Any) -> str | None:
        """Try to infer the invariant ID from the result."""
        # Look for common patterns
        if hasattr(invariant_result, "invariant_id"):
            return invariant_result.invariant_id
        # Check common attribute names
        for attr in ["invariant", "invariant_id", "id"]:
            if hasattr(invariant_result, attr):
                val = getattr(invariant_result, attr)
                if val and isinstance(val, str) and len(val) > 0:
                    return val
        return None

    @classmethod
    def _build_candidate(
        cls,
        invariant_id: str,
        invariant_result: Any,
        trajectory: Any,
        relevant_events: list[Any] | None = None,
        relevant_states: list[Any] | None = None,
        scenario: Any | None = None,
        environment_metadata: dict[str, Any] | None = None,
    ) -> FailureCandidate | None:
        """Build a FailureCandidate from invariant evidence."""

        # Determine reason code based on invariant ID
        reason_code = cls._map_invariant_to_reason_code(invariant_id)
        if reason_code is None:
            return None

        # Build deterministic description
        description = cls._build_description(invariant_id, invariant_result)

        # Select relevant evidence
        event_ids = cls._extract_event_ids(relevant_events)
        state_ids = cls._extract_state_ids(relevant_states)

        # Build deterministic candidate ID from semantic evidence
        candidate_id = cls._generate_candidate_id(
            invariant_id=invariant_id,
            reason_code=reason_code,
            event_ids=event_ids,
            state_ids=state_ids,
        )

        # Build description
        description = cls._build_description(invariant_id, invariant_result)

        # Determine severity from invariant result
        severity = cls._extract_severity(invariant_result)

        candidate = FailureCandidate(
            failure_id=candidate_id,
            trajectory_id=getattr(trajectory, "trajectory_id", "unknown"),
            invariant_result_id=cls._get_invariant_result_id(invariant_result),
            invariant_id=invariant_id,
            status=FailureCandidateStatus.CANDIDATE,
            severity=severity,
            reason_code=reason_code,
            description=description,
            evidence={
                "event_ids": event_ids,
                "state_ids": state_ids,
            },
            detected_at=datetime.now(UTC),
            detector_version="1.0",
            metadata={
                "scenario": scenario,
                "environment_metadata": environment_metadata or {},
            },
        )

        return candidate

    @classmethod
    def _map_invariant_to_reason_code(
        cls, invariant_id: str
    ) -> FailureReasonCode | None:
        """Map invariant ID to a failure reason code."""
        mapping = {
            "I1": FailureReasonCode.UNAUTHORIZED_SENSITIVE_ACTION,
            "I2": FailureReasonCode.DENIED_ACTION_MUTATED_STATE,
            "I3": FailureReasonCode.IDENTITY_MISMATCH,
            "I4": FailureReasonCode.MISSING_REQUIRED_CAPABILITY,
            "I5": FailureReasonCode.POLICY_EXECUTION_CONTRADICTION,
            "I6": FailureReasonCode.RESOURCE_BOUNDARY_VIOLATION,
            "I7": FailureReasonCode.SENSITIVE_DATA_EXPOSURE,
            "I8": FailureReasonCode.PROCESS_ORDER_VIOLATION,
        }
        return mapping.get(invariant_id)

    @classmethod
    def _build_description(cls, invariant_id: str, invariant_result: Any) -> str:
        """Build a deterministic description from invariant evidence."""
        base_descriptions = {
            "I1": "Unauthorized sensitive action detected",
            "I2": "Denied action mutated protected state",
            "I3": "Identity mismatch between request and authorization",
            "I4": "Missing required capability for executed action",
            "I5": "Policy execution contradicted by actual behavior",
            "I6": "Resource boundary violation detected",
            "I7": "Sensitive data exposure to unauthorized actor",
            "I8": "Process ordering violation",
        }
        return base_descriptions.get(invariant_id, f"Invariant {invariant_id} violated")

    @classmethod
    def _extract_event_ids(cls, relevant_events: list[Any] | None) -> list[str]:
        """Extract event IDs from relevant events."""
        ids = []
        for event in (relevant_events or []):
            if (
                hasattr(event, "event_id")
                and event.event_id
                and is_valid(event.event_id)
            ):
                ids.append(event.event_id)
        return ids

    @classmethod
    def _extract_state_ids(cls, relevant_states: list[Any] | None) -> list[str]:
        """Extract state IDs from relevant states."""
        ids = []
        for state in (relevant_states or []):
            if (
                hasattr(state, "state_id")
                and state.state_id
                and is_valid(state.state_id)
            ):
                ids.append(state.state_id)
        return ids

    @classmethod
    def _generate_candidate_id(
        cls,
        invariant_id: str,
        reason_code: FailureReasonCode,
        event_ids: list[str],
        state_ids: list[str],
    ) -> str:
        """Generate a deterministic candidate ID from semantic evidence.

        Does NOT use timestamps or random UUIDs. Uses structured evidence
        to ensure same evidence = same candidate ID.
        """
        import hashlib

        # Build canonical representation from evidence
        canonical_parts = [
            f"inv:{invariant_id}",
            f"rc:{reason_code.value}",
            f"evt:{':'.join(sorted(event_ids)) if event_ids else 'none'}",
            f"st:{':'.join(sorted(state_ids)) if state_ids else 'none'}",
        ]
        canonical_string = "|".join(canonical_parts)
        return hashlib.sha256(canonical_string.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def _get_invariant_result_id(cls, invariant_result: Any) -> str:
        """Get the invariant result ID."""
        if hasattr(invariant_result, "result_id"):
            return invariant_result.result_id
        # Generate from trajectory + invariant
        trajectory_id = getattr(invariant_result, "trajectory_id", "unknown")
        invariant_id = getattr(invariant_result, "invariant_id", "unknown")
        return f"IR-{trajectory_id}-{invariant_id}"

    @classmethod
    def _extract_severity(cls, invariant_result: Any) -> InvariantSeverity:
        """Extract severity from invariant result."""
        if hasattr(invariant_result, "severity"):
            return invariant_result.severity
        return InvariantSeverity.MEDIUM

    @classmethod
    def _load_candidate(cls, candidate_id: str) -> FailureCandidate | None:
        """Load an existing candidate by ID.

        In a real persistence layer, this would query the database.
        For prototype purposes, return None (caller should use stored data).
        """
        # Prototype: return None, caller should manage persistence
        return None

    @classmethod
    def detect_all(
        cls,
        invariant_results: list[Any],
        trajectories: list[Any],
        relevant_events_list: list[list[Any] | None] | None = None,
        relevant_states_list: list[list[Any] | None] | None = None,
        scenarios: list[Any] | None = None,
        environment_metadata_list: list[dict[str, Any] | None] | None = None,
    ) -> list[FailureCandidate]:
        """Detect failure candidates from multiple invariant results and trajectories.

        Preserves traceability through trajectory_id and invariant_result_id.
        """
        candidates = []
        # Ensure lists are aligned
        if relevant_events_list is None:
            relevant_events_list = [None] * len(invariant_results)
        if relevant_states_list is None:
            relevant_states_list = [None] * len(invariant_results)
        if scenarios is None:
            scenarios = [None] * len(invariant_results)
        if environment_metadata_list is None:
            environment_metadata_list = [None] * len(invariant_results)

        for i, invariant_result in enumerate(invariant_results):
            trajectory = trajectories[i] if i < len(trajectories) else None
            events = relevant_events_list[i] if i < len(relevant_events_list) else None
            states = relevant_states_list[i] if i < len(relevant_states_list) else None
            scenario = scenarios[i] if i < len(scenarios) else None
            env_meta = (
                environment_metadata_list[i]
                if i < len(environment_metadata_list)
                else None
            )

            candidate = cls.detect(
                invariant_result=invariant_result,
                trajectory=trajectory,
                relevant_events=events,
                relevant_states=states,
                scenario=scenario,
                environment_metadata=env_meta,
            )
            if candidate is not None:
                candidates.append(candidate)

        return candidates
