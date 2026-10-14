"""Agent adapter interface/protocol for AI agent integration.

The interface is designed so that a future real LLM adapter can implement the
same contract. The mock agent implements this interface so the evaluator is
testable without external APIs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from agent_eval.domain.enums import (
    AgentBehavior,
)
from agent_eval.domain.identifiers import (
    AgentId,
)
from agent_eval.environments.support import SupportEnvironment


class AgentAdapter(ABC):
    """Abstract interface for AI agent adapters.

    Both the deterministic mock agent and future real LLM adapters must implement
    this contract. This permits the evaluator to remain testable without external
    APIs.
    """

    @abstractmethod
    def initialize(
        self,
        task: dict[str, Any],
        environment: SupportEnvironment,
        agent_id: AgentId,
        **kwargs: Any,
    ) -> None:
        """Initialize the agent with a task and environment.

        Args:
            task: Structured task description.
            environment: The controlled environment instance.
            agent_id: Unique agent identifier.
            **kwargs: Additional agent-specific configuration.
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the agent to its initial state.

        Clears action counters, retry counters, lifecycle state, observations,
        and internal execution state. Does NOT mutate the environment.
        """
        ...

    @abstractmethod
    def act(
        self,
        available_tools: list[str] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Select and return the next action.

        Returns:
            (action, observation) tuple where:
                action: Dict with action_type, tool_name, arguments, step_number, metadata
                observation: Dict with observation_type, tool_name, success, result,
                          error_code, policy_decision, state_changed, metadata

        The agent must interact only through the Tool Gateway (environment.execute_tool).
        """
        ...

    @abstractmethod
    def observe(
        self,
        observation: dict[str, Any],
    ) -> None:
        """Process the environment's response to the last action.

        The observation contains only information actually exposed to the agent:
            - tool_name
            - success/failure
            - result or error_code
            - policy decision
            - state changes
        The agent must NOT store private reasoning, chain-of-thought, or evaluator-only data.
        """
        ...

    @abstractmethod
    def terminate(self) -> dict[str, Any]:
        """Terminate the agent and return an execution result.

        Returns:
            Dict with status, actions, observations, termination_reason, steps, metadata.

        The termination_reason should be one of:
            TASK_COMPLETED, POLICY_DENIED, RESOURCE_EXHAUSTED, MAX_STEPS, RECOVERY_EXHAUSTED, ERROR
        """
        ...

    @property
    @abstractmethod
    def lifecycle_state(self) -> str:
        """Return the current agent lifecycle state."""
        ...

    @property
    @abstractmethod
    def step_count(self) -> int:
        """Return the number of steps taken in the current execution."""
        ...

    @property
    @abstractmethod
    def behavior_mode(self) -> AgentBehavior:
        """Return the agent's current behavior mode."""
        ...
