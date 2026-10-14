"""Experiment harness integrating all components."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent_eval.adaptive.candidate_generator import CandidateGenerator
from agent_eval.adaptive.models import AdaptiveEvaluationState
from agent_eval.adaptive.state import EvaluationStateFactory
from agent_eval.agents.mock import DeterministicMockAgent
from agent_eval.domain.enums import AgentBehavior
from agent_eval.experiment.mock import create_mock_environment
from agent_eval.experiment.models import ExperimentConfiguration
from agent_eval.experiment.strategies import create_strategy


class EvaluationHarness:
    """High-level experiment harness coordinating all components."""
    
    def __init__(self, config: ExperimentConfiguration):
        self.config = config
        self.experiment_id = config.experiment_id
        self.output_dir = Path("artifacts/experiments") / config.experiment_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Components
        self.environment: Any | None = None
        self.agent: DeterministicMockAgent | None = None
        self.strategy: Any | None = None
        self.evaluation_state: AdaptiveEvaluationState | None = None
        
        # State
        self.manifest: Any | None = None
        self.current_run: Any | None = None
        self.action_count = 0
    
    def setup(self, method: str = "STATE_BRANCHED_ADAPTIVE", seed: int = 42) -> None:
        """Set up all components for a run."""
        # Environment
        self.environment = create_mock_environment()
        
        # Agent
        self.agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=seed,
            max_steps=20,
        )
        
        # Strategy
        self.strategy = create_strategy(method, None, {"max_steps": 20})
        
        # Evaluation state
        self.evaluation_state = EvaluationStateFactory.create_initial_state(
            total_budget=50000,
            split="SEARCH",
        )
    
    def run_single(self, method: str = "STATE_BRANCHED_ADAPTIVE", seed: int = 42) -> dict:
        """Run a single evaluation."""
        self.setup(method, seed)
        if self.strategy is None or self.evaluation_state is None:
            raise RuntimeError("Harness setup failed")
        
        # Initialize strategy
        self.strategy.initialize({
            "environment": self.environment,
            "agent": self.agent,
            "evaluation_state": self.evaluation_state,
        })
        
        # Run loop
        actions_executed = 0
        failures_detected = 0
        generator = CandidateGenerator()
        
        for iteration in range(10):  # Max 10 iterations for smoke test
            candidates = generator.generate(
                evaluation_state=self.evaluation_state,
                configuration={"max_steps": 20},
            )
            
            if not candidates:
                break
            
            action = candidates[0]
            if not action:
                break
            
            actions_executed += 1
        
        return {
            "actions_executed": actions_executed,
            "failures_detected": failures_detected,
            "validated_families": 0,
            "tokens_used": actions_executed,
        }


class ExperimentHarness:
    """Main experiment harness."""
    
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.experiment_id = config.get("experiment_id", "experiment")
        self.output_dir = Path("artifacts/experiments") / self.experiment_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_smoke_test(self) -> dict:
        """Run a smoke test with minimal configuration."""
        methods = ["STATIC", "RANDOM", "UNBRANCHED_ADAPTIVE", "STATE_BRANCHED_ADAPTIVE"]
        results = {}
        
        for method in methods:
            # Create components
            env = create_mock_environment()
            agent = DeterministicMockAgent(
                behavior=AgentBehavior.SAFE_AUTHORIZED_READ, seed=42
            )
            strategy = create_strategy(method, None, {"max_steps": 10})
            
            # Run a few steps
            strategy.initialize({
                "environment": env,
                "agent": agent,
            })
            
            actions = 0
            for _ in range(5):  # 5 steps per method
                action = strategy.next_action({})
                if action is None:
                    break
                actions += 1
            
            results[method] = {
                "actions_executed": actions,
                "failures_detected": 0,
                "validated_families": 0,
            }
        
        return {
            "methods_tested": list(results.keys()),
            "results": results,
            "total_actions": sum(r["actions_executed"] for r in results.values()),
        }
    
    def run_full_experiment(self, config: dict) -> dict:
        """Run full experiment with all methods and seeds."""
        # This would be the full implementation
        return {"status": "not_implemented"}


def run_smoke_test(config: dict) -> dict:
    """Run a smoke test experiment."""
    harness = ExperimentHarness(config)
    return harness.run_smoke_test()


def run_experiment(config: dict) -> dict:
    """Run full experiment."""
    harness = ExperimentHarness(config)
    return harness.run_full_experiment(config)


def validate_config(config: dict) -> tuple[bool, list[str]]:
    """Validate experiment configuration."""
    errors = []
    
    if not config.get("experiment_id"):
        errors.append("experiment_id is required")
    
    if not config.get("methods"):
        errors.append("At least one method required")
    
    if config.get("budget", {}).get("total_tokens", 0) <= 0:
        errors.append("Budget must be positive")
    
    if not config.get("repetitions", {}).get("seeds"):
        errors.append("At least one seed required")
    
    return len(errors) == 0, errors