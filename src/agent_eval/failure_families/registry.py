"""Failure family registry for tracking and managing families."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from agent_eval.domain.identifiers import make_id


class FailureFamilyRegistry:
    """Registry for managing failure families."""

    def __init__(self):
        # Primary store: family_id -> FailureFamily
        self._families: dict[str, Any] = {}

        # Secondary indexes
        self._by_member: dict[str, str] = {}  # failure_id -> family_id
        self._by_invariant: dict[str, list[str]] = defaultdict(list)
        self._by_reason_code: dict[str, list[str]] = defaultdict(list)
        self._by_taxonomy: dict[str, list[str]] = defaultdict(list)

        # Clustering run history
        self._runs: dict[str, Any] = {}

        # Fingerprint index for deterministic identity
        self._fingerprints: dict[str, str] = {}  # canonical_signature -> family_id

    def add_family(self, family: Any) -> str:
        """Add a failure family to the registry.

        Returns the family_id. If a family with the same canonical signature
        already exists, returns the existing family_id (idempotency).
        """
        # Compute canonical fingerprint
        fingerprint = family.family_signature

        # Idempotency: check if family with same signature exists
        if fingerprint in self._fingerprints:
            existing_id = self._fingerprints[fingerprint]
            existing_family = self._families[existing_id]
            # Merge members if new family has additional members
            new_members = set(family.member_failure_ids)
            existing_members = set(self._families[existing_id].member_failure_ids)
            merged_members = sorted(existing_members | new_members)

            if set(merged_members) != existing_members:
                # Update existing family
                existing_family = self._families[existing_id]
                existing_family.member_failure_ids = merged_members
                existing_family.family_size = len(merged_members)
                self._reindex_family(existing_id)

            return existing_id

        # New family
        family_id = family.family_id
        if not family_id.startswith("FF-"):
            family_id = f"FF-{make_id('ff')}"
            family.family_id = family_id

        self._families[family_id] = family
        self._fingerprints[fingerprint] = family_id
        self._reindex_family(family_id)

        return family_id

    def _reindex_family(self, family_id: str):
        """Update secondary indexes for a family."""
        family = self._families[family_id]

        for mid in family.member_failure_ids:
            self._by_member[mid] = family_id
            # Find the failure to get its invariant and reason code
            # This would require access to the failure objects
            # For now, we'll index by failure_id only

        # Index by taxonomy
        for label in family.taxonomy_labels:
            if family_id not in self._by_taxonomy[label]:
                self._by_taxonomy[label].append(family_id)

    def get_family(self, family_id: str) -> Any | None:
        """Get a family by ID."""
        return self._families.get(family_id)

    def get_family_by_fingerprint(self, fingerprint: str) -> Any | None:
        """Get a family by its canonical fingerprint."""
        family_id = self._fingerprints.get(fingerprint)
        if family_id:
            return self._families.get(family_id)
        return None

    def get_family_for_failure(self, failure_id: str) -> Any | None:
        """Get the family that contains a given failure."""
        family_id = self._by_member.get(failure_id)
        if family_id:
            return self._families.get(family_id)
        return None

    def get_families_by_invariant(self, invariant_id: str) -> list[Any]:
        """Get all families containing failures with a given invariant."""
        return [self._families[fid] for fid in self._by_invariant.get(invariant_id, [])]

    def get_families_by_reason_code(self, reason_code: str) -> list[Any]:
        """Get all families containing failures with a given reason code."""
        return [
            self._families[fid] for fid in self._by_reason_code.get(reason_code, [])
        ]

    def get_families_by_taxonomy(self, taxonomy_label: str) -> list[Any]:
        """Get all families with a given taxonomy label."""
        return [
            self._families[fid] for fid in self._by_taxonomy.get(taxonomy_label, [])
        ]

    def list_families(self) -> list[Any]:
        """List all families."""
        return list(self._families.values())

    def list_family_ids(self) -> list[str]:
        """List all family IDs."""
        return list(self._families.keys())

    def get_family_count(self) -> int:
        """Get total number of families."""
        return len(self._families)

    def get_member_count(self) -> int:
        """Get total number of member failures across all families."""
        return sum(len(f.member_failure_ids) for f in self._families.values())

    def get_singleton_count(self) -> int:
        """Get number of singleton families."""
        return sum(1 for f in self._families.values() if f.family_size == 1)

    def get_average_family_size(self) -> float:
        """Get average family size."""
        if not self._families:
            return 0.0
        return sum(f.family_size for f in self._families.values()) / len(self._families)

    def get_average_coherence(self) -> float:
        """Get average coherence across all families."""
        if not self._families:
            return 0.0
        return sum(f.coherence_score for f in self._families.values()) / len(
            self._families
        )

    def remove_family(self, family_id: str) -> bool:
        """Remove a family from the registry."""
        if family_id not in self._families:
            return False

        family = self._families[family_id]

        # Remove from member index
        for mid in family.member_failure_ids:
            if self._by_member.get(mid) == family_id:
                del self._by_member[mid]

        # Remove from fingerprint index
        fingerprint = family.family_signature
        if (
            fingerprint in self._fingerprints
            and self._fingerprints[fingerprint] == family_id
        ):
            del self._fingerprints[fingerprint]

        # Remove from taxonomy index
        for label in family.taxonomy_labels:
            if family_id in self._by_taxonomy.get(label, []):
                self._by_taxonomy[label].remove(family_id)
                if not self._by_taxonomy[label]:
                    del self._by_taxonomy[label]

        # Remove family
        del self._families[family_id]
        return True

    def clear(self):
        """Clear the registry."""
        self._families.clear()
        self._by_member.clear()
        self._by_invariant.clear()
        self._by_reason_code.clear()
        self._by_taxonomy.clear()
        self._fingerprints.clear()

    def get_statistics(self) -> dict[str, Any]:
        """Get registry statistics."""
        if not self._families:
            return {
                "family_count": 0,
                "total_members": 0,
                "singleton_count": 0,
                "average_size": 0.0,
                "average_coherence": 0.0,
            }

        families = list(self._families.values())

        return {
            "family_count": len(families),
            "total_members": sum(f.family_size for f in families),
            "singleton_count": sum(1 for f in families if f.family_size == 1),
            "average_size": sum(f.family_size for f in families) / len(families),
            "average_coherence": sum(f.coherence_score for f in families)
            / len(families),
            "taxonomy_distribution": {
                label: len(fids) for label, fids in self._by_taxonomy.items()
            },
        }


class ClusteringRunRegistry:
    """Registry for clustering run history."""

    def __init__(self):
        self._runs: dict[str, Any] = {}

    def add_run(self, run: Any) -> str:
        """Add a clustering run record."""
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

    def clear(self):
        self._runs.clear()


# Global registries
_family_registry: FailureFamilyRegistry | None = None
_run_registry: ClusteringRunRegistry | None = None


def get_failure_family_registry() -> FailureFamilyRegistry:
    """Get the global failure family registry (singleton)."""
    global _family_registry
    if _family_registry is None:
        _family_registry = FailureFamilyRegistry()
    return _family_registry


def get_clustering_run_registry() -> ClusteringRunRegistry:
    """Get the global clustering run registry (singleton)."""
    global _run_registry
    if _run_registry is None:
        _run_registry = ClusteringRunRegistry()
    return _run_registry


def create_failure_family(
    member_failures: list[Any],
    representative_id: str,
    config: Any = None,
) -> Any:
    """Create a failure family from a list of validated failures."""
    from agent_eval.failure_families.clustering import (
        AgglomerativeClusterer,
        ClusteringConfig,
    )

    # Use provided config or default
    if config is None:
        config = ClusteringConfig()

    clusterer = AgglomerativeClusterer(config)
    families = clusterer.cluster(member_failures)

    # Register families
    registry = get_failure_family_registry()
    for family in families:
        registry.add_family(family)

    return families
