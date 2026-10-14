"""Clustering algorithm for failure family formation."""

from __future__ import annotations

import hashlib
from collections import Counter
from datetime import UTC, datetime
from typing import Any

from agent_eval.domain.identifiers import make_id
from agent_eval.failure_families.models import (
    REASON_CODE_TO_TAXONOMY,
    ClusteringConfig,
    ClusteringRun,
    FailureFamily,
    FamilyCoherence,
    FamilySignature,
)
from agent_eval.failure_families.similarity import (
    FeatureSimilarityMatrix,
    SimilarityCalculator,
)


class AgglomerativeClusterer:
    """Agglomerative clustering for failure families."""

    def __init__(self, config: ClusteringConfig):
        self.config = config
        self.calculator = SimilarityCalculator(config.similarity_weights)
        self.matrix_calculator = FeatureSimilarityMatrix(self.calculator)

    def cluster(
        self,
        validated_failures: list[Any],
    ) -> list[Any]:
        """Perform agglomerative clustering on validated failures."""
        if not validated_failures:
            return []

        if len(validated_failures) == 1:
            return [self._create_singleton_family(validated_failures[0])]

        # Compute similarity matrix
        similarity_matrix = self._compute_similarity_matrix(validated_failures)

        # Convert to distance matrix
        distance_matrix = {}
        for key, sim in similarity_matrix.items():
            distance_matrix[key] = 1.0 - sim

        # Perform agglomerative clustering
        clusters = self._agglomerative_clustering(
            validated_failures,
            distance_matrix,
        )

        # Create families from clusters
        families = []
        for cluster in clusters:
            if len(cluster) == 0:
                continue
            family = self._create_family_from_cluster(cluster, validated_failures)
            families.append(family)

        return families

    def _compute_similarity_matrix(
        self,
        failures: list[Any],
    ) -> dict[tuple[str, str], float]:
        """Compute full similarity matrix."""
        matrix = {}
        n = len(failures)

        for i in range(n):
            for j in range(i, n):
                fi = failures[i]
                fj = failures[j]

                if i == j:
                    sim = 1.0
                else:
                    sim, _ = self.calculator.calculate(
                        fi,
                        fj,
                    )

                matrix[(fi.failure_id, fj.failure_id)] = sim
                matrix[(fj.failure_id, fi.failure_id)] = sim

        return matrix

    def _agglomerative_clustering(
        self,
        failures: list[Any],
        distance_matrix: dict[tuple[str, str], float],
    ) -> list[list[Any]]:
        """Perform agglomerative clustering."""
        # Initialize each failure as its own cluster
        clusters = [[f] for f in failures]

        # Build cluster distance cache
        cluster_distances = {}
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = self._cluster_distance(clusters[i], clusters[j], distance_matrix)
                cluster_distances[(i, j)] = dist

        # Merge until threshold
        threshold = self.config.distance_threshold

        while True:
            # Find closest pair of clusters
            min_dist = float("inf")
            merge_pair = None

            for (i, j), dist in cluster_distances.items():
                if dist < min_dist and dist <= threshold:
                    min_dist = dist
                    merge_pair = (i, j)

            if merge_pair is None:
                break

            i, j = merge_pair
            if i > j:
                i, j = j, i

            # Merge clusters
            merged = clusters[i] + clusters[j]

            # Remove old clusters (remove higher index first)
            clusters.pop(j)
            clusters.pop(i)
            clusters.insert(i, merged)

            # Recompute distances for new cluster
            new_distances = {}
            for idx in range(len(clusters)):
                if idx == i:
                    continue
                a, b = min(idx, i), max(idx, i)
                dist = self._cluster_distance(clusters[a], clusters[b], None)
                new_distances[(a, b)] = dist

            # Update distance cache
            cluster_distances = {
                k: v
                for k, v in cluster_distances.items()
                if k[0] != i and k[0] != j and k[1] != i and k[1] != j
            }
            cluster_distances.update(new_distances)

            # Early stopping check
            if self.config.early_stopping and len(clusters) <= 1:
                break

        return clusters

    def _cluster_distance(
        self,
        cluster_a: list[Any],
        cluster_b: list[Any],
        distance_matrix: dict[tuple[str, str], float] | None,
    ) -> float:
        """Calculate distance between two clusters using configured linkage."""
        dm = distance_matrix or {}
        if self.config.linkage == "single":
            return self._single_linkage(cluster_a, cluster_b, dm)
        elif self.config.linkage == "complete":
            return self._complete_linkage(cluster_a, cluster_b, dm)
        elif self.config.linkage == "average":
            return self._average_linkage(cluster_a, cluster_b, dm)
        elif self.config.linkage == "ward":
            return self._ward_linkage(cluster_a, cluster_b, dm)
        else:
            return self._average_linkage(cluster_a, cluster_b, dm)

    def _single_linkage(
        self,
        cluster_a: list[Any],
        cluster_b: list[Any],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """Single linkage: minimum distance between any two points."""
        min_dist = float("inf")
        for fa in cluster_a:
            for fb in cluster_b:
                key = (fa.failure_id, fb.failure_id)
                if key in distance_matrix:
                    dist = distance_matrix[key]
                    min_dist = min(min_dist, dist)
        return min_dist if min_dist != float("inf") else 1.0

    def _complete_linkage(
        self,
        cluster_a: list[Any],
        cluster_b: list[Any],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """Complete linkage: maximum distance between any two points."""
        max_dist = 0.0
        for fa in cluster_a:
            for fb in cluster_b:
                key = (fa.failure_id, fb.failure_id)
                if key in distance_matrix:
                    dist = distance_matrix[key]
                    max_dist = max(max_dist, dist)
        return max_dist

    def _average_linkage(
        self,
        cluster_a: list[Any],
        cluster_b: list[Any],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """Average linkage: average distance between all pairs."""
        total = 0.0
        count = 0
        for fa in cluster_a:
            for fb in cluster_b:
                key = (fa.failure_id, fb.failure_id)
                if key in distance_matrix:
                    total += distance_matrix[key]
                    count += 1
        return total / count if count > 0 else 1.0

    def _ward_linkage(
        self,
        cluster_a: list[Any],
        cluster_b: list[Any],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """Ward linkage: increase in sum of squared distances."""
        # Simplified: use average linkage as approximation
        return self._average_linkage(cluster_a, cluster_b, distance_matrix)

    def _create_family_from_cluster(
        self,
        cluster: list[Any],
        all_failures: list[Any],
    ) -> Any:
        """Create a FailureFamily from a cluster of validated failures."""
        if len(cluster) == 1:
            return self._create_singleton_family(cluster[0])

        # Extract features for all members
        member_ids = [f.failure_id for f in cluster]

        # Compute coherence
        coherence = self._compute_coherence(cluster)

        # Determine dominant features
        dominant = self._compute_dominant_features(cluster)

        # Create family signature
        signature = FamilySignature(
            primary_invariant=dominant.get("invariant_id"),
            primary_reason_code=dominant.get("reason_code"),
            taxonomy=dominant.get("taxonomy_label"),
            dominant_action=dominant.get("action"),
            dominant_resource_type=dominant.get("resource_type"),
            dominant_state_transition=dominant.get("state_transition"),
        )

        # Create canonical fingerprint
        canonical = signature.to_canonical_string()
        family_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]

        # Choose representative
        representative_id = self._choose_representative(cluster)

        # Build distributions
        severity_dist: Counter[str] = Counter()
        invariant_dist: Counter[str] = Counter()
        reason_dist: Counter[str] = Counter()
        env_dist: Counter[str] = Counter()

        for f in cluster:
            severity = (
                f.candidate.severity.value
                if hasattr(f.candidate.severity, "value")
                else str(f.candidate.severity)
            )
            severity_dist[severity] += 1
            invariant_dist[f.invariant_id] += 1
            rc = (
                f.candidate.reason_code.value
                if hasattr(f.candidate.reason_code, "value")
                else str(f.candidate.reason_code)
            )
            reason_dist[rc] += 1
            env_dist["default"] += 1  # Simplified

        family = FailureFamily(
            family_id=f"FF-{family_id}",
            member_failure_ids=member_ids,
            representative_failure_id=representative_id,
            family_signature=canonical,
            family_size=len(cluster),
            taxonomy_labels=list(
                {
                    f.candidate.reason_code.value
                    if hasattr(f.candidate.reason_code, "value")
                    else str(f.candidate.reason_code)
                    for f in cluster
                }
            ),
            coherence_score=coherence.average_pairwise_similarity,
            created_at=datetime.now(UTC),
            clustering_version="1.0",
            severity_distribution=dict(severity_dist),
            invariant_distribution=dict(invariant_dist),
            reason_code_distribution=dict(reason_dist),
            environment_distribution=dict(env_dist),
        )

        return family

    def _create_singleton_family(self, failure: Any) -> Any:
        """Create a singleton family for a single failure."""
        rc = (
            failure.candidate.reason_code.value
            if hasattr(failure.candidate.reason_code, "value")
            else str(failure.candidate.reason_code)
        )
        canonical = f"inv:{failure.invariant_id}|rc:{rc}"
        family_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
        severity = (
            failure.candidate.severity.value
            if hasattr(failure.candidate.severity, "value")
            else str(failure.candidate.severity)
        )

        return FailureFamily(
            family_id=f"FF-{family_id}",
            member_failure_ids=[failure.failure_id],
            representative_failure_id=failure.failure_id,
            family_signature=canonical,
            family_size=1,
            taxonomy_labels=[self._assign_taxonomy(failure) or rc],
            coherence_score=1.0,
            created_at=datetime.now(UTC),
            clustering_version="1.0",
            severity_distribution={severity: 1},
            invariant_distribution={failure.invariant_id: 1},
            reason_code_distribution={rc: 1},
            environment_distribution={"default": 1},
        )

    def _compute_coherence(self, cluster: list[Any]) -> Any:
        """Compute coherence metrics for a cluster."""
        if len(cluster) <= 1:
            return FamilyCoherence(
                coherence_score=1.0,
                average_pairwise_similarity=1.0,
                minimum_pairwise_similarity=1.0,
                maximum_pairwise_similarity=1.0,
            )

        similarities = []
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                sim, _ = self.calculator.calculate(
                    cluster[i],
                    cluster[j],
                )
                similarities.append(sim)

        if not similarities:
            return FamilyCoherence(
                coherence_score=1.0,
                average_pairwise_similarity=1.0,
                minimum_pairwise_similarity=1.0,
                maximum_pairwise_similarity=1.0,
            )

        return FamilyCoherence(
            coherence_score=sum(similarities) / len(similarities),
            average_pairwise_similarity=sum(similarities) / len(similarities),
            minimum_pairwise_similarity=min(similarities),
            maximum_pairwise_similarity=max(similarities),
        )

    def _compute_dominant_features(self, cluster: list[Any]) -> dict[str, Any]:
        """Compute dominant features for a cluster."""
        # Count features
        invariant_counts: Counter[str] = Counter()
        reason_counts: Counter[str] = Counter()
        action_counts: Counter[str] = Counter()
        resource_counts: Counter[str] = Counter()
        state_transition_counts: Counter[str] = Counter()
        taxonomy_counts: Counter[str] = Counter()

        for f in cluster:
            invariant_counts[f.invariant_id] += 1
            rc = (
                f.candidate.reason_code.value
                if hasattr(f.candidate.reason_code, "value")
                else str(f.candidate.reason_code)
            )
            reason_counts[rc] += 1

            action = self._extract_action(f)
            if action:
                action_counts[action] += 1

            resource = self._extract_resource_type(f)
            if resource:
                resource_counts[resource] += 1

            st = self._extract_state_transition(f)
            if st:
                state_transition_counts[st] += 1

            tax = self._assign_taxonomy(f)
            if tax:
                taxonomy_counts[tax] += 1

        return {
            "invariant_id": invariant_counts.most_common(1)[0][0]
            if invariant_counts
            else None,
            "reason_code": reason_counts.most_common(1)[0][0]
            if reason_counts
            else None,
            "action": action_counts.most_common(1)[0][0] if action_counts else None,
            "resource_type": resource_counts.most_common(1)[0][0]
            if resource_counts
            else None,
            "state_transition": state_transition_counts.most_common(1)[0][0]
            if state_transition_counts
            else None,
            "taxonomy_label": taxonomy_counts.most_common(1)[0][0]
            if taxonomy_counts
            else None,
        }

    def _extract_action(self, f: Any) -> str | None:
        evidence = f.candidate.evidence or {}
        if isinstance(evidence, dict):
            return evidence.get("action") or evidence.get("tool_name")
        return None

    def _extract_resource_type(self, f: Any) -> str | None:
        evidence = f.candidate.evidence or {}
        if isinstance(evidence, dict):
            if "resource_type" in evidence:
                return evidence["resource_type"]
            if "resource_id" in evidence:
                rid = evidence["resource_id"]
                if isinstance(rid, str):
                    if "CUST" in rid:
                        return "customer"
                    elif "ACC" in rid:
                        return "account"
                    elif "TXN" in rid:
                        return "transaction"
                    elif "TKT" in rid:
                        return "ticket"
        return None

    def _extract_state_transition(self, f: Any) -> str | None:
        evidence = f.candidate.evidence or {}
        if isinstance(evidence, dict):
            return evidence.get("state_transition")
        return None

    def _assign_taxonomy(self, f: Any) -> str | None:
        rc = (
            f.candidate.reason_code.value
            if hasattr(f.candidate.reason_code, "value")
            else str(f.candidate.reason_code)
        )
        return REASON_CODE_TO_TAXONOMY.get(rc, "UNCLASSIFIED")

    def _choose_representative(self, cluster: list[Any]) -> str:
        """Choose representative deterministically."""
        # Sort by: highest rep_k, then highest evidence completeness, then lexical
        sorted_cluster = sorted(
            cluster,
            key=lambda f: (
                -f.rep_k,
                -len(f.candidate.evidence.get("event_ids", []))
                if f.candidate.evidence
                else 0,
                f.failure_id,
            ),
        )
        return sorted_cluster[0].failure_id


def create_clustering_run(
    config: ClusteringConfig,
    input_count: int,
    eligible_count: int,
) -> ClusteringRun:
    """Create a new clustering run record."""
    return ClusteringRun(
        run_id=make_id("clust"),
        configuration={
            "algorithm": config.algorithm,
            "distance_threshold": config.distance_threshold,
            "linkage": config.linkage,
            "minimum_family_size": config.minimum_family_size,
            "similarity_weights": config.similarity_weights.dict(),
            "eligibility_policy": config.eligibility_policy.dict(),
        },
        input_failure_count=0,
        eligible_failure_count=0,
        family_count=0,
        created_at=datetime.now(UTC),
    )


def build_family_signature(cluster: list[Any]) -> str:
    """Build a canonical family signature from a cluster."""
    if not cluster:
        return "inv:unknown|rc:unknown"
    invariants = [f.invariant_id for f in cluster]
    reasons = [
        f.candidate.reason_code.value
        if hasattr(f.candidate.reason_code, "value")
        else str(f.candidate.reason_code)
        for f in cluster
    ]

    invariant = Counter(invariants).most_common(1)[0][0]
    reason = Counter(reasons).most_common(1)[0][0]

    return f"inv:{invariant}|rc:{reason}"
