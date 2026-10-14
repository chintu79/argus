"""Adaptive test selection and failure-directed exploration for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

from agent_eval.adaptive.budget import (
    BudgetLedger,
    BudgetManager,
)
from agent_eval.adaptive.candidate_generator import (
    CandidateGenerator,
    MutationOperatorDefinition,
    get_mutation_operator,
    list_mutation_operators,
    register_mutation_operator,
)
from agent_eval.adaptive.cost_model import (
    CostBreakdown,
    CostModel,
    estimate_candidate_cost,
)
from agent_eval.adaptive.information_gain import (
    InformationGainEstimator,
    estimate_information_gain,
)
from agent_eval.adaptive.models import (
    AdaptiveBudget,
    AdaptiveConfig,
    AdaptiveDecision,
    AdaptiveEvaluationState,
    AdaptiveIteration,
    CandidateSource,
    EvaluationSplit,
    MutationOperator,
    SelectionPolicy,
    SelectionPolicyConfig,
    TestCandidate,
)
from agent_eval.adaptive.novelty import (
    NoveltyEstimator,
    compute_batch_novelty,
    compute_novelty,
)
from agent_eval.adaptive.priority import (
    CoverageEstimator,
    FailureProbabilityEstimator,
    PriorityComponents,
    PriorityResult,
    PriorityScorer,
    calculate_priority,
)
from agent_eval.adaptive.repository import (
    AdaptiveRepository,
    get_adaptive_repository,
)
from agent_eval.adaptive.selector import (
    AdaptiveSelector,
    FailureDirectedPolicy,
    RandomPolicy,
    SelectionPolicyInterface,
    StaticPolicy,
    select_next_test,
)
from agent_eval.adaptive.state import (
    EvaluationStateFactory,
    EvaluationStateManager,
)

__all__ = [
    "AdaptiveBudget",
    "AdaptiveConfig",
    "AdaptiveDecision",
    "AdaptiveEvaluationState",
    "AdaptiveIteration",
    # Repository
    "AdaptiveRepository",
    "AdaptiveSelector",
    "BudgetLedger",
    # Budget
    "BudgetManager",
    # Candidate Generation
    "CandidateGenerator",
    "CandidateSource",
    "CostBreakdown",
    # Cost Model
    "CostModel",
    "CoverageEstimator",
    "EvaluationSplit",
    "EvaluationStateFactory",
    # State
    "EvaluationStateManager",
    "FailureDirectedPolicy",
    "FailureProbabilityEstimator",
    # Information Gain
    "InformationGainEstimator",
    "MutationOperator",
    "MutationOperatorDefinition",
    # Novelty
    "NoveltyEstimator",
    # Priority
    "PriorityComponents",
    "PriorityResult",
    "PriorityScorer",
    "RandomPolicy",
    "SelectionPolicy",
    "SelectionPolicyConfig",
    # Selector & Policies
    "SelectionPolicyInterface",
    "StaticPolicy",
    # Models
    "TestCandidate",
    "calculate_priority",
    "compute_batch_novelty",
    "compute_novelty",
    "estimate_candidate_cost",
    "estimate_information_gain",
    "get_adaptive_repository",
    "get_mutation_operator",
    "list_mutation_operators",
    "register_mutation_operator",
    "select_next_test",
]
