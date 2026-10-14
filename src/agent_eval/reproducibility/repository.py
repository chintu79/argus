"""Repository for reproducibility verification results."""

from __future__ import annotations

from agent_eval.reproducibility.models import (
    ReproducibilityRequest,
    ReproducibilityResult,
    VerificationRun,
)


class ReproducibilityRepository:
    """Repository for storing and retrieving reproducibility verification results."""

    def __init__(self):
        # In-memory stores (would be replaced with database in production)
        self._requests: dict[str, ReproducibilityRequest] = {}
        self._results: dict[str, ReproducibilityResult] = {}
        self._runs: dict[str, VerificationRun] = {}

        # Indexes
        self._results_by_failure: dict[str, list[str]] = {}
        self._runs_by_verification: dict[str, list[str]] = {}

    # ── Requests ──────────────────────────────────────────────

    def save_request(self, request: ReproducibilityRequest) -> str:
        """Save a reproducibility request."""
        # Generate verification_id if not present
        if not request.verification_id:
            from agent_eval.domain.identifiers import make_id

            request.verification_id = make_id("verify")
        self._requests[request.verification_id] = request
        return request.verification_id

    def get_request(self, verification_id: str) -> ReproducibilityRequest | None:
        """Get a request by verification ID."""
        return self._requests.get(verification_id)

    # ── Results ───────────────────────────────────────────────

    def save_result(self, result: ReproducibilityResult) -> str:
        """Save a reproducibility result."""
        self._results[result.verification_id] = result

        # Update failure index
        if result.failure_id not in self._results_by_failure:
            self._results_by_failure[result.failure_id] = []
        if result.verification_id not in self._results_by_failure[result.failure_id]:
            self._results_by_failure[result.failure_id].append(result.verification_id)

        return result.verification_id

    def get_result(self, verification_id: str) -> ReproducibilityResult | None:
        """Get a result by verification ID."""
        return self._results.get(verification_id)

    def get_results_by_failure(self, failure_id: str) -> list[ReproducibilityResult]:
        """Get all verification results for a failure candidate."""
        verification_ids = self._results_by_failure.get(failure_id, [])
        return [self._results[vid] for vid in verification_ids if vid in self._results]

    # ── Runs ──────────────────────────────────────────────────

    def save_run(self, run: VerificationRun) -> str:
        """Save a verification run."""
        self._runs[run.run_id] = run

        # Update verification index
        if run.verification_id not in self._runs_by_verification:
            self._runs_by_verification[run.verification_id] = []
        if run.run_id not in self._runs_by_verification[run.verification_id]:
            self._runs_by_verification[run.verification_id].append(run.run_id)

        return run.run_id

    def get_run(self, run_id: str) -> VerificationRun | None:
        """Get a run by ID."""
        return self._runs.get(run_id)

    def get_runs_by_verification(self, verification_id: str) -> list[VerificationRun]:
        """Get all runs for a verification."""
        run_ids = self._runs_by_verification.get(verification_id, [])
        return [self._runs[rid] for rid in run_ids if rid in self._runs]
