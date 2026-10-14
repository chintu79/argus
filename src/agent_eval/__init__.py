"""Budget-Constrained Adaptive Security Evaluation of AI Agents."""

__version__ = "0.1.0"


# Domain re-exports for convenience (Phase 1: identifiers, enums, common)

from agent_eval.domain.common import (
    BaseDomainModel,
    DomainMetadata,
    JSONSerializable,
    Timestamp,
    VersionedModel,
)
from agent_eval.domain.enums import (
    AgentBehavior,
    BudgetUnit,
    DifficultyLevel,
    EventType,
    ExecutionMode,
    ExecutionOutcome,
    FailureCategory,
    FailureValidationStatus,
    InvariantOutcome,
    PolicyDecision,
    RiskLevel,
    ScenarioType,
)
from agent_eval.domain.identifiers import (
    AgentId,
    BranchId,
    BudgetId,
    CandidateId,
    EnvironmentId,
    EventId,
    ExecutionId,
    ExperimentId,
    FailureFamilyId,
    FailureId,
    InvariantEvaluationId,
    InvariantId,
    RunId,
    ScenarioId,
    SnapshotId,
    StateId,
    TrajectoryId,
    is_valid,
    make_id,
)

__all__ = [
    "AgentBehavior",
    "AgentId",
    "BaseDomainModel",
    "BranchId",
    "BudgetId",
    "BudgetUnit",
    "CandidateId",
    "DifficultyLevel",
    # Common
    "DomainMetadata",
    "EnvironmentId",
    "EventId",
    "EventType",
    "ExecutionId",
    # Enums
    "ExecutionMode",
    "ExecutionOutcome",
    # Identifiers
    "ExperimentId",
    "FailureCategory",
    "FailureFamilyId",
    "FailureId",
    "FailureValidationStatus",
    "InvariantEvaluationId",
    "InvariantId",
    "InvariantOutcome",
    "JSONSerializable",
    "PolicyDecision",
    "RiskLevel",
    "RunId",
    "ScenarioId",
    "ScenarioType",
    "SnapshotId",
    "StateId",
    "Timestamp",
    "TrajectoryId",
    "VersionedModel",
    "__version__",
    "is_valid",
    "make_id",
]
