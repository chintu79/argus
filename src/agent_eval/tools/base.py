"""Base types and protocols for tool definitions and registry.

Framework-independent, Pydantic/v2-compatible, suitable for JSON serialization.
"""

from __future__ import annotations

import builtins
from abc import ABC, abstractmethod
from typing import Any

from agent_eval.domain.common import DomainMetadata


class ToolDefinitionBase(ABC):
    """Base protocol for tool definitions.

    Every tool must define these characteristics explicitly.
    """

    @property
    @abstractmethod
    def tool_name(self) -> str:
        """Unique tool identifier name."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the tool's purpose."""

    @property
    @abstractmethod
    def required_capabilities(self) -> list[str]:
        """Capabilities required for this tool to execute."""

    @property
    @abstractmethod
    def accepted_arguments(self) -> dict[str, Any]:
        """Expected argument schema for tool invocation."""

    @property
    @abstractmethod
    def output_schema(self) -> type:
        """Expected Python type for tool output."""

    @property
    @abstractmethod
    def side_effects(self) -> list[str]:
        """Classified side effects: READ, WRITE, EXTERNAL_EFFECT, RESOURCE_CONSUMING."""

    @property
    @abstractmethod
    def enabled(self) -> bool:
        """Whether the tool is currently enabled for execution."""

    @property
    @abstractmethod
    def version(self) -> str:
        """Tool definition version string."""

    @property
    @abstractmethod
    def metadata(self) -> DomainMetadata:
        """JSON-serializable metadata bag."""


class ToolRegistryProtocol(ABC):
    """Protocol for tool registry operations."""

    @abstractmethod
    def register(self, definition: ToolDefinitionBase) -> None:
        """Register a tool definition."""

    @abstractmethod
    def get(self, tool_name: str) -> ToolDefinitionBase | None:
        """Get a tool definition by name."""

    @abstractmethod
    def list(self) -> builtins.list[ToolDefinitionBase]:
        """List all registered tool definitions."""

    @abstractmethod
    def exists(self, tool_name: str) -> bool:
        """Check if a tool is registered."""

    @abstractmethod
    def disable(self, tool_name: str) -> None:
        """Disable a tool (mark as not enabled)."""

    @abstractmethod
    def enable(self, tool_name: str) -> None:
        """Enable a tool."""
