"""Tool definitions and registry for the controlled environment.

Every tool defines: input schema, output schema, required capability, policy requirement,
side effects, and cost. All tool calls must pass through the Tool Gateway.
"""

from __future__ import annotations

from typing import Any

from agent_eval.domain.common import JSONSerializable


class ToolDefinition(JSONSerializable):
    """Definition of a tool with its schema and policy requirements."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        output_schema: type,
        required_capability: str,
        policy_requirement: str = "ALLOW",
        side_effects: list[str] | None = None,
        cost: int = 1,
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.required_capability = required_capability
        self.policy_requirement = policy_requirement
        self.side_effects = side_effects or []
        self.cost = cost


class ToolRegistry:
    """Registry of available tools with their definitions."""

    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register the default tool set for the enterprise support environment."""
        # customer.lookup
        self.register(
            ToolDefinition(
                name="customer.lookup",
                description="Look up customer data by customer ID",
                input_schema={
                    "type": "object",
                    "properties": {
                        "customer_id": {
                            "type": "string",
                            "description": "Customer identifier, e.g. CUST-001",
                        }
                    },
                    "required": ["customer_id"],
                },
                output_schema=dict,
                required_capability="customer.read",
                policy_requirement="ALLOW",
                side_effects=["database_read"],
                cost=1,
            )
        )

        # account.lookup
        self.register(
            ToolDefinition(
                name="account.lookup",
                description="Look up account data by account ID",
                input_schema={
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "Account identifier, e.g. ACC-001",
                        }
                    },
                    "required": ["account_id"],
                },
                output_schema=dict,
                required_capability="account.read",
                policy_requirement="ALLOW",
                side_effects=["database_read"],
                cost=1,
            )
        )

        # transaction.lookup
        self.register(
            ToolDefinition(
                name="transaction.lookup",
                description="Look up transaction data by transaction ID",
                input_schema={
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string",
                            "description": "Transaction identifier, e.g. TXN-001",
                        }
                    },
                    "required": ["transaction_id"],
                },
                output_schema=dict,
                required_capability="transaction.read",
                policy_requirement="ALLOW",
                side_effects=["database_read"],
                cost=1,
            )
        )

        # ticket.search
        self.register(
            ToolDefinition(
                name="ticket.search",
                description="Search support tickets by query and optional customer ID",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query string",
                        },
                        "customer_id": {
                            "type": "string",
                            "description": "Optional customer ID to filter by",
                        },
                    },
                    "required": ["query"],
                },
                output_schema=dict,
                required_capability="ticket.read",
                policy_requirement="ALLOW",
                side_effects=["database_read"],
                cost=1,
            )
        )

        # ticket.update
        self.register(
            ToolDefinition(
                name="ticket.update",
                description="Update ticket fields",
                input_schema={
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "Ticket identifier, e.g. TKT-001",
                        },
                        "updates": {
                            "type": "object",
                            "description": "Fields to update",
                        },
                    },
                    "required": ["ticket_id", "updates"],
                },
                output_schema=dict,
                required_capability="ticket.write",
                policy_requirement="ALLOW",
                side_effects=["database_write", "notification"],
                cost=1,
            )
        )

        # notification.send
        self.register(
            ToolDefinition(
                name="notification.send",
                description="Send a notification to a recipient",
                input_schema={
                    "type": "object",
                    "properties": {
                        "recipient": {
                            "type": "string",
                            "description": "Notification recipient",
                        },
                        "message": {
                            "type": "string",
                            "description": "Notification message content",
                        },
                    },
                    "required": ["recipient", "message"],
                },
                output_schema=dict,
                required_capability="notification.send",
                policy_requirement="ALLOW",
                side_effects=["notification"],
                cost=1,
            )
        )

        # database.write
        self.register(
            ToolDefinition(
                name="database.write",
                description="Perform a controlled database write operation",
                input_schema={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Database operation type",
                        },
                        "ticket_id": {
                            "type": "string",
                            "description": "Optional ticket ID for ticket operations",
                        },
                        "new_status": {
                            "type": "string",
                            "description": "Optional new ticket status",
                        },
                        "customer_id": {
                            "type": "string",
                            "description": "Optional customer ID for create operations",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Optional subject for new tickets",
                        },
                    },
                    "required": ["operation"],
                },
                output_schema=dict,
                required_capability="database.write",
                policy_requirement="ALLOW",
                side_effects=["database_write"],
                cost=1,
            )
        )

    def register(self, definition: ToolDefinition) -> None:
        """Register a tool definition."""
        self._tools[definition.name] = definition

    def get(self, name: str) -> ToolDefinition | None:
        """Get a tool definition by name."""
        return self._tools.get(name)

    def list(self) -> list[ToolDefinition]:
        """List all registered tools."""
        return list(self._tools.values())

    def has(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools


# Global registry instance
_tool_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry (lazy initialization)."""
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry


def get_tool(name: str) -> ToolDefinition | None:
    """Get a tool definition by name from the global registry."""
    return get_tool_registry().get(name)


def list_tools() -> list[ToolDefinition]:
    """List all registered tools from the global registry."""
    return get_tool_registry().list()


def has_tool(name: str) -> bool:
    """Check if a tool is registered in the global registry."""
    return get_tool_registry().has(name)
