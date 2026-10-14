"""Verification runner - executes individual verification runs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from agent_eval.domain.identifiers import make_id
from agent_eval.reproducibility.models import (
    ReproducibilityRequest,
    SignatureMatchResult,
    VerificationRun,
    VerificationRunStatus,
)
from agent_eval.reproducibility.signature import (
    SignatureComparator,
    SignatureExtractor,
)


class VerificationRunner:
    """Executes individual verification runs against a scenario."""

    def __init__(self, agent: Any, environment: Any):
        self._agent = agent
        self._environment = environment

    def execute_verification_run(
        self,
        run: VerificationRun,
        request: ReproducibilityRequest,
        scenario: Any,
        agent: Any,
        environment: Any,
        target_signature: Any,
    ) -> VerificationRun:
        """Execute a single verification run and compare against target signature.

        Flow:
        1. Reset environment and agent
        2. Set seed
        3. Execute scenario
        4. Capture trajectory
        5. Evaluate invariants
        6. Extract signatures
        7. Compare against target
        """
        run.status = VerificationRunStatus.RUNNING
        run.started_at = datetime.now(UTC)

        try:
            # Step 1: Reset environment and agent
            self._reset_execution_state(environment, agent, run.seed)

            # Step 2: Execute scenario
            trajectory, invariant_results = self._execute_scenario(
                scenario, agent, environment, run.seed
            )

            run.trajectory_id = getattr(trajectory, "trajectory_id", None)
            run.invariant_results = self._serialize_invariant_results(invariant_results)

            # Step 2: Extract signatures from this run
            observed_signatures = (
                SignatureExtractor.extract_from_trajectory_and_results(
                    trajectory, invariant_results
                )
            )

            # Step 3: Compare against target signature
            if target_signature:
                match_result = SignatureComparator.compare_against_list(
                    target_signature, observed_signatures
                )
                run.target_matched = match_result
            else:
                run.target_matched = SignatureMatchResult.INCONCLUSIVE

            run.status = VerificationRunStatus.COMPLETED

        except Exception as e:
            run.status = VerificationRunStatus.FAILED
            run.error = str(e)

        run.completed_at = datetime.now(UTC)
        return run

    def _reset_execution_state(
        self,
        environment: Any,
        agent: Any,
        seed: int,
    ) -> None:
        """Reset environment and agent to clean initial state."""
        # Reset environment
        if hasattr(environment, "reset"):
            environment.reset()

        # Reset agent
        if hasattr(agent, "reset"):
            agent.reset()

        # Set seed for deterministic behavior
        if hasattr(agent, "seed"):
            agent.seed = seed
        if hasattr(environment, "seed"):
            environment.seed = seed

    def _execute_scenario(
        self,
        scenario: Any,
        agent: Any,
        environment: Any,
        seed: int,
    ) -> tuple:
        """Execute the scenario and return trajectory and invariant results.

        This is a placeholder that should be replaced with actual
        execution engine integration.
        """
        # Placeholder - actual execution would use the Phase 6 trajectory collector
        # and Phase 7 invariant engine
        trajectory = None
        invariant_results: list[Any] = []

        # The actual implementation would:
        # 1. Initialize agent with scenario task
        # 2. Run agent through Tool Gateway / Environment
        # 3. Collect trajectory via Phase 6 collector
        # 4. Evaluate invariants via Phase 7 engine
        # 5. Return trajectory and results

        # For now, return mock objects
        from types import SimpleNamespace

        trajectory = SimpleNamespace(
            trajectory_id=f"traj-{make_id('traj')}",
            events=[],
        )
        invariant_results = []

        return trajectory, invariant_results

    def _serialize_invariant_results(self, results: list[Any]) -> list[dict[str, Any]]:
        """Serialize invariant results for storage."""
        serialized = []
        for result in results:
            if hasattr(result, "model_dump"):
                serialized.append(result.model_dump())
            elif hasattr(result, "__dict__"):
                serialized.append(
                    {k: v for k, v in result.__dict__.items() if not k.startswith("_")}
                )
            else:
                serialized.append(str(result))
        return serialized
