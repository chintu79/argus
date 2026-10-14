# Demonstration Script

## Purpose

This script guides the user through the BCADE-AI demonstration, illustrating the complete pipeline from environment initialization through failure detection, validation, and metrics generation.

## Flow

### 1. Project Initialization

The demonstration begins by initializing the BCADE-AI project with the smoke test configuration. This sets up the repository structure, configuration files, and default experiment parameters.

### 2. Configuration Validation

The experiment configuration is validated to ensure all required parameters are present:
- Budget tokens (default: 50,000)
- Mock agent settings
- Invariant definitions
- Branching configuration
- Adaptive selector parameters

### 3. Controlled Environment Creation

A controlled evaluation environment is created with:
- Mock agent instance
- Defined invariants
- Seed-controlled randomness
- Budget tracking

### 4. Baseline Execution

A baseline execution run is performed to establish the starting state and collect initial metrics.

### 5. Adaptive Candidate Selection

The adaptive selector evaluates the candidate pool and selects evaluation candidates based on:
- Failure probability (estimated from previous runs)
- Coverage (diversity of explored space)
- Novelty (novel failure modes)
- Cost (budget consumption per candidate)

### 6. State Snapshot and Branching

The current execution state is snapshotted, and a branch is created from the snapshot. This allows related test conditions to be explored without rebuilding the entire trajectory.

### 7. Controlled Perturbation

A controlled perturbation is injected into the branched execution state. In the demonstration, this is a prompt injection attempt designed to test the `prompt_injection_guard` invariant.

### 8. Invariant Evaluation

During branched execution, invariants are continuously evaluated. The `prompt_injection_guard` invariant checks whether prompt injection attempts are detected and prevented.

### 9. Failure Detection

If an invariant violation is detected, a failure candidate is recorded. The failure candidate includes:
- The observed violation
- The invariant that was violated
- The execution state at the time of violation
- The budget consumed up to that point

### 10. Failure Reproduction

The failure candidate is independently replayed from the same initial state (or a different seed) to validate that the failure is consistent and not a stochastic artifact.

### 11. Failure Signature and Family Assignment

A failure signature is generated for the validated failure, and the failure is assigned to a family based on shared mechanism characteristics.

### 12. Metrics Generation

Evaluation metrics are computed:
- FDE (Failure Discovery Efficiency): validated failures per 1000 budget tokens
- CPF (Cost per Failure): budget tokens per validated failure
- TTFF (Time to First Failure): budget units until first validated failure
- Rep_k: reproducibility across k seeds
- FRR: failure reproduction rate

### 13. Visualization

A discovery curve visualization is generated, showing cumulative validated failures against budget units consumed across the adaptive selection runs.

### 14. Evidence Packaging

All evidence artifacts are packaged:
- Run-level metrics
- Failure assignments and families
- Visualization outputs
- Budget accounting records
- Hypothesis test results

## Termination

The demonstration completes after evidence packaging. All artifacts are persisted in the experiment directory for later review, audit, and reproducibility verification.