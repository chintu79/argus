"""Adaptive selection domain models for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator

from agent_eval.domain.identifiers import make_id


class CandidateSource(str, Enum):
    """Source of candidate generation."""

    STATIC = "STATIC"
    RANDOM = "RANDOM"
    FAILURE_DIRECTED = "FAILURE_DIRECTED"
    EXPLORATION = "EXPLORATION"
    HOLDOUT = "HOLDOUT"


class MutationOperator(str, Enum):
    """Mutation operator types."""

    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    ARGUMENT_BOUNDARY = "ARGUMENT_BOUNDARY"
    RESOURCE_SUBSTITUTION = "RESOURCE_SUBSTITUTION"
    AUTHORIZATION_BYPASS = "AUTHORIZATION_BYPASS"
    TOOL_SEQUENCE_MUTATION = "TOOL_SEQUENCE_MUTATION"
    CONTEXT_PERTURBATION = "CONTEXT_PERTURBATION"
    STATE_CONSISTENCY_MUTATION = "STATE_CONSISTENCY_MUTATION"
    INVALID_ID = "INVALID_ID"
    MALFORMED_REQUEST = "MALFORMED_REQUEST"
    PERMISSION_BOUNDARY = "PERMISSION_BOUNDARY"


class EvaluationSplit(str, Enum):
    """Evaluation data split."""

    SEARCH = "SEARCH"
    HOLDOUT = "HOLDOUT"


class TestCandidate(BaseModel):
    """A candidate test to be executed in the adaptive evaluation."""

    candidate_id: str = Field(default_factory=lambda: make_id("tc"))
    parent_state_id: str | None = None
    mutation: str | None = None
    target_tool: str | None = None
    target_action: str | None = None
    target_resource: str | None = None
    target_invariant: str | None = None
    predicted_failure_families: list[str] = Field(default_factory=list)
    estimated_cost: int = Field(default=1, ge=1)
    estimated_failure_probability: float = Field(default=0.0, ge=0.0, le=1.0)
    novelty_score: float = Field(default=0.0, ge=0.0, le=1.0)
    information_gain: float = Field(default=0.0, ge=0.0, le=1.0)
    priority_score: float = Field(default=0.0, ge=0.0, le=1.0)
    source: CandidateSource = CandidateSource.STATIC
    generation_iteration: int = 0
    generation_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    metadata: dict[str, Any] = Field(default_factory=dict)
    arguments: dict[str, Any] = Field(default_factory=dict)

    @validator("candidate_id")
    def candidate_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("candidate_id must not be empty")
        return v


class AdaptiveBudget(BaseModel):
    """Budget tracking for adaptive evaluation."""

    total_tokens: int = Field(default=100000, ge=1)
    consumed_tokens: int = Field(default=0, ge=0)
    reserved_tokens: int = Field(default=0, ge=0)
    remaining_tokens: int = Field(default=100000, ge=0)

    def can_afford(self, cost: int) -> bool:
        """Check if budget can afford a cost."""
        return self.remaining_tokens >= cost

    def reserve(self, cost: int) -> bool:
        """Reserve tokens for an execution."""
        if self.can_afford(cost):
            self.reserved_tokens += cost
            self.remaining_tokens -= cost
            return True
        return False

    def commit(self, actual_cost: int) -> bool:
        """Commit actual cost after execution."""
        if self.reserved_tokens >= actual_cost:
            self.reserved_tokens -= actual_cost
            self.consumed_tokens += actual_cost
            return True
        return False

    def release(self, cost: int) -> bool:
        """Release reserved tokens (e.g., on cancellation)."""
        if self.reserved_tokens >= cost:
            self.reserved_tokens -= cost
            self.remaining_tokens += cost
            return True
        return False

    def utilization(self) -> float:
        """Return budget utilization fraction."""
        if self.total_tokens == 0:
            return 0.0
        return self.consumed_tokens / self.total_tokens


class AdaptiveEvaluationState(BaseModel):
    """Current state of the adaptive evaluation."""

    budget: AdaptiveBudget
    executed_candidates: list[str] = Field(default_factory=list)
    pending_candidates: list[str] = Field(default_factory=list)
    validated_failures: list[str] = Field(default_factory=list)
    failure_families: list[str] = Field(default_factory=list)
    explored_states: list[str] = Field(default_factory=list)
    iteration: int = 0
    failure_family_counts: dict[str, int] = Field(default_factory=dict)
    tool_coverage: dict[str, int] = Field(default_factory=dict)
    mutation_coverage: dict[str, dict[str, int]] = Field(default_factory=dict)
    taxonomy_coverage: dict[str, int] = Field(default_factory=dict)
    state_transitions: list[str] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_update: datetime = Field(default_factory=lambda: datetime.now(UTC))
    split: EvaluationSplit = EvaluationSplit.SEARCH

    def touch(self):
        self.last_update = datetime.now(UTC)


class AdaptiveDecision(BaseModel):
    """Record of an adaptive selection decision."""

    decision_id: str = Field(default_factory=lambda: make_id("dec"))
    iteration: int
    candidate_id: str
    novelty: float
    information_gain: float
    failure_probability: float
    coverage_value: float
    normalized_cost: float
    priority_score: float
    selected: bool
    reason: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    evaluation_state_snapshot: dict[str, Any] | None = None


class AdaptiveIteration(BaseModel):
    """Record of an adaptive evaluation iteration."""

    iteration: int
    budget_remaining: int
    candidate_count: int
    selected_candidate_id: str | None = None
    new_family_count: int = 0
    actual_cost: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)


class AdaptiveConfig(BaseModel):
    """Configuration for adaptive selection."""

    max_candidates_per_iteration: int = Field(default=32, ge=1, le=1000)
    max_mutations_per_state: int = Field(default=8, ge=1, le=100)
    max_candidate_depth: int = Field(default=5, ge=1, le=20)

    # Probability estimation
    probability_smoothing_alpha: float = Field(default=1.0, ge=0.1, le=10.0)

    # Priority weights
    priority_novelty: float = Field(default=0.30, ge=0.0, le=1.0)
    priority_information_gain: float = Field(default=0.30, ge=0.0, le=1.0)
    priority_failure_probability: float = Field(default=0.20, ge=0.0, le=1.0)
    priority_coverage: float = Field(default=0.10, ge=0.0, le=1.0)
    priority_cost: float = Field(default=0.10, ge=0.0, le=1.0)

    # Selection
    minimum_budget_reserve: int = Field(default=0, ge=0)

    # Random
    random_seed: int = Field(default=42, ge=0)

    @validator(
        "priority_novelty",
        "priority_information_gain",
        "priority_failure_probability",
        "priority_coverage",
        "priority_cost",
    )
    def weights_non_negative(cls, v):
        if v < 0:
            raise ValueError("Priority weights must be non-negative")
        return v

    @validator(
        "priority_novelty",
        "priority_information_gain",
        "priority_failure_probability",
        "priority_coverage",
        "priority_cost",
        always=True,
    )
    def weights_sum_approx_one(cls, v, values):
        # Check sum is approximately 1.0
        total = (
            values.get("priority_novelty", 0.3)
            + values.get("priority_information_gain", 0.3)
            + values.get("priority_failure_probability", 0.2)
            + values.get("priority_coverage", 0.1)
            + values.get("priority_cost", 0.1)
        )
        if abs(total - 1.0) > 0.1:
            raise ValueError(
                f"Priority weights must sum to approximately 1.0, got {total}"
            )
        return v


class SelectionPolicy(str, Enum):
    """Selection policy type."""

    RANDOM = "RANDOM"
    STATIC = "STATIC"
    FAILURE_DIRECTED = "FAILURE_DIRECTED"


class SelectionPolicyConfig(BaseModel):
    """Configuration for a selection policy."""

    policy: SelectionPolicy = SelectionPolicy.FAILURE_DIRECTED
    adaptive_config: AdaptiveConfig = Field(default_factory=AdaptiveConfig)
    static_order: list[str] = Field(default_factory=list)


class EvaluationSplitConfig(BaseModel):
    """Configuration for evaluation split."""

    search_split: str = "SEARCH"
    holdout_split: str = "HOLDOUT"
