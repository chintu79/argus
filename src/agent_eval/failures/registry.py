"""Failure candidate registry.

Manages persistent and in-memory tracking of failure candidates,
ensuring idempotency and retrieval by various keys.
"""

from __future__ import annotations

from agent_eval.failures.models import FailureCandidate


class FailureCandidateRegistry:
    """Registry for tracking failure candidates.

    Supports retrieval by:
    - failure_id
    - trajectory_id
    - invariant_id
    - reason_code
    - list all candidates
    """

    def __init__(self):
        # Primary store: failure_id -> FailureCandidate
        self._by_id: dict[str, FailureCandidate] = {}

        # Secondary indexes
        self._by_trajectory: dict[
            str, list[str]
        ] = {}  # trajectory_id -> [failure_id, ...]
        self._by_invariant: dict[
            str, list[str]
        ] = {}  # invariant_id -> [failure_id, ...]
        self._by_reason: dict[str, list[str]] = {}  # reason_code -> [failure_id, ...]

    def add(self, candidate: FailureCandidate) -> str:
        """Add a failure candidate to the registry.

        Returns the failure_id. If a candidate with the same ID already exists,
        it is returned without duplication (idempotency).
        """
        fid = candidate.failure_id

        # Idempotency: if already registered, return existing
        if fid in self._by_id:
            return fid

        self._by_id[fid] = candidate

        # Update secondary indexes
        trajectory_id = candidate.trajectory_id
        invariant_id = candidate.invariant_id
        reason_code = candidate.reason_code.value

        if trajectory_id not in self._by_trajectory:
            self._by_trajectory[trajectory_id] = []
        if fid not in self._by_trajectory[trajectory_id]:
            self._by_trajectory[trajectory_id].append(fid)

        if invariant_id not in self._by_invariant:
            self._by_invariant[invariant_id] = []
        if fid not in self._by_invariant[invariant_id]:
            self._by_invariant[invariant_id].append(fid)

        if reason_code not in self._by_reason:
            self._by_reason[reason_code] = []
        if fid not in self._by_reason[reason_code]:
            self._by_reason[reason_code].append(fid)

        return fid

    def get(self, failure_id: str) -> FailureCandidate | None:
        """Get a failure candidate by ID."""
        return self._by_id.get(failure_id)

    def get_by_trajectory(self, trajectory_id: str) -> list[FailureCandidate]:
        """Get all failure candidates for a trajectory."""
        failure_ids = self._by_trajectory.get(trajectory_id, [])
        return [self._by_id[fid] for fid in failure_ids if fid in self._by_id]

    def get_by_invariant(self, invariant_id: str) -> list[FailureCandidate]:
        """Get all failure candidates for a given invariant."""
        failure_ids = self._by_invariant.get(invariant_id, [])
        return [self._by_id[fid] for fid in failure_ids if fid in self._by_id]

    def get_by_reason_code(self, reason_code: str) -> list[FailureCandidate]:
        """Get all failure candidates with a given reason code."""
        failure_ids = self._by_reason.get(reason_code, [])
        return [self._by_id[fid] for fid in failure_ids if fid in self._by_id]

    def list_all(self) -> list[FailureCandidate]:
        """List all failure candidates."""
        return list(self._by_id.values())

    def remove(self, failure_id: str) -> bool:
        """Remove a failure candidate by ID."""
        if failure_id not in self._by_id:
            return False

        candidate = self._by_id.pop(failure_id)

        # Update secondary indexes
        trajectory_id = candidate.trajectory_id
        invariant_id = candidate.invariant_id
        reason_code = candidate.reason_code.value

        if trajectory_id in self._by_trajectory:
            if failure_id in self._by_trajectory[trajectory_id]:
                self._by_trajectory[trajectory_id].remove(failure_id)
            if not self._by_trajectory[trajectory_id]:
                del self._by_trajectory[trajectory_id]

        if invariant_id in self._by_invariant:
            if failure_id in self._by_invariant[invariant_id]:
                self._by_invariant[invariant_id].remove(failure_id)
            if not self._by_invariant[invariant_id]:
                del self._by_invariant[invariant_id]

        if reason_code in self._by_reason:
            if failure_id in self._by_reason[reason_code]:
                self._by_reason[reason_code].remove(failure_id)
            if not self._by_reason[reason_code]:
                del self._by_reason[reason_code]

        return True


# Global registry instance
_failure_candidate_registry: FailureCandidateRegistry | None = None


def get_failure_candidate_registry() -> FailureCandidateRegistry:
    """Get the global failure candidate registry (singleton)."""
    global _failure_candidate_registry
    if _failure_candidate_registry is None:
        _failure_candidate_registry = FailureCandidateRegistry()
    return _failure_candidate_registry
