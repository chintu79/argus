# System Architecture Document

**Document ID:** SAD-003  
**Document Type:** System Architecture  
**Version:** 1.0  
**Status:** Baseline Architecture  
**Related Documents:**
- `01-project-specification.md`
- `02-research-questions-success-criteria.md`

---

# 1. Architecture Overview

## 1.1 System Name

**Budget-Constrained Adaptive Security Evaluation Platform**

---

## 1.2 Architecture Purpose

This document defines the technical architecture of the research prototype
for budget-constrained adaptive security and reliability evaluation of AI agents.

The architecture translates the research objectives into an executable software
system consisting of:

- scenario generation
- candidate management
- adaptive test selection
- agent execution
- controlled environment interaction
- trajectory recording
- intermediate-state analysis
- state snapshotting
- execution branching
- invariant evaluation
- failure detection
- failure classification
- failure clustering
- reproducibility testing
- metamorphic testing
- hidden-holdout evaluation
- metric computation
- experiment tracking
- result visualization

---

# 2. Architectural Principle

The system is designed around the following loop:

```text
Generate
   ↓
Select
   ↓
Execute
   ↓
Observe
   ↓
Analyze
   ↓
Branch
   ↓
Evaluate
   ↓
Validate
   ↓
Generalize
   ↓
Learn
   ↓
Select Again

The architecture therefore contains two major flows:

Control Flow

Determines:

What should the system execute next?

Data Flow

Determines:

What evidence was produced by previous executions?

These flows meet inside the adaptive selection subsystem.

3. High-Level Architecture
┌──────────────────────────────────────────────────────────────────────────────┐
│                         EXPERIMENT CONTROLLER                                │
│                                                                              │
│  Experiment Config │ Budget Manager │ Seed Manager │ Run Manager            │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         TEST GENERATION LAYER                                │
│                                                                              │
│  Seed Task Generator │ Scenario Generator │ Attack Generator                │
│  Perturbation Generator │ Candidate Repository                              │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                     ADAPTIVE SELECTION LAYER                                │
│                                                                              │
│  Candidate Scorer │ Exploration │ Exploitation │ Novelty │ Cost │ Diversity │
│  Variance / Uncertainty │ Budget Constraint │ Selection Policy              │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       AGENT EXECUTION LAYER                                  │
│                                                                              │
│  Agent Adapter │ LLM Interface │ Context/Memory │ Tool Client               │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      CONTROLLED ENVIRONMENT                                  │
│                                                                              │
│ Tool Gateway │ Policy Engine │ Database Simulator │ External Mocks           │
│ Fault Injector │ Environment State │ Resource Limits                        │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       TRAJECTORY COLLECTION                                  │
│                                                                              │
│ Event Logger │ State Recorder │ Tool Logger │ Cost Tracker │ Trace Builder  │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    STATE ANALYSIS & SNAPSHOTTING                             │
│                                                                              │
│ State Extractor │ Interesting-State Detector │ Serializer │ Snapshot Store   │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         BRANCHING ENGINE                                     │
│                                                                              │
│ Branch Manager │ Perturbation Engine │ Restore Engine │ Branch Executor      │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                     INVARIANT & FAILURE ENGINE                               │
│                                                                              │
│ Invariant Registry │ Evaluator │ Evidence Collector │ Failure Detector       │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE ANALYSIS LAYER                                    │
│                                                                              │
│ Signature Generator │ Classifier │ Similarity Engine │ Clustering Engine     │
│ Failure Family Repository                                                    │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                ┌───────────────┼──────────────────┐
                │               │                  │
                ▼               ▼                  ▼
┌──────────────────────┐ ┌──────────────────┐ ┌──────────────────────────────┐
│ REPRODUCIBILITY     │ │ METAMORPHIC      │ │ HIDDEN HOLDOUT              │
│ VALIDATION           │ │ TESTING          │ │ EVALUATION                  │
│                      │ │                  │ │                              │
│ Replay Engine        │ │ Transformations  │ │ Holdout Generator            │
│ Multi-run Analysis   │ │ Base/Variant     │ │ Unseen Scenarios             │
└──────────┬───────────┘ └────────┬─────────┘ └──────────────┬───────────────┘
           │                      │                          │
           └──────────────────────┼──────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          METRICS ENGINE                                      │
│                                                                              │
│ Discovery │ Efficiency │ Reproducibility │ Generalization │ Reliability      │
│ Cost │ Statistical Analysis                                               │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         RESULTS & REPORTING                                  │
│                                                                              │
│ Experiment Database │ Result Files │ Dashboard │ Research Reports            │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                │ Feedback
                                ▼
                     ┌────────────────────────┐
                     │ ADAPTIVE SELECTOR      │
                     │ Updated Evidence       │
                     └────────────────────────┘
4. Architectural Layers

The system is divided into the following layers.

Layer	Responsibility
Experiment Control	Controls experiment lifecycle and configuration
Test Generation	Produces candidate scenarios
Adaptive Selection	Chooses the next evaluation
Agent Execution	Executes the evaluated AI agent
Environment	Provides controlled tools and state
Trajectory Collection	Records execution evidence
State Management	Identifies, stores, and restores states
Branching	Creates alternative continuations
Evaluation	Checks invariants and detects failures
Failure Analysis	Classifies and groups failures
Validation	Replays and transforms failures
Holdout	Tests generalization
Metrics	Computes experimental measurements
Storage	Persists research data
Reporting	Presents experimental results
5. Component Architecture
5.1 Experiment Controller
Responsibility

The Experiment Controller is the top-level orchestration component.

It creates and manages an experiment from configuration through completion.

Responsibilities
load experiment configuration
validate configuration
initialize random seeds
initialize storage
initialize agent
initialize environment
initialize budget manager
initialize candidate generator
initialize adaptive selector
execute evaluation loop
terminate when budget is exhausted
trigger final validation
trigger metric calculation
generate experiment summary
Input
ExperimentConfig
Output
ExperimentResult
5.2 Budget Manager
Responsibility

Track and enforce the evaluation budget.

Budget Types

The initial implementation should support:

maximum tokens
maximum executions
maximum branches
maximum replay attempts
optional wall-clock time
State
BudgetState
├── total_budget
├── consumed_budget
├── remaining_budget
├── token_usage
├── execution_count
├── branch_count
└── replay_count
Interface
can_execute(cost_estimate) -> bool

reserve(cost_estimate) -> Reservation

commit(reservation, actual_cost) -> None

remaining() -> BudgetState
Requirement

Budget accounting must use actual observed costs where available.

5.3 Seed Manager
Responsibility

Provide reproducible random seeds.

Responsibilities
initialize experiment seed
derive run-specific seeds
derive branch-specific seeds
record seed lineage
Example
Experiment Seed
      ↓
Run Seed
      ↓
Branch Seed
5.4 Test Generation Layer

The test generation layer creates candidate evaluation scenarios.

It contains:

Seed Task Generator
Scenario Generator
Attack Generator
Perturbation Generator
Candidate Builder
Candidate Repository
5.5 Seed Task Generator
Responsibility

Generate or load initial task definitions.

Output
Task
├── task_id
├── description
├── category
├── expected_behavior
├── constraints
└── invariants
5.6 Scenario Generator
Responsibility

Transform seed tasks into concrete evaluation scenarios.

Scenario types include:

security scenarios
reliability scenarios
robustness scenarios
adversarial scenarios
recovery scenarios
5.7 Attack Generator
Responsibility

Generate controlled adversarial conditions.

Examples:

unauthorized request
privilege escalation attempt
malicious tool response
conflicting instruction
sensitive-data request
unexpected environment state

The attack generator must produce structured attacks rather than arbitrary
untracked strings.

5.8 Perturbation Generator
Responsibility

Generate transformations for:

branching
metamorphic testing
robustness testing

Examples:

Wording Perturbation
Tool Response Perturbation
Context Perturbation
Environment Perturbation
State Perturbation
Tool Ordering Perturbation
5.9 Candidate Repository

Stores all candidate tests.

Each candidate contains:

candidate_id
task_id
scenario_type
attack_type
environment_config
perturbation
expected_behavior
invariants
estimated_cost
selection_statistics
6. Adaptive Selection Layer

The adaptive selector determines which candidate should be evaluated next.

6.1 Candidate Scorer

The scorer calculates a candidate acquisition score.

Conceptual model:

Score =
Yield
+
Exploration
+
Novelty
+
Severity
+
Uncertainty
-
Cost

The exact algorithm is defined separately in:

08-adaptive-test-selection-specification.md

6.2 Exploration Component

Promotes candidates that have not been sufficiently evaluated.

Possible inputs:

selection count
candidate uncertainty
candidate coverage
family coverage
6.3 Exploitation Component

Promotes candidates associated with evidence of failure.

Possible signals:

historical failure yield
failure severity
recent failure frequency
6.4 Novelty Component

Estimates whether a candidate provides information different from previously
evaluated scenarios.

Potential features:

scenario embedding
attack category
tool combination
environment state
failure-family distance
6.5 Cost Component

Estimates the expected cost of evaluating a candidate.

The selector should consider:

Estimated Token Cost
Estimated Execution Cost
Estimated Branch Cost
Estimated Analysis Cost
6.6 Selection Policy

The selection policy combines the scoring components and selects the next
candidate subject to the budget.

Output:

SelectionDecision
├── candidate_id
├── score
├── estimated_cost
├── selection_reason
└── budget_remaining
7. Agent Execution Layer

The agent execution layer provides a model-independent interface for the
agent being evaluated.

7.1 Agent Adapter

The Agent Adapter isolates the evaluation framework from a specific
agent implementation.

Interface:

initialize(config)

start(task, environment)

step(observation)

execute_tool(tool_call)

terminate()

get_state()

The implementation should allow different agents/models to be evaluated
without rewriting the evaluation engine.

7.2 LLM Interface

Responsible for communication with the configured model.

It records:

model name
model version
request
response metadata
token usage
latency
errors

The system should avoid storing private chain-of-thought.

7.3 Context / Memory Manager

Maintains the context required by the evaluated agent.

Potential state includes:

conversation history
task state
tool observations
allowed context
persistent memory where applicable
7.4 Tool Client

Provides the agent with the available tool interface.

All tool calls must pass through the Tool Gateway.

8. Controlled Environment

The controlled environment is a core security boundary.

It prevents uncontrolled agent actions from reaching arbitrary external
systems during experiments.

8.1 Tool Gateway

Every tool call passes through the Tool Gateway.

Agent
  ↓
Tool Gateway
  ↓
Policy Engine
  ↓
Tool

The gateway records:

agent identity
tool
arguments
requested capability
policy decision
result
latency
8.2 Policy Engine

Determines whether an action is authorized.

Input:

agent_identity
requested_tool
requested_operation
requested_resource

Output:

ALLOW
DENY
REQUIRE_CONFIRMATION
8.3 Capability Registry

Defines the capabilities associated with each agent.

Example:

{
  "agent_role": "support_agent",
  "capabilities": [
    "customer.read",
    "customer.search"
  ]
}
8.4 Tool Registry

Defines:

tool name
input schema
output schema
required capability
resource scope
side-effect level
8.5 Database Simulator

Provides controlled data resources.

Examples:

customer database
HR database
product database
transaction database

Sensitive values should be synthetic.

8.6 External Service Mock

Simulates external systems such as:

email
payment
messaging
ticketing
file storage

The mock prevents uncontrolled real-world side effects.

8.7 Fault Injector

Introduces controlled faults.

Examples:

malformed response
timeout
missing field
permission error
stale information
conflicting information
delayed response
8.8 Environment State Manager

Maintains the environment's mutable state.

It must support:

get_state()
serialize_state()
restore_state()
apply_transition()
9. Trajectory Collection Layer

The trajectory layer records all observable execution events.

9.1 Event Logger

Records events such as:

task start
model request
model response metadata
tool call
tool response
policy decision
environment transition
invariant evaluation
error
termination
9.2 State Recorder

Records references to environment and execution state.

9.3 Tool Logger

Records:

tool_name
arguments
request_time
response
policy_decision
execution_time
9.4 Cost Tracker

Tracks:

input tokens
output tokens
total tokens
execution time
tool execution time
snapshot size
snapshot time
restore time
9.5 Trace Builder

Combines individual events into a trajectory.

Trace
├── run_id
├── task_id
├── events[]
├── states[]
├── tool_calls[]
├── cost
└── outcome
10. State Analysis Layer

The state-analysis layer identifies states that may be useful for further
evaluation.

10.1 State Extractor

Extracts a normalized representation of the current execution state.

Potential fields:

task_progress
current_action
selected_tool
tool_arguments
authorization_state
environment_state
context_reference
recovery_state
10.2 Interesting-State Detector

Determines whether a state is worth snapshotting or branching.

Potential signals:

security boundary crossed
sensitive tool selected
unusual action
high uncertainty
policy conflict
invariant proximity
novel state
recovery decision
suspicious behavior

The detector should be configurable.

10.3 State Normalizer

Converts state into a consistent representation for:

comparison
hashing
similarity analysis
snapshotting
clustering
11. Snapshot Manager

The Snapshot Manager creates and restores supported execution states.

11.1 Snapshot Serializer

Converts state into persistent representation.

11.2 Snapshot Store

Stores:

snapshot_id
source_run_id
source_state_id
serialized_state
configuration_hash
creation_timestamp
11.3 Snapshot Validator

Before a snapshot can be used, verify:

required state exists
serialization succeeded
integrity hash matches
configuration is compatible
11.4 Restore Engine

Restores a snapshot into a clean branch execution environment.

The restored environment must not modify the original parent execution.

11.5 Snapshot Isolation

Each restored branch receives isolated mutable state.

Snapshot S
   │
   ├── Branch A → Environment A
   ├── Branch B → Environment B
   └── Branch C → Environment C

Changes in one branch must not affect another branch.

12. Branching Engine

The Branching Engine creates alternative executions.

12.1 Branch Manager

Creates and tracks branch lineage.

Experiment
    ↓
Run
    ↓
State
    ↓
Snapshot
    ↓
Branch
12.2 Perturbation Engine

Applies a defined perturbation to a restored state.

Example:

Snapshot
   ↓
Change Tool Response
   ↓
Execute
12.3 Branch Executor

Runs the agent from the restored state.

It must create a new run ID.

12.4 Branch Lineage

Every branch stores:

branch_id
parent_run_id
parent_state_id
parent_snapshot_id
perturbation_id
branch_seed
13. Invariant Evaluation Layer

The invariant engine evaluates expected behavior.

13.1 Invariant Registry

Stores invariant definitions.

Example:

AUTH-001

Condition:
Requested capability must belong to the agent's authorized capability set.
13.2 Invariant Evaluator

Receives:

trajectory
current_state
environment_state
policy_events

and returns:

PASS
FAIL
NOT_APPLICABLE
UNKNOWN
13.3 Evidence Collector

Stores the evidence supporting a failed invariant.

Example:

Agent:
support_agent

Requested:
customer.delete

Authorized:
customer.read

Observed:
customer.delete

Result:
VIOLATION
14. Failure Detection Layer

The Failure Detector converts invariant violations into structured failure
records.

14.1 Failure Detector

Input:

InvariantResult
Trajectory
State
Environment

Output:

FailureRecord
14.2 Failure Record
failure_id
run_id
step
invariant_id
category
severity
evidence
state_id
signature
14.3 Failure Severity

Severity should be determined using an explicit configurable policy.

Possible dimensions:

data sensitivity
privilege level
external side effect
reversibility
impact
authorization violation

Severity must not be manually invented after seeing the results.

15. Failure Analysis Layer
15.1 Failure Signature Generator

Creates normalized representations of failures.

Example:

Invariant:
AUTH-001

Tool:
database.read

Violation:
unauthorized_data_access

Resource:
customer_records

Agent Role:
support_agent
15.2 Failure Classifier

Assigns categories such as:

Security
Reliability
Robustness
Recovery
Tool Misuse
Authorization
Data Exposure
15.3 Similarity Engine

Compares failure signatures.

Potential approaches:

structured feature similarity
embedding similarity
hybrid similarity
15.4 Clustering Engine

Groups related failures.

Possible algorithms:

hierarchical clustering
DBSCAN
HDBSCAN
graph-based clustering

The selected algorithm should be specified in the implementation methodology.

15.5 Failure Family Store

Stores:

family_id
member_failure_ids
representative_signature
category
severity
reproducibility
holdout_results
16. Reproducibility Validation

The Reproducibility Engine determines whether a failure can be reproduced.

16.1 Replay Manager

Receives:

failure_id
replay_count

and executes independent replay attempts.

16.2 Replay Isolation

Each replay should begin from the defined initial state or explicitly
defined replay state.

Replay runs must not modify the original failure record.

16.3 Reproduction Analyzer

Calculates:

Successful Reproductions
/
Replay Attempts
16.4 Stability Classifier

Possible output:

STABLE
PROBABILISTIC
FLAKY
NON_REPRODUCIBLE
17. Metamorphic Testing Engine

The Metamorphic Testing Engine evaluates scenario transformations.

17.1 Transformation Registry

Stores transformations.

Examples:

WORDING_VARIATION
IRRELEVANT_CONTEXT
TASK_REFORMULATION
TOOL_ORDER_CHANGE
ENVIRONMENT_VARIATION
STATE_PERTURBATION
17.2 Base Execution

The original scenario is executed and recorded.

17.3 Transformed Execution

A transformation is applied and the resulting scenario is executed.

17.4 Comparison Engine

Compares:

invariant results
agent actions
tool usage
task outcome
failure status
18. Hidden Holdout Engine

The Hidden Holdout Engine evaluates whether discovered failures generalize.

18.1 Holdout Generator

Generates or selects scenarios that are excluded from discovery.

18.2 Holdout Isolation

Holdout results must not influence:

adaptive scoring
candidate generation
clustering
failure-family construction

until the holdout evaluation is complete.

18.3 Failure-Family Matcher

Determines whether a holdout failure matches an existing failure family.

18.4 Generalization Analyzer

Calculates:

holdout detection rate
family transfer rate
false positives
false negatives
19. Metrics Engine

The Metrics Engine calculates research metrics from stored experimental data.

19.1 Discovery Metrics
candidate count
execution count
detected failures
validated failures
failure families
19.2 Efficiency Metrics
failures per execution
failures per 1K tokens
families per unit cost
19.3 Reproducibility Metrics
replay attempts
successful reproductions
reproduction rate
19.4 Generalization Metrics
holdout scenarios
detected holdout failures
holdout detection rate
family transfer rate
19.5 Cost Metrics
token cost
execution cost
snapshot cost
restore cost
branch cost
analysis cost
verification cost
19.6 Reliability Metrics
task success
unsafe action rate
recovery success
mean recovery steps
20. Experiment Storage Architecture

The research prototype should use a simple persistent storage architecture.

                    ┌─────────────────────┐
                    │ Experiment Metadata │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ↓                ↓                ↓
       ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
       │ SQLite      │  │ JSONL Traces│  │ Snapshots    │
       │ Metadata    │  │             │  │              │
       └─────────────┘  └─────────────┘  └──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ↓
                       Metrics / Analysis
21. Data Ownership

Each component owns a defined category of data.

Component	Primary Data
Experiment Controller	experiment metadata
Candidate Generator	candidate scenarios
Selector	selection statistics
Executor	run metadata
Trace Collector	trajectories
Snapshot Manager	snapshots
Branch Manager	branch lineage
Invariant Engine	invariant results
Failure Engine	failure records
Clustering Engine	failure families
Replay Engine	replay results
Holdout Engine	holdout results
Metrics Engine	derived metrics
22. End-to-End Execution Flow
Step 1: Experiment Initialization
Load Configuration
       ↓
Validate Configuration
       ↓
Initialize Seed
       ↓
Initialize Storage
       ↓
Initialize Budget
Step 2: Candidate Generation
Seed Tasks
    ↓
Scenario Generator
    ↓
Attack / Perturbation Generator
    ↓
Candidate Repository
Step 3: Candidate Selection
Candidate Pool
    ↓
Calculate Scores
    ↓
Apply Budget Constraint
    ↓
Select Candidate
Step 4: Agent Execution
Candidate
    ↓
Agent
    ↓
Tool Gateway
    ↓
Policy Engine
    ↓
Environment
Step 5: Trace Collection

Every observable event is recorded.

Action
Observation
Tool Call
Policy Decision
State
Cost
Latency
Step 6: State Analysis

The system evaluates whether intermediate states are interesting enough
to investigate.

Step 7: Snapshot

If selected:

State
 ↓
Serialize
 ↓
Validate
 ↓
Store Snapshot
Step 8: Branching
Snapshot
   ├── Perturbation A → Branch A
   ├── Perturbation B → Branch B
   └── Perturbation C → Branch C
Step 9: Invariant Evaluation

Every relevant execution is checked against applicable invariants.

Step 10: Failure Creation

When an invariant is violated:

Violation
   ↓
Evidence
   ↓
Failure Record
Step 11: Failure Analysis
Failure
   ↓
Signature
   ↓
Classification
   ↓
Similarity
   ↓
Failure Family
Step 12: Validation

Selected failures are replayed.

Step 13: Metamorphic Evaluation

Selected failures and scenarios are transformed and re-executed.

Step 14: Holdout Evaluation

Validated failure families are evaluated against unseen scenarios.

Step 15: Metrics

The metrics engine calculates experimental results.

Step 16: Feedback

Selection statistics are updated.

New Evidence
     ↓
Candidate Statistics
     ↓
Adaptive Selector
     ↓
Next Evaluation
23. Main Control Loop

The core controller follows this conceptual algorithm:

initialize_experiment()

while budget_manager.has_remaining_budget():

    candidates = candidate_repository.get_available()

    selection = adaptive_selector.select(
        candidates=candidates,
        budget=budget_manager.state(),
        evidence=evidence_store
    )

    if not budget_manager.can_execute(selection.estimated_cost):
        break

    run = executor.execute(selection.candidate)

    trace = trace_collector.collect(run)

    states = state_analyzer.analyze(trace)

    for state in states:

        if interesting_state_detector.is_interesting(state):

            snapshot = snapshot_manager.create(state)

            branches = branch_manager.generate(snapshot)

            for branch in branches:
                branch_executor.execute(branch)

    invariant_results = invariant_engine.evaluate(trace)

    failures = failure_detector.detect(
        trace,
        invariant_results
    )

    failure_analyzer.process(failures)

    budget_manager.commit_actual_cost(run.cost)

    adaptive_selector.update(
        trace=trace,
        failures=failures
    )

run_validation()

run_holdout_evaluation()

calculate_metrics()

generate_results()

The actual implementation may use asynchronous execution, queues, or
parallel workers later, but the logical behavior must remain equivalent.

24. Asynchronous Execution

The architecture should allow future parallel execution.

Potential workers:

Worker Pool
├── Agent Execution Worker
├── Branch Worker
├── Replay Worker
├── Metamorphic Worker
└── Holdout Worker

However, adaptive selection decisions must remain synchronized with the
evidence available at the time of selection.

Parallel execution must not accidentally allow future information to
influence earlier selection decisions.

25. Security Architecture

The security architecture uses explicit boundaries.

┌─────────────────────────────────────────────┐
│ Evaluation Controller                       │
│                                             │
│ Trusted orchestration                      │
└──────────────────────┬──────────────────────┘
                       │
                       │ controlled interface
                       ▼
┌─────────────────────────────────────────────┐
│ AI Agent                                    │
│                                             │
│ Potentially unsafe behavior                 │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ Tool Gateway + Policy Engine                │
│                                             │
│ Security enforcement boundary               │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ Controlled Environment                      │
│                                             │
│ Synthetic data / simulated services         │
└─────────────────────────────────────────────┘
26. Agent Isolation

The evaluated agent must not have unrestricted access to:

host filesystem
host network
production databases
production credentials
arbitrary external services

unless explicitly required and safely isolated for a specific experiment.

27. Snapshot Security

Snapshots may contain:

environment state
synthetic data
context
authorization information
tool state

Snapshots must therefore:

remain isolated
have controlled access
be integrity checked
be associated with experiment IDs
not leak between experiments
28. Experiment Isolation

Each experiment should have:

experiment_id
experiment_directory
experiment_database
experiment_trace_namespace
experiment_snapshot_namespace

No experiment should silently consume another experiment's data.

29. Failure Data Flow
Agent Action
      ↓
Tool Gateway
      ↓
Policy Decision
      ↓
Environment Transition
      ↓
Trajectory Event
      ↓
Invariant Evaluation
      ↓
Violation?
   /       \
 NO         YES
 |           |
Continue     Evidence
             ↓
          Failure
             ↓
          Signature
             ↓
          Family
             ↓
          Replay
             ↓
          Holdout
30. Adaptive Feedback Architecture

The adaptive selector receives evidence from previous executions.

                 ┌─────────────────────────┐
                 │ Candidate Pool           │
                 └────────────┬────────────┘
                              ↓
                    Adaptive Selection
                              ↓
                         Execution
                              ↓
                         Trajectory
                              ↓
                   Failure / Outcome Data
                              ↓
                    Evidence Repository
                              ↓
                  Candidate Statistics
                              │
                              └──────────────→
                                Selector

Evidence may include:

success/failure
failure category
severity
novelty
uncertainty
execution cost
family coverage
branch yield
31. State and Branch Lineage

The architecture must maintain complete lineage.

Experiment
    │
    └── Run R1
          │
          ├── State S1
          │
          ├── State S2
          │      │
          │      └── Snapshot SS2
          │              │
          │              ├── Branch B1
          │              │      └── Run R2
          │              │
          │              ├── Branch B2
          │              │      └── Run R3
          │              │
          │              └── Branch B3
          │                     └── Run R4
          │
          └── State S3

This lineage is essential for:

debugging
reproducibility
cost analysis
failure attribution
research reporting
32. Configuration Architecture

The system should use version-controlled configuration.

Example:

experiment:
  id: exp_001
  seed: 42

agent:
  model: example-model
  temperature: 0
  prompt_version: prompt_v1

environment:
  version: env_v1

selection:
  strategy: adaptive
  novelty_weight: 0.2
  exploration_weight: 0.3
  severity_weight: 0.2
  cost_weight: 0.3

branching:
  enabled: true
  max_branches_per_snapshot: 3

validation:
  replay_count: 5
  metamorphic_testing: true
  holdout_testing: true

budget:
  max_tokens: 100000
  max_executions: 500
  max_branches: 1000

Actual configuration fields will be finalized in the experiment configuration
document.

33. Recommended Repository Architecture
project/
│
├── README.md
├── pyproject.toml
│
├── docs/
│   ├── 01-project-specification.md
│   ├── 02-research-questions-success-criteria.md
│   ├── 03-system-architecture.md
│   └── ...
│
├── src/
│   └── agent_eval/
│       │
│       ├── config/
│       ├── agents/
│       ├── environments/
│       ├── tools/
│       ├── scenarios/
│       ├── selection/
│       ├── execution/
│       ├── trajectories/
│       ├── states/
│       ├── snapshots/
│       ├── branching/
│       ├── invariants/
│       ├── failures/
│       ├── clustering/
│       ├── validation/
│       ├── metamorphic/
│       ├── holdout/
│       ├── metrics/
│       ├── experiments/
│       └── reporting/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── system/
│   └── fixtures/
│
├── configs/
│   ├── baseline/
│   ├── adaptive/
│   └── experiments/
│
├── data/
│   ├── scenarios/
│   ├── traces/
│   ├── snapshots/
│   └── results/
│
├── experiments/
│
└── dashboard/
34. Module Dependency Direction

The architecture should avoid circular dependencies.

Preferred dependency direction:

Configuration
      ↓
Domain Models
      ↓
Core Interfaces
      ↓
Implementations
      ↓
Orchestration
      ↓
Reporting

For example:

Domain Models
     ↑
     │
Agent Adapter
Environment
Trace Collector
Snapshot Manager
Invariant Engine

The individual modules should communicate through defined interfaces rather
than directly depending on implementation details.

35. Core Domain Objects

The system should use explicit domain models.

Required objects include:

Experiment
ExperimentConfig
Budget
Task
Scenario
CandidateTest
SelectionDecision
Agent
Environment
Tool
Policy
Run
Trajectory
Event
State
Snapshot
Branch
Invariant
InvariantResult
Failure
FailureSignature
FailureFamily
ReplayResult
MetamorphicTest
HoldoutCase
MetricResult
ExperimentResult

These objects should be defined centrally so that different modules do not
invent incompatible representations of the same concept.

36. Interface Contracts

Major components should communicate through interfaces.

Example:

class AgentExecutor:
    def execute(
        self,
        task: Task,
        environment: Environment
    ) -> Run:
        ...
class CandidateSelector:
    def select(
        self,
        candidates: list[CandidateTest],
        budget: BudgetState,
        evidence: EvidenceStore
    ) -> SelectionDecision:
        ...
class SnapshotManager:
    def create(
        self,
        state: State
    ) -> Snapshot:
        ...

    def restore(
        self,
        snapshot: Snapshot
    ) -> Environment:
        ...
class InvariantEvaluator:
    def evaluate(
        self,
        trajectory: Trajectory
    ) -> list[InvariantResult]:
        ...

Interfaces should be stable even when internal implementations change.

37. Failure Containment

A failure in one execution must not terminate the entire experiment.

Examples:

Agent Error
Tool Error
Environment Error
Snapshot Error
Branch Error
Model API Error

should produce structured error records.

The Experiment Controller should determine whether the failure is:

retryable
recoverable
isolated to one run
fatal to the experiment
38. Logging Architecture

Three logging levels should be supported.

System Logs

Operational events.

Examples:

service startup
configuration loading
worker status
Experiment Logs

Research execution events.

Examples:

candidate selected
run started
run completed
branch created
failure detected
Trace Logs

Detailed agent/environment events.

Examples:

tool call
observation
policy decision
state transition

Research traces must be stored separately from ordinary application logs.

39. Error Handling

Each module should return structured errors where possible.

Example:

Error
├── error_id
├── component
├── run_id
├── severity
├── type
├── message
├── recoverable
└── timestamp

The system should never silently discard an execution because an error occurred.

40. Observability

The system should expose:

experiment progress
budget usage
execution count
branch count
failure count
queue state
errors
current candidate
selector statistics

This is required for debugging long-running experiments.

41. Performance Considerations

The architecture should initially prioritize:

correctness
reproducibility
observability
experimental validity

before optimization.

Premature optimization of the research prototype should not obscure
whether the algorithm actually works.

Potential later optimizations include:

parallel branch execution
cached state representations
vectorized similarity calculations
asynchronous model calls
compressed traces
object storage
distributed workers
42. Scalability Path
Prototype
Single Process
+
SQLite
+
JSONL
+
Local Docker Environment
Intermediate
FastAPI
+
Worker Queue
+
PostgreSQL
+
Object Storage
Large-Scale Research
Experiment Controller
        ↓
Worker Scheduler
        ↓
Execution Worker Pool
        ↓
Distributed Environments
        ↓
Central Experiment Store

The project should not implement the large-scale architecture until the
single-machine research prototype is validated.

43. Dashboard Architecture

The dashboard is a separate presentation layer.

Experiment Data
      ↓
Metrics Engine
      ↓
Result API
      ↓
Dashboard

The dashboard must not independently calculate research metrics using
hard-coded values.

44. Dashboard Views

The dashboard should eventually provide:

Overview
experiment status
budget
execution count
failures
families
Adaptive Selection
candidate scores
selected candidates
exploration/exploitation
budget allocation
Trajectories
execution timeline
tool calls
state transitions
Branches
snapshot lineage
branch tree
branch outcomes
Failures
invariant violations
evidence
severity
failure families
Reproducibility
replay attempts
reproduction rate
stability classes
Metamorphic Testing
transformation
base outcome
transformed outcome
invariant comparison
Holdout
holdout cases
family matches
generalization metrics
Experimental Comparison
baseline metrics
proposed method metrics
ablation results
45. Architecture Invariants

The following architectural properties must always hold.

AI Agent Cannot Bypass Tool Gateway

All controlled tool operations pass through the gateway.

Branches Are Isolated

A branch cannot modify its parent execution.

Holdout Data Is Isolated

Holdout results cannot influence discovery before evaluation.

Budget Is Centralized

Individual modules cannot independently exceed the experiment budget.

Results Are Data-Driven

Metrics are computed from stored experiment data.

Every Branch Has Lineage

Every branch must reference its parent snapshot.

Every Failure Has Evidence

A failure cannot exist without recorded evidence.

Every Experiment Has Configuration

An experiment cannot be considered valid without configuration metadata.

46. Architecture Decision Summary
Decision	Choice
Architecture style	Modular layered architecture
Primary implementation	Python
Agent interface	Model-agnostic adapter
Environment	Controlled/simulated
Tool access	Tool Gateway
Security enforcement	Policy Engine
Trace storage	JSONL + SQLite initially
Snapshot storage	Serialized state
Branching	State-based
Adaptive selection	Pluggable acquisition strategy
Invariant evaluation	Executable rules
Failure grouping	Signature + clustering
Replay	Independent execution
Metamorphic testing	Transformation-based
Generalization	Hidden holdout
Experiment tracking	Versioned configuration + metadata
Dashboard	Presentation layer over experiment data
47. Architecture Boundaries

The following distinctions must remain explicit.

State Snapshot ≠ LLM KV Cache

The initial architecture snapshots supported environment/execution state.

KV-cache restoration is not assumed.

Candidate ≠ Failure

A candidate is something the system intends to evaluate.

A failure is an evidence-backed invariant violation.

Failure ≠ Failure Family

A failure is an individual occurrence.

A failure family represents a group of related failures.

Discovery ≠ Validation

Discovery identifies candidate failures.

Validation determines whether they reproduce and generalize.

Dashboard ≠ Evaluation Engine

The dashboard visualizes experiment data.

It does not define experimental truth.

48. Final Architecture

The complete system can be summarized as:

                         ┌──────────────────────┐
                         │ Experiment Controller│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Candidate Generator  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Adaptive Selector    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────┐
                 │        Agent Execution            │
                 │                                  │
                 │  Agent → Tool Gateway → Policy   │
                 │                    ↓              │
                 │              Environment         │
                 └────────────────┬─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────────┐
                         │ Trajectory Collector│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ State Analyzer       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Snapshot Manager     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Branch Manager       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                  ┌──────────────┐      ┌──────────────┐
                  │ Branch A     │      │ Branch B     │
                  └──────┬───────┘      └──────┬───────┘
                         │                     │
                         └──────────┬──────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Invariant Engine     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Failure Detector     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Failure Analyzer     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Failure Families     │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │ Replay       │    │ Metamorphic  │    │ Hidden       │
        │ Validation   │    │ Testing      │    │ Holdout      │
        └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
               │                   │                   │
               └───────────────────┼───────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │ Metrics Engine       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         ▼                      ▼
                ┌────────────────┐      ┌─────────────────┐
                │ Experiment DB  │      │ Dashboard /     │
                │ + Result Store │      │ Research Report │
                └────────────────┘      └─────────────────┘
49. Architectural Objective

The architecture exists to enable the following experimentally measurable loop:

Discover
   ↓
Capture
   ↓
Branch
   ↓
Evaluate
   ↓
Validate
   ↓
Generalize
   ↓
Measure Cost
   ↓
Update Selection
   ↓
Discover Again

The architecture is considered valid only when each stage can produce
traceable, reproducible evidence for the next stage.

The system should therefore be built as a research evaluation engine first
and a visual dashboard second.

The dashboard is useful for seeing the machinery.

The machinery is what makes the research defensible.