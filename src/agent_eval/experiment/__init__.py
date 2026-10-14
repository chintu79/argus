"""Experiment harness for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

from agent_eval.experiment.cli import experiment
from agent_eval.experiment.mock import MockEnvironment, create_mock_environment
from agent_eval.experiment.models import (
    EvaluationAction,
    EvaluationMethod,
    EvaluationResult,
    ExperimentCondition,
    ExperimentConfiguration,
    ExperimentManifest,
    ExperimentRun,
    ExperimentStatus,
)
from agent_eval.experiment.runner import (
    ExperimentRunner,
    dry_run,
    run_experiment,
)

# Aliases for backwards compatibility
ExperimentMethod = EvaluationMethod
Method = EvaluationMethod

__all__ = [
    "EvaluationAction",
    "EvaluationMethod",
    "EvaluationResult",
    "ExperimentCondition",
    "ExperimentConfiguration",
    "ExperimentManifest",
    "ExperimentMethod",
    "ExperimentRun",
    "ExperimentRunner",
    "ExperimentStatus",
    "Method",
    "MockEnvironment",
    "create_mock_environment",
    "dry_run",
    "experiment",
    "run_experiment",
]
