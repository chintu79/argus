"""Evaluation state management for adaptive evaluation."""

from __future__ import annotations

from typing import Any

from agent_eval.adaptive.models import (
    AdaptiveBudget,
    AdaptiveConfig,
    AdaptiveEvaluationState,
    EvaluationSplit,
)


class EvaluationStateManager:
    """Manages the adaptive evaluation state."""

    def __init__(self, config: AdaptiveConfig | None = None):
        self.config = config or AdaptiveConfig()
        self._state = AdaptiveEvaluationState(
            budget=AdaptiveBudget(total_tokens=100000),
        )

    @property
    def state(self) -> AdaptiveEvaluationState:
        return self._state

    def initialize(
        self,
        total_budget: int = 100000,
        split: str = "SEARCH",
    ):
        """Initialize evaluation state."""
        self._state = AdaptiveEvaluationState(
            budget=AdaptiveBudget(total_tokens=total_budget),
            split=EvaluationSplit.SEARCH
            if split == "SEARCH"
            else EvaluationSplit.HOLDOUT,
        )

    def record_candidate_execution(
        self,
        candidate_id: str,
        actual_cost: int,
        failure_occurred: bool = False,
        failure_family: str | None = None,
    ):
        """Record that a candidate was executed."""
        self._state.executed_candidates.append(candidate_id)
        self._state.budget.commit(actual_cost)

        if failure_occurred and failure_family:
            self._state.validated_failures.append(failure_family)
            if failure_family not in self._state.failure_families:
                self._state.failure_families.append(failure_family)
            self._state.failure_family_counts[failure_family] = (
                self._state.failure_family_counts.get(failure_family, 0) + 1
            )

        self._state.iteration += 1
        self._state.touch()

    def record_explored_state(self, state_id: str):
        """Record that a state has been explored."""
        if state_id not in self._state.explored_states:
            self._state.explored_states.append(state_id)

    def update_tool_coverage(self, tool: str):
        """Update tool usage coverage."""
        self._state.tool_coverage[tool] = self._state.tool_coverage.get(tool, 0) + 1

    def update_mutation_coverage(self, tool: str, mutation: str):
        """Update mutation coverage for a tool."""
        if tool not in self._state.mutation_coverage:
            self._state.mutation_coverage[tool] = {}
        self._state.mutation_coverage[tool][mutation] = (
            self._state.mutation_coverage[tool].get(mutation, 0) + 1
        )

    def update_taxonomy_coverage(self, invariant: str):
        """Update taxonomy coverage."""
        if invariant:
            self._state.taxonomy_coverage[invariant] = (
                self._state.taxonomy_coverage.get(invariant, 0) + 1
            )

    def record_state_transition(self, transition: str):
        """Record a state transition pattern."""
        self._state.state_transitions.append(transition)

    def get_budget_remaining(self) -> int:
        return self._state.budget.remaining_tokens

    def get_budget_utilization(self) -> float:
        return self._state.budget.utilization()

    def can_continue(self, min_budget: int = 10) -> bool:
        """Check if evaluation can continue."""
        return self._state.budget.remaining_tokens >= 10

    def get_progress(self) -> dict[str, Any]:
        """Get evaluation progress summary."""
        return {
            "iteration": self._state.iteration,
            "budget_remaining": self._state.budget.remaining_tokens,
            "budget_utilization": self._state.budget.utilization(),
            "candidates_executed": len(self._state.executed_candidates),
            "validated_failures": len(self._state.validated_failures),
            "failure_families": len(self._state.failure_families),
            "explored_states": len(self._state.explored_states),
            "tool_coverage": dict(self._state.tool_coverage),
            "mutation_coverage": {
                tool: sum(muts.values())
                for tool, muts in self._state.mutation_coverage.items()
            },
            "taxonomy_coverage": len(self._state.taxonomy_coverage),
        }

    def save_snapshot(self) -> dict[str, Any]:
        """Create a serializable snapshot of the state."""
        return {
            "iteration": self._state.iteration,
            "budget": {
                "total_tokens": self._state.budget.total_tokens,
                "consumed_tokens": self._state.budget.consumed_tokens,
                "reserved_tokens": self._state.budget.reserved_tokens,
                "remaining_tokens": self._state.budget.remaining_tokens,
            },
            "executed_candidates": list(self._state.executed_candidates),
            "validated_failures": list(self._state.validated_failures),
            "failure_families": list(self._state.failure_families),
            "failure_family_counts": dict(self._state.failure_family_counts),
            "tool_coverage": dict(self._state.tool_coverage),
            "mutation_coverage": {
                tool: dict(muts) for tool, muts in self._state.mutation_coverage.items()
            },
            "taxonomy_coverage": dict(self._state.taxonomy_coverage),
            "explored_states": list(self._state.explored_states),
            "state_transitions": list(self._state.state_transitions),
        }

    def load_snapshot(self, snapshot: dict[str, Any]):
        """Load state from snapshot."""
        self._state = AdaptiveEvaluationState(
            budget=AdaptiveBudget(
                total_tokens=snapshot["budget"]["total_tokens"],
                consumed_tokens=snapshot["budget"]["consumed_tokens"],
                reserved_tokens=snapshot["budget"]["reserved_tokens"],
                remaining_tokens=snapshot["budget"]["remaining_tokens"],
            ),
            executed_candidates=snapshot["executed_candidates"],
            validated_failures=snapshot["validated_failures"],
            failure_families=snapshot["failure_families"],
            failure_family_counts=snapshot.get("failure_family_counts", {}),
            tool_coverage=snapshot.get("tool_coverage", {}),
            mutation_coverage={
                tool: dict(muts)
                for tool, muts in snapshot.get("mutation_coverage", {}).items()
            },
            taxonomy_coverage=snapshot.get("taxonomy_coverage", {}),
            explored_states=snapshot.get("explored_states", []),
            state_transitions=snapshot.get("state_transitions", []),
            iteration=snapshot.get("iteration", 0),
        )


class EvaluationStateFactory:
    """Factory for creating evaluation states."""

    @staticmethod
    def create_initial_state(
        total_budget: int = 100000,
        split: str = "SEARCH",
        config: Any | None = None,
    ) -> AdaptiveEvaluationState:
        """Create initial evaluation state."""
        return AdaptiveEvaluationState(
            budget=AdaptiveBudget(total_tokens=total_budget),
            split=EvaluationSplit.SEARCH
            if split == "SEARCH"
            else EvaluationSplit.HOLDOUT,
        )

    @staticmethod
    def create_holdout_state(
        total_budget: int = 10000,
        config: Any | None = None,
    ) -> AdaptiveEvaluationState:
        """Create holdout evaluation state."""
        return AdaptiveEvaluationState(
            budget=AdaptiveBudget(total_tokens=total_budget),
            split=EvaluationSplit.HOLDOUT,
        )
