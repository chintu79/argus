"""Base environment interface for deterministic, controllable execution."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EnvironmentInterface(ABC):
    """Abstract interface for controlled environments.

    All environments must implement this protocol.
    The domain layer depends only on this interface, not on SQLite or concrete implementations.
    """

    @abstractmethod
    def initialize(self, config: dict[str, Any] | None = None) -> None:
        """Reset and initialize the environment to a known state."""
        ...

    @abstractmethod
    def reset(self) -> None:
        """Restore the environment to its initial configured state."""
        ...

    @abstractmethod
    def get_state(self) -> dict[str, Any]:
        """Return the current controlled environment state.

        The returned dict must be safe for JSON serialization.
        It must NOT expose host filesystem data, environment variables, credentials, or secrets.
        """
        ...

    @abstractmethod
    def apply_action(self, action: str, **kwargs) -> tuple[bool, dict[str, Any]]:
        """Apply an action to the environment.

        Returns (success, state_changed) where state_changed indicates
        whether any environment state was modified.
        """
        ...

    @abstractmethod
    def inject_fault(self, fault_type: str, **kwargs) -> None:
        """Inject a deterministic fault into the environment."""
        ...

    @abstractmethod
    def get_resource_state(self) -> dict[str, Any]:
        """Return resource-level accounting (tool calls, reads, writes, etc.)."""
        ...

    @abstractmethod
    def get_service_state(self) -> dict[str, Any]:
        """Return service availability state."""
        ...
