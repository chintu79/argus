"""Priority scoring for adaptive test selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent_eval.adaptive.cost_model import CostModel
from agent_eval.adaptive.information_gain import InformationGainEstimator
from agent_eval.adaptive.models import (
    AdaptiveConfig,
    AdaptiveEvaluationState,
    TestCandidate,
)
from agent_eval.adaptive.novelty import NoveltyEstimator


@dataclass
class PriorityComponents:
    """Individual components of the priority score."""

    novelty: float = 0.0
    information_gain: float = 0.0
    failure_probability: float = 0.0
    coverage_value: float = 0.0
    normalized_cost: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {
            "novelty": self.novelty,
            "information_gain": self.information_gain,
            "failure_probability": self.failure_probability,
            "coverage": self.coverage_value,
            "normalized_cost": self.normalized_cost,
        }


@dataclass
class PriorityResult:
    """Complete priority scoring result."""

    candidate_id: str
    priority_score: float
    components: PriorityComponents
    reason: str


class CoverageEstimator:
    """Estimates coverage value of a candidate."""

    def __init__(self):
        pass

    def estimate(
        self,
        candidate: TestCandidate,
        evaluation_state: AdaptiveEvaluationState,
    ) -> float:
        """
        Estimate coverage value of a candidate.

        Returns value in [0.0, 1.0] representing how much
        this candidate covers under-explored dimensions.
        """
        scores = []
        weights = []

        # Tool coverage
        tool_cov = self._tool_coverage(candidate.target_tool, evaluation_state)
        scores.append(tool_cov)
        weights.append(0.25)

        # Mutation coverage
        m_cov = self._mutation_coverage(
            candidate.mutation, candidate.target_tool, evaluation_state
        )
        scores.append(m_cov)
        weights.append(0.25)

        # Taxonomy coverage
        t_cov = self._taxonomy_coverage(candidate.target_invariant, evaluation_state)
        scores.append(t_cov)
        weights.append(0.2)

        # Resource coverage
        r_cov = self._resource_coverage(candidate.target_resource, evaluation_state)
        scores.append(r_cov)
        weights.append(0.2)

        # State transition coverage
        s_cov = self._transition_coverage(evaluation_state)
        scores.append(s_cov)
        weights.append(0.1)

        if not scores:
            return 0.5

        total_w = sum(weights)
        if total_w == 0:
            return 0.5

        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        return min(1.0, max(0.0, weighted_sum / sum(weights)))

    def _tool_coverage(
        self, tool: str | None, state: AdaptiveEvaluationState
    ) -> float:
        if not tool:
            return 0.5
        coverage = state.tool_coverage
        if not coverage:
            return 1.0  # Completely unexplored
        count = coverage.get(tool, 0)
        max_c = max(coverage.values()) if coverage else 1
        return max(0.0, 1.0 - (count / max(1, max_c)))

    def _mutation_coverage(
        self,
        mutation: str | None,
        tool: str | None,
        state: AdaptiveEvaluationState,
    ) -> float:
        if not mutation or not tool:
            return 0.5
        mut_cov = getattr(state, "mutation_coverage", {})
        tool_mutations = mut_cov.get(tool, {})
        count = tool_mutations.get(mutation, 0)
        total = sum(tool_mutations.values()) if tool_mutations else 1
        return max(0.0, 1.0 - (count / max(1, total)))

    def _taxonomy_coverage(self, invariant: str | None, state: Any) -> float:
        if not invariant:
            return 0.5
        tax_cov = getattr(state, "taxonomy_coverage", {})
        count = tax_cov.get(invariant, 0)
        max_c = max(tax_cov.values()) if tax_cov else 1
        return max(0.0, 1.0 - (count / max(1, max_c)))

    def _resource_coverage(self, resource: str | None, state: Any) -> float:
        # Simplified - check if resource type has been explored
        if not resource:
            return 0.5
        return 0.7  # Default moderate coverage

    def _transition_coverage(self, state: Any) -> float:
        transitions = getattr(state, "state_transitions", [])
        if not transitions:
            return 1.0
        unique = len(set(transitions))
        total = len(transitions)
        return max(0.2, 1.0 - (unique / max(1, total)))


class FailureProbabilityEstimator:
    """Estimates probability of failure for a candidate."""

    def __init__(self, smoothing_alpha: float = 1.0):
        self.smoothing_alpha = smoothing_alpha
        self._execution_history: dict[
            str, tuple[int, int]
        ] = {}  # key -> (failures, total)

    def estimate(
        self,
        candidate: TestCandidate,
        evaluation_state: AdaptiveEvaluationState,
    ) -> float:
        """
        Estimate probability that this candidate will produce a failure.

        Returns:
            Probability in [0.0, 1.0]
        """
        # Key dimensions for probability estimation
        key = self._make_key(candidate)

        if key in self._execution_history:
            failures, total = self._execution_history[key]
            return (failures + self.smoothing_alpha) / (
                total + 2 * self.smoothing_alpha
            )

        # No history for exact key - use family-level statistics
        family_prob = self._family_level_probability(candidate)

        # Also consider tool-level probability
        tool_prob = self._tool_level_probability(candidate.target_tool)

        # Combine with weights
        return 0.6 * family_prob + 0.4 * tool_prob

    def _make_key(self, candidate: TestCandidate) -> str:
        """Create a key for exact candidate matching."""
        parts = []
        if candidate.target_tool:
            parts.append(f"tool:{candidate.target_tool}")
        if candidate.mutation:
            parts.append(f"mut:{candidate.mutation}")
        if candidate.target_resource:
            parts.append(f"res:{candidate.target_resource}")
        if candidate.target_invariant:
            parts.append(f"inv:{candidate.target_invariant}")
        return "|".join(parts) if parts else "default"

    def _family_level_probability(self, candidate: TestCandidate) -> float:
        """Get failure probability at family level."""
        # Check if candidate targets known failure families
        if candidate.predicted_failure_families:
            # High probability if targeting known failure family
            return 0.7
        return 0.3

    def _tool_level_probability(self, tool: str | None) -> float:
        """Get failure probability for a tool."""
        # Default probabilities per tool
        tool_probs = {
            "customer.lookup": 0.15,
            "account.lookup": 0.15,
            "transaction.lookup": 0.10,
            "ticket.search": 0.10,
            "ticket.update": 0.30,
            "notification.send": 0.05,
            "database.write": 0.40,
        }
        return tool_probs.get(tool, 0.2) if tool else 0.2

    def record_execution(self, candidate: TestCandidate, failed: bool):
        """Record execution outcome for future estimates."""
        key = self._make_key(candidate)
        failures, total = self._execution_history.get(key, (0, 0))
        self._execution_history[key] = (failures + (1 if failed else 0), total + 1)


class PriorityScorer:
    """Computes priority scores for test candidates."""

    def __init__(self, config: AdaptiveConfig):
        self.config = config
        self.novelty_estimator = NoveltyEstimator()
        self.information_gain_estimator = InformationGainEstimator()
        self.failure_prob_estimator = FailureProbabilityEstimator()
        self.coverage_estimator = CoverageEstimator()
        self.cost_model = CostModel(config)

        # Weights from config
        self.weights = {
            "novelty": config.priority_novelty,
            "information_gain": config.priority_information_gain,
            "failure_probability": config.priority_failure_probability,
            "coverage": config.priority_coverage,
            "cost": config.priority_cost,
        }

    def score(
        self,
        candidate: TestCandidate,
        evaluation_state: AdaptiveEvaluationState,
    ) -> PriorityResult:
        """Calculate priority score for a candidate."""
        # Compute components
        novelty = NoveltyEstimator().estimate(candidate, evaluation_state)
        info_gain = InformationGainEstimator().estimate(candidate, evaluation_state)
        fail_prob = self.failure_prob_estimator.estimate(candidate, evaluation_state)
        coverage = CoverageEstimator().estimate(candidate, evaluation_state)

        # Normalize cost
        cost_model = CostModel()
        estimated_cost = cost_model.estimate_cost(candidate, evaluation_state)
        max_cost = self._max_possible_cost()
        normalized_cost = min(1.0, estimated_cost / max(1, max_cost))

        # Components
        components = PriorityComponents(
            novelty=novelty,
            information_gain=info_gain,
            failure_probability=fail_prob,
            coverage_value=coverage,
            normalized_cost=normalized_cost,
        )

        # Calculate weighted score (cost is subtracted)
        score = (
            self.weights["novelty"] * novelty
            + self.weights["information_gain"] * info_gain
            + self.weights["failure_probability"] * fail_prob
            + self.weights["coverage"] * coverage
            - self.weights["cost"] * normalized_cost
        )

        # Clamp to [0, 1]
        score = max(0.0, min(1.0, score))

        # Generate reason
        reason = self._generate_reason(
            novelty, info_gain, fail_prob, coverage, normalized_cost
        )

        return PriorityResult(
            candidate_id=candidate.candidate_id,
            priority_score=score,
            components=components,
            reason=reason,
        )

    def _max_possible_cost(self) -> int:
        """Maximum possible cost for normalization."""
        # Rough upper bound: database.write with authorization bypass
        return int(25 * 2.0)  # 50

    def _generate_reason(
        self,
        novelty: float,
        info_gain: float,
        fail_prob: float,
        coverage: float,
        norm_cost: float,
    ) -> str:
        """Generate human-readable reason for priority."""
        reasons = []
        if novelty > 0.7:
            reasons.append("high novelty")
        if info_gain > 0.7:
            reasons.append("high expected information gain")
        if fail_prob > 0.7:
            reasons.append("high expected failure probability")
        if coverage > 0.7:
            reasons.append("covers under-explored area")
        if norm_cost < 0.3:
            reasons.append("low cost")
        elif norm_cost > 0.7:
            reasons.append("high cost")

        if not reasons:
            return "balanced exploration/exploitation"
        return "high " + " + ".join(reasons)


def calculate_priority(
    candidate: TestCandidate,
    evaluation_state: AdaptiveEvaluationState,
    config: AdaptiveConfig,
) -> PriorityResult:
    """Convenience function to calculate priority."""
    scorer = PriorityScorer(config)
    return scorer.score(candidate, evaluation_state)
