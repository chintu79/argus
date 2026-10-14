"""SQLAlchemy persistence models corresponding to domain entities.

These models map directly to SQLite tables and are NOT the domain models.
The domain layer (src/agent_eval.domain) must not import this module.
"""

from __future__ import annotations

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base

# ── Experiment ──────────────────────────────────────────────────────────────


class ExperimentModel(Base):
    """Persistence model for experiments."""

    __tablename__ = "experiments"

    experiment_id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    version = Column(String, nullable=False, default="1.0.0")
    research_question = Column(Text, nullable=True)
    method = Column(String, nullable=True)
    budget_id = Column(String, ForeignKey("budgets.budget_id"), nullable=True)
    agent_id = Column(String, ForeignKey("agents.agent_id"), nullable=True)
    environment_id = Column(String, ForeignKey("environments.environment_id"), nullable=True)
    scenario_pool_id = Column(String, nullable=True)
    seed = Column(Integer, nullable=True)
    configuration_hash = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    budget = relationship("BudgetModel", back_populates="experiment")
    agent = relationship("AgentModel", back_populates="experiment", uselist=False)
    environment = relationship(
        "EnvironmentModel", back_populates="experiment", uselist=False
    )


# ── Agent ───────────────────────────────────────────────────────────────────


class AgentModel(Base):
    """Persistence model for agent configurations."""

    __tablename__ = "agents"

    agent_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    system_configuration = Column(JSON, nullable=True, default=dict)
    generation_configuration = Column(JSON, nullable=True, default=dict)
    capabilities = Column(JSON, nullable=True, default=list)
    policy_constraints = Column(JSON, nullable=True, default=dict)
    memory_configuration = Column(JSON, nullable=True, default=dict)
    determinism_configuration = Column(JSON, nullable=True, default=dict)
    version = Column(String, nullable=False, default="1.0.0")
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    experiment = relationship("ExperimentModel", back_populates="agent")


# ── Environment ─────────────────────────────────────────────────────────────


class EnvironmentModel(Base):
    """Persistence model for environment configurations."""

    __tablename__ = "environments"

    environment_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False, default="1.0.0")
    tool_registry = Column(JSON, nullable=True, default=dict)
    policy_configuration = Column(JSON, nullable=True, default=dict)
    fault_configuration = Column(JSON, nullable=True, default=dict)
    state_configuration = Column(JSON, nullable=True, default=dict)
    capability_registry = Column(JSON, nullable=True, default=list)
    service_configuration = Column(JSON, nullable=True, default=dict)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    experiment = relationship("ExperimentModel", back_populates="environment")


# ── Scenario ────────────────────────────────────────────────────────────────


class ScenarioModel(Base):
    """Persistence model for scenarios."""

    __tablename__ = "scenarios"

    scenario_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    scenario_type = Column(String, nullable=False)
    version = Column(String, nullable=False, default="1.0.0")
    difficulty = Column(Integer, nullable=True)  # 1-5 scale
    risk_level = Column(String, nullable=True)
    preconditions = Column(Text, nullable=True)
    initial_state = Column(JSON, nullable=True, default=dict)
    goal = Column(Text, nullable=True)
    attack_objective = Column(Text, nullable=True)
    attack_surface = Column(Text, nullable=True)
    expected_behavior = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True, default=list)
    seed = Column(Integer, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    candidates = relationship(
        "CandidateModel", back_populates="scenario", cascade="all, delete-orphan"
    )


# ── Candidate ───────────────────────────────────────────────────────────────


class CandidateModel(Base):
    """Persistence model for candidates."""

    __tablename__ = "candidates"

    candidate_id = Column(String, primary_key=True)
    scenario_id = Column(String, ForeignKey("scenarios.scenario_id"), nullable=False)
    scenario_version = Column(String, nullable=False, default="1.0.0")
    candidate_type = Column(String, nullable=True)
    parameters = Column(JSON, nullable=True, default=dict)
    estimated_cost = Column(Integer, nullable=True, default=0)
    novelty_score = Column(Integer, nullable=True, default=0)
    branch_potential = Column(Integer, nullable=True, default=0)
    severity_score = Column(Integer, nullable=True, default=0)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    scenario = relationship("ScenarioModel")
    executions = relationship(
        "ExecutionModel", back_populates="candidate", cascade="all, delete-orphan"
    )


# ── Execution ───────────────────────────────────────────────────────────────


class ExecutionModel(Base):
    """Persistence model for executions."""

    __tablename__ = "executions"

    execution_id = Column(String, primary_key=True)
    experiment_id = Column(
        String, ForeignKey("experiments.experiment_id"), nullable=False
    )
    run_id = Column(String, nullable=True)
    candidate_id = Column(String, ForeignKey("candidates.candidate_id"), nullable=False)
    scenario_id = Column(String, ForeignKey("scenarios.scenario_id"), nullable=False)
    agent_id = Column(String, ForeignKey("agents.agent_id"), nullable=True)
    environment_id = Column(
        String, ForeignKey("environments.environment_id"), nullable=True
    )
    execution_mode = Column(String, nullable=False, default="NORMAL")
    seed = Column(Integer, nullable=True)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="running")
    outcome = Column(String, nullable=True)  # PASS, FAIL, etc.
    trajectory_id = Column(
        String, ForeignKey("trajectories.trajectory_id"), nullable=True
    )
    parent_execution_id = Column(
        String, ForeignKey("executions.execution_id"), nullable=True
    )
    parent_snapshot_id = Column(String, ForeignKey("states.state_id"), nullable=True)
    cost = Column(Integer, nullable=True, default=0)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    experiment = relationship("ExperimentModel")
    candidate = relationship("CandidateModel", back_populates="executions")
    scenario = relationship("ScenarioModel")
    agent = relationship("AgentModel", uselist=False)
    environment = relationship("EnvironmentModel", uselist=False)
    trajectory = relationship(
        "TrajectoryModel",
        back_populates="execution",
        uselist=False,
        cascade="all, delete-orphan",
    )
    parent_execution = relationship(
        "ExecutionModel", remote_side=[execution_id], foreign_keys=[parent_execution_id]
    )


# ── Trajectory ─────────────────────────────────────────────────────────────


class TrajectoryModel(Base):
    """Persistence model for trajectories."""

    __tablename__ = "trajectories"

    trajectory_id = Column(String, primary_key=True)
    execution_id = Column(String, ForeignKey("executions.execution_id"), nullable=False)
    initial_state_id = Column(String, ForeignKey("states.state_id"), nullable=True)
    final_state_id = Column(String, ForeignKey("states.state_id"), nullable=True)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    execution = relationship("ExecutionModel", back_populates="trajectory")
    events = relationship(
        "TrajectoryEventModel",
        back_populates="trajectory",
        cascade="all, delete-orphan",
    )
    final_state = relationship("StateModel", foreign_keys=[final_state_id])


# ── Trajectory Event ───────────────────────────────────────────────────────


class TrajectoryEventModel(Base):
    """Persistence model for trajectory events."""

    __tablename__ = "trajectory_events"

    event_id = Column(String, primary_key=True)
    trajectory_id = Column(
        String, ForeignKey("trajectories.trajectory_id"), nullable=False
    )
    sequence_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String, nullable=False)  # EventType enum name
    state_id = Column(String, ForeignKey("states.state_id"), nullable=True)
    payload = Column(JSON, nullable=True, default=dict)
    source = Column(String, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Indexes are handled via __table_args__

    __table_args__ = (
        Index("ix_trajectory_event_trajectory_seq", "trajectory_id", "sequence_number"),
        Index("ix_trajectory_event_state", "state_id"),
    )

    # Relationship
    trajectory = relationship("TrajectoryModel", back_populates="events")


# ── State ───────────────────────────────────────────────────────────────────


class StateModel(Base):
    """Persistence model for execution/environment states."""

    __tablename__ = "states"

    state_id = Column(String, primary_key=True)
    execution_id = Column(String, ForeignKey("executions.execution_id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    identity_state = Column(JSON, nullable=True, default=dict)
    authorization_state = Column(JSON, nullable=True, default=dict)
    data_state = Column(JSON, nullable=True, default=dict)
    tool_state = Column(JSON, nullable=True, default=dict)
    service_state = Column(JSON, nullable=True, default=dict)
    policy_state = Column(JSON, nullable=True, default=dict)
    task_state = Column(JSON, nullable=True, default=dict)
    fault_state = Column(JSON, nullable=True, default=dict)
    resource_state = Column(JSON, nullable=True, default=dict)
    parent_state_id = Column(String, ForeignKey("states.state_id"), nullable=True)
    state_hash = Column(String, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Indexes
    __table_args__ = (
        Index("ix_states_execution", "execution_id"),
        Index("ix_states_parent", "parent_state_id"),
        Index("ix_states_hash", "state_hash"),
    )

    # Relationships
    execution = relationship("ExecutionModel")
    parent_state = relationship("StateModel", remote_side=[state_id])


# ── Invariant ───────────────────────────────────────────────────────────────


class InvariantModel(Base):
    """Persistence model for invariants."""

    __tablename__ = "invariants"

    invariant_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    expression_or_rule = Column(Text, nullable=True)
    version = Column(String, nullable=False, default="1.0.0")
    enabled = Column(Boolean, nullable=False, default=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    evaluations = relationship(
        "InvariantEvaluationModel",
        back_populates="invariant",
        cascade="all, delete-orphan",
    )


# ── Invariant Evaluation ────────────────────────────────────────────────────


class InvariantEvaluationModel(Base):
    """Persistence model for invariant evaluations."""

    __tablename__ = "invariant_evaluations"

    invariant_evaluation_id = Column(String, primary_key=True)
    invariant_id = Column(String, ForeignKey("invariants.invariant_id"), nullable=False)
    execution_id = Column(String, ForeignKey("executions.execution_id"), nullable=False)
    trajectory_id = Column(
        String, ForeignKey("trajectories.trajectory_id"), nullable=True
    )
    outcome = Column(String, nullable=False)  # InvariantOutcome enum name
    evaluated_at = Column(DateTime, nullable=False)
    evidence = Column(JSON, nullable=True, default=dict)
    event_ids = Column(JSON, nullable=True, default=list)
    state_ids = Column(JSON, nullable=True, default=list)
    explanation = Column(Text, nullable=True)
    detector_version = Column(String, nullable=True, default="1.0.0")
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    invariant = relationship("InvariantModel", back_populates="evaluations")


# ── Budget ──────────────────────────────────────────────────────────────────


class BudgetModel(Base):
    """Persistence model for budgets."""

    __tablename__ = "budgets"

    budget_id = Column(String, primary_key=True)
    unit = Column(String, nullable=False)  # BudgetUnit enum name
    total_budget = Column(Integer, nullable=False, default=0)
    generation_cost = Column(Integer, nullable=True, default=0)
    execution_cost = Column(Integer, nullable=True, default=0)
    branch_cost = Column(Integer, nullable=True, default=0)
    snapshot_cost = Column(Integer, nullable=True, default=0)
    restore_cost = Column(Integer, nullable=True, default=0)
    analysis_cost = Column(Integer, nullable=True, default=0)
    verification_cost = Column(Integer, nullable=True, default=0)
    consumed = Column(Integer, nullable=True, default=0)
    remaining = Column(Integer, nullable=True, default=0)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    experiment = relationship("ExperimentModel", back_populates="budget", uselist=False)


# ── Failure Candidate ───────────────────────────────────────────────────────


class FailureCandidateModel(Base):
    """Persistence model for failure candidates."""

    __tablename__ = "failure_candidates"

    failure_id = Column(String, primary_key=True)
    execution_id = Column(String, ForeignKey("executions.execution_id"), nullable=False)
    trajectory_id = Column(
        String, ForeignKey("trajectories.trajectory_id"), nullable=False
    )
    invariant_id = Column(String, ForeignKey("invariants.invariant_id"), nullable=False)
    invariant_evaluation_id = Column(
        String,
        ForeignKey("invariant_evaluations.invariant_evaluation_id"),
        nullable=False,
    )
    category = Column(String, nullable=True)
    validation_status = Column(
        String, nullable=False
    )  # FailureValidationStatus enum name
    event_ids = Column(JSON, nullable=True, default=list)
    state_ids = Column(JSON, nullable=True, default=list)
    description = Column(Text, nullable=True)
    evidence = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    execution = relationship("ExecutionModel")
    trajectory = relationship("TrajectoryModel")
    invariant = relationship("InvariantModel")
    invariant_evaluation = relationship(
        "InvariantEvaluationModel"
    )


# ── Validated Failure ───────────────────────────────────────────────────────


class ValidatedFailureModel(Base):
    """Persistence model for validated failures."""

    __tablename__ = "validated_failures"

    failure_id = Column(String, primary_key=True)
    execution_id = Column(String, ForeignKey("executions.execution_id"), nullable=False)
    trajectory_id = Column(
        String, ForeignKey("trajectories.trajectory_id"), nullable=False
    )
    invariant_id = Column(String, ForeignKey("invariants.invariant_id"), nullable=False)
    invariant_evaluation_id = Column(
        String,
        ForeignKey("invariant_evaluations.invariant_evaluation_id"),
        nullable=False,
    )
    category = Column(String, nullable=True)
    validation_status = Column(
        String, nullable=False
    )  # FailureValidationStatus.VALIDATED
    event_ids = Column(JSON, nullable=True, default=list)
    state_ids = Column(JSON, nullable=True, default=list)
    description = Column(Text, nullable=True)
    evidence = Column(Text, nullable=True)
    family_id = Column(String, nullable=True)
    canonical_signature = Column(String, nullable=True)
    reproduction_count = Column(Integer, nullable=True, default=0)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    execution = relationship("ExecutionModel")
    trajectory = relationship("TrajectoryModel")
    invariant = relationship("InvariantModel")
    invariant_evaluation = relationship(
        "InvariantEvaluationModel"
    )
