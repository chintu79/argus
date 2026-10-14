"""Cost estimation model for adaptive test selection."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar

from agent_eval.adaptive.models import (
    AdaptiveConfig,
    AdaptiveEvaluationState,
)


class CostCategory(str, Enum):
    """Categories of execution cost."""

    TOOL_INVOCATION = "tool_invocation"
    AUTHORIZATION_CHECK = "authorization_check"
    POLICY_EVALUATION = "policy_evaluation"
    STATE_TRANSITION = "state_transition"
    FAULT_INJECTION = "fault_injection"
    DATA_SERIALIZATION = "data_serialization"
    TRAJECTORY_LOGGING = "trajectory_logging"
    INVARIANT_EVALUATION = "invariant_evaluation"
    FAILURE_DETECTION = "failure_detection"
    REPRODUCIBILITY = "reproducibility"


@dataclass
class CostBreakdown:
    """Detailed breakdown of estimated execution cost."""

    tool_invocation: int = 1
    authorization_check: int = 1
    policy_evaluation: int = 1
    state_transition: int = 1
    fault_injection: int = 0
    data_serialization: int = 1
    trajectory_logging: int = 1
    invariant_evaluation: int = 1
    failure_detection: int = 1
    reproducibility: int = 0

    def total(self) -> int:
        return sum(
            [
                self.tool_invocation,
                self.authorization_check,
                self.policy_evaluation,
                self.state_transition,
                self.fault_injection,
                self.data_serialization,
                self.trajectory_logging,
                self.invariant_evaluation,
                self.failure_detection,
                self.reproducibility,
            ]
        )


class CostModel:
    """Estimates execution cost for test candidates."""

    # Base cost per tool type (in tokens/units)
    TOOL_BASE_COSTS: ClassVar[dict[str, int]] = {
        "customer.lookup": 10,
        "account.lookup": 10,
        "transaction.lookup": 10,
        "ticket.search": 15,
        "ticket.update": 20,
        "notification.send": 5,
        "database.write": 25,
    }

    # Additional cost per mutation type
    MUTATION_COST_MULTIPLIERS: ClassVar[dict[str, float]] = {
        "INVALID_ARGUMENT": 1.0,
        "ARGUMENT_BOUNDARY": 1.2,
        "RESOURCE_SUBSTITUTION": 1.5,
        "AUTHORIZATION_BYPASS": 2.0,
        "TOOL_SEQUENCE_MUTATION": 1.5,
        "CONTEXT_PERTURBATION": 1.2,
        "STATE_CONSISTENCY_MUTATION": 1.5,
        "INVALID_ID": 1.0,
        "MALFORMED_REQUEST": 1.2,
        "PERMISSION_BOUNDARY": 1.8,
    }

    # Cost per additional tool in sequence
    SEQUENCE_COST_PER_TOOL = 5

    # Reproducibility verification cost (multiplier of base cost)
    REPRODUCIBILITY_MULTIPLIER = 2.0

    def __init__(self, config: AdaptiveConfig | None = None):
        self.config = config or AdaptiveConfig()

    def estimate_cost(
        self,
        candidate: Any,
        evaluation_state: AdaptiveEvaluationState,
    ) -> int:
        """
        Estimate execution cost for a candidate.

        Returns:
            Estimated cost in tokens/units
        """
        base_cost = self._base_tool_cost(candidate.target_tool)
        mutation_multiplier = self._mutation_multiplier(candidate.mutation)

        # Base cost
        mult = (
            candidate.mutation_cost_multiplier
            if hasattr(candidate, "mutation_cost_multiplier")
            else mutation_multiplier
        )
        cost = int(base_cost * mult)

        # Add sequence cost if multi-tool
        if hasattr(candidate, "target_tools") and candidate.target_tools:
            cost += (len(candidate.target_tools) - 1) * self.SEQUENCE_COST_PER_TOOL

        # Add fault injection cost
        if hasattr(candidate, "fault_type") and candidate.fault_type:
            cost += 10  # Additional overhead for fault injection

        # Add reproducibility cost if this is a verification run
        if hasattr(candidate, "is_reproduction") and candidate.is_reproduction:
            cost = int(cost * self.REPRODUCIBILITY_MULTIPLIER)

        # Apply minimum cost
        cost = max(cost, 1)

        return cost

    def _base_tool_cost(self, tool_name: str | None) -> int:
        """Get base cost for a tool."""
        if not tool_name:
            return 10
        return self.TOOL_BASE_COSTS.get(tool_name, 10)

    def _mutation_multiplier(self, mutation: str | None) -> float:
        """Get cost multiplier for mutation type."""
        if not mutation:
            return 1.0
        return self.MUTATION_COST_MULTIPLIERS.get(mutation, 1.0)

    def estimate_batch_cost(
        self,
        candidates: list[Any],
        evaluation_state: Any,
    ) -> list[int]:
        """Estimate costs for a batch of candidates."""
        return [self.estimate_cost(c, evaluation_state) for c in candidates]

    def can_afford(
        self,
        candidate: Any,
        evaluation_state: Any,
        budget: int,
    ) -> bool:
        """Check if candidate fits within budget."""
        estimated = self.estimate_cost(candidate, evaluation_state)
        return estimated <= budget

    def detailed_breakdown(
        self,
        candidate: Any,
    ) -> dict[str, int]:
        """Get detailed cost breakdown."""
        breakdown = {
            "tool_invocation": 1,
            "authorization_check": 1,
            "policy_evaluation": 1,
            "state_transition": 1,
            "data_serialization": 1,
            "trajectory_logging": 1,
            "invariant_evaluation": 1,
            "failure_detection": 1,
        }

        # Add mutation-specific costs
        if candidate.mutation:
            mult = self.MUTATION_COST_MULTIPLIERS.get(candidate.mutation, 1.0)
            if mult > 1.0:
                breakdown["mutation_overhead"] = int((mult - 1.0) * 10)

        # Add fault injection
        if hasattr(candidate, "fault_type") and candidate.fault_type:
            breakdown["fault_injection"] = 10

        # Reproducibility
        if hasattr(candidate, "is_reproduction") and candidate.is_reproduction:
            breakdown["reproducibility"] = sum(breakdown.values())

        return breakdown


def estimate_candidate_cost(
    candidate: Any,
    evaluation_state: Any,
) -> int:
    """Convenience function to estimate candidate cost."""
    model = CostModel()
    return model.estimate_cost(candidate, evaluation_state)
