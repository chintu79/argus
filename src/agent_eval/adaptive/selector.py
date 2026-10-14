"""Adaptive test selector implementations."""

from __future__ import annotations

import random
from typing import Any

from agent_eval.adaptive.candidate_generator import CandidateGenerator
from agent_eval.adaptive.cost_model import CostModel
from agent_eval.adaptive.models import (
    AdaptiveConfig,
    AdaptiveEvaluationState,
    CandidateSource,
    EvaluationSplit,
    TestCandidate,
)
from agent_eval.adaptive.priority import (
    PriorityComponents,
    PriorityResult,
    PriorityScorer,
)


class SelectionPolicyInterface:
    """Interface for selection policies."""

    def select(
        self,
        candidates: list[TestCandidate],
        evaluation_state: Any,
    ) -> TestCandidate | None:
        raise NotImplementedError


class RandomPolicy(SelectionPolicyInterface):
    """Random selection with deterministic seeding."""

    def __init__(self, seed: int = 42):
        self._rng = random.Random(seed)

    def select(
        self,
        candidates: list[TestCandidate],
        evaluation_state: Any,
    ) -> TestCandidate | None:
        valid = [c for c in candidates if self._is_valid(c, evaluation_state)]
        if not valid:
            return None
        return self._rng.choice(valid)

    def _is_valid(self, candidate: TestCandidate, state: Any) -> bool:
        return candidate.estimated_cost <= getattr(state, "budget", {}).get(
            "remaining_tokens", float("inf")
        )


class StaticPolicy(SelectionPolicyInterface):
    """Static ordered selection."""

    def __init__(self, order: list[str]):
        self._order = order
        self._index = 0
        self._selected: set[str] = set()

    def select(
        self,
        candidates: list[TestCandidate],
        evaluation_state: Any,
    ) -> TestCandidate | None:
        # Filter valid
        valid = [c for c in candidates if self._is_valid(c, evaluation_state)]
        if not valid:
            return None

        # Try to follow static order
        for tool_name in self._order:
            for c in valid:
                if c.target_tool == tool_name and c.candidate_id not in self._selected:
                    self._selected.add(c.candidate_id)
                    return c

        # Fallback to first valid
        return valid[0] if valid else None

    def _is_valid(self, candidate: TestCandidate, state: Any) -> bool:
        budget = getattr(state, "budget", None)
        if budget and hasattr(budget, "remaining_tokens"):
            return candidate.estimated_cost <= budget.remaining_tokens
        return True


class FailureDirectedPolicy(SelectionPolicyInterface):
    """Failure-directed adaptive selection with priority scoring."""

    def __init__(self, config: AdaptiveConfig):
        self.config = config
        self.priority_scorer = PriorityScorer(config)
        self.cost_model = CostModel()
        self._rng = random.Random(config.random_seed)

    def select(
        self,
        candidates: list[TestCandidate],
        evaluation_state: AdaptiveEvaluationState,
    ) -> TestCandidate | None:
        """Select the highest priority candidate."""
        # Filter valid candidates
        valid = self._filter_valid(candidates, evaluation_state)

        if not valid:
            return None

        # Score all valid candidates
        scored = self._score_all(candidates, evaluation_state)

        if not scored:
            return None

        # Sort by priority (descending), then by tie-breakers
        scored.sort(key=self._sort_key, reverse=True)

        # Select highest priority
        selected_candidate, _ = scored[0]

        return selected_candidate

    def _filter_valid(
        self,
        candidates: list[TestCandidate],
        evaluation_state: AdaptiveEvaluationState,
    ) -> list[TestCandidate]:
        """Filter candidates that are valid for execution."""
        valid = []
        budget_remaining = evaluation_state.budget.remaining_tokens
        min_reserve = self.config.minimum_budget_reserve

        for c in candidates:
            # Check if already executed
            if c.candidate_id in evaluation_state.executed_candidates:
                continue

            # Check budget
            if not evaluation_state.budget.can_afford(c.estimated_cost):
                continue

            # Check minimum budget reserve
            if budget_remaining - c.estimated_cost < min_reserve:
                continue

            # Cost must be positive
            if c.estimated_cost <= 0:
                continue

            # Cost must be within remaining budget
            if c.estimated_cost > budget_remaining:
                continue

            # Ensure candidate is from search split
            if (
                evaluation_state.split == EvaluationSplit.SEARCH
                and c.source == CandidateSource.HOLDOUT
            ):
                continue

            valid.append(c)

        return valid

    def _score_all(
        self,
        candidates: list[TestCandidate],
        evaluation_state: AdaptiveEvaluationState,
    ) -> list[tuple[TestCandidate, PriorityResult]]:
        """Score all valid candidates."""
        scorer = PriorityScorer(self.config)
        results = []

        for c in candidates:
            try:
                result = scorer.score(c, evaluation_state)
                results.append((c, result))
            except Exception:
                # Assign zero score on error
                dummy = PriorityResult(
                    candidate_id=c.candidate_id,
                    priority_score=0.0,
                    components=PriorityComponents(),
                    reason="scoring error",
                )
                results.append((c, dummy))

        return results

    def _sort_key(self, item: tuple[TestCandidate, PriorityResult]) -> tuple:
        """Deterministic sorting key for candidates."""
        candidate, result = item

        # Primary: priority score (descending)
        # Secondary: information gain (descending)
        # Tertiary: novelty (descending)
        # Quaternary: negative cost (ascending cost)
        # Quinary: candidate_id (lexicographic)

        components = getattr(result, "components", None)
        ig = getattr(components, "information_gain", 0.0) if components else 0.0
        nov = getattr(components, "novelty", 0.0) if components else 0.0
        cost = getattr(components, "normalized_cost", 1.0) if components else 1.0

        return (
            -result.priority_score,
            -ig,
            -nov,
            cost,
            candidate.candidate_id,
        )


class AdaptiveSelector:
    """Main adaptive selector that uses configured policy."""

    def __init__(self, config: AdaptiveConfig | None = None):
        self.config = config or AdaptiveConfig()
        self._policy: SelectionPolicyInterface = FailureDirectedPolicy(self.config)
        self.generator = CandidateGenerator()

    def set_policy(self, policy: SelectionPolicyInterface):
        """Set the selection policy."""
        self._policy = policy

    def select_next(
        self,
        evaluation_state: AdaptiveEvaluationState,
        parent_state_id: str | None = None,
    ) -> TestCandidate | None:
        """Generate candidates and select the next one."""
        # Generate candidates
        candidates = self.generator.generate(
            evaluation_state, parent_state_id, self.config
        )

        # Select using policy
        selected = self._policy.select(candidates, evaluation_state)

        return selected

    def generate_candidates(
        self,
        evaluation_state: AdaptiveEvaluationState,
        parent_state_id: str | None = None,
    ) -> list[TestCandidate]:
        """Generate candidates without selecting."""
        return self.generator.generate(evaluation_state, parent_state_id, self.config)

    def score_candidates(
        self,
        candidates: list[TestCandidate],
        evaluation_state: AdaptiveEvaluationState,
    ) -> list[tuple[Any, float]]:
        """Score candidates and return sorted list."""
        scored = []
        for c in candidates:
            result = PriorityScorer(AdaptiveConfig()).score(c, evaluation_state)
            scored.append((c, result.priority_score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


def select_next_test(
    evaluation_state: AdaptiveEvaluationState,
    config: AdaptiveConfig | None = None,
) -> TestCandidate | None:
    """Convenience function to select next test."""
    selector = AdaptiveSelector(config)
    return selector.select_next(evaluation_state)
