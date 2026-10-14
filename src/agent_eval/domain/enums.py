"""
Enumerations for the Budget-Constrained Adaptive Security Evaluation prototype.

All enums are JSON-serializable and framework-independent.
"""

from __future__ import annotations

from enum import Enum, auto


class EvaluationSplit(Enum):
    SEARCH = auto()
    HOLDOUT = auto()


class ExecutionMode(Enum):
    """Mode of execution context."""

    NORMAL = auto()
    BRANCH = auto()
    REPLAY = auto()
    METAMORPHIC_BASE = auto()
    METAMORPHIC_TRANSFORMED = auto()
    HOLDOUT = auto()


class ExecutionOutcome(Enum):
    """Outcome of an execution."""

    PASS = auto()
    FAIL = auto()
    INCONCLUSIVE = auto()
    INVALID = auto()
    ERROR = auto()


class InvariantOutcome(Enum):
    """Result of invariant evaluation."""

    SATISFIED = auto()
    VIOLATED = auto()
    INCONCLUSIVE = auto()
    INVALID = auto()
    ERROR = auto()


class EventType(Enum):
    """Observable execution events captured in trajectories."""

    AGENT_OUTPUT = auto()
    TOOL_REQUEST = auto()
    TOOL_RESPONSE = auto()
    POLICY_DECISION = auto()
    STATE_TRANSITION = auto()
    FAULT_INJECTION = auto()
    SNAPSHOT = auto()
    BRANCH = auto()
    INVARIANT_EVALUATION = auto()
    TERMINATION = auto()
    ERROR = auto()
    COST = auto()


class PolicyDecision(Enum):
    """Policy engine decisions."""

    ALLOW = auto()
    DENY = auto()
    REVIEW = auto()
    ERROR = auto()


class FailureCategory(Enum):
    """Hierarchical failure domain categories."""

    SECURITY = auto()
    RELIABILITY = auto()
    ROBUSTNESS = auto()
    POLICY = auto()
    AUTHORIZATION = auto()
    DATA_EXPOSURE = auto()
    STATE_INTEGRITY = auto()
    RESOURCE = auto()
    EVALUATOR = auto()
    ENVIRONMENT = auto()
    INFRASTRUCTURE = auto()
    SCENARIO = auto()


class FailureValidationStatus(Enum):
    """Status of failure validation."""

    CANDIDATE = auto()
    VALIDATED = auto()
    REJECTED = auto()
    INCONCLUSIVE = auto()


class InvariantSeverity(Enum):
    """Severity levels for invariants."""

    INFO = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class BudgetUnit(Enum):
    """Cost measurement units."""

    MODEL_CALLS = auto()
    TOKENS = auto()
    COMPUTE_TIME = auto()
    WALL_CLOCK = auto()
    MONETARY = auto()
    EXECUTION_UNITS = auto()
    COMPOSITE = auto()


class AgentBehavior(Enum):
    """Deterministic mock-agent behaviors for testing."""

    SAFE_AUTHORIZED_READ = auto()
    UNSAFE_UNAUTHORIZED_READ = auto()
    UNSAFE_WRITE = auto()
    POLICY_BYPASS = auto()
    SAFE_RECOVERY = auto()
    UNSAFE_RECOVERY = auto()
    RESOURCE_ABUSE = auto()


class ScenarioType(Enum):
    """Types of security evaluation scenarios."""

    BENIGN = auto()
    AUTHORIZATION = auto()
    TOOL_SECURITY = auto()
    PROMPT_INJECTION = auto()
    DATA_EXPOSURE = auto()
    STATE_MANIPULATION = auto()
    SEQUENCE_ATTACK = auto()
    FAULT_TOLERANCE = auto()
    ROBUSTNESS = auto()
    RESOURCE_ABUSE = auto()
    RECOVERY = auto()
    BRANCH_ATTACK = auto()
    METAMORPHIC = auto()
    HOLDOUT = auto()


class DifficultyLevel(Enum):
    """Difficulty scale 1-5 as specified."""

    LEVEL_1 = auto()
    LEVEL_2 = auto()
    LEVEL_3 = auto()
    LEVEL_4 = auto()
    LEVEL_5 = auto()


class RiskLevel(Enum):
    """Risk level categorization."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()
