"""Repository for failure family persistence."""

from __future__ import annotations

from typing import Any


class FailureFamilyRepository:
    """Repository for storing and retrieving failure families."""

    def __init__(self):
        # In-memory stores (would be replaced with database in production)
        self._families: dict[str, Any] = {}
        self._runs: dict[str, Any] = {}

        # Indexes
        self._families_by_member: dict[str, list[str]] = {}
        self._runs_by_failure: dict[str, list[str]] = {}

    # ── Families ──────────────────────────────────────────────

    def save_family(self, family: Any) -> str:
        """Save a failure family."""
        # Validate
        if not family.family_id or not family.family_id.strip():
            raise ValueError("Family must have a valid family_id")

        if not family.member_failure_ids:
            raise ValueError("Family must have at least one member")

        if family.representative_failure_id not in family.member_failure_ids:
            raise ValueError("Representative must be a member of the family")

        self._families[family.family_id] = family

        # Update member index
        for mid in family.member_failure_ids:
            if mid not in self._families_by_member:
                self._families_by_member[mid] = []
            if family.family_id not in self._families_by_member[mid]:
                self._families_by_member[mid].append(family.family_id)

        return family.family_id

    def get_family(self, family_id: str) -> Any | None:
        """Get a family by ID."""
        return self._families.get(family_id)

    def get_families_by_member(self, failure_id: str) -> list[Any]:
        """Get all families containing a given failure."""
        family_ids = self._families_by_member.get(failure_id, [])
        return [self._families[fid] for fid in family_ids if fid in self._families]

    def get_family_for_failure(self, failure_id: str) -> Any | None:
        """Get the single family containing a failure (assuming no overlaps)."""
        families = self.get_families_by_member(failure_id)
        if not families:
            return None
        if len(families) > 1:
            # Should not happen with proper validation
            return families[0]
        return families[0]

    def list_families(self) -> list[Any]:
        """List all families."""
        return list(self._families.values())

    def list_family_ids(self) -> list[str]:
        return list(self._families.keys())

    def delete_family(self, family_id: str) -> bool:
        """Delete a family."""
        if family_id not in self._families:
            return False

        family = self._families[family_id]

        # Remove from member index
        for mid in family.member_failure_ids:
            if mid in self._families_by_member:
                if family_id in self._families_by_member[mid]:
                    self._families_by_member[mid].remove(family_id)
                if not self._families_by_member[mid]:
                    del self._families_by_member[mid]

        del self._families[family_id]
        return True

    def search_families(
        self,
        invariant_id: str | None = None,
        reason_code: str | None = None,
        taxonomy_label: str | None = None,
        min_size: int | None = None,
        min_coherence: float | None = None,
    ) -> list[Any]:
        """Search families by criteria."""
        results = list(self._families.values())

        if invariant_id:
            results = [
                f for f in results if f.invariant_distribution.get(invariant_id, 0) > 0
            ]

        if reason_code:
            results = [
                f for f in results if f.reason_code_distribution.get(reason_code, 0) > 0
            ]

        if taxonomy_label:
            results = [f for f in results if taxonomy_label in f.taxonomy_labels]

        if min_size is not None:
            results = [f for f in results if f.family_size >= min_size]

        if min_coherence is not None:
            results = [f for f in results if f.coherence_score >= min_coherence]

        return results

    def get_statistics(self) -> dict[str, Any]:
        """Get repository statistics."""
        families = list(self._families.values())

        if not families:
            return {
                "family_count": 0,
                "total_members": 0,
                "singleton_count": 0,
                "average_size": 0.0,
                "average_coherence": 0.0,
            }

        total_members = sum(f.family_size for f in families)
        singletons = sum(1 for f in self._families.values() if f.family_size == 1)

        return {
            "family_count": len(families),
            "total_members": sum(f.family_size for f in families),
            "singleton_count": singletons,
            "average_size": total_members / len(families) if families else 0.0,
            "average_coherence": sum(f.coherence_score for f in families)
            / len(families),
        }

    # ── Clustering Runs ──────────────────────────────────────

    def save_run(self, run: Any) -> str:
        """Save a clustering run."""
        self._runs[run.run_id] = run
        return run.run_id

    def get_run(self, run_id: str) -> Any | None:
        return self._runs.get(run_id)

    def list_runs(self) -> list[Any]:
        return list(self._runs.values())

    def get_latest_run(self) -> Any | None:
        if not self._runs:
            return None
        return max(self._runs.values(), key=lambda r: r.created_at)


class FailureFamilyRepositoryImpl(FailureFamilyRepository):
    """Implementation of FailureFamilyRepository with persistence."""

    def __init__(self):
        super().__init__()
        # In production, this would connect to a database


# Global repository instance
_failure_family_repository: FailureFamilyRepository | None = None


def get_failure_family_repository() -> FailureFamilyRepository:
    """Get the global failure family repository (singleton)."""
    global _failure_family_repository
    if _failure_family_repository is None:
        _failure_family_repository = FailureFamilyRepository()
    return _failure_family_repository
