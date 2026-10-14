"""Information gain estimation for adaptive test selection."""

from __future__ import annotations

import math
from dataclasses import dataclass

from agent_eval.adaptive.models import AdaptiveEvaluationState, TestCandidate


@dataclass
class FailureDistribution:
    """Represents a probability distribution over failure families."""

    family_probabilities: dict[str, float]
    unknown_probability: float

    def entropy(self) -> float:
        """Calculate Shannon entropy of the distribution."""
        entropy = 0.0
        for prob in self.family_probabilities.values():
            if prob > 0:
                entropy -= prob * math.log2(prob)
        if self.unknown_probability > 0:
            entropy -= self.unknown_probability * math.log2(self.unknown_probability)
        return entropy


class InformationGainEstimator:
    """Estimates expected information gain from executing a candidate."""

    def __init__(self, smoothing_alpha: float = 1.0):
        self.smoothing_alpha = smoothing_alpha

    def estimate(
        self,
        candidate: TestCandidate,
        evaluation_state: AdaptiveEvaluationState,
    ) -> float:
        """
        Estimate expected information gain from executing a candidate.

        Returns:
            Expected information gain in bits [0.0, 1.0] (normalized)
        """
        # Build current belief distribution over failure families
        current_distribution = self._build_current_distribution(evaluation_state)

        # Current entropy
        current_entropy = current_distribution.entropy()

        # Estimate expected posterior entropy after this candidate
        expected_posterior_entropy = self._estimate_posterior_entropy(
            candidate, evaluation_state, current_distribution
        )

        # Information gain = reduction in entropy
        ig = current_entropy - expected_posterior_entropy

        # Normalize to [0, 1] (max possible entropy is log2(N_families + 1))
        max_families = max(1, len(set(evaluation_state.failure_families)) + 1)
        max_entropy = math.log2(max_families)

        if max_entropy > 0:
            return min(1.0, ig / max_entropy)
        return 0.0

    def _build_current_distribution(
        self, evaluation_state: AdaptiveEvaluationState
    ) -> FailureDistribution:
        """Build current belief distribution over failure families."""
        # Use family counts from evaluation state
        family_counts = evaluation_state.failure_family_counts
        total = sum(family_counts.values())

        if total == 0:
            # No families discovered yet - uniform over "unknown"
            return FailureDistribution(
                family_probabilities={},
                unknown_probability=1.0,
            )

        # Laplace smoothing
        alpha = 1.0
        n_families = len(family_counts)

        family_probabilities = {}
        for family_id, count in family_counts.items():
            family_probabilities[family_id] = (count + alpha) / (
                total + alpha * (n_families + 1)
            )

        # Unknown probability
        unknown_prob = alpha / (total + alpha * (n_families + 1))

        return FailureDistribution(
            family_probabilities=family_probabilities,
            unknown_probability=unknown_prob,
        )

    def _estimate_posterior_entropy(
        self,
        candidate: TestCandidate,
        evaluation_state: AdaptiveEvaluationState,
        current_distribution: FailureDistribution,
    ) -> float:
        """
        Estimate expected posterior entropy after executing candidate.

        This is an approximation using the failure probability and predicted families.
        """
        predicted_families = candidate.predicted_failure_families
        if not predicted_families:
            # No specific prediction - small entropy reduction
            return current_distribution.entropy() * 0.9

        # Estimate failure probability
        failure_prob = candidate.estimated_failure_probability

        # For each predicted family, estimate posterior
        expected_entropy = 0.0

        # Case 1: Failure occurs (with probability failure_prob)
        # Update distribution with new evidence for predicted families
        if failure_prob > 0:
            # Update distribution with new failure
            posterior = self._update_distribution_with_failure(
                candidate, evaluation_state
            )
            expected_entropy += failure_prob * posterior.entropy()

        # Case 2: No failure (with probability 1 - failure_prob)
        # Distribution shifts slightly towards "no failure"
        if failure_prob < 1.0:
            no_failure_dist = self._update_distribution_no_failure(evaluation_state)
            expected_entropy += (1.0 - failure_prob) * no_failure_dist.entropy()

        return expected_entropy

    def _update_distribution_with_failure(
        self,
        candidate: TestCandidate,
        evaluation_state: AdaptiveEvaluationState,
    ) -> FailureDistribution:
        """Update distribution assuming a failure occurred in predicted families."""

        family_counts: dict[str, float] = {
            k: float(v) for k, v in evaluation_state.failure_family_counts.items()
        }

        # Add pseudo-counts for predicted families
        for fam_id in candidate.predicted_failure_families:
            if fam_id in family_counts:
                family_counts[fam_id] += 2.0  # Stronger update for observed failure
            else:
                family_counts[fam_id] = 2.0

        return self._counts_to_distribution(family_counts)

    def _update_distribution_no_failure(
        self,
        evaluation_state: AdaptiveEvaluationState,
    ) -> FailureDistribution:
        """Update distribution assuming no failure occurred."""

        family_counts: dict[str, float] = {
            k: float(v) for k, v in evaluation_state.failure_family_counts.items()
        }

        # Slight update: slightly reduce probability of recent failures
        # (less evidence for failure = slightly lower probability)
        for fam_id in list(family_counts.keys()):
            family_counts[fam_id] = max(0.0, family_counts[fam_id] - 0.1)

        return self._counts_to_distribution(family_counts)

    def _counts_to_distribution(
        self, family_counts: dict[str, float]
    ) -> FailureDistribution:
        """Convert counts to probability distribution."""
        total = sum(family_counts.values())
        alpha = 1.0
        n_families = len([k for k, v in family_counts.items() if v > 0])

        family_probs = {}
        for fam_id, count in family_counts.items():
            if count > 0:
                family_probs[fam_id] = (count + alpha) / (
                    total + alpha * (n_families + 1)
                )

        unknown = alpha / (total + alpha * (n_families + 1))

        return FailureDistribution(
            family_probabilities=family_probs,
            unknown_probability=unknown,
        )


def estimate_information_gain(
    candidate: TestCandidate,
    evaluation_state: AdaptiveEvaluationState,
) -> float:
    """Convenience function to estimate information gain."""
    estimator = InformationGainEstimator()
    return estimator.estimate(candidate, evaluation_state)
