# Research Questions & Success Criteria

**Document ID:** RQSC-002  
**Document Type:** Research Questions and Success Criteria  
**Version:** 1.0  
**Status:** Baseline Specification  
**Related Document:** `01-project-specification.md`

---

# 1. Purpose

This document defines the research questions, hypotheses, evaluation objectives,
success criteria, measurable outcomes, and evidence requirements for the project:

> **Budget-Constrained Adaptive Security Evaluation of AI Agents**

The purpose of this document is to establish how the proposed system will be
scientifically evaluated.

It answers:

1. What exactly is being investigated?
2. What claims is the project attempting to evaluate?
3. What questions must the experiments answer?
4. What constitutes evidence for or against each research question?
5. What metrics will be used?
6. What conditions must be satisfied before a result can be considered successful?
7. Which results must remain empirical rather than being assumed in advance?

This document does **not** assume that the proposed method will outperform
the baselines. The experiments must determine that.

---

# 2. Research Project

## 2.1 Project Title

**Budget-Constrained Adaptive Security Evaluation of AI Agents**

---

## 2.2 Research Domain

The project operates at the intersection of:

- Agentic AI
- Generative AI
- AI security
- AI reliability
- Autonomous-agent evaluation
- Cybersecurity
- Adaptive testing
- Software testing
- Experimental AI evaluation

---

# 3. Research Problem

Autonomous AI agents operate through sequences of decisions and interactions
with tools and environments.

A single task may generate a trajectory containing:

```text
Task
  ↓
Decision
  ↓
Tool Call
  ↓
Observation
  ↓
State Transition
  ↓
Decision
  ↓
Tool Call
  ↓
...
  ↓
Final Outcome

Security or reliability failures may occur at intermediate points in this
trajectory.

Conventional independent scenario execution can repeatedly execute common
trajectory prefixes.

At the same time, evaluating a large number of scenarios can become expensive
under a limited token, execution, or time budget.

The research problem is therefore:

    How can an evaluation system allocate a limited budget adaptively while
    exploiting informative intermediate agent states to efficiently discover,
    validate, and generalize security and reliability failures?

4. Research Goal

The overall research goal is to experimentally evaluate whether combining:

Budget-Constrained Adaptive Test Selection
+
State-Based Execution Branching
+
Trajectory Analysis
+
Executable Invariant Checking
+
Failure Validation
+
Hidden-Holdout Evaluation

provides a useful approach for AI-agent security and reliability evaluation.

The project does not assume that the combination is superior.

Its purpose is to test that proposition experimentally.
5. Research Objectives
RO-01: Adaptive Evaluation

Determine whether adaptive selection can allocate evaluation resources more
efficiently than non-adaptive selection under equivalent budgets.
RO-02: State-Based Branching

Determine whether reusing suitable intermediate execution states can reduce
redundant execution compared with independently restarting complete scenarios.
RO-03: Failure Discovery

Measure the ability of the evaluation framework to discover security and
reliability failures.
RO-04: Failure Validation

Determine how many discovered failures can be reproduced through independent
execution.
RO-05: Failure Family Identification

Determine whether individual failures can be grouped into meaningful
failure families based on observable characteristics.
RO-06: Metamorphic Robustness

Determine whether discovered failure behavior persists or changes under
controlled transformations of the original scenarios.
RO-07: Generalization

Determine whether failure families discovered during exploration can be
detected in previously unseen holdout scenarios.
RO-08: Cost Analysis

Measure the computational and token costs associated with:

    independent execution

    adaptive selection

    state snapshotting

    state restoration

    branching

    failure analysis

    validation

    holdout evaluation

RO-09: Component Contribution

Determine the contribution of individual components through ablation experiments.
6. Central Research Question
CRQ

    Can budget-constrained adaptive test selection combined with
    state-based execution branching improve the efficiency of AI-agent
    security and reliability evaluation while preserving or improving
    failure validation and generalization?

This is the primary research question.

All secondary research questions should contribute evidence toward answering it.
7. Research Questions
RQ1: Adaptive Failure Discovery

    RQ1: Under an equivalent evaluation budget, does adaptive test selection
    discover more validated AI-agent failures than non-adaptive test selection?

Motivation

A limited evaluation budget requires decisions about which scenario should
be executed next.

The adaptive system attempts to prioritize candidates using information
obtained during previous executions.
Independent Variable

Test-selection strategy:

    Random

    Uniform

    Adaptive

Controlled Variables

Where possible, keep constant:

    agent

    model version

    prompt

    environment

    scenario pool

    total budget

    available tools

    security policies

    evaluation conditions

Dependent Variables

Primary:

    validated failures discovered

    validated failure families discovered

Secondary:

    failures per execution

    failures per 1K tokens

    failures per unit cost

    unique failure discovery rate

Evidence Required

The experiment must record:

strategy
budget
executions
tokens
failures
validated_failures
failure_families

The comparison must use equivalent evaluation budgets.
Interpretation

A higher number of discovered failures under the same budget would provide
evidence supporting improved discovery efficiency.

A lower or equivalent result would provide evidence that adaptive selection
does not provide the expected advantage under the tested conditions.

The experiment must not assume superiority beforehand.
8. RQ2: State-Based Branching Efficiency

    RQ2: Does state-based branching reduce redundant execution cost compared
    with independent execution of related scenarios?

Motivation

Multiple related scenarios may share execution prefixes.

State-based branching attempts to reuse an intermediate state rather than
replaying the entire prefix.
Comparison
Baseline

Scenario A
    ↓
Complete Execution

Scenario B
    ↓
Complete Execution

Scenario C
    ↓
Complete Execution

Branching Approach

Initial Execution
      ↓
Shared State S
   ↙  ↓  ↘
  A   B   C

Independent Variables

    branching enabled

    branching disabled

Dependent Variables

    total tokens

    total execution steps

    execution count

    prefix execution count

    snapshot cost

    restore cost

    branch cost

    total evaluation cost

Required Cost Model

The experiment must account for:

Total Cost =
Prefix Cost
+
Branch Cost
+
Snapshot Cost
+
Restore Cost
+
Analysis Cost

Success Evidence

Evidence for improved efficiency requires:

    comparable evaluation coverage,

    comparable failure discovery opportunity,

    measured cost reduction,

    accounting for snapshot and restoration overhead.

A reduction must not be claimed if snapshot or restoration costs are excluded.
9. RQ3: Failure Discovery Quality

    RQ3: Can the proposed framework discover security and reliability
    failures across diverse agent scenarios?

This question evaluates the breadth of failures detected rather than only
the total number.
Failure Categories

The evaluation should include categories such as:
Security

    unauthorized data access

    unauthorized tool access

    privilege violations

    policy bypass

    sensitive-data exposure

    unsafe external action

Reliability

    task failure

    incorrect tool use

    invalid tool arguments

    repeated action loops

    state inconsistency

    recovery failure

Robustness

    failure under wording changes

    failure under irrelevant context

    failure under equivalent task reformulation

    failure under environment variation

Metrics

    total candidate failures

    validated failures

    unique failure families

    failure category distribution

    severity distribution

    failure discovery rate

10. RQ4: Failure Reproducibility

    RQ4: To what extent are failures discovered by the system reproducible
    under independent replay?

Motivation

An observed failure may be caused by:

    stochastic model behavior

    environment randomness

    transient conditions

    unstable state

    scenario-specific interactions

Therefore, a single occurrence should not automatically be treated as
a stable finding.
Measurement

For each failure:

Reproduction Rate =
Successful Reproductions
/
Total Replay Attempts

Failure Stability Categories

The system may classify failures as:

    Stable

    Probabilistic

    Flaky

    Non-Reproducible

Required Reporting

Each validated failure should include:

failure_id
replay_attempts
successful_replays
reproduction_rate
stability_class

Important Rule

Low reproducibility does not automatically mean that a failure should be
deleted.

It should instead be classified appropriately and retained as evidence of
potential probabilistic behavior where applicable.
11. RQ5: Failure Family Quality

    RQ5: Can the system group individual failures into meaningful and
    distinguishable failure families?

Motivation

Multiple test cases may trigger the same underlying failure mechanism.

Counting every occurrence independently could exaggerate the diversity of
the discovered failure space.
Evaluation

The system should compare:

Individual Failures
        ↓
Failure Signatures
        ↓
Clusters
        ↓
Failure Families

Evaluation Dimensions

Failure families should be assessed for:

    internal similarity

    semantic consistency

    separation from other families

    representative quality

    taxonomy consistency

Required Output

Each family should have:

family_id
member_failures
representative_signature
category
severity
reproducibility
holdout_performance

12. RQ6: Metamorphic Robustness

    RQ6: Do discovered failure behaviors remain observable under
    controlled transformations of their originating scenarios?

Motivation

A failure that occurs only because of one exact wording or superficial
scenario detail may not represent a broader behavioral weakness.

Metamorphic testing investigates this without requiring a manually labeled
expected output for every transformed scenario.
Transformations

Potential transformations include:

    wording changes

    irrelevant context insertion

    equivalent task reformulation

    tool-order variation

    environment variation

    state perturbation

Evaluation

For each selected scenario:

Base Scenario
     ↓
Base Execution
     ↓
Invariant Result

Transformed Scenario
     ↓
Transformed Execution
     ↓
Invariant Result

Measurements

    transformation count

    preserved failures

    disappeared failures

    newly introduced failures

    invariant changes

    metamorphic violation rate

13. RQ7: Hidden-Holdout Generalization

    RQ7: Do failure families discovered during exploration generalize to
    unseen scenarios?

Motivation

A system may perform well on scenarios that resemble the scenarios from
which its failures were originally discovered.

This does not establish generalization.
Evaluation Structure

Discovery Scenarios
       ↓
Failure Discovery
       ↓
Failure Family Construction
       ↓
HOLDOUT SCENARIOS
       ↓
Independent Evaluation
       ↓
Failure-Family Detection

Holdout Requirements

Holdout scenarios must not influence:

    candidate selection

    failure-family construction

    adaptive reward estimation

    clustering decisions

before final holdout evaluation.
Metrics
Holdout Detection Rate

Correctly Detected Relevant Holdout Failures
/
Relevant Holdout Cases

Failure-Family Transfer Rate

Holdout Cases Matching Known Failure Families
/
Relevant Holdout Cases

Interpretation

Successful holdout detection provides evidence that the discovered failure
mechanism is not limited to the original discovery scenarios.

Failure to generalize is also a valid research result.
14. RQ8: Budget Efficiency

    RQ8: How does the proposed evaluation strategy trade evaluation cost
    against failure discovery and validation?

Cost Dimensions

The system must measure:

    tokens

    execution count

    execution time

    branch count

    snapshot count

    snapshot creation cost

    restoration cost

    analysis cost

    verification cost

Primary Efficiency Metrics
Failures per 1K Tokens

Validated Failures
/
(Total Tokens / 1000)

Failures per Execution

Validated Failures
/
Total Executions

Failure Families per Unit Cost

Validated Failure Families
/
Total Evaluation Cost

Important Requirement

Cost efficiency must never be calculated using only agent-generation
tokens if the proposed method introduces additional snapshot, restoration,
or analysis overhead.
15. RQ9: Component Contribution

    RQ9: Which components of the proposed framework contribute to
    evaluation performance?

The complete method contains multiple mechanisms.

A positive result from the entire system does not establish that every
component is necessary.
Components for Ablation

The evaluation should consider removing:

    Adaptive selection

    State branching

    Novelty component

    Uncertainty / variance component

    Severity component

    Reproducibility validation

    Metamorphic testing

    Hidden-holdout validation

Comparison

Full System
    ↓
Remove One Component
    ↓
Re-run Experiment
    ↓
Compare Metrics

16. RQ10: Reliability of the Evaluation Framework

    RQ10: Does the evaluation framework itself produce consistent and
    reproducible measurements across repeated experiments?

This question evaluates the evaluator.
Required Checks

Repeated experiments should examine:

    failure counts

    family counts

    cost

    selection behavior

    reproducibility measurements

    generalization measurements

Experimental Controls

Record:

    random seed

    model version

    prompt version

    environment version

    scenario version

    code version

    configuration

17. Research Hypotheses

The following hypotheses define propositions to be experimentally tested.

They are not expected results.
H1: Adaptive Selection Hypothesis

Under equivalent evaluation budgets, adaptive test selection will produce
a different failure discovery efficiency than non-adaptive selection.

The experiment will determine the direction and magnitude of the difference.
H2: Branching Efficiency Hypothesis

For scenarios with sufficiently reusable intermediate states, state-based
branching will reduce redundant execution compared with independent
full-scenario execution.
H3: Validation Hypothesis

Independent replay will distinguish stable failures from probabilistic,
flaky, and non-reproducible behaviors.
H4: Failure-Family Hypothesis

Clustering failure signatures will identify groups of related failures
that represent common behavioral mechanisms.
H5: Generalization Hypothesis

Some discovered failure families will be observable in unseen holdout
scenarios.

The proportion of such cases must be experimentally determined.
H6: Component Contribution Hypothesis

Removing important components of the proposed framework will change
failure discovery, validation, cost, or generalization performance.
18. Primary Success Criteria

The project is considered experimentally successful if it can produce
reliable evidence addressing the central research question.

The following are required.
SC-01: Working Evaluation Loop

The system must successfully execute the complete evaluation pipeline:

Scenario
→ Selection
→ Agent Execution
→ Trajectory
→ State Analysis
→ Branching
→ Invariant Checking
→ Failure Detection
→ Validation
→ Holdout Evaluation
→ Metrics

SC-02: Budget Enforcement

The evaluation system must enforce configured limits.

Examples:

Maximum Tokens
Maximum Executions
Maximum Branches
Maximum Replay Attempts
Maximum Evaluation Time

No experiment should silently exceed its configured budget.
SC-03: Reproducible Experiment Configuration

Every experiment must record sufficient configuration information to reproduce
the experiment as closely as technically possible.

Required information includes:

    experiment ID

    model version

    prompt version

    environment version

    scenario version

    code version

    random seed

    budget

    strategy configuration

SC-04: Measurable Failure Discovery

The system must produce structured failure records containing:

    failure ID

    violated invariant

    evidence

    execution ID

    trajectory position

    failure category

    severity

    signature

SC-05: Independent Validation

At least selected discovered failures must be independently replayed.

The system must calculate reproduction statistics.
SC-06: Failure Family Construction

The system must support grouping related failures into failure families.

The grouping process must be reproducible from stored data.
SC-07: Hidden-Holdout Evaluation

The system must support evaluation on scenarios that were not used during
failure discovery.

Holdout results must remain separated from discovery data until evaluation.
SC-08: Baseline Comparison

The proposed method must be comparable against at least:

    random selection

    uniform selection

    independent execution

Additional component-level baselines should be included where feasible.
SC-09: Cost Accounting

The system must measure the actual costs introduced by:

    execution

    branching

    snapshot creation

    restoration

    analysis

    verification

SC-10: Real Experimental Data

All final research metrics must originate from actual experiment data.

The dashboard and reports must not use fabricated values.
19. Secondary Success Criteria

The following strengthen the research implementation but should not be
confused with assumptions of positive results.
SC-11: Deterministic Infrastructure

Where technically possible, identical configurations and seeds should
produce consistent infrastructure behavior.
SC-12: Failure Injection Detection

The evaluation framework should successfully detect intentionally
introduced known failures.

This validates the invariant and failure-detection pipeline.
SC-13: Snapshot Integrity

A restored snapshot should produce a state equivalent to the recorded
snapshot within the defined state-equivalence criteria.
SC-14: Branch Lineage

Every branch should be traceable to:

Experiment
→ Run
→ State
→ Snapshot
→ Branch

SC-15: Trace Completeness

A completed execution should contain sufficient trace information to
reconstruct the evaluated trajectory.
20. Metric Groups

The project's metrics are divided into six major groups.
20.1 Discovery Metrics

    candidate tests executed

    candidate failures

    validated failures

    unique failure families

    failure discovery rate

20.2 Efficiency Metrics

    tokens consumed

    executions

    branches

    failures per execution

    failures per 1K tokens

    families per unit cost

20.3 Reproducibility Metrics

    replay attempts

    successful reproductions

    reproduction rate

    stability category

20.4 Generalization Metrics

    holdout scenarios

    relevant holdout cases

    detected holdout failures

    holdout detection rate

    failure-family transfer rate

20.5 Reliability Metrics

    task success rate

    unsafe action rate

    recovery success rate

    recovery steps

    invalid tool calls

20.6 System Overhead Metrics

    snapshot creation time

    snapshot size

    restoration time

    branch creation time

    analysis time

    storage consumption

21. Statistical Success Requirements

A result should not be judged from a single experimental run where
stochasticity can materially affect the outcome.

Where practical, experiments should use multiple independent seeds.

For comparative results, report:

    sample size

    mean

    median where appropriate

    standard deviation or variance

    confidence intervals where appropriate

    effect size where appropriate

    random seeds

    experimental configuration

The exact statistical tests will be defined in the experimental methodology
and statistical analysis documentation.
22. Fair Comparison Requirements

Comparisons between methods must use comparable conditions.

The following should remain consistent unless intentionally varied:

    agent model

    model version

    system prompt

    tools

    environment

    scenario pool

    security policies

    evaluation budget

    holdout set

    evaluation duration

    validation procedure

If a condition differs, the experiment must explicitly document the difference.
23. Budget Equivalence

The proposed method and baselines must be compared under clearly defined
budget conditions.

Possible budget controls include:
Token Budget

All methods receive the same maximum token budget.
Execution Budget

All methods receive the same maximum number of executions.
Time Budget

All methods receive the same maximum wall-clock time.

The chosen budget definition must be reported for every comparison.
24. What Does Not Count as Success

The following are not sufficient evidence for project success:

    a polished dashboard

    a working UI

    a large number of generated scenarios

    a large number of detected anomalies

    hard-coded metrics

    simulated charts presented as results

    one successful failure demonstration

    one successful branch demonstration

    an unvalidated UCB-V implementation

    an unsupported percentage of token savings

    taxonomy labels without verified mappings

    claims of OWASP compliance

    a successful demo without baseline comparison

The research contribution must be supported by measured experiments.
25. Failure Conditions for the Research

The project should explicitly record when a research hypothesis is not supported.

Examples include:

    adaptive selection does not improve discovery efficiency

    branching overhead exceeds savings

    failure families do not generalize

    replay rates are too low for reliable validation

    adaptive selection becomes overly exploitative

    clustering produces unstable families

    holdout performance collapses

    the evaluation infrastructure introduces significant measurement bias

These are legitimate research findings.

The system should not be engineered to manufacture positive results.
26. Evidence Hierarchy

Research claims should follow this evidence hierarchy.

Level 1
Observed Execution

        ↓

Level 2
Invariant Violation

        ↓

Level 3
Independent Replay

        ↓

Level 4
Failure Family Evidence

        ↓

Level 5
Metamorphic Validation

        ↓

Level 6
Hidden-Holdout Evidence

        ↓

Level 7
Cross-Experiment Replication

A claim should not be presented at a stronger level than the available
evidence supports.
27. Research Result Categories

Final results should be classified into categories such as:
Supported

Evidence is consistent with the research hypothesis under the tested
conditions.
Not Supported

The experiment does not provide evidence supporting the hypothesis.
Inconclusive

The experiment does not provide sufficient evidence to determine the result.
Conditional

The effect appears only under particular conditions.

For example:

    State branching improved efficiency only for scenarios with high prefix
    overlap.

This is more useful than forcing every result into “worked” or “failed.”
28. Minimum Experimental Matrix

The initial experimental matrix should include:
Experiment	Selection	Branching	Purpose
E1	Random	Off	Random baseline
E2	Uniform	Off	Uniform baseline
E3	Adaptive	Off	Measure adaptive selection
E4	Random	On	Measure branching independently
E5	Uniform	On	Branching baseline
E6	Adaptive	On	Proposed combined method

Each experiment should use comparable scenario pools and budgets.
29. Minimum Validation Matrix

For discovered failures:
Validation	Required
Initial detection	Yes
Independent replay	Yes
Failure signature	Yes
Failure-family assignment	Yes
Metamorphic testing	Selected failures
Hidden holdout	Validated families
Cross-seed replay	Where practical
30. Success Criteria Summary

The project should ultimately answer the following:

1. Can the system discover failures?
        ↓
2. Can it discover them under a constrained budget?
        ↓
3. Does adaptive selection improve resource allocation?
        ↓
4. Does state branching reduce redundant execution?
        ↓
5. Can discovered failures be reproduced?
        ↓
6. Can related failures be grouped into families?
        ↓
7. Do those families survive controlled transformations?
        ↓
8. Do they generalize to unseen scenarios?
        ↓
9. What is the cost of achieving these results?
        ↓
10. Which components actually contribute?

31. Final Research Success Definition

The project will be considered a successful research implementation when it
can provide a reproducible experimental framework that:

    Evaluates AI agents in controlled environments.

    Generates and executes diverse security and reliability scenarios.

    Selects evaluations under an explicit budget.

    Captures observable execution trajectories.

    Identifies and reuses supported intermediate states.

    Creates and evaluates alternative execution branches.

    Detects invariant violations using executable checks.

    Produces evidence-backed failure records.

    Validates failures through independent replay.

    Groups related failures into failure families.

    Evaluates selected failures using metamorphic transformations.

    Tests discovered failure families on hidden scenarios.

    Measures generalization.

    Compares the proposed approach against defined baselines.

    Quantifies all relevant evaluation costs.

    Records sufficient metadata for reproducibility.

    Produces results directly from experimental data.

The project does not require the proposed approach to outperform every
baseline to be scientifically successful.

A well-controlled experiment showing that the proposed approach does not
provide an expected advantage is still a valid research outcome.
32. Final Research Question

All experiments ultimately contribute to answering:

    Under a fixed and explicitly measured evaluation budget, does combining
    adaptive test selection with trajectory-aware state-based branching enable
    more efficient discovery and validation of AI-agent security and reliability
    failures, while producing failure families that reproduce and generalize
    to unseen scenarios?


### Document boundary

This document should remain focused on **research questions, hypotheses, measurable outcomes, and what counts as evidence**.

The next document, **`03-system-architecture.md`**, should not repeat all of this. It should take these requirements and turn them into the concrete architecture: services/modules, data flows, control flows, state management, storage, execution engine, selector, snapshot manager, failure engine, validation engine, and their interfaces.