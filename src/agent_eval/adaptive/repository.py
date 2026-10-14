"""Repository for adaptive evaluation persistence."""

from __future__ import annotations

from typing import Any

from agent_eval.adaptive.models import (
    AdaptiveEvaluationState,
    TestCandidate,
)
from agent_eval.domain.identifiers import is_valid


class AdaptiveRepository:
    """Repository for persisting adaptive evaluation data."""

    def __init__(self):
        # In-memory stores (would be replaced with database in production)
        self._candidates: dict[str, TestCandidate] = {}
        self._states: dict[str, AdaptiveEvaluationState] = {}
        self._decisions: dict[str, Any] = {}
        self._iterations: dict[int, Any] = {}

        # Indexes
        self._candidates_by_iteration: dict[int, list[str]] = {}
        self._decisions_by_iteration: dict[int, list[str]] = {}
        self._candidates_by_tool: dict[str, list[str]] = {}
        self._candidates_by_source: dict[str, list[str]] = {}

    # ── Candidates ──────────────────────────────────────────────

    def save_candidate(self, candidate: TestCandidate) -> str:
        """Save a test candidate."""
        # Validate
        if not candidate.candidate_id or not is_valid(candidate.candidate_id):
            raise ValueError("Candidate must have a valid candidate_id")

        if candidate.estimated_cost <= 0:
            raise ValueError("Candidate must have positive estimated cost")

        self._candidates[candidate.candidate_id] = candidate

        # Update indexes
        iteration = candidate.generation_iteration
        if iteration not in self._candidates_by_iteration:
            self._candidates_by_iteration[iteration] = []
        if candidate.candidate_id not in self._candidates_by_iteration[iteration]:
            self._candidates_by_iteration[iteration].append(candidate.candidate_id)

        if candidate.target_tool:
            if candidate.target_tool not in self._candidates_by_tool:
                self._candidates_by_tool[candidate.target_tool] = []
            if (
                candidate.candidate_id
                not in self._candidates_by_tool[candidate.target_tool]
            ):
                self._candidates_by_tool[candidate.target_tool].append(
                    candidate.candidate_id
                )

        source = (
            candidate.source.value
            if hasattr(candidate.source, "value")
            else str(candidate.source)
        )
        if source not in self._candidates_by_source:
            self._candidates_by_source[source] = []
        if candidate.candidate_id not in self._candidates_by_source[source]:
            self._candidates_by_source[source].append(candidate.candidate_id)

        return candidate.candidate_id

    def get_candidate(self, candidate_id: str) -> TestCandidate | None:
        """Get a candidate by ID."""
        return self._candidates.get(candidate_id)

    def get_candidates_by_iteration(self, iteration: int) -> list[TestCandidate]:
        """Get all candidates from an iteration."""
        ids = self._candidates_by_iteration.get(iteration, [])
        return [self._candidates[id] for id in ids if id in self._candidates]

    def get_candidates_by_tool(self, tool: str) -> list[TestCandidate]:
        """Get all candidates for a specific tool."""
        ids = self._candidates_by_tool.get(tool, [])
        return [self._candidates[id] for id in ids if id in self._candidates]

    def get_candidates_by_source(self, source: str) -> list[TestCandidate]:
        """Get all candidates from a source."""
        ids = self._candidates_by_source.get(source, [])
        return [self._candidates[id] for id in ids if id in self._candidates]

    def list_candidates(self) -> list[TestCandidate]:
        """List all candidates."""
        return list(self._candidates.values())

    def get_candidates_by_iteration_range(
        self,
        start: int,
        end: int,
    ) -> list[TestCandidate]:
        """Get candidates from a range of iterations."""
        results = []
        for i in range(start, end + 1):
            results.extend(self.get_candidates_by_iteration(i))
        return results

    # ── States ─────────────────────────────────────────────────

    def save_state(self, state: Any, state_id: str) -> str:
        """Save an evaluation state."""
        self._states[state_id] = state
        return state_id

    def get_state(self, state_id: str) -> Any | None:
        """Get an evaluation state by ID."""
        return self._states.get(state_id)

    def list_states(self) -> list[Any]:
        """List all states."""
        return list(self._states.values())

    def delete_state(self, state_id: str) -> bool:
        """Delete a state."""
        if state_id in self._states:
            del self._states[state_id]
            return True
        return False

    # ── Decisions ──────────────────────────────────────────────

    def save_decision(self, decision: Any) -> str:
        """Save an adaptive decision."""
        if not decision.decision_id:
            from agent_eval.domain.identifiers import make_id

            decision.decision_id = make_id("dec")

        self._decisions[decision.decision_id] = decision

        # Update iteration index
        iteration = decision.iteration
        if iteration not in self._decisions_by_iteration:
            self._decisions_by_iteration[iteration] = []
        if decision.decision_id not in self._decisions_by_iteration[iteration]:
            self._decisions_by_iteration[iteration].append(decision.decision_id)

        return decision.decision_id

    def get_decision(self, decision_id: str) -> Any | None:
        """Get a decision by ID."""
        return self._decisions.get(decision_id)

    def get_decisions_by_iteration(self, iteration: int) -> list[Any]:
        """Get all decisions for an iteration."""
        ids = self._decisions_by_iteration.get(iteration, [])
        return [self._decisions[id] for id in ids if id in self._decisions]

    def list_decisions(self) -> list[Any]:
        """List all decisions."""
        return list(self._decisions.values())

    # ── Iterations ─────────────────────────────────────────────

    def save_iteration(self, iteration: Any) -> str:
        """Save an iteration record."""
        self._iterations[iteration.iteration] = iteration
        return str(iteration.iteration)

    def get_iteration(self, iteration_num: int) -> Any | None:
        """Get an iteration by number."""
        return self._iterations.get(iteration_num)

    def list_iterations(self) -> list[Any]:
        """List all iterations."""
        return sorted(self._iterations.values(), key=lambda x: x.iteration)

    def get_latest_iteration(self) -> Any | None:
        """Get the most recent iteration."""
        if not self._iterations:
            return None
        return max(self._iterations.values(), key=lambda x: x.iteration)

    # ── Queries ────────────────────────────────────────────────

    def get_candidates_pending_execution(
        self,
        evaluation_state: Any,
    ) -> list[TestCandidate]:
        """Get candidates that haven't been executed yet."""
        executed = set(evaluation_state.executed_candidates)
        return [c for c in self._candidates.values() if c.candidate_id not in executed]

    def get_candidates_over_budget(
        self,
        budget_remaining: int,
    ) -> list[TestCandidate]:
        """Get candidates that exceed the remaining budget."""
        return [
            c for c in self._candidates.values() if c.estimated_cost > budget_remaining
        ]

    def get_candidate_statistics(self) -> dict[str, Any]:
        """Get statistics about candidates."""
        total = len(self._candidates)
        if total == 0:
            return {
                "total": 0,
                "by_source": {},
                "by_tool": {},
                "by_iteration": {},
                "avg_cost": 0.0,
            }

        by_source: dict[str, int] = {}
        by_tool: dict[str, int] = {}
        by_iteration: dict[int, int] = {}
        total_cost = 0

        for c in self._candidates.values():
            # By source
            source = c.source.value if hasattr(c.source, "value") else str(c.source)
            by_source[source] = by_source.get(source, 0) + 1

            # By tool
            if c.target_tool:
                by_tool[c.target_tool] = by_tool.get(c.target_tool, 0) + 1

            # By iteration
            by_iteration[c.generation_iteration] = (
                by_iteration.get(c.generation_iteration, 0) + 1
            )

            total_cost += c.estimated_cost

        return {
            "total": len(self._candidates),
            "by_source": by_source,
            "by_tool": by_tool,
            "by_iteration": by_iteration,
            "avg_cost": total_cost / total if total > 0 else 0.0,
        }


# Global repository instance
_adaptive_repository: AdaptiveRepository | None = None


def get_adaptive_repository() -> AdaptiveRepository:
    """Get the global adaptive repository (singleton)."""
    global _adaptive_repository
    if _adaptive_repository is None:
        _adaptive_repository = AdaptiveRepository()
    return _adaptive_repository
