"""Budget-Constrained Adaptive Security Evaluation of AI Agents."""

__version__ = "0.1.0"

# Core domain re-exports for convenience
from agent_eval.domain.models import (
    Scenario,
    Candidate,
    Agent,
    Environment,
    Execution,
    Trajectory,
    TrajectoryEvent,
    State,
    Invariant,
    InvariantEvaluation,
    FailureCandidate,
    ValidatedFailure,
    Budget,
)

from agent_eval.domain.value_objects import (
    EventType,
    InvariantStatus,
    FailureStatus,
    BudgetStatus,
)

# Public API surface (minimal for Phase 0)
from agent_eval.cli.main import main

__all__ = [
    "__version__",
    "Scenario",
    "Candidate",
    "Agent",
    "Environment",
    "Execution",
    "Trajectory",
    "TrajectoryEvent",
    "State",
    "Invariant",
    "InvariantEvaluation",
    "FailureCandidate",
    "ValidatedFailure",
    "Budget",
    "EventType",
    "InvariantStatus",
    "FailureStatus",
    "BudgetStatus",
    "main",
]