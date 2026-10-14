"""Experiment runner for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from agent_eval.adaptive.candidate_generator import CandidateGenerator
from agent_eval.adaptive.models import (
    AdaptiveConfig,
    AdaptiveEvaluationState,
    TestCandidate,
)
from agent_eval.adaptive.repository import AdaptiveRepository
from agent_eval.adaptive.selector import AdaptiveSelector
from agent_eval.adaptive.state import EvaluationStateFactory
from agent_eval.agents.mock import DeterministicMockAgent
from agent_eval.domain.enums import AgentBehavior, InvariantSeverity
from agent_eval.domain.identifiers import make_id, sanitize_id_for_path
from agent_eval.experiment.mock import create_mock_environment
from agent_eval.experiment.models import (
    EvaluationMethod,
    ExperimentConfiguration,
    ExperimentManifest,
    ExperimentRun,
    ExperimentStatus,
)
from agent_eval.experiment.strategies import MockExecutor, create_strategy
from agent_eval.failures.models import (
    FailureCandidate,
    FailureCandidateStatus,
    FailureReasonCode,
)

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """Main experiment runner orchestrating evaluation execution."""
    
    def __init__(self, config: ExperimentConfiguration):
        self.config = config
        self.experiment_id = config.experiment_id
        self.output_dir = Path(config.output_dir) / config.experiment_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Core components
        self.environment: Any | None = None
        self.agent: DeterministicMockAgent | None = None
        self.strategy: Any | None = None
        self.evaluation_state: AdaptiveEvaluationState | None = None
        self.run: ExperimentRun | None = None
        
        # Persistence
        self.manifest: ExperimentManifest | None = None
        self.current_run: ExperimentRun | None = None
        
        # Checkpoint
        self.checkpoint_enabled = getattr(config.checkpoint, "enabled", True)
        self.checkpoint_interval = getattr(config.checkpoint, "every_n_actions", 10)
        self.action_count = 0
        
        # Repositories
        self.adaptive_repository = AdaptiveRepository()
    
    def validate_configuration(self) -> tuple[bool, list[str]]:
        """Validate experiment configuration before execution."""
        errors = []
        
        # Check methods
        if not self.config.methods:
            errors.append("No evaluation methods specified")
        
        # Check budget
        budget = self.config.budget.get("total_tokens", 0) if isinstance(self.config.budget, dict) else getattr(self.config.budget, "total_tokens", 0)
        if budget <= 0:
            errors.append("Budget must be positive")
        
        # Check seeds
        if isinstance(self.config.repetitions, dict):
            seeds = self.config.repetitions.get("seeds", [])
        else:
            seeds = getattr(self.config.repetitions, "seeds", [])
        if not seeds:
            errors.append("At least one seed required")
        
        # Check agent config
        agent_config = self.config.agent
        if not agent_config:
            errors.append("Agent configuration required")
        
        # Check output directory
        if not self.output_dir:
            errors.append("Output directory required")
        
        return len(errors) == 0, errors
        
    def dry_run(self) -> dict[str, Any]:
        """Perform a dry run showing execution plan."""
        seeds = self.config.repetitions.get("seeds", [1]) if isinstance(self.config.repetitions, dict) else getattr(self.config.repetitions, "seeds", [1])
        total_runs = len(self.config.methods) * len(seeds)
        task_limit = getattr(self.config.tasks, "limit", None)
        
        return {
            "experiment_id": self.experiment_id,
            "methods": [m.value for m in self.config.methods],
            "seeds": seeds,
            "tasks": task_limit if task_limit is not None else "all",
            "budget": getattr(self.config.budget, "total_tokens", 500000),
            "total_runs": total_runs,
            "estimated_actions_per_run": "variable",
            "output_dir": str(self.output_dir),
            "dry_run": True,
        }
    
    def initialize_environment(self, condition: Any) -> None:
        """Initialize the evaluation environment."""
        # Create mock environment for now
        self.environment = create_mock_environment()
    
    def initialize_agent(self, seed: int) -> None:
        """Initialize the agent with given seed."""
        self.agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=seed,
            max_steps=getattr(self.config.evaluation, "max_steps", 20),
        )
    
    def initialize_strategy(
        self,
        method: EvaluationMethod,
        condition: Any,
        config: dict[str, Any] | ExperimentConfiguration,
    ) -> None:
        """Initialize the evaluation strategy."""
        cfg_dict = config if isinstance(config, dict) else config.model_dump()
        self.strategy = create_strategy(method.value, None, cfg_dict)
    
    def initialize_evaluation_state(self, seed: int) -> None:
        """Initialize the adaptive evaluation state."""
        self.evaluation_state = EvaluationStateFactory.create_initial_state(
            total_budget=getattr(self.config.budget, "total_tokens", 500000),
            split="SEARCH",
        )
    
    def run_experiment(self) -> ExperimentManifest:
        """Execute the complete experiment."""
        # Validate configuration
        valid, errors = self.validate_configuration()
        if not valid:
            raise ValueError(f"Configuration invalid: {errors}")
        
        seeds = self.config.repetitions.get("seeds", [1]) if isinstance(self.config.repetitions, dict) else getattr(self.config.repetitions, "seeds", [1])
        total_runs = len(self.config.methods) * len(seeds)
        
        # Create manifest
        self.manifest = ExperimentManifest(
            experiment_id=self.experiment_id,
            code_version=self._get_code_version(),
            config_hash=self._compute_config_hash(),
            agent_configuration_hash=self._hash_dict(self.config.agent),
            environment_version="mock-1.0",
            task_set_hash=self._compute_task_set_hash(),
            created_at=datetime.now(UTC),
            methods=self.config.methods,
            total_runs=total_runs,
        )
        
        # Save manifest
        self._save_manifest()
        
        completed_runs = 0
        failed_runs = 0
        
        for method in self.config.methods:
            for seed in seeds:
                run = self._execute_run(method, seed)
                if run.status == ExperimentStatus.COMPLETED:
                    completed_runs += 1
                else:
                    failed_runs += 1
        
        # Update manifest
        assert self.manifest is not None
        self.manifest.completed_runs = completed_runs
        self.manifest.failed_runs = failed_runs
        self._save_manifest()
        
        return self.manifest
    
    def _execute_run(self, method: EvaluationMethod, seed: int) -> ExperimentRun:
        """Execute a single evaluation run."""
        run_id = make_id("run")
        run = ExperimentRun(
            run_id=run_id,
            experiment_id=self.experiment_id,
            method=method,
            seed=seed,
            started_at=datetime.now(UTC),
            status=ExperimentStatus.RUNNING,
        )
        
        # Create run directory
        run_dir = self.output_dir / "runs" / run.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Initialize components
            self.initialize_environment(None)
            self.initialize_agent(seed)
            self.initialize_strategy(method, None, self.config)
            self.initialize_evaluation_state(seed)
            
            # Create run record
            self.run = run
            run.status = ExperimentStatus.RUNNING
            self._save_run(run)
            
            # Initialize strategy with proper context
            assert self.strategy is not None
            self.strategy.initialize({
                "environment": self.environment,
                "agent": self.agent,
                "evaluation_state": self.evaluation_state,
                "config": self.config,
            })
            
            # Execute evaluation loop
            self._run_evaluation_loop(run)
            
            run.status = ExperimentStatus.COMPLETED
            run.completed_at = datetime.now(UTC)
            
        except Exception as e:
            logger.exception("Run %s failed", run.run_id)
            run.status = ExperimentStatus.FAILED
            run.completed_at = datetime.now(UTC)
            run.metadata["error"] = f"{type(e).__name__}: {e!s}"
            try:
                self._save_error(run, e)
            except Exception as save_err:
                logger.debug("Failed to save error: %s", save_err)
        
        finally:
            self._save_run(run)
            self._save_run_artifacts(run)
        
        return run
    
    def _run_evaluation_loop(self, run: ExperimentRun) -> None:
        """Main evaluation loop using the strategy."""
        
        if not self.strategy:
            return
        
        # Initialize strategy state
        self._strategy_state = self.strategy.initialize({
            "environment": self.environment,
            "agent": self.agent,
            "evaluation_state": self.evaluation_state,
            "config": self.config,
        })
        
        # Main loop
        iteration = 0
        max_iterations = 1000  # Safety limit
        
        while iteration < max_iterations:
            # Check if finished
            if self.strategy.is_finished(self._strategy_state):
                break
            
            if not self._can_continue():
                break
            
            # Get next action from strategy
            action = self.strategy.next_action(self._strategy_state)
            if not action:
                break
            
            # Execute action
            result = self._execute_action(action)
            
            # Process result
            self._process_result(result)
            
            # Observe result in strategy
            self._strategy_state = self.strategy.observe(self._strategy_state, result)
            
            # Update run metrics
            run.executions += 1
            run.tokens_used += result.tokens_used
            if result.failure_detected:
                run.failures_detected += 1
            
            # Checkpoint
            self.action_count += 1
            if self.checkpoint_enabled and self.action_count % self.checkpoint_interval == 0:
                self._checkpoint()
            
            iteration += 1
        
        # Update run metrics
        run.tokens_used = self.evaluation_state.budget.consumed_tokens if self.evaluation_state else 0
        run.failures_detected = run.failures_detected
        run.validated_failure_families = len(self.evaluation_state.failure_families) if self.evaluation_state else 0
    
    def _can_continue(self) -> bool:
        """Check if evaluation can continue."""
        # Check budget
        if self.evaluation_state:
            return self.evaluation_state.budget.can_afford(1)
        return True
    
    def _generate_candidates(self) -> list[TestCandidate]:
        """Generate test candidates using the candidate generator."""
        if self.evaluation_state is None:
            return []
        generator = CandidateGenerator()
        return generator.generate(
            evaluation_state=self.evaluation_state,
            configuration=self._create_adaptive_config(),
        )
    
    def _create_adaptive_config(self) -> AdaptiveConfig:
        """Create adaptive config from experiment configuration."""
        return AdaptiveConfig(
            max_candidates_per_iteration=getattr(self.config, "max_candidates_per_iteration", 10),
            max_mutations_per_state=getattr(self.config, "max_mutations_per_state", 3),
            max_candidate_depth=getattr(self.config, "max_candidate_depth", 5),
        )

    def _select_next_action(self, candidates: list[TestCandidate]) -> TestCandidate | None:
        """Select next action from candidates using the adaptive selector."""
        if not candidates or self.evaluation_state is None:
            return None
        
        selector = AdaptiveSelector(self._create_adaptive_config())
        return selector._policy.select(candidates, self.evaluation_state)
    
    def _execute_action(self, action: Any) -> Any:
        """Execute an evaluation action."""
        mock_executor = MockExecutor()
        return mock_executor.execute(action)
    
    def _process_result(self, result: Any) -> None:
        """Process execution result."""
        if result.failure_detected:
            _fc = FailureCandidate(
                failure_id=make_id("fc"),
                trajectory_id=make_id("traj"),
                invariant_result_id=make_id("ie"),
                invariant_id="I2",
                status=FailureCandidateStatus.CANDIDATE,
                severity=InvariantSeverity.CRITICAL,
                reason_code=FailureReasonCode.DENIED_ACTION_MUTATED_STATE,
                description="Detected failure",
                evidence=result.metadata if isinstance(result.metadata, dict) else {"raw": str(result.metadata)},
            )
            # detector would be called here if needed
    
    def _update_state(self, action: Any, result: Any) -> None:
        """Update evaluation state with result."""
        if self.evaluation_state:
            self.evaluation_state.budget.commit(result.tokens_used)
            if result.failure_detected:
                # Handle failure
                pass
    
    def _checkpoint(self) -> None:
        """Save checkpoint."""
    
    def _save_manifest(self) -> None:
        """Save experiment manifest."""
        if self.manifest is None:
            return
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(self.manifest.model_dump(mode="json"), f, indent=2, default=str)
    
    def _get_run_dir(self, run_id: str) -> Path:
        """Get validated and contained run directory."""
        safe_id = sanitize_id_for_path(run_id)
        run_dir = (self.output_dir / "runs" / safe_id).resolve()
        if not run_dir.is_relative_to(self.output_dir.resolve()):
            raise ValueError(f"Path traversal detected in run_id: {run_id}")
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def _save_run(self, run: ExperimentRun) -> None:
        """Save run record."""
        run_dir = self._get_run_dir(run.run_id)
        run_path = run_dir / "run.json"
        with open(run_path, "w") as f:
            json.dump(run.model_dump(mode="json"), f, indent=2, default=str)
    
    def _save_run_artifacts(self, run: ExperimentRun) -> None:
        """Save run artifacts (actions, results, etc.)."""
        run_dir = self._get_run_dir(run.run_id)
        
        # Save actions
        actions_path = run_dir / "actions.jsonl"
        with open(actions_path, "w") as f:
            pass  # Would write actions
        
        # Save results
        results_path = run_dir / "results.jsonl"
        with open(results_path, "w") as f:
            pass
        
        # Save summary
        summary_path = run_dir / "summary.json"
        summary = {
            "run_id": run.run_id,
            "method": run.method.value if hasattr(run.method, 'value') else str(run.method),
            "seed": run.seed,
            "status": run.status.value if hasattr(run.status, 'value') else str(run.status),
            "tokens_used": run.tokens_used,
            "executions": run.executions,
            "failures_detected": run.failures_detected,
            "validated_failure_families": run.validated_failure_families,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        }
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2, default=str)
    
    def _save_error(self, run: ExperimentRun, error: Exception) -> None:
        """Save error information."""
        run_dir = self._get_run_dir(run.run_id)
        error_path = run_dir / "error.json"
        with open(error_path, "w") as f:
            json.dump({
                "error": str(error),
                "type": type(error).__name__,
                "timestamp": datetime.now(UTC).isoformat(),
            }, f, indent=2)
    
    def _get_code_version(self) -> str:
        """Get code version (git commit hash)."""
        try:
            repo_root = Path(__file__).resolve().parents[3]
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=str(repo_root),
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, OSError) as git_err:
            logger.debug("Failed to get git commit hash: %s", git_err)
        return "unknown"
    
    @staticmethod
    def _hash_data(data: Any) -> str:
        """Hash serializable data using SHA-256."""
        s = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(s.encode()).hexdigest()[:16]

    def _compute_config_hash(self) -> str:
        """Compute hash of experiment configuration."""
        return self._hash_data(self.config.model_dump())
    
    def _compute_task_set_hash(self) -> str:
        """Compute hash of task set."""
        return self._hash_data(self.config.tasks)
    
    def _hash_dict(self, d: dict[str, Any]) -> str:
        """Hash a dictionary."""
        return self._hash_data(d)


def run_experiment(config: ExperimentConfiguration) -> ExperimentManifest:
    """Convenience function to run an experiment."""
    runner = ExperimentRunner(config)
    return runner.run_experiment()


def dry_run(config: ExperimentConfiguration) -> dict[str, Any]:
    """Perform a dry run of the experiment."""
    runner = ExperimentRunner(config)
    return runner.dry_run()