"""Evidence management for failure candidate detection.

Handles validation that referenced evidence actually exists in the trajectory,
ensuring candidate creation is idempotent and auditable.
"""

from __future__ import annotations

from typing import Any

from agent_eval.domain.identifiers import is_valid


class EvidenceValidator:
    """Validates that failure candidate evidence references are valid."""

    @classmethod
    def validate_event_references(
        cls,
        event_ids: list[str],
        available_events: list[Any],
    ) -> tuple[bool, list[str]]:
        """Validate that referenced event IDs exist in the available events.

        Returns (is_valid, list_of_missing_ids).
        """
        available_ids = set()
        for event in available_events:
            if (
                hasattr(event, "event_id")
                and event.event_id
                and is_valid(event.event_id)
            ):
                available_ids.add(event.event_id)

        missing = []
        for requested_id in event_ids:
            if not is_valid(requested_id):
                missing.append(f"invalid_id:{requested_id}")
            elif requested_id not in available_ids:
                missing.append(requested_id)

        return len(missing) == 0, missing

    @classmethod
    def validate_state_references(
        cls,
        state_ids: list[str],
        available_states: list[Any],
    ) -> tuple[bool, list[str]]:
        """Validate that referenced state IDs exist in the available states.

        Returns (is_valid, list_of_missing_ids).
        """
        available_ids = set()
        for state in available_states:
            if (
                hasattr(state, "state_id")
                and state.state_id
                and is_valid(state.state_id)
            ):
                available_ids.add(state.state_id)

        missing = []
        for requested_id in state_ids:
            if not is_valid(requested_id):
                missing.append(f"invalid_id:{requested_id}")
            elif requested_id not in available_ids:
                missing.append(requested_id)

        return len(missing) == 0, missing

    @classmethod
    def validate_trajectory_reference(
        cls,
        trajectory_id: str,
        available_trajectories: list[Any],
    ) -> bool:
        """Validate that a trajectory ID references an existing trajectory.

        Returns True if the trajectory ID is found.
        """
        for traj in available_trajectories:
            if hasattr(traj, "trajectory_id") and traj.trajectory_id == trajectory_id:
                return True
        return False


class EvidenceIntegrityError(ValueError):
    """Raised when evidence references are invalid."""
