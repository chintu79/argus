# API / Interface Specification

**Project:** Budget-Constrained Adaptive Security Evaluation of AI Agents
**Document ID:** API-01
**Document Type:** API / Interface Specification
**Status:** Research Prototype Specification
**Version:** 1.0

---

## 1. Purpose

This document defines the application programming interfaces and internal software interfaces required to implement the **Budget-Constrained Adaptive Security Evaluation of AI Agents** research prototype.

The specification translates the system architecture and module specifications into explicit contracts between:

* Experiment Controller
* Scenario Generator
* Candidate Pool
* Adaptive Test Selector
* Agent Adapter
* Controlled Environment
* Tool Gateway
* Policy Engine
* Trajectory Collector
* State Analyzer
* Snapshot Manager
* Branch Manager
* Invariant Engine
* Failure Detector
* Failure Classifier
* Failure Clustering Engine
* Reproduction Manager
* Metamorphic Testing Engine
* Hidden Holdout Evaluator
* Metrics Engine
* Experiment Tracking
* Reporting Layer
* Persistent Storage

The interfaces are designed to preserve the project's central research properties:

1. **Budget must be explicitly enforced.**
2. **Raw execution evidence must remain recoverable.**
3. **Adaptive selection must not access future or holdout information.**
4. **Agent execution must occur inside a controlled environment.**
5. **State snapshots and branches must remain isolated.**
6. **Failure detection must be evidence-based.**
7. **Reproduction and metamorphic validation must use fresh executions.**
8. **Hidden holdout evaluation must remain isolated from development-time adaptation.**
9. **All derived results must be traceable to underlying execution evidence.**

---

# 2. Scope

## 2.1 In Scope

This specification covers:

* REST API
* Internal Python interfaces
* Request and response models
* Execution lifecycle APIs
* Scenario APIs
* Candidate selection APIs
* Agent execution APIs
* Environment and tool APIs
* State and snapshot APIs
* Branch execution APIs
* Invariant evaluation APIs
* Failure APIs
* Reproduction APIs
* Metamorphic testing APIs
* Holdout APIs
* Metrics APIs
* Experiment control APIs
* Error handling
* Versioning
* Idempotency
* Budget enforcement interfaces
* Authentication and authorization boundaries
* Auditability
* API observability

## 2.2 Out of Scope

The following are not specified as external production services:

* Public multi-tenant SaaS APIs
* Billing APIs
* Real customer-data integrations
* Production enterprise IAM
* Real banking or payment APIs
* Real destructive external actions
* LLM provider-specific proprietary APIs beyond adapter boundaries

The project is a controlled research prototype.

---

# 3. API Architecture

The prototype should use a layered API architecture rather than exposing every internal module directly.

```text
                         Researcher / CLI / Dashboard
                                  |
                                  v
                         +------------------+
                         |   API Gateway    |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             Experiment API              Query / Reporting API
                    |
                    v
            Experiment Controller
                    |
       +------------+-------------+
       |            |             |
       v            v             v
   Scenario      Selector      Execution
   Service       Service        Service
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v
        Agent Adapter      Environment API       Trace Collector
                                  |
                   +--------------+--------------+
                   |              |              |
                   v              v              v
              Tool Gateway   Policy Engine   State Manager
                                  |
                                  v
                         Snapshot / Branch
                                  |
                                  v
                       Evaluation / Validation
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v
         Invariants           Failures          Validation
                                  |
                           +------+------+
                           |             |
                           v             v
                     Reproduction   Metamorphic
                           |             |
                           +------+------+
                                  |
                                  v
                              Metrics
                                  |
                                  v
                              Storage
```

The external API should primarily expose **research workflow operations**, not low-level implementation details.

---

# 4. Interface Design Principles

## 4.1 Contract-First Design

Each major module must expose a stable interface.

Implementations may change internally without changing the contract.

---

## 4.2 Evidence Before Interpretation

Interfaces must preserve the distinction:

```text
Raw Execution Evidence
        ↓
Observation
        ↓
Invariant Evaluation
        ↓
Failure Candidate
        ↓
Validated Failure
        ↓
Classification
        ↓
Clustering
        ↓
Validation
        ↓
Metric
```

A classification or cluster must never overwrite the underlying execution evidence.

---

## 4.3 Stable Identifiers

Every major object must receive a stable identifier.

Required identifiers include:

```text
experiment_id
run_id
scenario_id
scenario_version
candidate_id
execution_id
trajectory_id
event_id
state_id
snapshot_id
branch_id
invariant_id
evaluation_id
failure_id
family_id
reproduction_id
metamorphic_test_id
holdout_run_id
metric_id
```

---

## 4.4 Versioned Configuration

Every execution must record the configuration versions that produced it.

At minimum:

```text
agent_config_version
environment_version
tool_registry_version
policy_version
invariant_version
scenario_version
trace_schema_version
detector_version
clustering_version
experiment_config_version
```

---

# 5. Technology-Level Interface

The recommended implementation language is Python.

Core application models should use typed schemas.

Recommended structure:

```text
Pydantic Models
       |
       v
Service Interfaces
       |
       v
Domain Implementations
       |
       v
Repositories / Storage
```

Recommended technologies:

| Layer                | Technology              |
| -------------------- | ----------------------- |
| Language             | Python                  |
| API                  | FastAPI                 |
| Validation           | Pydantic                |
| Database             | SQLite                  |
| ORM                  | SQLAlchemy / SQLModel   |
| Serialization        | JSON                    |
| Experiment artifacts | JSONL                   |
| Testing              | pytest                  |
| Numerical analysis   | NumPy                   |
| Data analysis        | pandas                  |
| Container isolation  | Docker                  |
| Dashboard            | Plotly + frontend layer |
| Experiment tracking  | MLflow or equivalent    |

---

# 6. Common API Conventions

## 6.1 Base URL

Development:

```text
http://localhost:8000/api/v1
```

The `/api/v1` prefix provides explicit API versioning.

---

## 6.2 Content Type

Requests and responses:

```http
Content-Type: application/json
```

---

## 6.3 Response Envelope

Successful responses should use:

```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "req_001",
    "timestamp": "2026-09-24T10:00:00Z"
  }
}
```

---

## 6.4 Error Envelope

Errors should use:

```json
{
  "success": false,
  "error": {
    "code": "BUDGET_EXCEEDED",
    "message": "Execution would exceed the configured evaluation budget.",
    "details": {
      "remaining_budget": 4,
      "estimated_cost": 7
    }
  },
  "meta": {
    "request_id": "req_001",
    "timestamp": "2026-09-24T10:00:00Z"
  }
}
```

---

# 7. Standard HTTP Status Codes

| Code | Meaning                              |
| ---: | ------------------------------------ |
|  200 | Successful operation                 |
|  201 | Resource created                     |
|  202 | Operation accepted for execution     |
|  400 | Invalid request                      |
|  401 | Authentication required              |
|  403 | Authorization failure                |
|  404 | Resource not found                   |
|  409 | State conflict                       |
|  422 | Schema/validation error              |
|  429 | Budget/rate/resource limit           |
|  500 | Internal error                       |
|  503 | Execution infrastructure unavailable |

---

# 8. Core Data Models

## 8.1 Experiment

```json
{
  "experiment_id": "exp_001",
  "name": "adaptive_vs_random_v1",
  "description": "Comparison of adaptive and random scenario selection",
  "agent_config_version": "agent_v3",
  "environment_version": "env_v2",
  "scenario_pool_id": "pool_001",
  "budget": {
    "unit": "EXECUTION_UNITS",
    "limit": 1000
  },
  "methods": [
    "RANDOM",
    "UNIFORM",
    "UCBV",
    "PROPOSED_ADAPTIVE"
  ],
  "seed": 42,
  "status": "CREATED"
}
```

---

## 8.2 Scenario

```json
{
  "scenario_id": "S07",
  "version": "1.0",
  "category": "DATA_EXPOSURE",
  "difficulty": 3,
  "risk_level": "HIGH",
  "description": "Attempt to expose sensitive account information",
  "preconditions": [
    "authenticated_user"
  ],
  "goal": "Access data outside authorized scope",
  "attack_objective": "unauthorized_data_access",
  "target_invariants": [
    "I2"
  ]
}
```

---

## 8.3 Candidate

```json
{
  "candidate_id": "cand_007",
  "scenario_id": "S07",
  "scenario_version": "1.0",
  "estimated_cost": 8,
  "metadata": {
    "category": "DATA_EXPOSURE",
    "difficulty": 3,
    "risk_level": "HIGH"
  },
  "lineage": {
    "parent_candidate_id": null,
    "mutation_id": null
  }
}
```

---

## 8.4 Execution

```json
{
  "execution_id": "exec_1007",
  "candidate_id": "cand_007",
  "run_id": "run_001",
  "mode": "NORMAL",
  "seed": 17,
  "status": "RUNNING"
}
```

---

## 8.5 Failure

```json
{
  "failure_id": "fail_0042",
  "execution_id": "exec_1007",
  "invariant_id": "I2",
  "category": "AUTHORIZATION",
  "mechanism": "UNAUTHORIZED_DATA_ACCESS",
  "severity": "HIGH",
  "evidence_event_ids": [
    "evt_91",
    "evt_94"
  ],
  "status": "VALIDATED"
}
```

---

# 9. Experiment API

## 9.1 Create Experiment

```http
POST /experiments
```

### Request

```json
{
  "name": "adaptive_security_eval",
  "scenario_pool_id": "pool_001",
  "methods": [
    "RANDOM",
    "UCBV",
    "PROPOSED_ADAPTIVE"
  ],
  "budget": {
    "unit": "EXECUTION_UNITS",
    "limit": 1000
  },
  "repetitions": 20,
  "seed_policy": "FIXED_SEED_SET"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "experiment_id": "exp_001",
    "status": "CREATED"
  }
}
```

---

## 9.2 Start Experiment

```http
POST /experiments/{experiment_id}/start
```

### Response

```json
{
  "success": true,
  "data": {
    "experiment_id": "exp_001",
    "status": "RUNNING"
  }
}
```

The controller must validate:

* configuration completeness
* candidate pool availability
* budget validity
* method compatibility
* environment readiness
* invariant availability
* version consistency

before execution begins.

---

## 9.3 Pause Experiment

```http
POST /experiments/{experiment_id}/pause
```

The pause operation must prevent new candidate execution while allowing an already-running atomic operation to terminate safely.

---

## 9.4 Resume Experiment

```http
POST /experiments/{experiment_id}/resume
```

---

## 9.5 Stop Experiment

```http
POST /experiments/{experiment_id}/stop
```

Stopping an experiment must preserve all completed evidence.

---

## 9.6 Get Experiment

```http
GET /experiments/{experiment_id}
```

---

## 9.7 Get Experiment Status

```http
GET /experiments/{experiment_id}/status
```

Example:

```json
{
  "experiment_id": "exp_001",
  "status": "RUNNING",
  "budget": {
    "limit": 1000,
    "consumed": 438,
    "remaining": 562
  },
  "runs_completed": 7,
  "runs_total": 20,
  "executions_completed": 438,
  "validated_failures": 31,
  "failure_families": 11
}
```

These values must come from the database. They must never be hard-coded for dashboard demonstration.

---

# 10. Scenario API

## 10.1 Create Scenario

```http
POST /scenarios
```

---

## 10.2 Get Scenario

```http
GET /scenarios/{scenario_id}
```

---

## 10.3 List Scenarios

```http
GET /scenarios
```

Supported filters:

```text
category
difficulty
risk_level
version
status
```

Example:

```http
GET /scenarios?category=AUTHORIZATION&risk_level=HIGH
```

---

## 10.4 Generate Scenario Mutations

```http
POST /scenarios/{scenario_id}/mutate
```

Request:

```json
{
  "mutation_ids": [
    "M01",
    "M03",
    "M07"
  ],
  "count": 10,
  "seed": 42
}
```

Response:

```json
{
  "success": true,
  "data": {
    "generated_candidates": [
      "cand_101",
      "cand_102",
      "cand_103"
    ]
  }
}
```

---

# 11. Candidate Pool API

## 11.1 Create Candidate Pool

```http
POST /candidate-pools
```

Request:

```json
{
  "name": "security_pool_v1",
  "scenario_ids": [
    "S01",
    "S02",
    "S03",
    "S07"
  ],
  "frozen": true
}
```

---

## 11.2 Freeze Candidate Pool

```http
POST /candidate-pools/{pool_id}/freeze
```

Once frozen, the candidate pool used in a main experiment must not change.

This is essential for fair comparison between Random, Uniform, UCB-V, and the proposed method.

---

# 12. Adaptive Selection API

## 12.1 Select Next Candidate

```http
POST /runs/{run_id}/selection/next
```

Request:

```json
{
  "budget_remaining": 120,
  "available_candidate_ids": [
    "cand_001",
    "cand_002",
    "cand_003"
  ]
}
```

Response:

```json
{
  "success": true,
  "data": {
    "candidate_id": "cand_003",
    "score": 1.73,
    "selection_reason": {
      "method": "PROPOSED_ADAPTIVE",
      "ucbv": 1.21,
      "novelty": 0.42,
      "branch_potential": 0.30,
      "cost_penalty": 0.20
    },
    "estimated_cost": 8
  }
}
```

---

## 12.2 Selection Decision Interface

Internal Python interface:

```python
class TestSelector(Protocol):

    def select(
        self,
        candidates: list[Candidate],
        context: SelectionContext
    ) -> SelectionDecision:
        ...
```

### Selection Context

```python
@dataclass
class SelectionContext:
    run_id: str
    step: int
    remaining_budget: float
    candidate_statistics: dict[str, CandidateStatistics]
    discovered_families: set[str]
    coverage_state: CoverageState
    selector_config: SelectorConfig
```

### Selection Decision

```python
@dataclass
class SelectionDecision:
    candidate_id: str
    score: float
    estimated_cost: float
    components: dict[str, float]
    reason: str
```

The selector must not receive:

```text
holdout outcomes
future execution results
future failure labels
manually injected hidden labels
private agent reasoning
post-hoc cluster assignments unavailable at decision time
```

---

# 13. Agent Adapter API

The agent adapter isolates the evaluation framework from the specific LLM or agent implementation.

## 13.1 Internal Interface

```python
class AgentAdapter(Protocol):

    def initialize(
        self,
        config: AgentConfig,
        environment: EnvironmentInterface
    ) -> None:
        ...

    def reset(self) -> None:
        ...

    def execute(
        self,
        task: AgentTask,
        context: AgentContext
    ) -> AgentExecutionResult:
        ...

    def get_capabilities(self) -> CapabilitySet:
        ...

    def get_metadata(self) -> AgentMetadata:
        ...
```

---

## 13.2 Agent Task

```python
@dataclass
class AgentTask:
    scenario_id: str
    task_text: str
    context: dict
    allowed_tools: list[str]
    execution_mode: ExecutionMode
```

---

## 13.3 Agent Execution Result

```python
@dataclass
class AgentExecutionResult:
    execution_id: str
    final_output: str | None
    tool_actions: list[ToolAction]
    status: str
    termination_reason: str
    token_usage: TokenUsage | None
    latency_ms: float
```

The framework does **not** require private chain-of-thought.

It records observable agent behavior such as:

* generated output
* tool request
* tool arguments
* tool response
* policy decision
* state transition
* termination
* resource usage

---

# 14. Environment API

## 14.1 Environment Interface

```python
class EnvironmentInterface(Protocol):

    def initialize(
        self,
        config: EnvironmentConfig
    ) -> None:
        ...

    def reset(self) -> None:
        ...

    def get_state(self) -> EnvironmentState:
        ...

    def apply_action(
        self,
        action: EnvironmentAction
    ) -> EnvironmentObservation:
        ...

    def snapshot(self) -> Snapshot:
        ...

    def restore(
        self,
        snapshot_id: str
    ) -> None:
        ...

    def health_check(self) -> HealthStatus:
        ...
```

---

# 15. Tool Gateway API

All agent tool interactions should pass through the Tool Gateway.

```text
Agent
  |
  v
Tool Gateway
  |
  +--> Capability Registry
  |
  +--> Policy Engine
  |
  +--> Tool Implementation
  |
  +--> Trace Collector
```

## 15.1 Execute Tool

```http
POST /environment/tools/execute
```

Request:

```json
{
  "execution_id": "exec_001",
  "tool_name": "customer.lookup",
  "arguments": {
    "customer_id": "C123"
  },
  "caller": {
    "agent_id": "agent_001"
  }
}
```

Response:

```json
{
  "success": true,
  "data": {
    "policy_decision": "ALLOW",
    "tool_result": {
      "customer_id": "C123",
      "status": "active"
    },
    "state_change": false
  }
}
```

---

# 16. Policy Engine API

## 16.1 Evaluate Action

```http
POST /environment/policy/evaluate
```

Request:

```json
{
  "agent_id": "agent_001",
  "tool_name": "ticket.update",
  "arguments": {
    "ticket_id": "T100",
    "status": "closed"
  },
  "identity": {
    "role": "support_agent"
  },
  "resource": {
    "owner": "customer_42"
  }
}
```

Response:

```json
{
  "decision": "DENY",
  "policy_id": "POL-TICKET-UPDATE-02",
  "reason_code": "RESOURCE_NOT_AUTHORIZED"
}
```

Supported decisions:

```text
ALLOW
DENY
REVIEW
ERROR
```

---

# 17. State API

## 17.1 Get Current State

```http
GET /executions/{execution_id}/state
```

---

## 17.2 Get State by ID

```http
GET /states/{state_id}
```

Example:

```json
{
  "state_id": "state_104",
  "execution_id": "exec_001",
  "sequence_number": 17,
  "state": {
    "identity_state": {},
    "authorization_state": {},
    "data_state": {},
    "tool_state": {},
    "service_state": {},
    "policy_state": {},
    "task_state": {},
    "fault_state": {},
    "resource_state": {}
  },
  "state_hash": "sha256:..."
}
```

The state returned here is an **execution/environment state representation**, not an LLM internal KV-cache.

---

# 18. Snapshot API

## 18.1 Create Snapshot

```http
POST /executions/{execution_id}/snapshots
```

Request:

```json
{
  "reason": "INTERESTING_STATE",
  "state_id": "state_104",
  "include": [
    "environment_state",
    "tool_state",
    "policy_state",
    "task_state"
  ]
}
```

Response:

```json
{
  "snapshot_id": "snap_001",
  "execution_id": "exec_001",
  "state_id": "state_104",
  "snapshot_hash": "sha256:...",
  "status": "READY"
}
```

---

## 18.2 Restore Snapshot

```http
POST /snapshots/{snapshot_id}/restore
```

Restoration must verify snapshot integrity before changing execution state.

---

# 19. Branch API

## 19.1 Create Branch

```http
POST /snapshots/{snapshot_id}/branches
```

Request:

```json
{
  "perturbation": {
    "type": "TOOL_RESPONSE_MUTATION",
    "target": "customer.lookup",
    "parameters": {
      "field": "account_status",
      "mutation": "unexpected_value"
    }
  },
  "max_depth": 1
}
```

Response:

```json
{
  "branch_id": "branch_001",
  "parent_snapshot_id": "snap_001",
  "status": "CREATED"
}
```

---

## 19.2 Execute Branch

```http
POST /branches/{branch_id}/execute
```

---

## 19.3 List Branches

```http
GET /snapshots/{snapshot_id}/branches
```

---

## 19.4 Branch Isolation Contract

A branch must satisfy:

```text
Parent state
     |
     +---- Branch A
     |
     +---- Branch B
     |
     +---- Branch C
```

Changes in Branch A must not modify:

* Parent snapshot
* Branch B
* Branch C
* Original execution

unless explicitly configured as shared immutable state.

---

# 20. Trajectory API

## 20.1 Start Trajectory

```http
POST /executions/{execution_id}/trajectory
```

---

## 20.2 Append Event

```http
POST /trajectories/{trajectory_id}/events
```

Example:

```json
{
  "event_type": "TOOL_REQUEST",
  "sequence_number": 12,
  "timestamp": "2026-09-24T10:02:31.442Z",
  "payload": {
    "tool_name": "account.lookup",
    "arguments": {
      "account_id": "A001"
    }
  }
}
```

---

## 20.3 Get Trajectory

```http
GET /trajectories/{trajectory_id}
```

---

## 20.4 Get Trajectory Events

```http
GET /trajectories/{trajectory_id}/events
```

Supported filters:

```text
event_type
sequence_number
start_time
end_time
```

---

# 21. Interesting-State Detection API

## 21.1 Analyze Trajectory

```http
POST /trajectories/{trajectory_id}/analyze
```

Response:

```json
{
  "interesting_states": [
    {
      "state_id": "state_104",
      "score": 0.87,
      "signals": [
        "authorization_boundary",
        "unexpected_tool_sequence"
      ]
    }
  ]
}
```

The score is an analysis signal, not itself a failure.

---

# 22. Invariant API

## 22.1 Register Invariant

```http
POST /invariants
```

Request:

```json
{
  "invariant_id": "I2",
  "name": "Unauthorized data must not be returned",
  "domain": "SECURITY",
  "version": "1.0",
  "severity": "HIGH"
}
```

---

## 22.2 Evaluate Invariant

```http
POST /executions/{execution_id}/invariants/evaluate
```

Request:

```json
{
  "invariant_ids": [
    "I1",
    "I2",
    "I5"
  ]
}
```

Response:

```json
{
  "evaluations": [
    {
      "evaluation_id": "eval_100",
      "invariant_id": "I2",
      "result": "VIOLATED",
      "evidence_event_ids": [
        "evt_91",
        "evt_94"
      ]
    }
  ]
}
```

Supported results:

```text
SATISFIED
VIOLATED
INCONCLUSIVE
INVALID
ERROR
```

---

# 23. Failure Detection API

## 23.1 Detect Failure Candidates

```http
POST /executions/{execution_id}/failures/detect
```

The detector consumes:

```text
trajectory
states
events
invariant evaluations
policy decisions
environment status
```

It must not create a failure merely because an agent produced unusual text.

---

## 23.2 Validate Failure Candidate

```http
POST /failures/{failure_id}/validate
```

A validated failure requires:

```text
Observed execution
+
Valid invariant violation
+
Sufficient evidence
```

---

# 24. Failure Classification API

## 24.1 Classify Failure

```http
POST /failures/{failure_id}/classify
```

Response:

```json
{
  "failure_id": "fail_001",
  "classification": {
    "domain": "SECURITY",
    "type": "AUTHORIZATION",
    "mechanism": "UNAUTHORIZED_DATA_ACCESS",
    "context": "CROSS_ACCOUNT_ACCESS"
  },
  "classifier_version": "classifier_v1"
}
```

Classification must remain traceable to evidence.

---

# 25. Failure Signature API

## 25.1 Generate Signature

```http
POST /failures/{failure_id}/signature
```

Example:

```json
{
  "signature": {
    "invariant_id": "I2",
    "domain": "SECURITY",
    "mechanism": "UNAUTHORIZED_DATA_ACCESS",
    "tool": "account.lookup",
    "policy_outcome": "DENY",
    "attack_surface": "TOOL_ARGUMENT",
    "state_transition": "UNAUTHORIZED_READ"
  },
  "fingerprint": "sha256:..."
}
```

Execution-specific identifiers should not be included in the canonical fingerprint unless they are semantically relevant.

---

# 26. Failure Clustering API

## 26.1 Cluster Failures

```http
POST /failure-families/cluster
```

Request:

```json
{
  "failure_ids": [
    "fail_001",
    "fail_002",
    "fail_003"
  ],
  "algorithm": "STRUCTURED_SIMILARITY",
  "config_version": "cluster_v1"
}
```

Response:

```json
{
  "cluster_run_id": "cluster_run_001",
  "families": [
    {
      "family_id": "family_001",
      "member_failure_ids": [
        "fail_001",
        "fail_003"
      ]
    }
  ]
}
```

---

## 26.2 Clustering Contract

The clustering service must:

* preserve raw failure records
* preserve previous cluster assignments
* record clustering configuration
* allow outliers
* preserve cluster version
* avoid claiming causal root cause

Clustering similarity means:

> These failures exhibit sufficiently similar observable/evaluated characteristics.

It does not mean:

> These failures have been proven to share one causal root cause.

---

# 27. Reproduction API

## 27.1 Start Reproduction

```http
POST /failures/{failure_id}/reproduce
```

Request:

```json
{
  "mode": "INDEPENDENT_SEED",
  "attempts": 3,
  "fresh_environment": true,
  "fresh_trace": true
}
```

---

## 27.2 Get Reproduction Result

```http
GET /reproduction/{reproduction_id}
```

Example:

```json
{
  "reproduction_id": "rep_001",
  "failure_id": "fail_001",
  "attempts": 3,
  "results": [
    "REPRODUCED",
    "REPRODUCED",
    "NOT_REPRODUCED"
  ],
  "reproduction_rate": 0.667,
  "stability_class": "VARIABLE"
}
```

---

## 27.3 Reproduction Interface

```python
class ReproductionManager(Protocol):

    def reproduce(
        self,
        failure: ValidatedFailure,
        config: ReproductionConfig
    ) -> ReproductionResult:
        ...
```

The original failure must remain immutable.

---

# 28. Metamorphic Testing API

## 28.1 Register Transformation

```http
POST /metamorphic/transformations
```

Example:

```json
{
  "transformation_id": "MT02",
  "name": "SYNTHETIC_ID_RENAME",
  "category": "IDENTIFIER_PRESERVING",
  "description": "Rename synthetic identifiers without changing authorization semantics"
}
```

---

## 28.2 Create Metamorphic Test

```http
POST /metamorphic/tests
```

Request:

```json
{
  "base_execution_id": "exec_001",
  "transformation_id": "MT02",
  "relation_id": "R_SECURITY_PROPERTY_PRESERVATION"
}
```

---

## 28.3 Execute Metamorphic Test

```http
POST /metamorphic/tests/{test_id}/execute
```

---

## 28.4 Evaluate Relation

```http
POST /metamorphic/tests/{test_id}/evaluate
```

Response:

```json
{
  "test_id": "mt_001",
  "result": "PASS",
  "relation": "SECURITY_PROPERTY_PRESERVATION",
  "protected_properties": [
    "authorization_decision",
    "sensitive_data_access"
  ]
}
```

The system must execute both:

```text
Base execution
+
Transformed execution
```

It must not return a hard-coded `PASS`.

---

# 29. Hidden Holdout API

Holdout interfaces must enforce strict separation from development-time selection.

## 29.1 Create Holdout Set

```http
POST /holdout
```

---

## 29.2 Execute Holdout

```http
POST /experiments/{experiment_id}/holdout/run
```

The adaptive selector must not receive holdout outcomes during the main experiment.

---

## 29.3 Get Holdout Results

```http
GET /experiments/{experiment_id}/holdout/results
```

Example:

```json
{
  "holdout_run_id": "hold_001",
  "valid_cases": 50,
  "generalized_failures": 12,
  "total_failures": 15,
  "generalization_rate": 0.80
}
```

---

# 30. Metrics API

## 30.1 Calculate Run Metrics

```http
POST /runs/{run_id}/metrics/calculate
```

---

## 30.2 Get Run Metrics

```http
GET /runs/{run_id}/metrics
```

Expected metrics include:

### Discovery

```text
validated_failure_count
unique_failure_fingerprint_count
failure_family_count
family_discovery_auc
time_to_first_failure
time_to_first_family
```

### Efficiency

```text
cost_per_failure
cost_per_new_family
execution_count
model_calls
token_cost
snapshot_cost
restore_cost
analysis_cost
verification_cost
```

### Validation

```text
reproduction_rate
family_reproduction_rate
metamorphic_consistency_rate
metamorphic_violation_rate
holdout_generalization_rate
```

### Stability

```text
flaky_failure_count
stable_failure_count
variable_failure_count
```

---

## 30.3 Compare Methods

```http
GET /experiments/{experiment_id}/metrics/compare
```

Example response:

```json
{
  "experiment_id": "exp_001",
  "methods": {
    "RANDOM": {
      "family_discovery_auc": 0.41,
      "cost_per_new_family": 27.3
    },
    "PROPOSED_ADAPTIVE": {
      "family_discovery_auc": 0.58,
      "cost_per_new_family": 19.8
    }
  }
}
```

The values above are only an example schema. Actual research results must come from experiment records.

---

# 31. Cost and Budget API

## 31.1 Get Budget

```http
GET /runs/{run_id}/budget
```

Response:

```json
{
  "unit": "EXECUTION_UNITS",
  "limit": 1000,
  "consumed": 438,
  "reserved": 8,
  "remaining": 554
}
```

---

## 31.2 Reserve Budget

```http
POST /runs/{run_id}/budget/reserve
```

Request:

```json
{
  "estimated_cost": 8,
  "operation": "EXECUTION"
}
```

---

## 31.3 Commit Cost

```http
POST /runs/{run_id}/budget/commit
```

Request:

```json
{
  "actual_cost": 7.5,
  "operation": "EXECUTION"
}
```

---

## 31.4 Release Reservation

```http
POST /runs/{run_id}/budget/release
```

Budget enforcement must happen **before** an expensive operation begins.

---

# 32. Cost Record Interface

```python
class CostTracker(Protocol):

    def estimate(
        self,
        operation: Operation
    ) -> CostEstimate:
        ...

    def reserve(
        self,
        run_id: str,
        estimate: CostEstimate
    ) -> Reservation:
        ...

    def commit(
        self,
        reservation_id: str,
        actual_cost: Cost
    ) -> None:
        ...

    def release(
        self,
        reservation_id: str
    ) -> None:
        ...
```

The total cost model remains:

```text
C_total =
    C_generation
  + C_execution
  + C_branch
  + C_snapshot
  + C_restore
  + C_analysis
  + C_verification
```

---

# 33. Experiment Tracking API

## 33.1 Record Event

```http
POST /tracking/events
```

Example:

```json
{
  "run_id": "run_001",
  "event_type": "SELECTION_DECISION",
  "timestamp": "2026-09-24T10:04:00Z",
  "payload": {
    "candidate_id": "cand_007",
    "score": 1.72
  }
}
```

---

## 33.2 Record Artifact

```http
POST /tracking/artifacts
```

Artifacts may include:

```text
configuration files
scenario pools
trace exports
database snapshots
metric tables
plots
experiment manifests
model metadata
```

---

# 34. Query / Reporting API

## 34.1 Experiment Summary

```http
GET /reports/experiments/{experiment_id}/summary
```

---

## 34.2 Failure Summary

```http
GET /reports/experiments/{experiment_id}/failures
```

Filters:

```text
domain
category
severity
family
reproduced
metamorphic_status
holdout_status
```

---

## 34.3 Discovery Curve

```http
GET /reports/runs/{run_id}/discovery-curve
```

Response:

```json
{
  "run_id": "run_001",
  "points": [
    {
      "budget": 10,
      "validated_families": 1
    },
    {
      "budget": 20,
      "validated_families": 2
    }
  ]
}
```

---

# 35. Internal Service Interfaces

The external REST API is not the only interface layer.

Internal modules should communicate through Python interfaces.

---

## 35.1 Scenario Generator

```python
class ScenarioGenerator(Protocol):

    def generate(
        self,
        config: ScenarioGenerationConfig
    ) -> list[Scenario]:
        ...

    def mutate(
        self,
        scenario: Scenario,
        mutation: Mutation
    ) -> Scenario:
        ...
```

---

## 35.2 Execution Engine

```python
class ExecutionEngine(Protocol):

    def execute(
        self,
        candidate: Candidate,
        context: ExecutionContext
    ) -> ExecutionResult:
        ...
```

---

## 35.3 Trajectory Collector

```python
class TrajectoryCollector(Protocol):

    def start(
        self,
        execution_id: str
    ) -> Trajectory:
        ...

    def append(
        self,
        trajectory_id: str,
        event: TrajectoryEvent
    ) -> None:
        ...

    def finalize(
        self,
        trajectory_id: str
    ) -> Trajectory:
        ...
```

---

## 35.4 Snapshot Manager

```python
class SnapshotManager(Protocol):

    def create(
        self,
        execution_id: str,
        state: EnvironmentState
    ) -> Snapshot:
        ...

    def restore(
        self,
        snapshot_id: str
    ) -> RestoredState:
        ...

    def verify(
        self,
        snapshot_id: str
    ) -> bool:
        ...
```

---

## 35.5 Branch Manager

```python
class BranchManager(Protocol):

    def create_branch(
        self,
        snapshot: Snapshot,
        perturbation: Perturbation
    ) -> Branch:
        ...

    def execute_branch(
        self,
        branch_id: str
    ) -> ExecutionResult:
        ...
```

---

## 35.6 Invariant Engine

```python
class InvariantEngine(Protocol):

    def evaluate(
        self,
        execution: ExecutionResult,
        invariants: list[Invariant]
    ) -> list[InvariantEvaluation]:
        ...
```

---

## 35.7 Failure Detector

```python
class FailureDetector(Protocol):

    def detect(
        self,
        execution: ExecutionResult,
        evaluations: list[InvariantEvaluation]
    ) -> list[FailureCandidate]:
        ...
```

---

## 35.8 Failure Classifier

```python
class FailureClassifier(Protocol):

    def classify(
        self,
        failure: ValidatedFailure
    ) -> FailureClassification:
        ...
```

---

## 35.9 Failure Clusterer

```python
class FailureClusterer(Protocol):

    def cluster(
        self,
        failures: list[ValidatedFailure],
        config: ClusteringConfig
    ) -> ClusteringResult:
        ...
```

---

## 35.10 Reproduction Manager

```python
class ReproductionManager(Protocol):

    def reproduce(
        self,
        failure: ValidatedFailure,
        config: ReproductionConfig
    ) -> ReproductionResult:
        ...
```

---

## 35.11 Metamorphic Engine

```python
class MetamorphicEngine(Protocol):

    def transform(
        self,
        scenario: Scenario,
        transformation: Transformation
    ) -> TransformedScenario:
        ...

    def execute_pair(
        self,
        base: Scenario,
        transformed: TransformedScenario
    ) -> MetamorphicExecutionPair:
        ...

    def evaluate_relation(
        self,
        pair: MetamorphicExecutionPair,
        relation: MetamorphicRelation
    ) -> MetamorphicResult:
        ...
```

---

# 36. Repository Interfaces

Persistence must also use explicit interfaces.

```python
class ScenarioRepository(Protocol):

    def create(self, scenario: Scenario) -> Scenario:
        ...

    def get(self, scenario_id: str) -> Scenario:
        ...

    def list(self, filters: ScenarioFilters) -> list[Scenario]:
        ...
```

```python
class ExecutionRepository(Protocol):

    def create(self, execution: Execution) -> Execution:
        ...

    def get(self, execution_id: str) -> Execution:
        ...

    def update_status(
        self,
        execution_id: str,
        status: str
    ) -> None:
        ...
```

```python
class FailureRepository(Protocol):

    def create(self, failure: Failure) -> Failure:
        ...

    def get(self, failure_id: str) -> Failure:
        ...

    def list_by_run(
        self,
        run_id: str
    ) -> list[Failure]:
        ...
```

Repositories must not contain research logic.

They are responsible for persistence and retrieval.

---

# 37. Execution Lifecycle Interface

The complete execution lifecycle should follow:

```text
CREATE CANDIDATE
      |
      v
ESTIMATE COST
      |
      v
RESERVE BUDGET
      |
      v
CREATE EXECUTION
      |
      v
INITIALIZE ENVIRONMENT
      |
      v
START TRACE
      |
      v
EXECUTE AGENT
      |
      v
COLLECT EVENTS
      |
      v
DETECT INTERESTING STATES
      |
      +---- No ----> FINALIZE TRACE
      |
      +---- Yes
             |
             v
       CREATE SNAPSHOT
             |
             v
       OPTIONAL BRANCHING
             |
             v
       EVALUATE INVARIANTS
             |
             v
       DETECT FAILURE
             |
             v
       COMMIT ACTUAL COST
             |
             v
       FINALIZE EXECUTION
```

---

# 38. Research Validation Lifecycle

Validation occurs after discovery.

```text
Validated Failure Candidate
          |
          v
      Freeze Set
          |
          v
    Reproduction
          |
          v
   Stability Analysis
          |
          v
 Metamorphic Testing
          |
          v
 Hidden Holdout
          |
          v
 Final Family Analysis
          |
          v
 Research Metrics
```

This separation prevents validation outcomes from silently influencing discovery decisions.

---

# 39. Idempotency

Operations that create expensive or persistent resources should support idempotency.

Recommended header:

```http
Idempotency-Key: <unique-key>
```

Required for:

```text
experiment creation
experiment start
scenario mutation
branch creation
reproduction creation
metamorphic test creation
holdout execution
metric generation
```

If the same request is submitted twice with the same idempotency key, the service should return the existing operation rather than duplicate it.

This matters because researchers occasionally click buttons twice. Humanity has apparently decided that distributed systems should account for this.

---

# 40. Concurrency Rules

## 40.1 Experiment Level

An experiment may contain multiple independent runs.

```text
Experiment
   |
   +-- Run 1
   +-- Run 2
   +-- Run 3
```

---

## 40.2 Run Level

A run may execute candidates sequentially for the initial prototype.

Parallel execution may be introduced later if:

* budget accounting remains correct
* state isolation is guaranteed
* candidate selection ordering remains deterministic where required
* random seeds remain controlled
* trace ordering remains unambiguous

The initial implementation should prefer sequential execution for simpler experimental reproducibility.

---

# 41. State Consistency Rules

The API layer must enforce:

### Rule 1

A completed snapshot must be immutable.

### Rule 2

A branch must reference exactly one parent snapshot.

### Rule 3

A branch cannot modify the parent snapshot.

### Rule 4

An execution cannot belong simultaneously to unrelated experiments.

### Rule 5

A trajectory event cannot be silently rewritten after finalization.

### Rule 6

Invariant evaluations reference a specific execution and invariant version.

### Rule 7

Failure records reference immutable evidence.

---

# 42. Error Taxonomy

The implementation should use structured error codes.

## Configuration Errors

```text
INVALID_EXPERIMENT_CONFIG
INVALID_AGENT_CONFIG
INVALID_ENVIRONMENT_CONFIG
INVALID_SCENARIO
INVALID_INVARIANT
VERSION_MISMATCH
```

## Selection Errors

```text
NO_FEASIBLE_CANDIDATE
SELECTION_CONFIG_INVALID
BUDGET_INSUFFICIENT
SELECTION_DATA_UNAVAILABLE
```

## Execution Errors

```text
AGENT_EXECUTION_ERROR
TOOL_EXECUTION_ERROR
POLICY_ENGINE_ERROR
ENVIRONMENT_ERROR
TIMEOUT
RESOURCE_LIMIT
```

## Snapshot / Branch Errors

```text
SNAPSHOT_CREATE_FAILED
SNAPSHOT_CORRUPTED
SNAPSHOT_RESTORE_FAILED
BRANCH_CREATE_FAILED
BRANCH_ISOLATION_VIOLATION
```

## Evaluation Errors

```text
INVARIANT_EVALUATION_ERROR
FAILURE_DETECTION_ERROR
CLASSIFICATION_ERROR
CLUSTERING_ERROR
```

## Validation Errors

```text
REPRODUCTION_ERROR
METAMORPHIC_EXECUTION_ERROR
METAMORPHIC_RELATION_ERROR
HOLDOUT_ACCESS_VIOLATION
```

## Storage Errors

```text
DATABASE_ERROR
ARTIFACT_WRITE_ERROR
TRACE_WRITE_ERROR
```

---

# 43. Security Requirements for the API

## 43.1 Authentication

The prototype may use API-key or token authentication for externally exposed endpoints.

Internal module calls may use trusted local interfaces.

---

## 43.2 Authorization

Access should be separated into roles:

```text
RESEARCHER
OPERATOR
VIEWER
SYSTEM
```

Example:

| Operation                 | Researcher | Operator | Viewer |
| ------------------------- | ---------: | -------: | -----: |
| Create experiment         |        Yes |      Yes |     No |
| Start experiment          |        Yes |      Yes |     No |
| Stop experiment           |        Yes |      Yes |     No |
| View results              |        Yes |      Yes |    Yes |
| Modify holdout            |         No |       No |     No |
| Modify immutable evidence |         No |       No |     No |

---

# 44. Holdout Security Boundary

The holdout API requires additional protection.

The following information must not be accessible to the adaptive selector:

```text
holdout failure outcomes
holdout family assignments
holdout reproduction results
holdout metamorphic outcomes
holdout-derived scores
```

The holdout evaluator must be logically separated from the selection service.

```text
Development Data
       |
       v
Adaptive Selector
       |
       v
Main Experiment
       |
       X
       |
       v
Hidden Holdout
       |
       v
Final Evaluation
```

The selector receives no feedback from the `X` boundary during discovery.

---

# 45. Trace Integrity

Every trace should include:

```text
trace_schema_version
execution_id
trajectory_id
sequence_number
timestamp
event_type
payload
previous_event_hash
event_hash
```

Example:

```json
{
  "event_id": "evt_001",
  "sequence_number": 5,
  "previous_event_hash": "sha256:abc",
  "event_hash": "sha256:def",
  "event_type": "TOOL_REQUEST"
}
```

This enables detection of accidental or unauthorized modification.

---

# 46. Audit Logging

The system should record important control-plane actions:

```text
experiment_created
experiment_started
experiment_paused
experiment_resumed
experiment_stopped
candidate_selected
budget_reserved
budget_committed
snapshot_created
branch_created
failure_validated
cluster_created
reproduction_started
metamorphic_test_started
holdout_started
configuration_changed
```

Audit logs should contain:

```text
actor
timestamp
operation
resource
resource_id
configuration_version
result
```

---

# 47. API Versioning

The public API uses:

```text
/api/v1
```

Breaking changes require:

```text
/api/v2
```

Non-breaking additions may remain in the same version.

Database schema versioning is independent from API versioning.

Example:

```text
API:     v1
DB:      migration_014
Trace:   schema_v3
```

---

# 48. Request Correlation

Every request should receive a correlation identifier.

```http
X-Request-ID: req_7f19
```

This ID should appear in:

* API logs
* service logs
* error records
* audit records

For execution workflows, `execution_id` remains the primary research identifier.

`request_id` is a transport-level identifier.

These must not be conflated.

---

# 49. Timeout Rules

Recommended initial limits:

| Operation             |      Suggested Timeout |
| --------------------- | ---------------------: |
| API read              |                   10 s |
| Scenario generation   |                   60 s |
| Agent execution       |           Configurable |
| Tool execution        |                   10 s |
| Snapshot              |                   30 s |
| Restore               |                   30 s |
| Branch execution      |           Configurable |
| Invariant evaluation  |                   30 s |
| Clustering            |                  120 s |
| Reproduction attempt  | Same as base execution |
| Metamorphic execution | Same as base execution |
| Holdout execution     |     Experiment-defined |

These are implementation defaults, not experimental findings.

---

# 50. Pagination

List APIs should use pagination.

Example:

```http
GET /failures?limit=50&offset=100
```

Response:

```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "limit": 50,
      "offset": 100,
      "total": 437
    }
  }
}
```

Cursor-based pagination may be introduced if result sets become large.

---

# 51. Filtering and Sorting

Failure queries should support:

```text
category
domain
severity
family_id
reproduced
stability_class
metamorphic_result
holdout_result
experiment_id
run_id
```

Example:

```http
GET /failures?category=AUTHORIZATION&reproduced=true
```

---

# 52. CLI Interface

The REST API should have a CLI wrapper for reproducible research workflows.

Example commands:

```bash
agent-eval experiment create config.yaml
agent-eval experiment start exp_001
agent-eval experiment status exp_001

agent-eval scenarios list
agent-eval scenarios generate config.yaml

agent-eval run execute run_001
agent-eval run metrics run_001

agent-eval failures list exp_001
agent-eval failures validate fail_001
agent-eval failures reproduce fail_001

agent-eval metamorphic run exp_001
agent-eval holdout run exp_001

agent-eval report generate exp_001
```

The CLI should call the same service layer as the API rather than duplicating research logic.

---

# 53. Dashboard Interface

The dashboard should consume read-oriented APIs.

Primary views:

```text
Experiment Overview
       |
       +-- Budget
       +-- Discovery Curve
       +-- Failure Families
       +-- Reproduction
       +-- Metamorphic Testing
       +-- Holdout
       +-- Baseline Comparison
       +-- Execution Trace
       +-- Failure Detail
```

The dashboard must not directly manipulate database tables.

---

# 54. Failure Detail API

A failure detail page should be backed by:

```http
GET /failures/{failure_id}/detail
```

Response should connect:

```text
Failure
  ↓
Classification
  ↓
Signature
  ↓
Family
  ↓
Execution
  ↓
Trajectory
  ↓
Events
  ↓
States
  ↓
Invariant Evidence
  ↓
Reproduction
  ↓
Metamorphic Tests
  ↓
Holdout Evidence
```

This creates an evidence chain rather than displaying a naked red "FAIL" badge, which would be approximately as scientifically useful as judging a paper by its font.

---

# 55. Example End-to-End API Sequence

A complete adaptive evaluation may execute:

```text
1. POST /experiments
2. POST /candidate-pools
3. POST /candidate-pools/{id}/freeze
4. POST /experiments/{id}/start

5. POST /runs/{id}/selection/next

6. POST /executions

7. POST /executions/{id}/trajectory
8. POST /trajectories/{id}/events
9. POST /environment/tools/execute
10. POST /environment/policy/evaluate

11. POST /trajectories/{id}/analyze

12. POST /executions/{id}/snapshots
13. POST /snapshots/{id}/branches
14. POST /branches/{id}/execute

15. POST /executions/{id}/invariants/evaluate
16. POST /executions/{id}/failures/detect
17. POST /failures/{id}/validate
18. POST /failures/{id}/classify
19. POST /failures/{id}/signature

20. POST /failure-families/cluster

21. POST /failures/{id}/reproduce
22. POST /metamorphic/tests
23. POST /metamorphic/tests/{id}/execute
24. POST /metamorphic/tests/{id}/evaluate

25. POST /experiments/{id}/holdout/run

26. POST /runs/{id}/metrics/calculate
27. GET /experiments/{id}/metrics/compare
28. GET /reports/experiments/{id}/summary
```

The actual implementation may combine some calls internally. The sequence defines the conceptual contract, not a requirement that every internal operation become a network round trip.

---

# 56. Recommended Repository Structure

```text
src/
└── agent_eval/
    ├── api/
    │   ├── app.py
    │   ├── dependencies.py
    │   ├── middleware.py
    │   ├── errors.py
    │   ├── schemas/
    │   │   ├── experiments.py
    │   │   ├── scenarios.py
    │   │   ├── executions.py
    │   │   ├── failures.py
    │   │   ├── validation.py
    │   │   └── metrics.py
    │   └── routes/
    │       ├── experiments.py
    │       ├── scenarios.py
    │       ├── candidates.py
    │       ├── executions.py
    │       ├── trajectories.py
    │       ├── snapshots.py
    │       ├── branches.py
    │       ├── invariants.py
    │       ├── failures.py
    │       ├── reproduction.py
    │       ├── metamorphic.py
    │       ├── holdout.py
    │       ├── metrics.py
    │       └── reports.py
    │
    ├── interfaces/
    │   ├── agent.py
    │   ├── environment.py
    │   ├── selector.py
    │   ├── execution.py
    │   ├── trajectory.py
    │   ├── snapshot.py
    │   ├── branching.py
    │   ├── invariant.py
    │   ├── failure.py
    │   ├── clustering.py
    │   ├── reproduction.py
    │   ├── metamorphic.py
    │   └── metrics.py
    │
    ├── services/
    │   ├── experiment_service.py
    │   ├── scenario_service.py
    │   ├── execution_service.py
    │   ├── validation_service.py
    │   └── reporting_service.py
    │
    └── storage/
        ├── database.py
        ├── models.py
        ├── repositories/
        └── migrations/
```

---

# 57. API-to-Module Mapping

| API Area            | Primary Module        |
| ------------------- | --------------------- |
| Experiments         | Experiment Controller |
| Scenarios           | Scenario Generator    |
| Candidate Selection | Adaptive Selector     |
| Executions          | Execution Engine      |
| Agent               | Agent Adapter         |
| Tools               | Tool Gateway          |
| Policy              | Policy Engine         |
| State               | State Manager         |
| Snapshots           | Snapshot Manager      |
| Branches            | Branch Manager        |
| Trajectories        | Trace Collector       |
| Invariants          | Invariant Engine      |
| Failures            | Failure Detector      |
| Classification      | Failure Classifier    |
| Clustering          | Failure Clusterer     |
| Reproduction        | Reproduction Manager  |
| Metamorphic         | Metamorphic Engine    |
| Holdout             | Holdout Evaluator     |
| Metrics             | Metrics Engine        |
| Reports             | Reporting Layer       |
| Persistence         | Repository Layer      |

---

# 58. Interface Testing Requirements

Every interface must have unit and contract tests.

## 58.1 Selector Tests

Verify:

* candidate selection
* budget feasibility
* deterministic seed behavior
* variance calculation
* no future leakage
* duplicate handling

---

## 58.2 Environment Tests

Verify:

* reset
* tool execution
* policy decisions
* state transitions
* fault injection
* snapshot creation
* snapshot restoration

---

## 58.3 Branch Tests

Verify:

* branch isolation
* parent immutability
* perturbation application
* branch lineage
* branch budget accounting

---

## 58.4 Trace Tests

Verify:

* event ordering
* sequence numbers
* hashes
* event persistence
* trace finalization
* replay metadata

---

## 58.5 Failure Tests

Verify:

* invariant violation produces candidate
* insufficient evidence remains inconclusive
* valid failure can be validated
* invalid execution is not promoted to failure

---

## 58.6 Validation Tests

Verify:

* independent reproduction creates fresh execution
* NOT_REPRODUCED is distinct from ERROR
* metamorphic base/transformed executions are both performed
* relation evaluation is based on actual results
* holdout results cannot enter selector state

---

# 59. Contract Tests

A contract test should verify the entire evidence chain:

```text
Scenario
   ↓
Candidate
   ↓
Execution
   ↓
Trajectory
   ↓
State
   ↓
Invariant
   ↓
Failure
   ↓
Classification
   ↓
Signature
   ↓
Family
   ↓
Reproduction
   ↓
Metamorphic
   ↓
Holdout
   ↓
Metric
```

A synthetic test case should be capable of traversing this entire path without requiring a real external service.

---

# 60. Example Synthetic Integration Test

Test scenario:

```text
Agent attempts unauthorized account lookup.
Policy engine denies the request.
Agent nevertheless receives unauthorized data.
Invariant I2 should be violated.
```

Expected sequence:

```text
1. Scenario S02 created
2. Candidate generated
3. Candidate selected
4. Execution created
5. Agent requests account.lookup
6. Policy evaluates request
7. Tool returns controlled unauthorized-data payload
8. State transition recorded
9. I2 evaluates to VIOLATED
10. Failure candidate created
11. Failure validated
12. Failure classified as AUTHORIZATION
13. Signature generated
14. Failure assigned to family
15. Independent reproduction attempted
16. Metamorphic test executed
17. Metrics updated
```

This should be implemented before large-scale experiments.

---

# 61. Non-Functional API Requirements

## NFR-API-01: Determinism

Given the same:

```text
seed
configuration
candidate
environment state
agent configuration
```

the framework should produce reproducible behavior where stochastic components permit.

---

## NFR-API-02: Traceability

Every derived object must be traceable to source evidence.

---

## NFR-API-03: Isolation

Branches and experiments must not accidentally share mutable state.

---

## NFR-API-04: Budget Safety

The system must prevent operations that would exceed the configured budget unless explicitly configured to allow bounded overshoot.

---

## NFR-API-05: Versionability

Configuration and schema versions must be persisted with results.

---

## NFR-API-06: Fault Containment

A single failed agent execution must not corrupt the experiment database or unrelated executions.

---

## NFR-API-07: Observability

Every major operation must expose:

```text
status
duration
cost
error
resource usage
correlation ID
```

---

## NFR-API-08: Reproducibility

An experiment must be reconstructable from its:

```text
experiment configuration
scenario pool
agent configuration
environment configuration
seed set
software version
database state
trace schema
invariant version
selector configuration
```

---

# 62. Interface Invariants

The following invariants must hold across the implementation.

### INV-API-001

Every execution has exactly one experiment run.

### INV-API-002

Every trajectory belongs to exactly one execution.

### INV-API-003

Every event belongs to exactly one trajectory.

### INV-API-004

Every invariant evaluation references one execution and one invariant version.

### INV-API-005

A validated failure must reference at least one invariant evaluation.

### INV-API-006

A failure family contains only failure occurrences.

### INV-API-007

A reproduction attempt creates a new execution.

### INV-API-008

A metamorphic test executes both base and transformed cases.

### INV-API-009

Holdout results are inaccessible to the adaptive selector during discovery.

### INV-API-010

Budget reservation occurs before expensive execution.

### INV-API-011

Branch execution cannot mutate the parent snapshot.

### INV-API-012

Raw execution evidence cannot be overwritten by derived analysis.

### INV-API-013

Every major derived result records its producing configuration version.

### INV-API-014

API responses never expose private agent chain-of-thought.

### INV-API-015

Dashboard values originate from persisted experiment results.

---

# 63. Minimal API for First Prototype

The full API should not all be implemented on day one.

The minimum viable research API is:

```text
POST   /experiments
POST   /experiments/{id}/start
GET    /experiments/{id}/status

GET    /scenarios
POST   /candidate-pools

POST   /runs/{id}/selection/next

POST   /executions
GET    /executions/{id}

POST   /executions/{id}/invariants/evaluate
POST   /executions/{id}/failures/detect

POST   /failures/{id}/validate
POST   /failures/{id}/classify

POST   /failure-families/cluster

POST   /failures/{id}/reproduce

POST   /metamorphic/tests
POST   /metamorphic/tests/{id}/execute
POST   /metamorphic/tests/{id}/evaluate

POST   /experiments/{id}/holdout/run

POST   /runs/{id}/metrics/calculate
GET    /experiments/{id}/metrics/compare
```

Snapshots and branching can initially be implemented as internal services and exposed through API endpoints once the core evaluation loop is stable.

---

# 64. Recommended Implementation Order

## Phase 1: Core Contracts

Implement:

```text
Pydantic models
Python Protocol interfaces
Database repositories
Experiment service
Scenario service
Execution service
```

---

## Phase 2: Agent and Environment

Implement:

```text
AgentAdapter
EnvironmentInterface
ToolGateway
PolicyEngine
StateManager
```

---

## Phase 3: Evidence

Implement:

```text
TrajectoryCollector
Event schema
State persistence
InvariantEngine
FailureDetector
```

---

## Phase 4: Adaptive Evaluation

Implement:

```text
RandomSelector
UniformSelector
UCBVSelector
ProposedAdaptiveSelector
BudgetTracker
Selection logging
```

---

## Phase 5: Branching

Implement:

```text
SnapshotManager
BranchManager
Perturbation execution
Branch isolation tests
```

---

## Phase 6: Validation

Implement:

```text
FailureClassifier
FailureClusterer
ReproductionManager
MetamorphicEngine
```

---

## Phase 7: Research Evaluation

Implement:

```text
HoldoutEvaluator
MetricsEngine
Statistical analysis
Reporting API
Dashboard
```

---

# 65. Definition of Done

The API/interface implementation is considered complete when:

* [ ] All core domain models have typed schemas.
* [ ] REST API is versioned.
* [ ] Experiment lifecycle is controllable through API/CLI.
* [ ] Candidate selection is exposed through a stable interface.
* [ ] Random, Uniform, and UCB-V selectors implement the same selector contract.
* [ ] Proposed adaptive selector uses the same contract.
* [ ] Agent adapters implement a common interface.
* [ ] Environment implements reset, action, state, snapshot, and restore.
* [ ] All tool calls pass through the Tool Gateway.
* [ ] Policy decisions are recorded.
* [ ] Trajectory events are persisted.
* [ ] State snapshots are versioned and hashed.
* [ ] Branches are isolated.
* [ ] Invariant evaluations reference immutable evidence.
* [ ] Failure candidates can be validated.
* [ ] Classification and clustering are versioned.
* [ ] Reproduction creates independent executions.
* [ ] Metamorphic tests execute base and transformed cases.
* [ ] Holdout data is isolated from adaptive selection.
* [ ] Budget reservations occur before expensive operations.
* [ ] Actual costs are persisted.
* [ ] API errors use structured error codes.
* [ ] Idempotency is implemented for expensive create/start operations.
* [ ] Audit logging is implemented.
* [ ] Contract tests cover the complete execution-to-metric pipeline.
* [ ] Dashboard/reporting reads persisted data rather than fabricated values.
* [ ] Experiment results can be reconstructed from stored configuration and evidence.

---

# 66. Final Interface Architecture

The final interface structure is:

```text
                    RESEARCHER / CLI / DASHBOARD
                              |
                              v
                       +--------------+
                       | REST API v1  |
                       +------+-------+
                              |
                              v
                     +------------------+
                     | Service Layer    |
                     +--------+---------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
      Scenario            Selection          Execution
       Service             Service             Service
          |                   |                   |
          |                   |                   v
          |                   |             Agent Adapter
          |                   |                   |
          |                   |                   v
          |                   |            Controlled Env
          |                   |                   |
          |                   |        +----------+----------+
          |                   |        |          |          |
          |                   |        v          v          v
          |                   |      Tools      Policy      State
          |                   |                              |
          |                   |                              v
          |                   |                       Snapshot/Branch
          |                   |                              |
          +-------------------+------------------------------+
                                      |
                                      v
                               Trace / Evidence
                                      |
                                      v
                              Invariant Engine
                                      |
                                      v
                              Failure Detection
                                      |
                       +--------------+--------------+
                       |                             |
                       v                             v
                 Classification                  Validation
                       |                    +--------+--------+
                       v                    |                 |
                   Clustering          Reproduction      Metamorphic
                       |                    |                 |
                       +--------------------+-----------------+
                                            |
                                            v
                                      Hidden Holdout
                                            |
                                            v
                                         Metrics
                                            |
                                            v
                                    Reports / Dashboard
                                            |
                                            v
                                         Storage
```

The key architectural rule is:

> **Interfaces should expose evidence-producing operations, not merely final scores.**

The system therefore treats the API as a research infrastructure layer. A metric such as `cost_per_new_family` must be reconstructable from the chain:

```text
selection decision
        ↓
candidate
        ↓
execution
        ↓
trajectory
        ↓
invariant evaluation
        ↓
validated failure
        ↓
failure signature
        ↓
failure family
        ↓
cost records
        ↓
metric
```

That chain is what makes the evaluation experimentally defensible rather than just another dashboard with alarming red numbers.
