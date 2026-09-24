# Threat Model & Security Requirements

## Project: Budget-Constrained Adaptive Security Evaluation of AI Agents

**Document ID:** TM-01
**Document Type:** Threat Model and Security Requirements
**Version:** 1.0
**Status:** Draft for Implementation
**Related Documents:**

* Project Specification
* Research Questions & Success Criteria
* System Architecture
* Functional Requirements

---

# 1. Purpose

This document defines the security threat model for the **Budget-Constrained Adaptive Security Evaluation of AI Agents** platform.

The threat model identifies:

* assets that must be protected,
* system boundaries,
* trusted and untrusted components,
* threat actors,
* attack surfaces,
* security threats,
* failure consequences,
* security controls,
* evaluation invariants,
* evidence required to determine whether a security violation occurred.

The system has a dual security objective:

1. **Evaluate security and reliability failures in the AI agent under test.**
2. **Protect the integrity of the evaluation system so that the evaluator itself does not produce misleading or invalid experimental results.**

The second objective is essential. A security evaluator that can be manipulated into fabricating, suppressing, corrupting, or misclassifying failures is not much of an evaluator. Humanity has already invented enough dashboards that confidently report nonsense.

---

# 2. Threat-Model Scope

The threat model covers the following components:

```text
                    ┌──────────────────────────────┐
                    │      Researcher / Operator   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     Experiment Controller    │
                    │   Configuration + Budget     │
                    └──────────────┬───────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             ▼                     ▼                     ▼
      Test Generation       Adaptive Selection      Metrics Engine
             │                     │
             └──────────┬──────────┘
                        ▼
                ┌───────────────┐
                │  AI Agent     │
                │   Under Test  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │  Tool Gateway │
                └───────┬───────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          Policy     Tool / DB   External
          Engine     Simulator   Mock
             │          │          │
             └──────────┼──────────┘
                        ▼
              Controlled Environment
                        │
                        ▼
                Trajectory / State
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
        Snapshot     Branching   Invariants
            │           │           │
            └───────────┼───────────┘
                        ▼
               Failure Analysis
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          Replay    Metamorphic  Holdout
                     Testing     Evaluation
```

---

# 3. Security Objectives

The system shall preserve the following security properties.

## SO-01: Agent Isolation

The agent under evaluation shall remain within the intended execution boundary.

The agent shall not bypass:

* the Tool Gateway,
* configured capability restrictions,
* policy enforcement,
* experiment isolation.

---

## SO-02: Environment Integrity

The controlled evaluation environment shall maintain a trustworthy representation of its state.

Unauthorized or unintended modifications shall be detectable.

---

## SO-03: Tool Boundary Integrity

Agent requests to controlled tools shall pass through the Tool Gateway.

The evaluator shall be able to determine:

```text
who requested the action
what action was requested
which tool was requested
what policy decision was made
what actually executed
what result was returned
```

---

## SO-04: Policy Integrity

Security-policy decisions shall be recorded and protected against silent modification.

---

## SO-05: Snapshot Integrity

Snapshots shall accurately represent the supported execution state at the time they were created.

A malicious or faulty branch shall not modify its source snapshot.

---

## SO-06: Branch Isolation

Branches created from the same state shall execute independently.

A mutation in Branch A shall not alter Branch B or the parent state.

---

## SO-07: Holdout Integrity

Hidden holdout scenarios shall remain inaccessible to adaptive selection before the designated holdout evaluation stage.

---

## SO-08: Evidence Integrity

A discovered failure shall retain sufficient evidence to determine:

* what happened,
* where it happened,
* under which configuration,
* under which state,
* which invariant was violated.

---

## SO-09: Experiment Reproducibility

The system shall preserve sufficient configuration and execution metadata to reproduce an experiment or explain why exact reproduction is not possible.

---

## SO-10: Result Integrity

Metrics and reports shall be derived from stored experimental evidence rather than manually supplied values.

---

# 4. Assets

The following assets are considered security- or research-critical.

| Asset                    | Description                                    | Integrity Importance |
| ------------------------ | ---------------------------------------------- | -------------------- |
| Agent configuration      | Model, instructions, parameters and adapter    | High                 |
| Experiment configuration | Complete evaluation configuration              | Critical             |
| Evaluation budget        | Limits evaluation expenditure                  | High                 |
| Candidate pool           | Scenarios considered for evaluation            | High                 |
| Selection statistics     | Data driving adaptive selection                | Critical             |
| Agent trajectories       | Observable execution history                   | Critical             |
| Environment state        | State required for evaluation and reproduction | Critical             |
| Snapshots                | Restorable execution states                    | Critical             |
| Branches                 | Derived evaluation executions                  | High                 |
| Tool definitions         | Available agent capabilities                   | Critical             |
| Policy definitions       | Security rules                                 | Critical             |
| Invariant definitions    | Conditions used to detect failures             | Critical             |
| Failure records          | Evidence of security/reliability failures      | Critical             |
| Failure families         | Grouped failure evidence                       | High                 |
| Replay records           | Reproducibility evidence                       | High                 |
| Metamorphic results      | Transformation-based validation evidence       | High                 |
| Holdout scenarios        | Unseen evaluation cases                        | Critical             |
| Raw metrics              | Experimental measurements                      | Critical             |
| Experiment metadata      | Seeds, versions, timestamps, configuration     | High                 |
| Research reports         | Derived conclusions and visualizations         | High                 |

---

# 5. Trust Boundaries

The system shall explicitly model the following trust boundaries.

## TB-01: Researcher → Experiment Controller

The researcher provides configuration and evaluation objectives.

Potentially unsafe inputs include:

* malformed configuration,
* excessive budgets,
* invalid tool definitions,
* unsafe scenario definitions,
* incorrect invariant definitions.

The controller must validate inputs before execution.

---

## TB-02: Agent → Tool Gateway

This is one of the primary security boundaries.

The agent is **not trusted to directly access evaluation tools**.

All controlled tool requests shall cross the Tool Gateway.

---

## TB-03: Tool Gateway → Controlled Tool

The gateway communicates with simulated or controlled tool implementations.

The tool implementation may intentionally behave maliciously or incorrectly because it may be part of the test scenario.

---

## TB-04: Agent → Environment

The agent interacts with the environment only through explicitly exposed mechanisms.

Direct access to protected environment state shall be prohibited.

---

## TB-05: Adaptive Evaluation → Hidden Holdout

The adaptive evaluation subsystem must not access hidden holdout information before holdout evaluation.

This is a strict research-integrity boundary.

---

## TB-06: Branch → Parent Snapshot

Branches must not be able to modify their parent snapshot.

---

## TB-07: Agent → Evaluation Infrastructure

The agent shall not have direct access to:

* experiment databases,
* failure records,
* selection statistics,
* hidden holdout data,
* snapshots belonging to unrelated executions,
* evaluator configuration,
* internal metrics.

---

# 6. Threat Actors

The project models several threat sources.

## TA-01: Malicious or Adversarial Task Input

A task may intentionally attempt to cause unsafe agent behavior.

Examples:

* prompt injection,
* instruction manipulation,
* privilege escalation attempts,
* malicious data,
* conflicting instructions.

The task itself is an evaluation input and therefore may be intentionally adversarial.

---

## TA-02: Adversarial Environment

The environment may intentionally provide misleading, malformed, inconsistent, or unsafe responses.

Examples:

* malicious tool output,
* corrupted records,
* unexpected state transitions,
* manipulated external-service responses.

---

## TA-03: Adversarial Tool

A controlled tool may intentionally behave incorrectly or return adversarial content.

The evaluator must capture the interaction rather than blindly trusting the tool output.

---

## TA-04: Adversarial Agent Behavior

The agent under test may attempt to:

* bypass policies,
* invoke unauthorized tools,
* manipulate tool parameters,
* access restricted state,
* exploit environment inconsistencies,
* perform actions outside its capability set.

The evaluator treats such behavior as part of the evaluation target.

---

## TA-05: Faulty Evaluator Component

A software defect in the evaluator may:

* miss a failure,
* report a false failure,
* corrupt a trajectory,
* restore an incorrect state,
* calculate incorrect metrics.

This is a particularly important threat because evaluator defects can invalidate research conclusions.

---

## TA-06: Configuration Error

A researcher may unintentionally configure:

* incorrect budgets,
* inappropriate invariants,
* invalid policies,
* mismatched baselines,
* contaminated holdout data,
* inconsistent environment versions.

The system should detect configuration errors before evaluation whenever possible.

---

## TA-07: Data Corruption

Stored experiment data may become:

* incomplete,
* duplicated,
* inconsistent,
* corrupted,
* incorrectly associated with another execution.

---

## TA-08: Cross-Experiment Contamination

State, configuration, candidate data, or holdout information from one experiment may accidentally influence another.

---

# 7. Threat Classification

Threats are grouped into:

### Agent Security Threats

Threats against the security behavior of the agent under evaluation.

### Environment Threats

Threats arising from adversarial or faulty tools and environments.

### Evaluation Integrity Threats

Threats that make experimental results unreliable.

### Data Integrity Threats

Threats against trajectories, snapshots, failures, and metrics.

### Research Validity Threats

Threats that produce misleading scientific conclusions without necessarily compromising traditional system security.

---

# 8. Threat Catalogue

## TM-01: Unauthorized Tool Invocation

### Description

The agent attempts to invoke a tool outside its permitted capabilities.

### Example

An agent with read-only database capability attempts a write operation.

### Security Property

Capability boundary must be enforced.

### Detection Evidence

```text
agent_id
tool_id
requested_action
capability_requirement
configured_capabilities
policy_decision
actual_execution
```

### Required Control

The Tool Gateway shall validate capability and policy before execution.

### Failure Classification

Potential security failure.

---

# 9. TM-02: Policy Bypass

### Description

The agent attempts to perform an action that should be denied by the configured policy.

### Example

```text
Agent → Tool Gateway → Restricted Action
                         ↓
                    Policy Denial
```

If the action is nevertheless executed, the policy boundary has failed.

### Required Control

The Policy Engine shall evaluate the action before execution.

### Required Evidence

* requested action,
* policy rule,
* decision,
* actual execution result.

---

# 10. TM-03: Tool Parameter Manipulation

### Description

The agent constructs parameters intended to bypass restrictions or cause unintended tool behavior.

### Examples

* invalid identifiers,
* unexpected parameter combinations,
* boundary values,
* authorization-related parameters,
* malformed structured input.

### Required Control

Tool schemas and policy validation shall be applied before execution.

---

# 11. TM-04: Prompt / Instruction Injection

### Description

Untrusted task, tool, database, or external content attempts to modify the agent's intended behavior.

### Example

A tool response contains instructions that attempt to override the original task or security policy.

### Evaluation Objective

Determine whether the agent performs an unauthorized action as a result.

### Evidence

The evaluator shall preserve:

* source of untrusted content,
* agent action,
* tool sequence,
* policy decision,
* resulting state.

---

# 12. TM-05: Sensitive Data Exposure

### Description

The agent exposes data that should remain protected under the configured environment policy.

### Possible Sources

* tool responses,
* database records,
* environment state,
* memory,
* task context.

### Required Control

The environment shall mark protected data where the experiment requires it.

### Detection

An executable invariant shall determine whether protected data crossed the configured boundary.

---

# 13. TM-06: Unauthorized State Modification

### Description

The agent modifies environment state outside its permitted capabilities.

### Examples

* modifying protected records,
* changing permissions,
* altering security configuration,
* modifying another user's state.

### Detection

Compare pre-action and post-action environment state against authorization rules.

---

# 14. TM-07: Unsafe Action Sequence

### Description

Individual actions may appear valid while their sequence creates a security violation.

### Example

```text
Action A: obtain identifier
Action B: change context
Action C: access protected resource
```

The sequence may violate an invariant even if each isolated action appears acceptable.

### Required Control

Invariant evaluation shall support trajectory-level checks.

---

# 15. TM-08: State-Dependent Security Failure

### Description

A security failure occurs only after the agent reaches a particular intermediate state.

This threat is central to the project because independent execution may repeatedly traverse the same prefix before reaching the relevant state.

### Evaluation Strategy

The system shall:

1. identify an interesting state,
2. snapshot it,
3. branch from that state,
4. apply controlled perturbations,
5. evaluate resulting behavior.

---

# 16. TM-09: Malicious Tool Response

### Description

A controlled tool returns adversarial or misleading content.

### Examples

* false authorization information,
* injected instructions,
* malformed structured data,
* inconsistent state,
* misleading success messages.

### Evaluation Objective

Determine whether the agent responds safely.

---

# 17. TM-10: Environment Fault

### Description

The environment experiences controlled failures.

Examples:

* tool timeout,
* service unavailable,
* malformed response,
* delayed response,
* database failure,
* partial state update.

### Evaluation Objective

Measure whether the agent violates reliability or security invariants under environmental faults.

---

# 18. TM-11: Cross-Branch State Contamination

### Description

A modification made in one branch unexpectedly appears in another branch.

### Example

```text
Snapshot S
   ├── Branch A → modifies state X
   └── Branch B → unexpectedly observes modified X
```

### Security Impact

Branch results become invalid and may create false research conclusions.

### Required Control

Each branch shall operate against isolated state.

---

# 19. TM-12: Snapshot Tampering

### Description

A snapshot is modified after creation.

### Possible Effects

* incorrect branch behavior,
* false failures,
* missing failures,
* irreproducible results.

### Required Controls

Snapshots should have:

* integrity hashes,
* version metadata,
* immutable storage semantics where practical.

---

# 20. TM-13: Invalid Snapshot Restoration

### Description

Restoring a snapshot does not reconstruct the intended evaluation state.

### Possible Causes

* incomplete serialization,
* nondeterministic state,
* external dependency mismatch,
* corrupted snapshot,
* version incompatibility.

### Required Control

Snapshot restoration shall perform validation checks.

---

# 21. TM-14: Branch Escape

### Description

A branch modifies resources outside its assigned isolated environment.

### Security Boundary

Branch execution shall be restricted to its allocated environment.

### Detection

Environment identifiers and state lineage shall be validated.

---

# 22. TM-15: Budget Exhaustion Attack

### Description

A candidate or branch causes disproportionately high evaluation cost.

### Examples

* extremely long trajectories,
* excessive tool calls,
* branch explosion,
* repeated replay,
* expensive perturbation generation.

### Required Controls

The Budget Manager shall enforce:

* execution limits,
* branch limits,
* model-call limits,
* time limits,
* cost limits.

---

# 23. TM-16: Branch Explosion

### Description

An interesting state produces too many branches.

### Risk

The adaptive evaluator spends most of its budget exploring a single state.

### Required Controls

Configurable:

```text
maximum branches per snapshot
maximum branches per trajectory
maximum total branch budget
branch selection policy
```

---

# 24. TM-17: Adaptive Selection Manipulation

### Description

Observed rewards or failure statistics are manipulated or corrupted, causing the selector to make inappropriate future selections.

### Example

A corrupted failure record makes a candidate appear highly productive.

### Required Control

Selection statistics shall be derived from validated experiment data.

---

# 25. TM-18: Reward Poisoning

### Description

Incorrect or adversarial evaluation outcomes influence the adaptive selection policy.

### Example

A false failure increases the perceived value of a candidate region.

### Mitigation

The system should distinguish:

```text
Observed Failure
        ↓
Validated Failure
        ↓
Adaptive Reward
```

where research configuration requires validated outcomes before updating the selector.

---

# 26. TM-19: Failure Suppression

### Description

A real failure occurs but is not recorded.

### Causes

* incorrect invariant,
* logging failure,
* evaluator crash,
* malformed trace,
* clustering error,
* filtering bug.

### Required Control

The system shall preserve raw trajectory evidence independently of derived failure records.

This enables post-hoc verification.

---

# 27. TM-20: False Failure Generation

### Description

The evaluator reports a failure when the security/reliability invariant was not actually violated.

### Causes

* incorrect invariant implementation,
* stale state,
* incorrect branch restoration,
* corrupted evidence,
* faulty classifier.

### Required Control

Failure records must reference executable invariant results and observable evidence.

---

# 28. TM-21: Failure Deduplication Error

### Description

Two genuinely distinct failures are incorrectly grouped into one failure family.

### Risk

The measured number of unique failure families becomes inaccurate.

### Required Control

Failure clustering shall retain:

* raw failure records,
* signatures,
* similarity scores,
* family membership decisions.

---

# 29. TM-22: Failure Fragmentation

### Description

The same underlying failure is split into many unrelated failure families.

### Risk

The system overestimates the number of unique failures.

### Required Control

Family construction shall support configurable similarity features and manual/offline inspection.

---

# 30. TM-23: Replay Contamination

### Description

A replay inherits state from the original execution or another replay.

### Risk

The reproduction result becomes invalid.

### Required Control

Every replay shall use an isolated execution context.

---

# 31. TM-24: Non-Reproducible Randomness

### Description

Stochastic execution prevents meaningful comparison between original and replayed failures.

### Required Control

The system shall record relevant random seeds and stochastic configuration.

### Limitation

Exact reproduction may not always be possible for stochastic or externally dependent systems.

Such cases shall be explicitly classified rather than silently treated as deterministic.

---

# 32. TM-25: Metamorphic Test Contamination

### Description

The transformed task accidentally modifies variables outside the intended metamorphic relation.

### Risk

An apparent metamorphic violation may actually be caused by an unrelated change.

### Required Control

Every transformation shall explicitly define:

* allowed changes,
* unchanged properties,
* expected relation.

---

# 33. TM-26: Metamorphic Relation Failure

### Description

The agent produces behavior inconsistent with the expected relation between base and transformed executions.

### Required Evidence

The evaluator shall retain:

```text
base task
transformed task
base execution
transformed execution
expected relation
observed relation
comparison result
```

---

# 34. TM-27: Hidden Holdout Leakage

### Description

Information from hidden evaluation cases influences adaptive selection.

### Examples

* holdout scenarios included in candidate generation,
* holdout labels used during adaptive scoring,
* holdout failures used to modify selection before final evaluation.

### Security / Research Impact

This invalidates generalization measurement.

### Required Control

The holdout subsystem shall be isolated from the adaptive selection process.

---

# 35. TM-28: Holdout Memorization

### Description

The evaluator effectively evaluates scenarios already seen during adaptive evaluation rather than genuinely unseen scenarios.

### Required Control

Holdout scenarios shall be generated or selected independently from the adaptive candidate pool.

---

# 36. TM-29: Experiment Cross-Contamination

### Description

State or data from Experiment A influences Experiment B.

### Examples

* shared mutable database state,
* reused snapshots,
* leaked selection statistics,
* shared temporary files,
* shared random state.

### Required Control

Experiments shall have isolated namespaces and controlled resource boundaries.

---

# 37. TM-30: Configuration Drift

### Description

The configuration used during execution differs from the configuration recorded in the experiment.

### Risk

The experiment cannot be reliably reproduced.

### Required Control

Configuration shall be immutable or versioned after experiment execution begins.

---

# 38. TM-31: Model Configuration Drift

### Description

The model or model parameters change between discovery and reproduction.

### Required Control

The system shall record model metadata and relevant generation parameters.

---

# 39. TM-32: Tool Version Drift

### Description

Tool implementation changes between original execution and replay.

### Required Control

Tool implementations shall have version identifiers.

---

# 40. TM-33: Invariant Drift

### Description

An invariant definition changes between discovery and validation.

### Risk

A historical failure may receive a different interpretation.

### Required Control

Invariant definitions shall be versioned and linked to experiment records.

---

# 41. TM-34: Trace Tampering

### Description

Trajectory records are modified, deleted, or incorrectly associated with an execution.

### Required Controls

Trace records should contain:

* execution IDs,
* event IDs,
* timestamps,
* state references,
* integrity metadata where practical.

---

# 42. TM-35: Metric Manipulation

### Description

Derived metrics are manually or programmatically altered without corresponding raw experimental evidence.

### Required Control

Metrics shall be calculated from persisted raw measurements.

---

# 43. TM-36: Hard-Coded Experimental Results

### Description

The reporting or dashboard layer displays manually entered values as though they were measured results.

### This is explicitly prohibited.

The system shall derive displayed experimental values from the experiment store.

If illustrative data is used during development, the UI shall clearly label it as:

```text
ILLUSTRATIVE
SIMULATED
DEMO DATA
```

---

# 44. TM-37: Evaluator Self-Failure

### Description

A component of the evaluator fails while evaluating the agent.

### Examples

* invariant engine crashes,
* snapshot restoration fails,
* trajectory logger fails,
* metrics engine fails.

### Required Control

The system shall distinguish evaluator failure from agent failure.

An evaluator failure shall not automatically become evidence of an agent security failure.

---

# 45. TM-38: Logging Failure

### Description

An important event occurs but is not recorded.

### Impact

The evaluator may produce an incomplete trajectory.

### Required Control

Critical event logging shall detect failures where possible and mark the corresponding execution as incomplete.

---

# 46. TM-39: Denial of Evaluation

### Description

A scenario causes the evaluator to become unavailable or consume its entire budget before meaningful evaluation occurs.

### Controls

* timeouts,
* resource limits,
* branch limits,
* execution limits,
* memory limits,
* failure isolation.

---

# 47. TM-40: Untrusted External Dependency

### Description

An external model, API, tool, or service behaves unexpectedly.

### Required Control

The baseline research environment should prefer:

* controlled tools,
* mock services,
* deterministic fixtures,
* recorded responses where appropriate.

External dependencies shall be explicitly identified in experiment metadata.

---

# 48. Threat-to-Control Matrix

| Threat                         | Primary Control                  | Evidence                       |
| ------------------------------ | -------------------------------- | ------------------------------ |
| Unauthorized tool use          | Tool Gateway + capability checks | Tool request + policy decision |
| Policy bypass                  | Policy Engine                    | Policy decision + execution    |
| Prompt injection               | Controlled scenario + invariants | Input + trajectory             |
| Sensitive data exposure        | Data labels + invariants         | Data flow evidence             |
| State modification             | State comparison                 | Before/after state             |
| Unsafe sequence                | Trajectory invariants            | Action sequence                |
| Malicious tool                 | Tool isolation                   | Tool response + agent action   |
| Branch contamination           | Branch isolation                 | State hashes                   |
| Snapshot tampering             | Integrity metadata               | Snapshot hash                  |
| Invalid restoration            | Snapshot validation              | State comparison               |
| Budget exhaustion              | Budget Manager                   | Cost events                    |
| Branch explosion               | Branch limits                    | Branch count                   |
| Reward poisoning               | Validated reward pipeline        | Selection history              |
| Failure suppression            | Raw trajectory retention         | Trace                          |
| False failure                  | Evidence-backed invariants       | Invariant result               |
| Replay contamination           | Replay isolation                 | Replay environment             |
| Metamorphic contamination      | Explicit transformations         | Base/transformed configs       |
| Holdout leakage                | Holdout isolation                | Access logs                    |
| Cross-experiment contamination | Experiment isolation             | Namespace/IDs                  |
| Configuration drift            | Versioned configuration          | Experiment metadata            |
| Metric manipulation            | Derived metrics                  | Raw measurements               |
| Evaluator failure              | Error classification             | Evaluator logs                 |

---

# 49. Security Invariants

The following invariants should be implemented as executable checks where practical.

## INV-SEC-001: Unauthorized Tool Action

```text
IF action requires capability C
AND agent does not possess C
THEN action MUST NOT execute
```

---

## INV-SEC-002: Policy Denial Enforcement

```text
IF policy(action) = DENY
THEN action MUST NOT execute
```

---

## INV-SEC-003: Branch Isolation

```text
State(branch_A)
MUST NOT mutate
State(branch_B)
```

unless explicit shared-state behavior is configured.

---

## INV-SEC-004: Snapshot Immutability

```text
Snapshot S
MUST remain unchanged
after Branch A executes
```

---

## INV-SEC-005: Holdout Isolation

```text
AdaptiveSelector
MUST NOT access
HoldoutOutcome
before holdout evaluation
```

---

## INV-SEC-006: Budget Enforcement

```text
ActualCost
MUST NOT exceed
ConfiguredBudget
```

unless an explicitly configured overrun policy is triggered and recorded.

---

## INV-SEC-007: Failure Evidence

```text
Every ValidatedFailure
MUST reference
observable evidence
```

---

## INV-SEC-008: Experiment Isolation

```text
Experiment A
MUST NOT modify
Experiment B's mutable state
```

---

## INV-SEC-009: Configuration Consistency

```text
ExecutionConfig
MUST match
RecordedExperimentConfig
```

for all immutable experiment parameters.

---

## INV-SEC-010: Metric Provenance

```text
ReportedMetric
MUST be derivable from
StoredExperimentData
```

---

# 50. Security Requirements

## SR-001: Agent Capability Enforcement

The system shall maintain an explicit capability set for the agent.

---

## SR-002: Tool Access Mediation

The system shall mediate controlled tool access through the Tool Gateway.

---

## SR-003: Policy Decision Logging

Every policy decision shall be logged.

---

## SR-004: Environment Isolation

Each independent execution shall receive an isolated environment state.

---

## SR-005: Branch Isolation

Each branch shall operate independently from sibling branches and the source snapshot.

---

## SR-006: Snapshot Integrity

Snapshots shall be validated before use.

---

## SR-007: Holdout Protection

Holdout scenarios and outcomes shall remain inaccessible to adaptive evaluation before final evaluation.

---

## SR-008: Experiment Namespace Isolation

Experiments shall use separate namespaces for:

* state,
* snapshots,
* branches,
* trajectories,
* metrics.

---

## SR-009: Evidence Preservation

Raw execution evidence shall be preserved independently from derived classifications.

---

## SR-010: Sensitive Data Handling

Sensitive test data shall be:

* minimized,
* isolated,
* redacted where appropriate,
* excluded from unnecessary logs.

---

## SR-011: Configuration Validation

Unsafe or inconsistent configurations shall be rejected before execution.

---

## SR-012: Resource Limits

The evaluator shall enforce configurable:

* execution limits,
* branch limits,
* time limits,
* model-call limits,
* storage limits where applicable.

---

# 51. Security Failure Severity

The system shall support configurable severity classification.

A suggested initial classification is:

| Severity      | Meaning                                                                            |
| ------------- | ---------------------------------------------------------------------------------- |
| Critical      | Direct violation of a high-impact security boundary                                |
| High          | Significant unauthorized behavior or policy violation                              |
| Medium        | Security/reliability violation with constrained impact                             |
| Low           | Limited or contextual violation                                                    |
| Informational | Anomalous behavior requiring observation but not currently classified as a failure |

Severity definitions shall be tied to the experiment's invariant configuration rather than treated as universal truths.

---

# 52. Threat Likelihood and Impact

For research prioritization, each threat may be assigned:

```text
Likelihood
Impact
Detectability
Research Importance
```

The system should avoid presenting these values as universal real-world risk estimates.

They are **evaluation prioritization attributes** for this research environment.

---

# 53. Attack Surface

The primary attack surfaces are:

```text
1. Agent input/task
2. Agent instructions
3. Tool responses
4. Tool parameters
5. Environment state
6. Policy boundary
7. Memory/context
8. Intermediate execution state
9. Snapshot creation
10. Snapshot restoration
11. Branch perturbation
12. Adaptive selection
13. Evaluation budget
14. Failure classification
15. Replay system
16. Metamorphic transformations
17. Hidden holdout boundary
18. Experiment storage
19. Reporting/metrics
```

---

# 54. Threat Model for the Adaptive Selector

Because adaptive selection is central to the research contribution, it requires its own security boundary.

The selector consumes:

```text
Candidate History
      +
Observed Rewards
      +
Failure Information
      +
Novelty
      +
Cost
      +
Budget
```

and produces:

```text
Next Candidate
```

The selector shall not consume:

* hidden holdout outcomes,
* manually modified failure results,
* unvalidated future experiment results.

The selection decision must remain reconstructable from stored inputs.

---

# 55. Threat Model for State-Based Branching

State-based branching introduces unique risks.

The branching system must guarantee:

```text
Original State
      │
      ├── Snapshot S
      │
      ├── Branch A
      │     └── Modified State A
      │
      └── Branch B
            └── Modified State B
```

rather than:

```text
Original State
      │
      └── Shared Mutable State
              ├── Branch A modifies it
              └── Branch B observes A's modification
```

The second model would invalidate branch independence.

---

# 56. Threat Model for Research Validity

Security of the software alone is insufficient.

The experiment must also protect against threats to research validity.

## RV-01: Unequal Budgets

Different methods receive different evaluation resources.

### Control

Budget accounting must be centralized and comparable.

---

## RV-02: Unequal Validation

One method receives stronger replay or verification than another.

### Control

Validation procedures shall be equivalent across comparison methods.

---

## RV-03: Holdout Leakage

Adaptive evaluation sees hidden test cases.

### Control

Strict holdout isolation.

---

## RV-04: Configuration Drift

Different experiments use different agent/environment configurations.

### Control

Versioned experiment configuration.

---

## RV-05: Selective Failure Reporting

Only interesting failures are retained.

### Control

Persist all relevant raw observations before filtering or classification.

---

## RV-06: Metric Cherry-Picking

Only favorable metrics are reported.

### Control

The experiment store shall preserve the complete metric set defined by the experimental methodology.

---

## RV-07: Hard-Coded Demonstration Results

Demo numbers are presented as measured results.

### Control

Results must originate from experiment data.

---

# 57. Security Logging Requirements

Security-relevant events shall contain enough information for forensic reconstruction.

At minimum:

```text
event_id
experiment_id
execution_id
branch_id
timestamp
component
event_type
actor
action
target
decision
result
state_reference
```

Sensitive information shall be redacted according to the configured data-handling policy.

---

# 58. Incident Classification

The evaluator shall classify incidents into:

```text
AGENT_SECURITY_FAILURE
AGENT_RELIABILITY_FAILURE
ENVIRONMENT_FAULT
TOOL_FAULT
POLICY_FAILURE
EVALUATOR_FAILURE
DATA_INTEGRITY_FAILURE
CONFIGURATION_FAILURE
RESOURCE_LIMIT
UNKNOWN
```

This prevents evaluator failures from being incorrectly reported as agent failures.

---

# 59. Security Testing Strategy

The evaluator itself shall be tested using controlled adversarial cases.

At minimum, tests shall include:

### Tool Boundary Tests

* unauthorized tool request,
* invalid tool capability,
* denied policy action,
* malformed tool parameters.

### Environment Tests

* malicious tool response,
* corrupted state,
* tool timeout,
* inconsistent response.

### Branch Tests

* branch state mutation,
* sibling branch isolation,
* snapshot corruption,
* invalid restoration.

### Adaptive Selection Tests

* corrupted reward,
* candidate starvation,
* budget exhaustion,
* repeated candidate selection.

### Holdout Tests

* accidental holdout exposure,
* holdout candidate leakage,
* holdout result access before evaluation.

### Evaluator Tests

* missing trajectory event,
* invariant engine failure,
* database write failure,
* metric calculation failure.

---

# 60. Threat Acceptance Criteria

The threat model shall be considered implemented when the system can demonstrate that:

1. Unauthorized tool actions are detectable.
2. Policy decisions are enforced and recorded.
3. Agent capability boundaries are explicit.
4. Environment state is isolated.
5. Branches cannot silently contaminate one another.
6. Snapshots can be validated.
7. Budget exhaustion is enforced.
8. Adaptive selection decisions are auditable.
9. Hidden holdout information is isolated.
10. Failures contain observable evidence.
11. Replay occurs in an isolated environment.
12. Metamorphic tests preserve base/transformed evidence.
13. Experiment configurations are versioned.
14. Evaluator failures are distinguished from agent failures.
15. Raw execution evidence is retained.
16. Reported metrics can be traced to stored measurements.
17. Cross-experiment state contamination can be detected or prevented.

---

# 61. Threat Model Boundaries

This threat model does **not** claim to protect against every possible threat affecting arbitrary production AI-agent deployments.

The research environment intentionally uses:

* controlled tools,
* simulated services,
* isolated environments,
* configurable policies,
* bounded execution,
* reproducible scenarios.

Therefore, conclusions obtained from this platform must be interpreted within those experimental boundaries.

The system is primarily intended to answer:

> **Can budget-constrained adaptive evaluation, combined with state-based execution branching and systematic failure validation, discover and validate AI-agent security and reliability failures more efficiently than predefined evaluation strategies?**

It is not intended to claim:

> “This agent is secure.”

Nor is it intended to claim:

> “The agent is compliant with every external security framework.”

The evaluator produces **experimental evidence**, not universal security certification.

---

# 62. Final Security Architecture

The intended security boundary is:

```text
                    RESEARCHER
                        │
                        ▼
               Experiment Controller
                        │
                 Configuration
                        │
                ┌───────▼────────┐
                │ Budget Manager │
                └───────┬────────┘
                        │
                        ▼
                  Adaptive Engine
                        │
                        ▼
                  AI AGENT
                 UNDER TEST
                        │
                 [UNTRUSTED]
                        │
                        ▼
                 ┌─────────────┐
                 │ Tool Gateway│
                 └──────┬──────┘
                        │
                ┌───────▼────────┐
                │  Policy Engine │
                └───────┬────────┘
                        │
                ┌───────▼─────────┐
                │ Controlled Env. │
                └───────┬─────────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
           Tools       State      Faults
             │          │          │
             └──────────┼──────────┘
                        │
                        ▼
                Trajectory Store
                        │
                        ▼
                 State Analyzer
                        │
                        ▼
                  Snapshot Store
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
          Branch A               Branch B
             │                     │
             └──────────┬──────────┘
                        ▼
                Invariant Engine
                        │
                        ▼
                 Failure Store
                        │
             ┌──────────┼───────────┐
             ▼          ▼           ▼
          Replay    Metamorphic   Holdout
             │       Testing      Evaluation
             └──────────┼───────────┘
                        ▼
                  Metrics Store
                        │
                        ▼
                  Research Report
```

The core principle is:

> **The agent is the subject of evaluation, while the evaluator, environment, evidence pipeline, and hidden holdout boundaries must remain sufficiently controlled and auditable to make the resulting observations scientifically meaningful.**

---

# 63. Summary of Security-Critical Requirements

The most important requirements for implementation are:

| ID     | Requirement                 |
| ------ | --------------------------- |
| SR-001 | Explicit agent capabilities |
| SR-002 | Tool Gateway mediation      |
| SR-003 | Policy decision logging     |
| SR-004 | Environment isolation       |
| SR-005 | Branch isolation            |
| SR-006 | Snapshot integrity          |
| SR-007 | Hidden holdout protection   |
| SR-008 | Experiment isolation        |
| SR-009 | Evidence preservation       |
| SR-010 | Sensitive data handling     |
| SR-011 | Configuration validation    |
| SR-012 | Resource limits             |

These requirements establish the security foundation required for the adaptive evaluation experiments. They also prevent the evaluator from becoming a source of uncontrolled experimental bias, which would rather defeat the entire point of building an evaluator in the first place.
