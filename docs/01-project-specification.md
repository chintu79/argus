# Project Specification

## Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** PS-001  
**Document Type:** Project Specification  
**Version:** 1.0  
**Status:** Baseline Specification  
**Project Type:** Research Prototype  
**Domain:** Agentic AI, Generative AI, Cybersecurity, AI Safety, AI Evaluation  
**Primary Language:** Python  
**Primary Development Approach:** Modular research prototype with experiment-driven validation  

---

# 1. Executive Definition

## 1.1 Project Title

**Budget-Constrained Adaptive Security Evaluation of AI Agents**

---

## 1.2 Short Description

This project develops a research prototype for evaluating the security, reliability, robustness, and failure behavior of autonomous AI agents under a constrained evaluation budget.

The proposed system does not treat agent evaluation as a collection of independent full-task executions. Instead, it records agent execution trajectories, identifies potentially informative intermediate states, captures reusable execution states, and generates targeted alternative continuations from those states.

An adaptive test-selection mechanism determines which candidate scenarios or branches should be executed next based on experimentally measurable evidence such as historical failure yield, exploration requirements, novelty, severity, uncertainty, execution cost, and remaining evaluation budget.

Detected failures are not immediately treated as validated vulnerabilities. The system performs additional validation through independent replay, metamorphic testing, failure-family analysis, and evaluation against previously unseen holdout scenarios.

The final system therefore evaluates not only:

> "Did the agent fail?"

but also:

> "Can the failure be reproduced?"

> "What type of failure is it?"

> "Does it represent a distinct failure family?"

> "Does the failure generalize beyond the scenario in which it was discovered?"

> "How much evaluation budget was required to discover and validate it?"

---

# 2. Project Context

Autonomous AI agents increasingly combine large language models with tools, memory, external services, databases, APIs, and multi-step decision-making.

Unlike conventional language-model evaluation, agent evaluation involves sequential interaction with an environment.

A single agent task may involve:

```text
Task
  ↓
Planning / Decision
  ↓
Tool Selection
  ↓
Tool Invocation
  ↓
Observation
  ↓
State Update
  ↓
Next Decision
  ↓
Additional Tool Invocation
  ↓
...
  ↓
Final Outcome

A security or reliability failure may therefore occur at an intermediate point in the trajectory rather than only at the final output.

For example, an agent may:

receive a legitimate task,
select a permitted tool,
reach an intermediate state,
receive manipulated or unexpected information,
select an unauthorized operation,
violate an authorization invariant.

If evaluation always restarts the entire task from the beginning for every variation, many execution steps may be repeated unnecessarily.

This project investigates whether intermediate execution states can be used as starting points for targeted exploration.

3. Problem Statement
3.1 Primary Problem

AI-agent evaluation can become expensive and inefficient when large numbers of complete scenarios must be executed independently to discover relatively sparse security or reliability failures.

Independent execution can repeatedly traverse the same prefixes of agent trajectories.

At the same time, simple random testing may spend substantial evaluation budget on scenarios that provide little new information.

The project therefore addresses the following problem:

How can a limited evaluation budget be allocated adaptively to discover, validate, and generalize AI-agent security and reliability failures while reducing redundant execution?

3.2 Specific Problems Addressed

The system addresses five related problems.

Problem A: Evaluation Budget Inefficiency

A fixed computational or token budget limits the number of scenarios that can be evaluated.

The system must therefore prioritize evaluations that are expected to provide useful evidence.

Problem B: Redundant Prefix Execution

Multiple related scenarios may share substantial execution prefixes.

Executing every scenario independently can repeat those prefixes.

The proposed system investigates state-based branching as a mechanism for reusing suitable intermediate execution states.

Problem C: Failure Discovery Without Validation

A single observed abnormal behavior does not necessarily constitute a reliable security finding.

The system therefore separates:

Observed Failure
      ↓
Candidate Failure
      ↓
Independent Replay
      ↓
Validated Failure
Problem D: Failure Duplication

Different scenarios may expose the same underlying failure mechanism.

The system therefore creates failure signatures and groups similar failures into failure families.

Problem E: Unknown Generalization

A failure discovered on one scenario may be highly specific to that scenario.

The system therefore evaluates discovered failure families against unseen holdout scenarios.

4. Research Objective
4.1 Primary Objective

To design, implement, and experimentally evaluate a budget-constrained adaptive framework for discovering, validating, and generalizing security and reliability failures in autonomous AI agents using trajectory-aware state branching and adaptive test selection.

4.2 Secondary Objectives

The project aims to:

Construct a controlled environment for reproducible AI-agent evaluation.
Generate diverse security and reliability test scenarios.
Collect structured agent execution trajectories.
Identify informative intermediate execution states.
Capture reusable environment/execution snapshots.
Generate alternative branches from captured states.
Select evaluations adaptively under a fixed budget.
Detect security and reliability failures using executable invariants.
Group related failures into failure families.
Measure failure reproducibility.
Perform metamorphic testing of discovered behaviors.
Evaluate failure families on hidden holdout scenarios.
Measure generalization to unseen scenarios.
Compare the proposed approach against non-adaptive and non-branching baselines.
Quantify the computational cost and overhead of the proposed mechanisms.
5. Core Research Idea

The system combines three primary mechanisms.

5.1 Mechanism 1: Budget-Constrained Adaptive Evaluation

The system maintains a pool of candidate tests.

Instead of selecting candidates randomly, it calculates an acquisition value using measurable information such as:

previous failure yield
exploration requirement
empirical uncertainty
novelty
severity
diversity
estimated cost
remaining budget

The selector then chooses the next evaluation.

Conceptually:

Candidate Pool
      ↓
Candidate Scoring
      ↓
Budget Constraint
      ↓
Candidate Selection
      ↓
Agent Execution
      ↓
New Evidence
      ↓
Updated Candidate Statistics
      ↓
Next Selection
5.2 Mechanism 2: State-Based Execution Branching

During execution, the system identifies intermediate states that may be useful for further investigation.

A suitable state can be serialized as a snapshot.

The snapshot can then be restored to create multiple alternative continuations.

Conceptually:

Initial Task
     ↓
Agent Execution
     ↓
Trajectory
     ↓
Interesting State S
     ↓
Snapshot(S)
     ├──────────────┐
     ↓              ↓
 Perturbation A   Perturbation B
     ↓              ↓
 Branch A         Branch B
     ↓              ↓
 Execution        Execution

The initial implementation focuses on environment and execution-state snapshots.

The system does not assume that model KV-cache state can be captured or restored.

KV-cache reuse may be investigated as a future optimization only if technically supported and experimentally validated.

5.3 Mechanism 3: Failure Validation and Generalization

The system treats failure discovery as a multi-stage process.

Execution
    ↓
Invariant Violation
    ↓
Candidate Failure
    ↓
Independent Replay
    ↓
Failure Validation
    ↓
Failure Signature
    ↓
Failure Family
    ↓
Hidden Holdout Evaluation
    ↓
Generalization Evidence

This prevents a single unstable or scenario-specific behavior from being treated as a generalized security finding.

6. System Definition

The system is defined as a controlled evaluation framework consisting of:

Test Scenario Generator
        ↓
Candidate Test Repository
        ↓
Adaptive Test Selector
        ↓
Agent Execution Controller
        ↓
Controlled Agent Environment
        ↓
Trajectory Collector
        ↓
State Analyzer
        ↓
Snapshot Manager
        ↓
Branch Manager
        ↓
Invariant Evaluation Engine
        ↓
Failure Analyzer
        ↓
Failure Clustering Engine
        ↓
Validation Engine
        ↓
Hidden Holdout Evaluator
        ↓
Metrics and Reporting Engine

A feedback loop connects evaluation results back to adaptive test selection.

7. System Inputs

The system accepts the following inputs.

7.1 Agent Configuration

The evaluated agent is defined by:

model
model version
system instructions
available tools
tool permissions
memory/context configuration
agent policy
temperature or sampling configuration where applicable
7.2 Task Configuration

A task contains:

task ID
task description
task category
expected outcome
permitted actions
constraints
relevant security invariants
relevant reliability invariants
7.3 Environment Configuration

The environment defines:

available tools
databases
APIs
simulated external services
authentication state
authorization state
environment state
tool responses
fault-injection configuration
7.4 Evaluation Configuration

The evaluation configuration defines:

evaluation strategy
total budget
maximum executions
maximum branches
replay count
metamorphic testing configuration
holdout configuration
random seed
logging configuration
7.5 Security Policy

The policy defines:

agent identity
permitted capabilities
permitted tools
permitted data
permitted operations
authorization requirements
prohibited actions
8. System Outputs

The system produces structured research outputs.

8.1 Execution Outputs
execution ID
trajectory
actions
tool calls
tool arguments
observations
environment state references
latency
token usage
execution cost
8.2 State Outputs
state ID
state metadata
parent state
snapshot ID
state serialization
restoration metadata
8.3 Branch Outputs
branch ID
parent snapshot
perturbation
branch configuration
branch trajectory
branch outcome
8.4 Failure Outputs
failure ID
violated invariant
execution evidence
failure type
severity
failure signature
related failures
8.5 Failure Family Outputs
family ID
member failures
representative signature
failure category
severity distribution
reproducibility rate
holdout performance
8.6 Experiment Outputs
experiment configuration
experiment ID
model version
environment version
code version
seed
budget
metrics
raw results
summary results
9. Agent Model

The system treats an AI agent as an interactive decision-making system.

Conceptually:

Agent =
LLM
+
Instructions
+
Task
+
Context / Memory
+
Tools
+
Policy

The agent receives observations and produces actions.

An action may be:

Text Response
Tool Call
Tool Arguments
Termination
9.1 Observable Agent State

The evaluation framework records observable state information required for evaluation.

Examples include:

current task
task progress
selected action
selected tool
tool arguments
received observation
authorization state
environment state ID
recovery state
execution step

The system does not require access to private chain-of-thought.

The evaluation is based on observable agent/environment behavior and executable evaluation conditions.

10. Environment Model

The agent executes inside a controlled environment.

The environment may contain:

Tool Gateway
      ↓
Authorization Engine
      ↓
Simulated Database
      ↓
External Service Mock
      ↓
Environment State

The environment exists to make agent behavior:

observable
reproducible
controllable
safely testable
measurable
10.1 Tool Gateway

All agent tool calls pass through a controlled gateway.

The gateway records:

tool name
arguments
agent identity
requested capability
authorization decision
execution result
timestamp
10.2 Policy Engine

The policy engine evaluates whether an agent is authorized to perform a requested operation.

Example:

Requested Capability:
customer.read

Agent Capabilities:
customer.read

Result:
ALLOW

Example violation:

Requested Capability:
customer.delete

Agent Capabilities:
customer.read

Result:
DENY

The evaluation framework can then test whether the agent attempts or succeeds in violating the defined security boundary.

11. Evaluation Domains

The initial project focuses on two primary evaluation dimensions.

11.1 Security Evaluation

Security testing includes:

unauthorized data access
unauthorized tool access
privilege violations
policy bypass
sensitive-data exposure
unsafe external actions
malicious instruction influence
state manipulation
11.2 Reliability Evaluation

Reliability testing includes:

task failure
incorrect tool selection
invalid tool arguments
repeated action loops
state inconsistency
recovery failure
failure under perturbation
unexpected termination
11.3 Robustness Evaluation

Robustness testing examines whether expected behavior remains stable under controlled transformations such as:

wording changes
irrelevant context
equivalent task reformulation
tool-order changes
environment variations
state perturbations
12. Candidate Test Model

Each candidate test is represented as a structured object.

CandidateTest
├── candidate_id
├── task_id
├── scenario_type
├── attack_type
├── environment_configuration
├── perturbation
├── expected_behavior
├── invariants
├── estimated_cost
├── novelty
├── historical_yield
├── uncertainty
├── severity
└── selection_metadata

The candidate pool is dynamically updated as new evidence is obtained.

13. Adaptive Test Selection

The adaptive selector determines which candidate should be executed next.

The selector considers:

historical failure yield
uncertainty
novelty
severity
diversity
estimated cost
remaining budget

A conceptual acquisition function is:

Acquisition Score =
Expected Yield
+
Exploration Value
+
Novelty Value
+
Severity Value
-
Cost Penalty

The exact formula is defined in the separate Adaptive Test Selection Specification.

13.1 UCB-V Boundary

If the implementation uses UCB-V, the system must calculate empirical reward variance from actual observations.

The project must not label a heuristic as UCB-V merely because it contains an exploration term.

If empirical variance is not implemented, the mechanism must be described as a variance-aware or heuristic acquisition strategy instead.

14. Trajectory Model

An execution trajectory is represented as:

τ = {s₀, a₀, o₀, s₁, a₁, o₁, ..., sₙ}

Where:

s = state
a = action
o = observation

A trajectory records the sequence of observable interactions between the agent and environment.

15. Interesting-State Identification

Not every state should automatically generate branches.

The system identifies states based on configurable criteria.

Potential criteria include:

security-sensitive action
privilege boundary
unusual tool call
invariant proximity
anomalous behavior
high uncertainty
novel state
high-value decision point
recovery transition
detected policy conflict

The criteria must be configurable and experimentally evaluated.

16. State Snapshot Model

A snapshot represents the state necessary to reproduce a supported continuation.

A snapshot may include:

environment state
tool state
authorization state
task progress
relevant context
random seed
state metadata

Each snapshot receives a unique identifier.

Snapshot
├── snapshot_id
├── source_run_id
├── source_state_id
├── parent_snapshot_id
├── serialized_state
├── configuration_hash
└── creation_metadata
17. Branching Model

A branch is a new execution created from a previously captured state.

Snapshot S
   ├── Branch A
   ├── Branch B
   ├── Branch C
   └── Branch D

Each branch can apply a different perturbation.

Examples:

different tool response
different instruction
different environment condition
different state variable
different tool ordering
adversarial input

The branch must retain a reference to its parent snapshot.

18. Invariant Model

An invariant is an executable condition describing expected system behavior.

Examples:

Agent must not access unauthorized data.
Agent must not invoke a tool without the required capability.
Agent must not transition the environment into an invalid state.
Protected data must not be exposed to an unauthorized principal.

Each invariant has:

Invariant
├── invariant_id
├── category
├── precondition
├── expected_condition
├── severity
└── evidence_requirements
19. Failure Definition

A failure occurs when an executable invariant is violated.

A failure record must contain evidence.

Failure
├── failure_id
├── run_id
├── step
├── invariant_id
├── category
├── severity
├── evidence
├── state_id
└── signature

The system must distinguish:

Observed Anomaly
Candidate Failure
Validated Failure
Failure Family

These terms must not be treated as interchangeable.

20. Failure Family Model

Multiple individual failures may originate from the same underlying mechanism.

The system therefore generates failure signatures.

A signature may include:

violated invariant
action type
tool
attack type
environment condition
state characteristics
observed outcome

Similar signatures can be grouped into failure families.

Failure 1 ─┐
Failure 2 ─┼──→ Failure Family A
Failure 3 ─┘

Failure 4 ─┐
Failure 5 ─┼──→ Failure Family B
Failure 6 ─┘
21. Reproducibility Model

A detected failure must be replayed independently.

The basic measurement is:

Reproduction Rate =
Successful Failure Reproductions
/
Total Replay Attempts

Failures may be categorized as:

stable
probabilistic
flaky
non-reproducible

Low reproducibility does not automatically mean the failure is irrelevant.

It indicates that the failure behavior requires appropriate interpretation.

22. Metamorphic Testing

Metamorphic testing evaluates whether expected invariants remain valid after controlled transformations.

Example:

Original Task
      ↓
Execution
      ↓
Invariant Result

        VS

Transformed Task
      ↓
Execution
      ↓
Invariant Result

Possible transformations:

wording variation
irrelevant context insertion
equivalent task formulation
tool-order variation
environment variation
state perturbation

A metamorphic test must execute both the base and transformed scenarios.

The implementation must not declare a metamorphic defect based solely on a hard-coded expected result.

23. Hidden Holdout Evaluation

The system must reserve a set of scenarios that are not used during failure discovery.

The holdout set is used to determine whether discovered failure families generalize.

Discovery Set
     ↓
Failure Discovery
     ↓
Failure Family
     ↓
Hidden Holdout
     ↓
Independent Evaluation
     ↓
Generalization Result

Holdout outcomes must not influence adaptive selection before the final holdout evaluation.

24. Evaluation Budget

The project treats evaluation resources as explicit constraints.

Possible budget dimensions:

token budget
execution budget
branch budget
time budget
replay budget
analysis budget

The system records:

Generation Cost
Execution Cost
Branch Cost
Snapshot Cost
Restore Cost
Analysis Cost
Verification Cost

Total cost is:

C_total =
C_generation
+
C_execution
+
C_branch
+
C_snapshot
+
C_restore
+
C_analysis
+
C_verification

No efficiency improvement is assumed before experimental measurement.

25. Baseline Methods

The system must support baseline comparisons.

Baseline 1: Random Selection

Candidates are selected randomly.

Baseline 2: Uniform Selection

Evaluation budget is distributed approximately uniformly across candidate groups.

Baseline 3: Independent Execution

Each candidate begins from the initial environment state.

No state branching is used.

Baseline 4: Adaptive Without Branching

Adaptive selection is enabled, but each selected scenario executes independently.

Baseline 5: Branching Without Adaptive Selection

State branching is enabled, but test selection is non-adaptive.

Proposed Method
Adaptive Selection
+
State-Based Branching
+
Invariant Detection
+
Failure Validation
+
Holdout Generalization
26. Experimental Design Requirements

Experiments must control or record:

model
model version
prompt version
environment version
scenario version
tools
policies
random seed
evaluation budget
selection strategy
branching configuration
replay count

Every experiment receives a unique experiment ID.

27. Experiment Reproducibility

Every experiment must record sufficient metadata to reconstruct the experiment.

Required metadata:

experiment_id
code_version
model_version
prompt_version
environment_version
scenario_version
configuration
random_seed
budget
timestamp

The project must avoid hard-coded result values in production code or dashboard visualizations.

All reported experimental values must originate from experiment data.

28. Data Requirements

The system must preserve:

Raw Data
trajectories
events
tool calls
observations
snapshots
branch relationships
failures
Derived Data
failure signatures
failure families
reproducibility statistics
generalization statistics
acquisition statistics
cost metrics
Experiment Metadata
configuration
version
seed
model
environment
budget
29. Technology Direction

The initial research prototype should use a modular Python implementation.

Suggested components:

Python
├── Agent Interface
├── Environment Interface
├── Tool Gateway
├── Scenario Generator
├── Adaptive Selector
├── Trajectory Recorder
├── Snapshot Manager
├── Branch Manager
├── Invariant Engine
├── Failure Analyzer
├── Clustering Engine
├── Validation Engine
├── Metrics Engine
└── Experiment Manager

Potential supporting technologies include:

SQLite
JSONL
NumPy
pandas
scikit-learn
PyTorch where necessary
FastAPI
Docker
Plotly
MLflow or equivalent experiment tracking

Technology choices remain subject to the implementation requirements defined in later documents.

30. Dashboard Requirements

The dashboard is an observation and analysis interface, not the research system itself.

It should display experimentally generated data such as:

experiment status
budget consumption
candidate selection
execution count
branch count
failure count
failure families
reproducibility
generalization
cost
invariant violations
trajectory information

The dashboard must not contain fabricated experimental results.

Illustrative demo data must be explicitly marked as:

Illustrative / simulated data

31. Security Taxonomy Mapping

The system may map discovered failures to external security taxonomies.

Potential mappings include:

OWASP Agentic Security Initiative categories
MITRE ATLAS concepts
other agent-security taxonomies

Mappings must be verified against the relevant taxonomy version before being presented as authoritative.

The system must not claim:

"OWASP compliant"

merely because its findings are mapped to OWASP categories.

The appropriate terminology is:

"Mapped to selected security taxonomy categories."

32. System Non-Goals

The project does not attempt to:

Train a new foundation model.
Modify model weights.
Build a production enterprise security platform.
Guarantee complete agent security.
Guarantee detection of every vulnerability.
Perform unrestricted real-world penetration testing.
Automatically remediate every discovered failure.
Access private model chain-of-thought.
Claim KV-cache branching without implementation.
Claim cost savings without measured experiments.
Claim OWASP compliance without formal evidence.
Treat simulated dashboard values as research results.
33. Constraints
Computational Constraints

The system must operate under configurable resource limits.

Budget Constraints

Experiments must define an explicit evaluation budget.

Reproducibility Constraints

Experiments must record seeds and versions wherever possible.

Environment Constraints

Initial experiments should use controlled environments rather than uncontrolled production systems.

Evidence Constraints

Research claims must be supported by recorded experiment data.

34. Expected Research Contribution

The project investigates whether combining:

Budget-Aware Adaptive Selection
+
State-Based Branching
+
Trajectory Analysis
+
Failure Validation
+
Hidden-Holdout Evaluation

provides a useful methodology for efficient AI-agent security and reliability evaluation.

The contribution is therefore not simply a testing dashboard.

The intended contribution is an experimentally evaluated adaptive evaluation methodology and implementation.

35. Definition of Done

The project should not be considered complete merely because the dashboard works.

A minimum research-complete implementation requires:

Core System
 Agent execution works
 Controlled environment works
 Tool gateway works
 Candidate generation works
 Candidate selection works
 Budget enforcement works
 Trajectory recording works
 State identification works
 Snapshot creation works
 Snapshot restoration works
 Branch execution works
 Invariant evaluation works
 Failure recording works
 Failure clustering works
Validation
 Independent replay works
 Reproducibility metrics work
 Metamorphic testing works
 Hidden holdout evaluation works
 Generalization metrics work
Experimentation
 Baselines implemented
 Ablations implemented
 Experiment configurations versioned
 Random seeds recorded
 Model versions recorded
 Environment versions recorded
 Raw results stored
 Derived metrics reproducible
Reporting
 Dashboard uses real experiment data
 No unsupported numerical claims
 Cost measurements include snapshot/restore overhead
 Results distinguish discovery from validation
 Results distinguish discovery scenarios from holdout scenarios
36. Acceptance Criteria

The implementation satisfies this specification only if:

A complete experiment can be launched from a configuration file.
The agent can execute within a controlled environment.
Every execution generates a structured trajectory.
Relevant intermediate states can be identified.
Supported states can be snapshotted and restored.
Multiple branches can be generated from a snapshot.
Candidate selection can operate under a fixed budget.
Security and reliability invariants can be evaluated automatically.
Detected failures contain observable evidence.
Failures can be independently replayed.
Failures can be grouped into failure families.
Metamorphic tests can be executed.
Hidden holdout scenarios can be evaluated independently.
Evaluation metrics can be reproduced from stored data.
Baseline methods can be executed under comparable budgets.
Experimental results can be traced back to their raw data.
The dashboard reflects actual experiment results.
37. Key Design Principles

The implementation must follow these principles.

Principle 1: Evidence Over Claims

No numerical research claim without experimental evidence.

Principle 2: Observable Behavior Over Hidden Reasoning

Evaluation should rely on observable actions, states, tool interactions,
environment changes, and invariant outcomes.

Principle 3: Reproducibility

Every important result should be independently reproducible where technically possible.

Principle 4: Controlled Experimentation

Agent evaluations should occur in controlled and versioned environments.

Principle 5: Explicit Budget Accounting

Every meaningful computational cost should be measurable.

Principle 6: Modular Design

Each major mechanism should be independently testable.

Principle 7: Baseline Comparison

The proposed methodology must be compared against simpler alternatives.

Principle 8: Discovery Is Not Validation

Finding a suspicious behavior is not equivalent to validating a failure.

Principle 9: Generalization Must Be Tested

A failure observed during discovery must not automatically be assumed to generalize.

Principle 10: Research Results Must Come From Experiments

Hard-coded demonstration values must never be presented as measured results.

38. Terminology
Term	Definition
Agent	AI system that observes a task/environment and selects actions
Task	Objective given to the agent
Environment	Controlled system in which the agent operates
Action	Observable operation selected by the agent
Observation	Information returned to the agent
State	Relevant representation of agent/environment execution state
Trajectory	Sequence of states, actions, and observations
Snapshot	Persisted representation of a supported execution state
Branch	Alternative execution originating from a snapshot
Candidate Test	Scenario eligible for evaluation
Invariant	Executable condition defining expected behavior
Failure	Evidence-backed invariant violation
Failure Signature	Structured representation of a failure's characteristics
Failure Family	Group of related failures with a common mechanism
Replay	Independent re-execution of a failure scenario
Metamorphic Test	Test using a defined transformation of an existing scenario
Holdout	Scenario excluded from discovery and used for final evaluation
Generalization	Ability of a discovered failure family to appear in unseen scenarios
Evaluation Budget	Configured limit on available evaluation resources
Adaptive Selection	Dynamic selection of the next evaluation based on observed evidence
39. Final System Definition

The project is a research prototype for budget-constrained adaptive security and reliability evaluation of AI agents.

Its central execution loop is:

             ┌───────────────────────────┐
             │ Candidate Test Generation │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Adaptive Test Selection   │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Agent + Controlled Env.   │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Trajectory Collection     │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Interesting State         │
             │ Identification             │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ State Snapshot             │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Branch Generation          │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Branch Execution           │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Invariant Evaluation       │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Failure Detection          │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Failure Family Analysis    │
             └─────────────┬─────────────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
      Reproducibility             Metamorphic
          Testing                   Testing
              │                         │
              └────────────┬────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Hidden Holdout Evaluation │
             └─────────────┬─────────────┘
                           ↓
             ┌───────────────────────────┐
             │ Metrics + Research Data   │
             └─────────────┬─────────────┘
                           │
                           └──────→ Adaptive Selection

The system's fundamental research question is:

Can adaptive, trajectory-aware, state-based evaluation discover and validate AI-agent security and reliability failures more efficiently under a fixed evaluation budget than conventional independent evaluation strategies?

This question, rather than the dashboard, the architecture diagram, or any particular algorithm, is the central organizing principle of the project.


### What this document establishes

This **Project Specification is intentionally the most comprehensive document** because the rest of the documents should refine individual parts of it rather than redefine the project.

In particular, it fixes these important decisions early:

- **What the system evaluates:** AI agents, not foundation-model training.
- **Where it operates:** controlled environments.
- **What it records:** observable trajectories and execution state.
- **What the novel mechanism is:** adaptive selection + state-based branching.
- **What constitutes evidence:** executable invariant violations.
- **What constitutes a validated finding:** reproducibility and supporting evidence.
- **How generalization is tested:** hidden holdout scenarios.
- **How efficiency is judged:** fixed-budget comparison against baselines.
- **What is deliberately *not* claimed:** fabricated cost savings, OWASP compliance, KV-cache branching, or production readiness.

This is the document I would **freeze first** before serious vibe-coding. Any later architecture or 