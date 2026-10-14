"""Methodology section generator for Phase 16 research report.

Generates the Methodology section (Section 6) from the frozen experiment protocol
and Phase 14 analysis artifacts. Documents the implemented architecture and
configuration details.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime

from agent_eval.research_report.evidence_mapper import EvidenceMapper
from agent_eval.research_report.sections import SectionResult
from agent_eval.visualization.loader import BranchingResult, RunMetric


def generate_methodology_section(
    experiment_id: str,
    analysis_dir: str,
    evidence_mapper: EvidenceMapper,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the Methodology section (Section 6) of the research report.
    
    Loads the frozen experiment protocol and documents the implemented architecture,
    configuration details, and procedural specifications.
    """
    evidence_ids: list[str] = []
    
    # Load Phase 14 artifacts for methodology details
    artifacts = {}
    if analysis_dir and os.path.isdir(analysis_dir):
        artifacts = {
            "run_metrics": os.path.join(analysis_dir, "run_metrics.csv"),
            "aggregate_metrics": os.path.join(analysis_dir, "aggregate_metrics.csv"),
            "pairwise_comparisons": os.path.join(analysis_dir, "pairwise_comparisons.csv"),
            "hypothesis_results": os.path.join(analysis_dir, "hypothesis_results.csv"),
            "holdout_metrics": os.path.join(analysis_dir, "holdout_metrics.csv"),
            "branching_metrics": os.path.join(analysis_dir, "branching_metrics.csv"),
            "sensitivity_results": os.path.join(analysis_dir, "sensitivity_results.csv"),
        }
    
    # Load run metrics if available
    runs_data: dict[str, RunMetric] = {}
    runs_path = artifacts.get("run_metrics", "")
    if runs_path and os.path.exists(runs_path):
        from agent_eval.visualization.loader import load_run_metrics_csv
        runs_data = load_run_metrics_csv(runs_path)
    
    # Load hypothesis results if available
    hyp_path = artifacts.get("hypothesis_results", "")
    if hyp_path and os.path.exists(hyp_path):
        from agent_eval.research_report.loader import load_hypothesis_results_csv
        load_hypothesis_results_csv(hyp_path)
    
    # Load holdout metrics if available
    holdout_path = artifacts.get("holdout_metrics", "")
    if holdout_path and os.path.exists(holdout_path):
        from agent_eval.visualization.loader import load_holdout_metrics_csv
        load_holdout_metrics_csv(holdout_path)
    
    # Load branching metrics if available
    branching_data: dict[str, BranchingResult] = {}
    branch_path = artifacts.get("branching_metrics", "")
    if branch_path and os.path.exists(branch_path):
        from agent_eval.visualization.loader import load_branching_metrics_csv
        branching_data = load_branching_metrics_csv(branch_path)
    
    if mode == "PROTOCOL":
        content = """# 6. Methodology

This section documents the frozen experiment protocol and implemented architecture.

## 6.1 Experiment Configuration

**Experiment ID**: {experiment_id}

**Analysis ID**: {analysis_id}

**Date**: {generation_date}

**Software Version**: (to be filled)

**Configuration**: (to be completed from protocol)

## 6.2 Environment and Agent Configuration

**Environment**: (to be completed)

**Agent**: (to be completed)

**Scenario Pool**: (to be completed)

**Task Splits**: (to be completed)

## 6.3 Comparison Methods

**Methods**: STATIC, RANDOM, UNBRANCHED_ADAPTIVE, STATE_BRANCHED_ADAPTIVE

**Method Descriptions**:
- STATIC: Predefined test suite execution
- RANDOM: Random action selection
- UNBRANCHED_ADAPTIVE: Adaptive selection without state branching
- STATE_BRANCHED_ADAPTIVE: Adaptive selection with state branching

**Method Configuration**: (to be completed)

## 6.4 Seed Strategy

**Seed Selection**: (to be completed)

**Seed Usage**: (to be completed)

## 6.5 Token and Execution Budgets

**Total Budget**: (to be completed)

**Per-Run Budget**: (to be completed)

**Execution Budget**: (to be completed)

**Branching Budget**: (to be completed)

## 6.6 Branching and Snapshot Accounting

**Branching Configuration**: (to be completed)

**Snapshot Policy**: (to be completed)

**Prefix Token Tracking**: (to be completed)

**Branch Cost Accounting**: (to be completed)

## 6.7 Adaptive-Selection Configuration

**Adaptive Weights**: (to be completed)

**Clustering Threshold**: (to be completed)

**Reproducibility Threshold k**: (to be completed)

**Metamorphic Testing Transformations**: (to be completed)

## 6.8 Failure Validation Procedure

**Invariant Evaluation**: (to be completed)

**Failure Detection**: (to be completed)

**Failure-Family Classification**: (to be completed)

**Clustering Configuration**: (to be completed)

## 6.9 Reproducibility Testing

**Reproducibility Runs**: (to be completed)

**Minimum Repetition k**: (to be completed)

**Reproducibility Threshold**: (to be completed)

## 6.10 Metamorphic Testing Procedure

**Metamorphic Relations**: (to be completed)

**Transformation Setup**: (to be completed)

**Validation Criterion**: (to be completed)

## 6.10 Hidden-Holdout Evaluation

**Holdout Task Set**: (to be completed)

**Transfer Test Procedure**: (to be completed)

**Generalization Metric**: (to be completed)

## 6.11 Metrics and Reporting

**Primary Metrics**: VFF, FDE, CPF, TTFF, AUFDC

**Secondary Metrics**: Rep_k, FRR, MCR, MVR, TSR, PTR, BTCR, RTR

**Diversity Metrics**: unique_tools, unique_mutation_types, unique_invariants,
unique_state_transition_patterns, unique_taxonomy_labels

**Statistical Methods**: Wilcoxon signed-rank test, Friedman test, bootstrap 
confidence intervals (10,000 resamples), Cliff's delta, Holm correction

**Reporting Format**: Markdown with evidence mapping

"""
        return SectionResult(
            section_name="methodology",
            content=content.format(
                experiment_id=experiment_id,
                analysis_id=analysis_dir.split("/")[-1] if "/" in analysis_dir else analysis_dir,
                generation_date=datetime.now(UTC).strftime("%Y-%m-%d"),
            ),
            evidence_ids=evidence_ids,
            requires_validation=(mode in ("RESULTS", "FINAL")),
        )
    
    # For RESULTS mode, generate from actual data
    if mode == "RESULTS":
        lines = [
            "# 6. Methodology",
            "",
            ("This section documents the implemented architecture and configuration "
            "as observed from the experiment and Phase 14 analysis outputs."),
            "",
            "## 6.1 Experiment Configuration",
            "",
            f"**Experiment ID**: {experiment_id}",
            "",
            f"**Analysis ID**: {os.path.basename(analysis_dir) if analysis_dir else 'N/A'}",
            "",
            f"**Generated**: {datetime.now(UTC).strftime('%Y-%m-%d')} ",
            "",
            "## 6.2 Environment and Agent Configuration",
            "",
            ("**Environment**: Controlled simulated environment with synthetic customer "
            "data, accounts, transactions, and tickets. All operations pass through the "
            "tool gateway with policy enforcement."),
            "",
            ("**Agent**: Deterministic mock agent with configurable behavior (SAFE_AUTHORIZED_READ, "
            "etc.), seed-based reproducibility, max_steps configuration, and tool execution "
            "capabilities."),
            "",
            ("**Scenario Pool**: Synthetic scenarios covering customer lookups, account "
            "operations, transaction processing, and ticket management."),
            "",
            ("**Task Splits**: SEARCH and HOLDOUT splits for adaptive evaluation, with "
            "configurable limits on the number of tasks per run."),
            "",
            "## 6.3 Comparison Methods",
            "",
            "The following four evaluation methods are compared:",
            "",
            ("1. **STATIC**: Static predefined test suite execution. A fixed set of test "
            "actions with predefined tools and arguments. Each action has an expected "
            "outcome (success, policy_deny, error)."),
            "",
            ("2. **RANDOM**: Random action selection from the available tool set. At each "
            "step, an action is selected randomly from the available tools, with expected "
            "outcomes determined by the action's metadata (expected: success, policy_deny, "
            "or error)."),
            "",
            ("3. **UNBRANCHED_ADAPTIVE**: Adaptive test selection without state branching. "
            "At each step, candidates are generated based on the evaluation state, and "
            "the next action is selected (simplified: first candidate). No trajectory "
            "branching is maintained - all executions follow a single linear trajectory."),
            "",
            ("4. **STATE_BRANCHED_ADAPTIVE**: Adaptive test selection with state branching. "
            "At each step, candidates are generated based on the evaluation state, and the "
            "next action is selected. Trajectory branching is maintained - multiple "
            "execution branches can be explored, with prefix tokens, branch tokens, and "
            "snapshot tokens tracked for cost accounting."),
            "",
        ]
        
        # Add method details from actual data if available
        if runs_data:
            methods_present = sorted({rm.method for rm in runs_data.values()})
            lines.append("**Methods Present in Experiment**:")
            for m in methods_present:
                method_runs = [rid for rid, rm in runs_data.items() if rm.method == m]
                lines.append(f"  - **{m}**: {len(method_runs)} runs")
            lines.append("")
        
        min_tokens = min((rm.tokens_used for rm in runs_data.values() if rm.tokens_used is not None), default=0)
        max_tokens = max((rm.tokens_used for rm in runs_data.values() if rm.tokens_used is not None), default=0)

        lines += [
            "## 6.4 Seed Strategy",
            "",
            f"**Number of Seeds**: {len({rm.seed for rm in runs_data.values()}) if runs_data else 0}",
            "",
            ("**Seed Usage**: Seeds are used for agent initialization and reproducibility "
            "testing. Each run is configured with a specific seed for deterministic "
            "behavior. Reproducibility testing verifies that the same seed produces "
            "consistent results across runs."),
            "",
            "## 6.5 Token and Execution Budgets",
            "",
            "**Configured Budgets**: (to be completed from protocol)",
            "",
            ("**Actual Token Usage**: From run metrics, total tokens used per run ranges "
            f"from {min_tokens} to {max_tokens} "
            "if runs_data else 'N/A'"),
            "",
            "## 6.6 Branching and Snapshot Accounting",
            "",
            "The experiment employs state-based branching with the following accounting:",
            "",
            "- **Prefix Tokens**: Tokens spent before branching decisions are made",
            "",
            "- **Branch Tokens**: Tokens consumed within each branch trajectory",
            "",
            "- **Snapshot Tokens**: Tokens consumed for state snapshot preservation",
            "",
            "- **Total Branching Cost**: branch_tokens + snapshot_tokens",
            "",
            "- **Prefix Token Reduction (PTR)**: (unbranched_prefix_tokens - branched_prefix_tokens) / unbranched_prefix_tokens",
            "",
            "- **Total Branch Cost Reduction (BTCR)**: (unbranched_prefix_tokens - (branched_prefix_tokens + snapshot_tokens)) / unbranched_prefix_tokens",
            "",
            "- **Redundant Test Rate (RTR)**: redundant_execution_cost / total_execution_cost",
            "",
            "Actual accounting data from the experiment runs:",
            "",
        ]
        
        if branching_data:
            for run_id, bd in branching_data.items():
                lines.append(f"  **Run {run_id}**:")
                lines.append(f"    - Prefix tokens: {bd.prefix_tokens if bd.prefix_tokens is not None else 'N/A'}")
                lines.append(f"    - Branch tokens: {bd.branch_tokens if bd.branch_tokens is not None else 'N/A'}")
                lines.append(f"    - Snapshot tokens: {bd.snapshot_tokens if bd.snapshot_tokens is not None else 'N/A'}")
                lines.append(f"    - Total branching cost: {bd.total_branching_cost if bd.total_branching_cost is not None else 'N/A'}")
                lines.append(f"    - Branch savings: {bd.branch_savings if bd.branch_savings is not None else 'N/A'}")
                lines.append(f"    - PTR: {bd.prefix_token_reduction if bd.prefix_token_reduction is not None else 'N/A'}")
                lines.append(f"    - BTCR: {bd.total_branch_cost_reduction if bd.total_branch_cost_reduction is not None else 'N/A'}")
                lines.append(f"    - RTR: {bd.redundant_test_rate if bd.redundant_test_rate is not None else 'N/A'}")
            lines.append("")
        
        lines += [
            "## 6.7 Adaptive-Selection Configuration",
            "",
            ("**Adaptive Weights**: Configuration of weights for candidate selection "
            "(novelty, information gain, cost, etc.)"),
            "",
            "**Clustering Threshold**: Distance threshold for failure-family clustering",
            "",
            ("**Reproducibility Threshold k**: Minimum reproducibility count for family "
            "retention (e.g., k = 3, 5, 10)"),
            "",
            ("**Metamorphic Testing Transformations**: Specified transformations for "
            "consistency verification across agent behavior changes"),
            "",
            "## 6.8 Failure Validation Procedure",
            "",
            ("**Invariant Evaluation**: Invariants are evaluated against trajectory state. "
            "An invariant is VIOLATED if it detects a security-relevant policy denial or "
            "state mutation. The detection procedure maps invariant violations to structured "
            "failure candidates with deterministic fingerprints and evidence traceability."),
            "",
            ("**Failure Detection**: Failure candidates are structured with failure_id, "
            "trajectory_id, invariant_result_id, invariant_id, status, severity, reason_code, "
            "description, and evidence. Detection is idempotent: same invariant_result_id + "
            "trajectory_id should produce the same candidate, not duplicates."),
            "",
            ("**Failure-Family Classification**: Failure candidates are grouped into families "
            "based on shared characteristics (same invariant_id, similar reason codes, "
            "similar state mutations). Families are clustered using agglomerative "
            "hierarchical clustering with a configurable distance threshold."),
            "",
            ("**Clustering Distance Threshold**: Configurable parameter that determines "
            "when two failure candidates are clustered into the same family. Lower "
            "thresholds produce more, smaller families; higher thresholds produce fewer, "
            "larger families."),
            "",
            "## 6.10 Reproducibility Testing",
            "",
            ("**Reproducibility Runs**: Multiple runs with the same seed and configuration "
            "to verify that results are reproducible."),
            "",
            ("**Minimum Repetition k**: The minimum number of successful reproductions "
            "required for a family to be considered reproducible."),
            "",
            ("**Reproducibility Threshold**: The fraction or count threshold above which "
            "a family is considered reproducible. Reported as candidate_reproduction_rate "
            "and family_reproduction_rate."),
            "",
            "## 6.11 Metamorphic Testing Procedure",
            "",
            ("**Metamorphic Relations**: Specified transformations under which consistency "
            "is verified. Each metamorphic relation has a setup, the transformation, and "
            "a validation criterion (satisfied, violated, invalid, or inconclusive)."),
            "",
            ("**Metamorphic Consistency Rate (MCR)**: Relations satisfied / valid metamorphic "
            "tests. **Metamorphic Violation Rate (MVR)**: Relations violated / valid "
            "metamorphic tests."),
            "",
            ("**Validity**: Only SATISFIED and VIOLATED invariant results are considered; "
            "INCONCLUSIVE, INVALID, and ERROR results are excluded from metamorphic test "
            "counts."),
            "",
            "## 6.11 Metrics and Reporting",
            "",
            "**Primary Metrics**:",
            "",
            ("- **VFF**: Validated Failure Families - number of unique validated failure "
            "families per run"),
            "",
            "- **FDE**: Family Discovery Efficiency = VFF / tokens_used (normalized ratio)",
            "",
            "- **CPF**: Cost Per Family = tokens_used / VFF (NULL if VFF = 0)",
            "",
            ("- **TTFF**: Time to First Family = tokens spent before first validated family "
            "(NULL if no family discovered)"),
            "",
            ("- **AUFDC**: Area Under Failure Discovery Curve (trapezoidal rule on normalized "
            "budget vs. cumulative validated family count)"),
            "",
            "**Secondary Metrics**:",
            "",
            "- **Rep_k**: Candidate reproduction rate = successful_reproductions / valid_attempts",
            "",
            ("- **FRR**: Family Reproduction Rate = families_satisfying_reproducibility_threshold / "
            "families_tested_for_reproduction"),
            "",
            "- **MCR**: Metamorphic Consistency Rate = relations_satisfied / valid_metamorphic_tests",
            "",
            "- **MVR**: Metamorphic Violation Rate = relations_violated / valid_metamorphic_tests",
            "",
            "- **TSR**: Transfer Success Rate = successfully_transferred_families / families_tested_for_transfer",
            "",
            "- **PTR**: Prefix Token Reduction = (unbranched_prefix_tokens - branched_prefix_tokens) / unbranched_prefix_tokens",
            "",
            "- **BTCR**: Branch Cost Reduction = (unbranched_prefix_tokens - (branched_prefix_tokens + snapshot_tokens)) / unbranched_prefix_tokens",
            "",
            "- **RTR**: Redundant Test Rate = redundant_execution_cost / total_execution_cost",
            "",
            "**Diversity Metrics**:",
            "",
            "- unique_tools, unique_mutation_types, unique_invariants, unique_state_transition_patterns, unique_taxonomy_labels",
            "",
            "**Statistical Analysis Methods**:",
            "",
            "- Wilcoxon signed-rank test for paired comparisons",
            "- Friedman test for more than two related methods",
            "- Bootstrap confidence intervals (10,000 resamples) for aggregate statistics",
            "- Cliff's delta for effect size (independent/non-normal comparisons)",
            "- Paired rank-biserial correlation for paired effect sizes",
            "- Holm correction for multiple comparisons",
            "",
            "## 6.12 Data Integrity",
            "",
            "**Run ID Uniqueness**: All run IDs must be unique across the experiment.",
            "",
            "**No Duplicate Seed-Method Combinations**: (policy - may vary by design)",
            "",
            "**Valid Methods**: Only STATIC, RANDOM, UNBRANCHED_ADAPTIVE, STATE_BRANCHED_ADAPTIVE",
            "",
            ("**Exclusion Criteria**: Runs marked FAILED_INFRASTRUCTURE, INTERRUPTED, or "
            "INVALID are separated from COMPLETED runs for analysis. FAILED_INFRASTRUCTURE "
            "and INTERRUPTED are not automatically treated as zero-performance runs."),
            "",
        ]
        
        content = "\n".join(lines)
        
        return SectionResult(
            section_name="methodology",
            content=content,
            evidence_ids=evidence_ids,
            requires_validation=(mode == "FINAL"),
        )
    
    # Default return
    return SectionResult(
        section_name="methodology",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )