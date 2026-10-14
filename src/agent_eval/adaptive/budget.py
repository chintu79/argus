"""Budget management for adaptive evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from agent_eval.adaptive.models import AdaptiveBudget


class BudgetManager:
    """Manages budget for adaptive evaluation."""

    def __init__(self, total_budget: int = 100000):
        self.budget = AdaptiveBudget(total_tokens=total_budget)
        self._ledger: list[dict[str, Any]] = []

    @property
    def remaining(self) -> int:
        return self.budget.remaining_tokens

    @property
    def consumed(self) -> int:
        return self.budget.consumed_tokens

    @property
    def total(self) -> int:
        return self.budget.total_tokens

    @property
    def utilization(self) -> float:
        return self.budget.utilization()

    def can_afford(self, cost: int) -> bool:
        """Check if budget can afford a cost."""
        return self.budget.can_afford(cost)

    def reserve(self, cost: int) -> bool:
        """Reserve tokens for an execution."""
        return self.budget.reserve(cost)

    def commit(self, actual_cost: int) -> bool:
        """Commit actual cost after execution."""
        result = self.budget.commit(actual_cost)
        if result:
            self._ledger.append(
                {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "type": "commit",
                    "cost": actual_cost,
                    "remaining": self.budget.remaining_tokens,
                }
            )
        return result

    def release(self, cost: int) -> bool:
        """Release reserved tokens (e.g., on cancellation)."""
        result = self.budget.release(cost)
        if result:
            self._ledger.append(
                {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "type": "release",
                    "cost": cost,
                    "remaining": self.budget.remaining_tokens,
                }
            )
        return result

    def get_ledger(self) -> list[dict[str, Any]]:
        """Get the budget ledger."""
        return list(self._ledger)

    def get_status(self) -> dict[str, Any]:
        """Get current budget status."""
        return {
            "total": self.budget.total_tokens,
            "consumed": self.budget.consumed_tokens,
            "reserved": self.budget.reserved_tokens,
            "remaining": self.budget.remaining_tokens,
            "utilization": self.budget.utilization(),
        }

    def can_continue(self, min_budget: int = 10) -> bool:
        """Check if evaluation can continue."""
        return self.budget.remaining_tokens >= 10

    def reserve_for_verification(self, base_cost: int, multiplier: float = 2.0) -> bool:
        """Reserve budget for reproduction/verification."""
        verification_cost = int(base_cost * 2.0)
        return self.reserve(verification_cost)

    def get_remaining_ratio(self) -> float:
        """Get ratio of remaining budget."""
        if self.budget.total_tokens == 0:
            return 0.0
        return self.budget.remaining_tokens / self.budget.total_tokens


class BudgetLedger:
    """Structured budget ledger for persistence."""

    def __init__(self):
        self._entries: list[dict[str, Any]] = []

    def add_entry(
        self,
        entry_type: str,
        cost: int,
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ):
        """Add a ledger entry."""
        from agent_eval.domain.identifiers import make_id

        entry = {
            "entry_id": make_id("ledger"),
            "timestamp": datetime.now(UTC).isoformat(),
            "type": entry_type,
            "cost": cost,
            "description": description,
            "metadata": metadata or {},
        }
        self._entries.append(entry)

    def get_entries(self) -> list[dict[str, Any]]:
        return list(self._entries)

    def get_total_consumed(self) -> int:
        return sum(
            e["cost"] for e in self._entries if e["type"] in ("commit", "execution")
        )

    def get_by_type(self, entry_type: str) -> list[dict[str, Any]]:
        return [e for e in self._entries if e["type"] == entry_type]

    def export_jsonl(self) -> str:
        import json

        return "\n".join(json.dumps(e, default=str) for e in self._entries)
