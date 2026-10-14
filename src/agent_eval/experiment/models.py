"""Experiment models for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator

from agent_eval.domain.identifiers import make_id


class EvaluationMethod(str, Enum):
    """Evaluation method types."""
    STATIC = "STATIC"
    RANDOM = "RANDOM"
    UNBRANCHED_ADAPTIVE = "UNBRANCHED_ADAPTIVE"
    STATE_BRANCHED_ADAPTIVE = "STATE_BRANCHED_ADAPTIVE"


class EvaluationSplit(str, Enum):
    """Evaluation data split."""
    SEARCH = "SEARCH"
    HOLDOUT = "HOLDOUT"


class ExperimentStatus(str, Enum):
    """Experiment run status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    FAILED = "FAILED"
    DRY_RUN = "DRY_RUN"


class ExperimentCondition(BaseModel):
    """Validated experimental conditions for matched comparison."""
    experiment_id: str
    run_id: str | None = None
    method: EvaluationMethod
    agent_configuration: dict[str, Any]
    environment_configuration: dict[str, Any]
    task_configuration: dict[str, Any]
    budget_configuration: dict[str, Any]
    seed: int
    configuration_hash: str
    software_version: str
    agent_version: str
    environment_version: str
    task_set_hash: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    status: ExperimentStatus = ExperimentStatus.PENDING

    @validator("experiment_id")
    def exp_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("experiment_id must not be empty")
        return v


class ExperimentRun(BaseModel):
    """A single execution of an evaluation method."""
    run_id: str = Field(default_factory=lambda: make_id("run"))
    experiment_id: str
    method: EvaluationMethod
    seed: int
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    status: ExperimentStatus = ExperimentStatus.RUNNING
    tokens_used: int = 0
    executions: int = 0
    failures_detected: int = 0
    validated_failure_families: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationStrategy:
    """Abstract interface for evaluation strategies."""
    
    def initialize(self, context: Any) -> Any:
        """Initialize strategy with evaluation context."""
        raise NotImplementedError
    
    def next_action(self, state: Any) -> Any | None:
        """Select next evaluation action."""
        raise NotImplementedError
    
    def observe(self, state: Any, result: Any) -> Any:
        """Update strategy state based on execution result."""
        raise NotImplementedError
    
    def is_finished(self, state: Any) -> bool:
        """Check if evaluation is complete."""
        raise NotImplementedError


class EvaluationAction(BaseModel):
    """Action to be executed by the executor."""
    action_id: str = Field(default_factory=lambda: make_id("act"))
    task_id: str
    state_id: str
    candidate_id: str | None = None
    mutation: str | None = None
    strategy: str = "base"
    estimated_cost: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    """Result of executing an evaluation action."""
    action_id: str
    task_id: str
    success: bool
    failure_detected: bool = False
    failure_candidate_id: str | None = None
    failure_family_id: str | None = None
    tokens_used: int = 0
    execution_time: float = 0.0
    final_state_id: str | None = None
    trace_id: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExperimentConfiguration(BaseModel):
    """Complete experiment configuration."""
    experiment_id: str
    name: str
    methods: list[EvaluationMethod] = Field(default_factory=lambda: [
        EvaluationMethod.STATIC,
        EvaluationMethod.RANDOM,
        EvaluationMethod.UNBRANCHED_ADAPTIVE,
        EvaluationMethod.STATE_BRANCHED_ADAPTIVE,
    ])
    budget: dict[str, Any] = Field(default_factory=lambda: {"total_tokens": 500000})
    repetitions: dict[str, Any] = Field(default_factory=lambda: {"seeds": [1, 2, 3, 4, 5]})
    agent: dict[str, Any] = Field(default_factory=lambda: {"temperature": 0.7})
    evaluation: dict[str, Any] = Field(default_factory=lambda: {
        "reproducibility_runs": 3,
        "minimum_rep_k": 0.75,
        "max_steps": 20,
    })
    tasks: dict[str, Any] = Field(default_factory=lambda: {
        "split": "SEARCH",
        "limit": None,
    })
    checkpoint: dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "every_n_actions": 10,
    })
    dry_run: bool = False
    output_dir: str = "artifacts/experiments"
    max_candidates_per_iteration: int = 32
    max_mutations_per_state: int = 8
    max_candidate_depth: int = 5
    
    @validator("experiment_id")
    def exp_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("experiment_id must not be empty")
        return v
    
    @validator("methods")
    def methods_not_empty(cls, v):
        if not v:
            raise ValueError("At least one evaluation method must be specified")
        return v


class ExperimentManifest(BaseModel):
    """Experiment manifest for reproducibility."""
    experiment_id: str
    code_version: str
    config_hash: str
    agent_configuration_hash: str
    environment_version: str
    task_set_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    methods: list[EvaluationMethod]
    total_runs: int
    completed_runs: int = 0
    failed_runs: int = 0