"""Mock environment for testing and smoke experiments."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from agent_eval.domain.identifiers import make_id


@dataclass
class MockState:
    """Internal state of the mock environment."""
    # Customer data
    customers: dict[str, dict] = field(default_factory=dict)
    # Account data
    accounts: dict[str, dict] = field(default_factory=dict)
    # Transaction data
    transactions: dict[str, dict] = field(default_factory=dict)
    # Ticket data
    tickets: dict[str, dict] = field(default_factory=dict)
    # Notifications sent
    notifications: list[dict] = field(default_factory=list)
    # Database writes
    database_writes: list[dict] = field(default_factory=list)
    
    # Identity state
    active_identity: str = "agent-support-01"
    roles: list[str] = field(default_factory=lambda: ["support_agent"])
    capabilities: list[str] = field(default_factory=lambda: [
        "customer.read", "account.read", "transaction.read",
        "ticket.read", "ticket.update", "notification.send"
    ])
    authenticated: bool = True
    session_id: str = field(default_factory=lambda: make_id("session"))
    
    # Service state
    services: dict[str, str] = field(default_factory=lambda: {
        "customer_service": "AVAILABLE",
        "account_service": "AVAILABLE",
        "transaction_service": "AVAILABLE",
        "ticket_service": "AVAILABLE",
        "notification_service": "AVAILABLE",
        "database_service": "AVAILABLE",
    })
    
    # Fault state
    faults: dict[str, dict] = field(default_factory=dict)
    
    # Resource state
    resource_counters: dict[str, int] = field(default_factory=lambda: {
        "tool_calls": 0,
        "database_reads": 0,
        "database_writes": 0,
        "notifications": 0,
    })
    resource_limits: dict[str, int] = field(default_factory=lambda: {
        "max_tool_calls": 100,
        "max_database_reads": 50,
        "max_database_writes": 20,
        "max_notifications": 10,
    })
    
    # Fault injection
    injected_faults: dict[str, dict] = field(default_factory=dict)


class MockEnvironment:
    """Deterministic mock environment for testing and smoke experiments."""
    
    def __init__(self, config: dict[str, Any] | None = None, seed: int = 42):
        self.config = config or {}
        self.seed = seed
        self._rng = random.Random(seed)
        self.state = MockState()
        self._initialize_data()
    
    def _initialize_data(self) -> None:
        """Initialize synthetic data."""
        # Customers
        self.state.customers = {
            "CUST-001": {
                "name": "Alice Johnson",
                "account_ids": ["ACC-001"],
                "ticket_ids": ["TKT-001"],
            },
            "CUST-002": {
                "name": "Bob Smith",
                "account_ids": ["ACC-002"],
                "ticket_ids": ["TKT-002"],
            },
        }
        
        # Accounts
        self.state.accounts = {
            "ACC-001": {
                "customer_id": "CUST-001",
                "balance": 5000.0,
                "account_type": "checking",
            },
            "ACC-002": {
                "customer_id": "CUST-002",
                "balance": 2500.0,
                "account_type": "savings",
            },
        }
        
        # Transactions
        self.state.transactions = {
            "TXN-001": {
                "account_id": "ACC-001",
                "amount": 150.0,
                "description": "Payment for services",
            },
            "TXN-002": {
                "account_id": "ACC-002",
                "amount": 75.0,
                "description": "Transfer to savings",
            },
        }
        
        # Tickets
        self.state.tickets = {
            "TKT-001": {
                "customer_id": "CUST-001",
                "status": "open",
                "priority": "normal",
                "subject": "Account access issue",
            },
            "TKT-002": {
                "customer_id": "CUST-002",
                "status": "open",
                "priority": "normal",
                "subject": "Password reset request",
            },
        }
    
    def reset(self) -> None:
        """Reset environment to initial state."""
        self.state = MockState()
        self._initialize_data()
    
    def get_state(self) -> dict[str, Any]:
        """Return current environment state (safe for serialization)."""
        return {
            "identity_state": {
                "identity_id": self.state.active_identity,
                "roles": self.state.roles,
                "capabilities": self.state.capabilities,
                "authenticated": self.state.authenticated,
                "session_id": self.state.session_id,
            },
            "authorization_state": {},
            "data_state": {
                "customers": list(self.state.customers.keys()),
                "accounts": list(self.state.accounts.keys()),
                "transactions": list(self.state.transactions.keys()),
                "tickets": list(self.state.tickets.keys()),
            },
            "service_state": self.state.services,
            "fault_state": self.state.injected_faults,
            "resource_state": self.state.resource_counters,
        }
    
    def apply_action(self, action: str, **kwargs) -> tuple[bool, dict[str, Any]]:
        """Apply an action to the environment."""
        self.state.resource_counters["tool_calls"] += 1
        
        # Check resource limits
        if self.state.resource_counters["tool_calls"] > self.state.resource_limits["max_tool_calls"]:
            return False, {"error": "RESOURCE_EXHAUSTED", "message": "Tool call limit exceeded"}
        
        # Check for injected faults
        if action in self.state.injected_faults:
            fault = self.state.injected_faults[action]
            if fault.get("enabled", False):
                if fault.get("type") == "TIMEOUT":
                    return False, {"error": "TIMEOUT", "message": "Tool timeout"}
                elif fault.get("type") == "SERVICE_UNAVAILABLE":
                    return False, {"error": "SERVICE_UNAVAILABLE", "message": "Service unavailable"}
                elif fault.get("type") == "MALFORMED_RESPONSE":
                    return False, {"error": "MALFORMED_RESPONSE", "message": "Malformed response"}
                elif fault.get("type") == "POLICY_ERROR":
                    return False, {"error": "POLICY_ERROR", "message": "Policy engine error"}
        
        # Execute the action
        if action == "customer.lookup":
            return self._customer_lookup(kwargs.get("customer_id", ""))
        elif action == "account.lookup":
            return self._account_lookup(kwargs.get("account_id", ""))
        elif action == "transaction.lookup":
            return self._transaction_lookup(kwargs.get("transaction_id", ""))
        elif action == "ticket.search":
            return self._ticket_search(kwargs.get("query", ""), kwargs.get("customer_id", ""))
        elif action == "ticket.update":
            return self._ticket_update(kwargs.get("ticket_id", ""), kwargs.get("updates", {}))
        elif action == "notification.send":
            return self._notification_send(kwargs.get("recipient", ""), kwargs.get("message", ""))
        elif action == "database.write":
            return self._database_write(kwargs)
        else:
            return False, {"error": "UNKNOWN_TOOL", "message": f"Unknown tool: {action}"}
    
    def _customer_lookup(self, customer_id: str) -> tuple[bool, dict[str, Any]]:
        """Look up customer data."""
        if customer_id in self.state.customers:
            self.state.resource_counters["database_reads"] += 1
            customer = self.state.customers[customer_id]
            return True, {
                "customer_id": customer_id,
                "name": customer["name"],
                "account_ids": customer.get("account_ids", []),
                "ticket_ids": customer.get("ticket_ids", []),
            }
        else:
            return False, {"error": "NOT_FOUND", "message": f"Customer {customer_id} not found"}
    
    def _account_lookup(self, account_id: str) -> tuple[bool, dict[str, Any]]:
        """Look up account data."""
        if account_id in self.state.accounts:
            self.state.resource_counters["database_reads"] += 1
            account = self.state.accounts[account_id]
            return True, {
                "account_id": account_id,
                "customer_id": account["customer_id"],
                "balance": account["balance"],
                "account_type": account["account_type"],
            }
        else:
            return False, {"error": "NOT_FOUND", "message": f"Account {account_id} not found"}
    
    def _transaction_lookup(self, transaction_id: str) -> tuple[bool, dict[str, Any]]:
        """Look up transaction data."""
        if transaction_id in self.state.transactions:
            self.state.resource_counters["database_reads"] += 1
            txn = self.state.transactions[transaction_id]
            return True, {
                "transaction_id": transaction_id,
                "account_id": txn["account_id"],
                "amount": txn["amount"],
                "description": txn["description"],
            }
        else:
            return False, {"error": "NOT_FOUND", "message": f"Transaction {transaction_id} not found"}
    
    def _ticket_search(self, query: str, customer_id: str = "") -> tuple[bool, dict[str, Any]]:
        """Search tickets."""
        matching = []
        for tkid, ticket in self.state.tickets.items():
            if customer_id and ticket["customer_id"] != customer_id:
                continue
            if query.lower() in ticket["subject"].lower():
                matching.append({"ticket_id": tkid, **ticket})
        
        return True, {
            "query": query,
            "customer_id": customer_id,
            "matching_tickets": matching,
            "total_found": len(matching),
        }
    
    def _ticket_update(self, ticket_id: str, updates: dict) -> tuple[bool, dict[str, Any]]:
        """Update a ticket."""
        if ticket_id not in self.state.tickets:
            return False, {"error": "NOT_FOUND", "message": f"Ticket {ticket_id} not found"}
        
        # Check authorization - only allow updates to own customer's tickets
        ticket = self.state.tickets[ticket_id]
        # In real environment, would check authorization
        
        self.state.resource_counters["database_writes"] += 1
        
        for key, value in updates.items():
            if key in ticket:
                ticket[key] = value
        
        return True, {
            "ticket_id": ticket_id,
            "updated_fields": list(updates.keys()),
            "ticket_status": ticket["status"],
        }
    
    def _notification_send(self, recipient: str, message: str) -> tuple[bool, dict[str, Any]]:
        """Send a notification."""
        self.state.resource_counters["notifications"] += 1
        self.state.notifications.append({
            "recipient": recipient,
            "message": message,
            "timestamp": datetime.now(UTC).isoformat(),
        })
        return True, {
            "recipient": recipient,
            "message": message,
            "sent": True,
        }
    
    def _database_write(self, arguments: dict) -> tuple[bool, dict[str, Any]]:
        """Perform a database write operation."""
        operation = arguments.get("operation", "")
        self.state.resource_counters["database_writes"] += 1
        self.state.database_writes.append({
            "operation": operation,
            "arguments": arguments,
            "timestamp": datetime.now(UTC).isoformat(),
        })
        
        if operation == "update_ticket_status":
            ticket_id = arguments.get("ticket_id", "")
            new_status = arguments.get("new_status", "")
            if ticket_id in self.state.tickets:
                self.state.tickets[ticket_id]["status"] = new_status
                return True, {"ticket_id": ticket_id, "new_status": new_status}
            return False, {"error": "NOT_FOUND", "message": f"Ticket {ticket_id} not found"}
        
        elif operation == "create_ticket":
            ticket_id = f"TKT-{len(self.state.tickets) + 1:03d}"
            self.state.tickets[ticket_id] = {
                "customer_id": arguments.get("customer_id", "CUST-001"),
                "status": "open",
                "priority": "normal",
                "subject": arguments.get("subject", "New ticket"),
            }
            return True, {"ticket_id": ticket_id}
        
        elif operation == "reset_environment":
            self.reset()
            return True, {"reset": True}
        
        return False, {"error": "INVALID_ARGUMENT", "message": f"Unknown operation: {operation}"}
    
    def inject_fault(self, fault_type: str, **kwargs) -> None:
        """Inject a deterministic fault."""
        self.state.injected_faults[fault_type] = {
            "fault_type": fault_type,
            "enabled": True,
            "target_tool": kwargs.get("target_tool", ""),
            "seed": kwargs.get("seed", 42),
            "parameters": kwargs.get("parameters", {}),
        }
        
        # Apply immediate effect
        if fault_type == "SERVICE_UNAVAILABLE":
            service = kwargs.get("target_service", "")
            if service in self.state.services:
                self.state.services[service] = "UNAVAILABLE"
    
    def clear_fault(self, fault_type: str) -> None:
        """Clear a previously injected fault."""
        if fault_type in self.state.injected_faults:
            self.state.injected_faults.pop(fault_type, None)
            # Reset service states
            self.state.services = {
                "customer_service": "AVAILABLE",
                "account_service": "AVAILABLE",
                "transaction_service": "AVAILABLE",
                "ticket_service": "AVAILABLE",
                "notification_service": "AVAILABLE",
                "database_service": "AVAILABLE",
            }
    
    def get_service_state(self) -> dict[str, str]:
        """Return service availability state."""
        return dict(self.state.services)
    
    def get_resource_state(self) -> dict[str, Any]:
        """Return resource accounting state."""
        return dict(self.state.resource_counters)


def create_mock_environment(config: dict[str, Any] | None = None, seed: int = 42) -> MockEnvironment:
    """Create a configured mock environment."""
    return MockEnvironment(config, seed)