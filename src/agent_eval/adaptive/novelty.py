"""Novelty estimation for adaptive test selection."""

from __future__ import annotations

from typing import Any

from agent_eval.adaptive.models import TestCandidate
from agent_eval.failure_families.features import FeatureExtractor


class NoveltyEstimator:
    """Estimates novelty of a test candidate relative to explored state."""

    def __init__(self):
        self._feature_extractor = FeatureExtractor()
        self._seen_combinations: dict[str, int] = {}

    def estimate(
        self,
        candidate: TestCandidate,
        evaluation_state: Any,
    ) -> float:
        """
        Estimate novelty score for a candidate.

        Returns:
            Novelty score in [0.0, 1.0]
        """
        if not hasattr(evaluation_state, "mutation_coverage"):
            return 1.0  # No history = maximum novelty

        # Extract key dimensions
        tool = candidate.target_tool or ""
        mutation = candidate.mutation or ""
        resource = candidate.target_resource or ""
        invariant = candidate.target_invariant or ""

        # Check different novelty dimensions
        scores = []

        # 1. Tool novelty
        tool_novelty = self._tool_novelty(tool, evaluation_state)
        scores.append(("tool", tool_novelty, 0.25))

        # 2. Mutation novelty
        mutation_novelty = self._mutation_novelty(mutation, tool, evaluation_state)
        scores.append(("mutation", mutation_novelty, 0.25))

        # 3. Resource novelty
        resource_novelty = self._resource_novelty(resource, tool, evaluation_state)
        scores.append(("resource", resource_novelty, 0.2))

        # 4. Invariant novelty
        invariant_novelty = self._invariant_novelty(invariant, evaluation_state)
        scores.append(("invariant", invariant_novelty, 0.15))

        # 5. State transition novelty
        transition_novelty = self._transition_novelty(evaluation_state)
        scores.append(("transition", transition_novelty, 0.15))

        # Weighted average
        total_weight = sum(w for _, _, w in scores)
        if total_weight == 0:
            return 1.0

        weighted_sum = sum(score * weight for _, score, weight in scores)
        return min(1.0, max(0.0, weighted_sum / total_weight))

    def _tool_novelty(self, tool: str, evaluation_state: Any) -> float:
        """Novelty based on tool usage."""
        coverage = evaluation_state.tool_coverage
        if not coverage:
            return 1.0

        tool_count = coverage.get(tool, 0)
        max_count = max(coverage.values()) if coverage else 1

        if max_count == 0:
            return 1.0

        # Inverse frequency - less used tools are more novel
        return max(0.1, 1.0 - (tool_count / max(1, max_count)))

    def _mutation_novelty(
        self, mutation: str, tool: str, evaluation_state: Any
    ) -> float:
        """Novelty based on mutation type for a tool."""
        mutation_coverage = getattr(evaluation_state, "mutation_coverage", {})
        tool_mutations = mutation_coverage.get(tool, {})

        mutation_count = tool_mutations.get(mutation, 0)
        total_mutations = sum(tool_mutations.values()) if tool_mutations else 0

        if total_mutations == 0:
            return 1.0

        return max(0.1, 1.0 - (mutation_count / max(1, total_mutations)))

    def _resource_novelty(
        self, resource: str, tool: str, evaluation_state: Any
    ) -> float:
        """Novelty based on resource exploration."""
        # Check if this resource has been tested with this tool
        # Simplified: check if resource appears in explored states
        return 1.0  # Placeholder - would check actual resource coverage

    def _invariant_novelty(self, invariant: str, evaluation_state: Any) -> float:
        """Novelty based on invariant targeting."""
        if not invariant:
            return 0.5

        # Check if this invariant has been explored
        invariant_coverage = getattr(evaluation_state, "invariant_coverage", {})
        count = invariant_coverage.get(invariant, 0)
        max_count = max(invariant_coverage.values()) if invariant_coverage else 1

        if max_count == 0:
            return 1.0

        return max(0.1, 1.0 - (count / max(1, max_count)))

    def _transition_novelty(self, evaluation_state: Any) -> float:
        """Novelty based on state transition patterns."""
        # Check state transition patterns
        transitions = getattr(evaluation_state, "state_transitions", [])
        if not transitions:
            return 1.0

        # Count unique transition patterns
        unique = len(set(transitions))
        total = len(transitions)

        if total == 0:
            return 1.0

        # More unique transitions = more explored
        return max(0.2, 1.0 - (unique / max(1, total)))


def compute_novelty(
    candidate: Any,
    evaluation_state: Any,
) -> float:
    """Convenience function to compute novelty."""
    estimator = NoveltyEstimator()
    return estimator.estimate(candidate, evaluation_state)


def compute_batch_novelty(
    candidates: list[Any],
    evaluation_state: Any,
) -> dict[str, float]:
    """Compute novelty for a batch of candidates."""
    estimator = NoveltyEstimator()
    return {c.candidate_id: estimator.estimate(c, evaluation_state) for c in candidates}
