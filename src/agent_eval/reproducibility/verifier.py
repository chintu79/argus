"""Reproducibility verifier - orchestrates multi-seed verification runs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar

from agent_eval.domain.identifiers import make_id
from agent_eval.reproducibility.models import (
    ReproducibilityRequest,
    ReproducibilityResult,
    ReproducibilityStatus,
    VerificationRun,
    VerificationRunStatus,
)
from agent_eval.reproducibility.signature import (
    SignatureExtractor,
)


class ReproducibilityVerifier:
    """Orchestrates the complete reproducibility verification process."""

    def __init__(self, runner: Any, policy: Any = None):
        self._runner = runner
        self._policy = policy or ReproducibilityPolicy()

    def verify(
        self,
        request: ReproducibilityRequest,
        failure_candidate: Any,
        scenario: Any,
        agent: Any,
        environment: Any,
    ) -> ReproducibilityResult:
        """Execute a complete reproducibility verification.

        Flow:
        1. Extract target failure signature from original candidate
        2. For each seed, execute verification run
        3. Collect signatures from each run
        4. Compare against target signature
        5. Calculate Rep_k and evaluate threshold
        """
        # Create verification record
        verification_id = make_id("verify")
        result = ReproducibilityResult(
            failure_id=request.failure_id,
            verification_id=verification_id,
            k=request.k,
            threshold=request.threshold,
            status=ReproducibilityStatus.RUNNING,
            verifier_version="1.0",
        )

        # Step 1: Extract target signature
        target_signature = SignatureExtractor.extract_from_failure_candidate(
            failure_candidate,
            None,  # trajectory would be loaded from storage
        )

        # Step 2: Execute verification runs
        runs = []
        successful = 0

        for seed in request.verification_seeds:
            run = VerificationRun(
                run_id=make_id("run"),
                verification_id=verification_id,
                seed=seed,
                status=VerificationRunStatus.RUNNING,
                started_at=datetime.now(UTC),
            )

            try:
                # Execute verification run
                run_result = self._runner.execute_verification_run(
                    run=run,
                    request=request,
                    scenario=scenario,
                    agent=agent,
                    environment=environment,
                    target_signature=target_signature,
                )

                runs.append(run_result)

                if run_result.target_matched == "MATCH":
                    successful += 1

            except Exception as e:
                run.status = VerificationRunStatus.FAILED
                run.error = str(e)
                run.completed_at = datetime.now(UTC)
                runs.append(run)

        # Step 3: Calculate Rep_k
        rep_k = successful / request.k if request.k > 0 else 0.0

        # Step 4: Evaluate threshold
        if rep_k >= request.threshold:
            status = ReproducibilityStatus.REPRODUCIBLE
        elif successful > 0:
            status = ReproducibilityStatus.PARTIAL
        else:
            status = ReproducibilityStatus.NOT_REPRODUCIBLE

        # Finalize result
        result.successful_replications = successful
        result.rep_k = rep_k
        result.status = status
        result.runs = runs
        result.completed_at = datetime.now(UTC)

        return result


class ReproducibilityPolicy:
    """Default policy for reproducibility verification."""

    default_k = 3
    default_seeds: ClassVar[list[int]] = [101, 202, 303]
    default_threshold = 0.75
    default_temperature = 0.7
    early_stopping = False
    max_run_time_seconds = 300
