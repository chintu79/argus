"""Signature extraction and comparison for reproducibility verification.

Deterministic failure signature extraction from trajectories and
canonical comparison logic.
"""

from __future__ import annotations

from typing import Any

from agent_eval.reproducibility.models import (
    FailureSignature,
    SignatureMatchResult,
)


class SignatureExtractor:
    """Extracts deterministic failure signatures from trajectories and invariant results."""

    @classmethod
    def extract_from_failure_candidate(
        cls,
        failure_candidate: Any,
        trajectory: Any,
    ) -> FailureSignature:
        """Extract a canonical failure signature from a failure candidate and its trajectory."""
        # Extract invariant ID from failure candidate
        invariant_id = getattr(failure_candidate, "invariant_id", None)
        if not invariant_id:
            # Try to infer from trajectory or other context
            invariant_id = cls._infer_invariant_id(trajectory)
            if not invariant_id:
                invariant_id = "unknown"

        # Extract reason code
        reason_code = getattr(failure_candidate, "reason_code", None)
        if not reason_code and hasattr(failure_candidate, "reason_code"):
            reason_code = (
                failure_candidate.reason_code.value
                if hasattr(failure_candidate.reason_code, "value")
                else failure_candidate.reason_code
            )
        if not reason_code:
            # Map invariant ID to reason code
            reason_code = cls._map_invariant_to_reason_code(invariant_id)

        # Extract relevant evidence from trajectory
        action = cls._extract_action(trajectory, failure_candidate)
        resource = cls._extract_resource(trajectory, failure_candidate)
        state_transition = cls._extract_state_transition(trajectory)
        resource_type = cls._extract_resource_type(trajectory)
        policy_decision = cls._extract_policy_decision(trajectory)

        return FailureSignature(
            invariant_id=invariant_id,
            reason_code=reason_code,
            action=action,
            resource=resource,
            state_transition=state_transition,
            resource_type=resource_type,
            policy_decision=policy_decision,
        )

    @classmethod
    def extract_from_trajectory_and_results(
        cls,
        trajectory: Any,
        invariant_results: list[Any],
    ) -> list[FailureSignature]:
        """Extract failure signatures from a trajectory and its invariant results."""
        signatures = []

        for result in invariant_results:
            if not hasattr(result, "status") or result.status.name != "VIOLATED":
                continue

            invariant_id = getattr(result, "invariant_id", "unknown")
            reason_code = cls._map_invariant_to_reason_code(invariant_id)

            action = cls._extract_action_from_result(result)
            resource = cls._extract_resource_from_result(result)
            state_transition = cls._extract_state_transition_from_result(result)
            resource_type = cls._extract_resource_type_from_result(result)
            policy_decision = cls._extract_policy_decision_from_result(result)

            signature = FailureSignature(
                invariant_id=invariant_id,
                reason_code=reason_code,
                action=action,
                resource=resource,
                state_transition=state_transition,
                resource_type=resource_type,
                policy_decision=policy_decision,
            )
            signatures.append(signature)

        return signatures

    @staticmethod
    def _infer_invariant_id(trajectory: Any) -> str | None:
        """Try to infer invariant ID from trajectory context."""
        # Check if trajectory has invariant evaluation results
        if hasattr(trajectory, "invariant_results"):
            for result in trajectory.invariant_results:
                if hasattr(result, "status") and result.status.name == "VIOLATED":
                    return getattr(result, "invariant_id", None)
        return None

    @staticmethod
    def _map_invariant_to_reason_code(invariant_id: str) -> str:
        """Map invariant ID to reason code."""
        mapping = {
            "I1": "UNAUTHORIZED_SENSITIVE_ACTION",
            "I2": "DENIED_ACTION_MUTATED_STATE",
            "I3": "IDENTITY_MISMATCH",
            "I4": "MISSING_REQUIRED_CAPABILITY",
            "I5": "POLICY_EXECUTION_CONTRADICTION",
            "I6": "RESOURCE_BOUNDARY_VIOLATION",
            "I7": "SENSITIVE_DATA_EXPOSURE",
            "I8": "PROCESS_ORDER_VIOLATION",
        }
        return mapping.get(invariant_id, "UNKNOWN_REASON_CODE")

    @staticmethod
    def _extract_action(trajectory: Any, failure_candidate: Any) -> str | None:
        """Extract the action that triggered the violation."""
        # Look at the failure candidate's evidence
        if hasattr(failure_candidate, "evidence"):
            evidence = failure_candidate.evidence
            if isinstance(evidence, dict):
                # Check for tool name in evidence
                if "tool_name" in evidence:
                    return evidence["tool_name"]
                # Check for action in metadata
                if "action" in evidence:
                    return evidence["action"]

        # Look through trajectory events for tool requests
        if hasattr(trajectory, "events"):
            for event in trajectory.events:
                if (
                    hasattr(event, "event_type")
                    and event.event_type.name == "TOOL_REQUEST"
                ) and hasattr(event, "payload") and "tool_name" in event.payload:
                    return event.payload["tool_name"]

        return None

    @staticmethod
    def _extract_resource(trajectory: Any, failure_candidate: Any) -> str | None:
        """Extract the resource involved in the violation."""
        if hasattr(failure_candidate, "evidence"):
            evidence = failure_candidate.evidence
            if isinstance(evidence, dict):
                if "resource_id" in evidence:
                    return evidence["resource_id"]
                if "resource" in evidence:
                    return evidence["resource"]

        # Look through trajectory events for resource identifiers
        if hasattr(trajectory, "events"):
            for event in trajectory.events:
                if hasattr(event, "payload") and isinstance(event.payload, dict) and "resource_id" in event.payload:
                    return event.payload["resource_id"]

        return None

    @staticmethod
    def _extract_state_transition(trajectory: Any) -> str | None:
        """Extract state transition pattern from trajectory."""
        if not hasattr(trajectory, "events"):
            return None

        state_events = []
        for event in trajectory.events:
            if (
                hasattr(event, "event_type")
                and event.event_type.name == "STATE_TRANSITION"
            ) and hasattr(event, "payload") and isinstance(event.payload, dict):
                state_events.append(event.payload)

        if not state_events:
            return None

        # Build transition description from first relevant state change
        for se in state_events:
            if se.get("changed_components"):
                components = se["changed_components"]
                if isinstance(components, list) and components:
                    return f"CHANGED({':'.join(components)})"

        return "STATE_CHANGED" if state_events else None

    @staticmethod
    def _extract_resource_type(trajectory: Any) -> str | None:
        """Extract the type of resource involved."""
        if hasattr(trajectory, "events"):
            for event in trajectory.events:
                if hasattr(event, "payload") and isinstance(event.payload, dict) and "resource_type" in event.payload:
                    return event.payload["resource_type"]

        # Infer from tool names
        if hasattr(trajectory, "events"):
            for event in trajectory.events:
                if hasattr(event, "payload") and isinstance(event.payload, dict):
                    tool_name = event.payload.get("tool_name", "")
                    if "customer" in tool_name:
                        return "customer"
                    elif "account" in tool_name:
                        return "account"
                    elif "transaction" in tool_name:
                        return "transaction"
                    elif "ticket" in tool_name:
                        return "ticket"

        return None

    @staticmethod
    def _extract_policy_decision(trajectory: Any) -> str | None:
        """Extract the policy decision that occurred."""
        if hasattr(trajectory, "events"):
            for event in trajectory.events:
                if (
                    hasattr(event, "event_type")
                    and event.event_type.name == "POLICY_DECISION"
                ) and hasattr(event, "payload") and isinstance(event.payload, dict):
                    return event.payload.get("decision")

        return None

    @staticmethod
    def _extract_action_from_result(result: Any) -> str | None:
        """Extract action from invariant result."""
        if hasattr(result, "payload") and isinstance(result.payload, dict):
            return result.payload.get("action") or result.payload.get("tool_name")
        if hasattr(result, "action"):
            return result.action
        return None

    @staticmethod
    def _extract_resource_from_result(result: Any) -> str | None:
        """Extract resource from invariant result."""
        if hasattr(result, "payload") and isinstance(result.payload, dict):
            return result.payload.get("resource_id") or result.payload.get("resource")
        if hasattr(result, "resource"):
            return result.resource
        return None

    @staticmethod
    def _extract_state_transition_from_result(result: Any) -> str | None:
        """Extract state transition from invariant result."""
        if hasattr(result, "payload") and isinstance(result.payload, dict):
            return result.payload.get("state_transition")
        if hasattr(result, "state_transition"):
            return result.state_transition
        return None

    @staticmethod
    def _extract_resource_type_from_result(result: Any) -> str | None:
        """Extract resource type from invariant result."""
        if hasattr(result, "payload") and isinstance(result.payload, dict):
            return result.payload.get("resource_type")
        if hasattr(result, "resource_type"):
            return result.resource_type
        return None

    @staticmethod
    def _extract_policy_decision_from_result(result: Any) -> str | None:
        """Extract policy decision from invariant result."""
        if hasattr(result, "payload") and isinstance(result.payload, dict):
            return result.payload.get("policy_decision")
        if hasattr(result, "policy_decision"):
            return result.policy_decision
        return None


class SignatureComparator:
    """Compares failure signatures for reproducibility determination."""

    @classmethod
    def compare(
        cls,
        expected: FailureSignature,
        observed: FailureSignature,
    ) -> SignatureMatchResult:
        """Compare expected failure signature with observed signature.

        Returns MATCH, NO_MATCH, or INCONCLUSIVE.
        """
        # Primary matching on invariant_id and reason_code
        if expected.invariant_id != observed.invariant_id:
            return SignatureMatchResult.NO_MATCH

        if expected.reason_code != observed.reason_code:
            return SignatureMatchResult.NO_MATCH

        # Secondary fields: check if they match when both are present
        # If one is missing but the other has it, return INCONCLUSIVE
        secondary_fields = [
            ("action", expected.action, observed.action),
            ("resource", expected.resource, observed.resource),
            ("state_transition", expected.state_transition, observed.state_transition),
            ("resource_type", expected.resource_type, observed.resource_type),
            ("policy_decision", expected.policy_decision, observed.policy_decision),
        ]

        for _field_name, expected_val, observed_val in secondary_fields:
            if expected_val is not None and observed_val is not None:
                if expected_val != observed_val:
                    return SignatureMatchResult.NO_MATCH
            elif expected_val is not None and observed_val is None:
                # Expected has value but observed doesn't - inconclusive
                return SignatureMatchResult.INCONCLUSIVE
            elif expected_val is None and observed_val is not None:
                # Observed has extra info - that's okay
                pass

        # If we get here, primary fields match and no secondary conflicts
        return SignatureMatchResult.MATCH

    @classmethod
    def compare_against_list(
        cls,
        expected: FailureSignature,
        observed_list: list[FailureSignature],
    ) -> SignatureMatchResult:
        """Compare expected signature against a list of observed signatures.

        Returns MATCH if any observed signature matches.
        Returns INCONCLUSIVE if some are inconclusive and none match.
        Returns NO_MATCH if all are NO_MATCH.
        """
        any_inconclusive = False

        for observed in observed_list:
            result = cls.compare(expected, observed)
            if result == SignatureMatchResult.MATCH:
                return SignatureMatchResult.MATCH
            elif result == SignatureMatchResult.INCONCLUSIVE:
                any_inconclusive = True

        if any_inconclusive:
            return SignatureMatchResult.INCONCLUSIVE

        return SignatureMatchResult.NO_MATCH
