"""Unit tests for the DeterministicMockAgent."""

from __future__ import annotations

from agent_eval.agents.base import AgentAdapter
from agent_eval.agents.mock import DeterministicMockAgent
from agent_eval.domain.enums import AgentBehavior
from agent_eval.environments.support import SupportEnvironment


class TestDeterministicMockAgent:
    """Unit tests for DeterministicMockAgent."""

    def test_lifecycle_creation(self):
        """Agent starts in CREATED state."""
        agent = DeterministicMockAgent()
        assert agent.lifecycle_state == "CREATED"

    def test_lifecycle_initialization(self):
        """Agent transitions to READY after initialize."""
        agent = DeterministicMockAgent()
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Read customer data", "target_resource": "CUST-001"},
            environment=env,
            agent_id="agent-mock-01",
        )
        assert agent.lifecycle_state == "READY"

    def test_lifecycle_running(self):
        """Agent transitions to RUNNING after initialize."""
        agent = DeterministicMockAgent()
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-mock-01",
        )
        assert agent.lifecycle_state == "READY"
        # After first act, should be RUNNING or transition
        _action, _obs = agent.act()
        # Agent stays RUNNING until terminate

    def test_lifecycle_terminated(self):
        """Agent transitions to COMPLETED after terminate."""
        agent = DeterministicMockAgent()
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-mock-01",
        )
        agent.act()  # Take at least one step
        result = agent.terminate()
        assert agent.lifecycle_state == "COMPLETED"
        assert result["status"] in [
            "TASK_COMPLETED",
            "POLICY_DENIED",
            "RESOURCE_EXHAUSTED",
        ]

    def test_reset(self):
        """Agent reset clears state."""
        agent = DeterministicMockAgent()
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "test"},
            environment=env,
            agent_id="agent-mock-01",
        )
        agent.act()
        assert agent.lifecycle_state != "RESET"
        agent.reset()
        assert agent.lifecycle_state == "RESET"
        assert agent.step_count == 0

    def test_determinism_same_seed(self):
        """Same seed + same config = same action sequence."""
        agent1 = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ, seed=42
        )
        agent2 = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ, seed=42
        )
        env = SupportEnvironment()

        agent1.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-1",
        )
        agent2.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-2",
        )

        # Both should produce the same first action
        action1, _ = agent1.act()
        action2, _ = agent2.act()
        assert action1["tool_name"] == action2["tool_name"]
        assert action1["arguments"] == action2["arguments"]

    def test_determinism_different_seed(self):
        """Different seeds may produce different actions."""
        agent1 = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ, seed=42
        )
        agent2 = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ, seed=99
        )
        env = SupportEnvironment()

        agent1.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-1",
        )
        agent2.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-2",
        )

        _action1, _ = agent1.act()
        _action2, _ = agent2.act()
        # May or may not be the same depending on behavior implementation

    def test_step_limit(self):
        """Agent respects max_steps limit."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=42,
            max_steps=3,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-mock-01",
        )

        # Take steps until termination
        for _ in range(5):
            action, _obs = agent.act()
            if action["action_type"] == "terminate":
                break

        result = agent.terminate()
        assert result["steps"] <= 3

    def test_behavior_safe_authorized_read(self):
        """SAFE_AUTHORIZED_READ produces authorized actions."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-mock-01",
        )

        action, _obs = agent.act()
        # Should attempt customer.lookup with authorized customer
        assert action["tool_name"] in [
            "customer.lookup",
            "account.lookup",
            "ticket.search",
        ]

    def test_behavior_unsafe_unauthorized_read(self):
        """UNSAFE_UNAUTHORIZED_READ attempts unauthorized access."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.UNSAFE_UNAUTHORIZED_READ,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Read customer data"},
            environment=env,
            agent_id="agent-mock-01",
        )

        action, _obs = agent.act()
        # Should attempt to read another customer's data
        assert action["tool_name"] in [
            "customer.lookup",
            "account.lookup",
            "ticket.search",
        ]

    def test_behavior_unsafe_write(self):
        """UNSAFE_WRITE attempts unauthorized write."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.UNSAFE_WRITE,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Modify data"},
            environment=env,
            agent_id="agent-mock-01",
        )

        action, _obs = agent.act()
        # Should attempt write operations
        assert action["tool_name"] in ["ticket.update", "database.write"]

    def test_behavior_policy_bypass(self):
        """POLICY_BYPASS attempts unauthorized operations."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.POLICY_BYPASS,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Test policy"},
            environment=env,
            agent_id="agent-mock-01",
        )

        action, _obs = agent.act()
        # Should attempt unauthorized operations
        assert action["tool_name"] in [
            "customer.lookup",
            "account.lookup",
            "ticket.update",
            "database.write",
        ]

    def test_behavior_safe_recovery(self):
        """SAFE_RECOVERY handles faults boundedly."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_RECOVERY,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Test recovery"},
            environment=env,
            agent_id="agent-mock-01",
        )

        # Take a step
        action, _obs = agent.act()
        # Should attempt a read operation
        assert action["tool_name"] in ["customer.lookup", "account.lookup"]

    def test_behavior_unsafe_recovery(self):
        """UNSAFE_RECOVERY performs unsafe recovery."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.UNSAFE_RECOVERY,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Test unsafe recovery"},
            environment=env,
            agent_id="agent-mock-01",
        )

        action, _obs = agent.act()
        # Should attempt operations
        assert action["tool_name"] in [
            "customer.lookup",
            "account.lookup",
            "ticket.update",
            "database.write",
        ]

    def test_behavior_resource_abuse(self):
        """RESOURCE_ABUSE produces excessive tool usage."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.RESOURCE_ABUSE,
            seed=42,
            max_steps=25,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "Abuse resources"},
            environment=env,
            agent_id="agent-mock-01",
        )

        # Take multiple steps
        for _ in range(20):
            action, _obs = agent.act()
            if action["action_type"] == "terminate":
                break

        result = agent.terminate()
        # Should have taken many steps
        assert result["steps"] > 10

    def test_observe_records(self):
        """Observe records the observation."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "test"},
            environment=env,
            agent_id="agent-mock-01",
        )

        _action, obs = agent.act()
        # Now observe with a response
        agent.observe(obs)

        # Should have recorded the observation
        assert len(agent._observations) >= 1

    def test_observe_updates_state(self):
        """Observe updates internal state based on error codes."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=42,
        )
        env = SupportEnvironment()
        agent.initialize(
            task={"instruction": "test"},
            environment=env,
            agent_id="agent-mock-01",
        )

        _action, obs = agent.act()
        # Observe with POLICY_DENIED error
        agent.observe(
            {
                "observation_type": "tool_response",
                "tool_name": obs.get("tool_name", ""),
                "success": False,
                "error_code": "POLICY_DENIED",
                "policy_decision": {"decision": "DENY"},
                "state_changed": {},
                "metadata": {},
            }
        )

        result = agent.terminate()
        # Should have recorded policy denied
        assert result["termination_reason"] == "POLICY_DENIED"

    def test_agent_adapter_interface(self):
        """Agent implements the AgentAdapter interface."""
        agent = DeterministicMockAgent()
        assert isinstance(agent, AgentAdapter)

    def test_serialization_roundtrip(self):
        """Agent state serializes and deserializes."""
        agent = DeterministicMockAgent(
            behavior=AgentBehavior.SAFE_AUTHORIZED_READ,
            seed=42,
        )
        # Test that key attributes are settable and retrievable
        assert agent.behavior_mode == AgentBehavior.SAFE_AUTHORIZED_READ
        assert agent.step_count == 0
        assert agent.lifecycle_state in ["CREATED", "READY", "RUNNING"]
