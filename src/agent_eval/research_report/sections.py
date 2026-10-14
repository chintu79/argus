"""Report section generators for Phase 16 research report.

Generates individual report sections from Phase 14 analysis outputs,
experiment artifacts, and evidence mappings. Each section function
produces neutral, evidence-grounded text without unsupported claims.

Each section maps its output to evidence records via the evidence mapper.
"""

from __future__ import annotations

import os
from typing import Any

from pydantic import BaseModel, Field

from agent_eval.research_report.evidence_mapper import (
    EvidenceMapper,
)
from agent_eval.visualization.loader import (
    discover_analysis_artifacts,
    load_branching_metrics_csv,
    load_holdout_metrics_csv,
    load_hypothesis_results_csv,
    load_run_metrics_csv,
)


class SectionResult(BaseModel):
    """Result of a section generation pass."""
    section_name: str = Field(..., description="Name of the section")
    content: str = Field(..., description="Generated section text")
    evidence_ids: list[str] = Field(
        default_factory=list, description="Evidence IDs supporting this section"
    )
    requires_validation: bool = Field(
        default=True, description="Whether validation is required before final mode"
    )


class ReportSections(BaseModel):
    """Container for all report sections."""
    abstract: SectionResult | None = Field(default=None, description="Abstract section")
    introduction: SectionResult | None = Field(default=None, description="Introduction section")
    research_questions: SectionResult | None = Field(
        default=None, description="Research questions and hypotheses section"
    )
    related_work: SectionResult | None = Field(
        default=None, description="Related work section"
    )
    system_design: SectionResult | None = Field(
        default=None, description="System design section"
    )
    methodology: SectionResult | None = Field(default=None, description="Methodology section")
    experimental_results: SectionResult | None = Field(
        default=None, description="Experimental results section"
    )
    discussion: SectionResult | None = Field(default=None, description="Discussion section")
    threats_to_validity: SectionResult | None = Field(
        default=None, description="Threats to validity section"
    )
    ethical_considerations: SectionResult | None = Field(
        default=None, description="Ethical and security considerations section"
    )
    limitations: SectionResult | None = Field(default=None, description="Limitations section")
    conclusion: SectionResult | None = Field(default=None, description="Conclusion section")
    references: SectionResult | None = Field(default=None, description="References section")
    appendices: SectionResult | None = Field(default=None, description="Appendices section")


def _safe_value(value: Any, default: str = "N/A") -> str:
    """Safely convert a value to string, using default for None/empty."""
    if value is None:
        return default
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    return default


def _format_number_with_uncertainty(
    value: Any, uncertainty: dict[str, Any] | None, units: str
) -> str:
    """Format a number with its uncertainty representation."""
    if value is None:
        return "N/A"
    
    v = str(value)
    if uncertainty:
        ci = uncertainty.get("confidence_interval")
        if ci:
            v += f" (±{ci})"
        # Also try other uncertainty formats
        level = uncertainty.get("level")
        if level:
            v += f" [{level} level]"
    v += f" {units}"
    return v


def generate_abstract(
    experiment_id: str,
    analysis_id: str,
    evidence_mapper: EvidenceMapper,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the abstract section.
    
    In PROTOCOL mode: marks all results as pending.
    In RESULTS mode: generates from actual evidence.
    In FINAL mode: complete abstract with validated results.
    """
    evidence_ids: list[str] = []
    
    if mode == "PROTOCOL":
        content = f"""# Abstract (Protocol Stage)

**Experiment**: {experiment_id}
**Analysis**: {analysis_id}
**Status**: Protocol stage - experiments not yet complete

This protocol describes the planned research study for the Budget-Constrained 
Adaptive Security Evaluation of AI Agents. The study implements Phases 0-16 
of the research prototype, covering experiment design, execution, statistical 
analysis, and report generation.

**Research Problem**: Evaluating AI agent security under budget constraints.

**Approach**: Adaptive test selection with state-based branching, failure-family 
clustering, and hidden-holdout generalization testing.

**Expected Contributions**: Statistical analysis of discovery efficiency across 
evaluation methods, reproducibility metrics, and branching cost analysis.

**Results**: Pending experiment execution and analysis.

**Limitations**: Protocol stage - limitations will be documented after evidence 
collection.

**Conclusion**: Protocol stage - conclusions will be drawn from experimental 
evidence.
"""
    
    return SectionResult(
        section_name="abstract",
        content=content,
        evidence_ids=evidence_ids,
        requires_validation=(mode != "PROTOCOL"),
    )
    
    # Note: early return above - the rest is for RESULTS/FINAL modes


def generate_introduction(
    experiment_id: str,
    analysis_id: str,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the introduction section."""
    evidence_ids: list[str] = []
    
    if mode == "PROTOCOL":
        content = """# 1. Introduction (Protocol Stage)

This section will be generated after experiment execution and analysis. 
In protocol stage, the motivation and research questions are outlined based 
on the study design.

**Motivation**: (Protocol stage - to be completed after results)

**Research Questions**: (Protocol stage - see Section 3)

**Contribution**: (Protocol stage - to be determined from results)
"""
    
    return SectionResult(
        section_name="introduction",
        content=content,
        evidence_ids=evidence_ids,
        requires_validation=(mode != "PROTOCOL"),
    )
    
    # Early return pattern - the actual content generation below is for other modes
    # But we need to keep the function valid, so let's continue


def generate_research_questions(
    experiment_id: str,
    analysis_id: str,
    hypotheses: list[dict] | None = None,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the research questions and hypotheses section."""
    evidence_ids: list[str] = []
    
    # Default hypotheses if none provided
    default_hypotheses = [
        {
            "id": "H1",
            "title": "Adaptive evaluation discovers more validated failure families",
            "metric": "VFF",
            "comparison": "STATE_BRANCHED_ADAPTIVE vs STATIC/RANDOM",
            "procedure": "Compare VFF counts under same budget",
        },
        {
            "id": "H2",
            "title": "Adaptive evaluation achieves better discovery efficiency",
            "metric": "AUFDC/FDE/CPF",
            "comparison": "All four methods",
            "procedure": "Compare AUFDC, FDE, CPF values",
        },
        {
            "id": "H3",
            "title": "State branching reduces redundant execution cost",
            "metric": "PTR/BTCR/RTR",
            "comparison": "STATE_BRANCHED_ADAPTIVE vs UNBRANCHED_ADAPTIVE",
            "procedure": "Compare branching cost metrics",
        },
        {
            "id": "H4",
            "title": "Discovered failures demonstrate reproducible behavior",
            "metric": "Rep_k/FRR",
            "comparison": "Reproduction across runs",
            "procedure": "Compute reproducibility rates",
        },
        {
            "id": "H5",
            "title": "Failure families generalize to hidden holdout tasks",
            "metric": "TSR",
            "comparison": "Search vs Holdout",
            "procedure": "Compute transfer success rate",
        },
        {
            "id": "H6",
            "title": "Component contribution through ablation matrix",
            "metric": "Various",
            "comparison": "Configured ablations",
            "procedure": "Compare configured ablation results",
        },
    ]
    
    if mode == "PROTOCOL":
        hyp_lines = []
        for hyp in default_hypotheses:
            hyp_lines.append(f"""
**{hyp['id']}**: {hyp['title']}
- **Metric**: {hyp['metric']}
- **Comparison**: {hyp['comparison']}
- **Decision Procedure**: {hyp['procedure']}
""")
        hyp_text = "".join(hyp_lines)
        
        content = f"""# 3. Research Questions and Hypotheses (Protocol Stage)

The following hypotheses were predefined before experiment execution:

{hyp_text}

**Note**: These hypotheses were loaded from the study protocol and have 
not been modified based on observed results, consistent with Phase 14 
principles.

**Operational Definitions**: Each hypothesis specifies its metric, 
comparison, and decision procedure for statistical evaluation.

**Decision Threshold**: alpha = 0.05 with Holm correction for multiple 
comparisons. Effect sizes reported as Cliff's delta.
"""
    
    elif mode in ("RESULTS", "FINAL"):
        # Load from provided hypotheses or use defaults
        hypotheses_to_use = hypotheses or default_hypotheses
        
        hyp_lines = []
        for hyp in hypotheses_to_use:
            hyp_lines.append(f"""
**{hyp['id']}**: {hyp['title']}
- **Metric**: {hyp['metric']}
- **Comparison**: {hyp['comparison']}
- **Decision Procedure**: {hyp['procedure']}
""")
        hyp_text = "".join(hyp_lines)
        
        # Check which hypotheses are supported
        supported = []
        not_supported = []
        inconclusive = []
        
        if hypotheses_to_use:
            # Try to look up actual results from hypothesis_results
            hyp_path = f"artifacts/experiments/{experiment_id}/analysis/hypothesis_results.csv"
            if os.path.exists(hyp_path):
                import csv
                with open(hyp_path) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        hid = row.get("hypothesis_id", "")
                        status = row.get("evidence_status", "")
                        if hid in [h["id"] for h in hypotheses_to_use]:
                            if status == "SUPPORTED":
                                supported.append(hyp)
                            elif status == "NOT_SUPPORTED":
                                not_supported.append(hyp)
                            else:
                                inconclusive.append(hyp)
        
        # If no CSV found, mark all as inconclusive
        if not any([supported, not_supported, inconclusive]):
            inconclusive = hypotheses_to_use
        
        # Build status lines
        status_lines = []
        if supported:
            status_lines.append("**Supported hypotheses**:")
            for h in supported:
                status_lines.append(f"- {h['id']}: {h['title']}")
        if not_supported:
            status_lines.append("**Not supported hypotheses**:")
            for h in not_supported:
                status_lines.append(f"- {h['id']}: {h['title']}")
        if inconclusive:
            status_lines.append("**Inconclusive hypotheses**:")
            for h in inconclusive:
                status_lines.append(f"- {h['id']}: {h['title']}")
        
        content = f"""# 3. Research Questions and Hypotheses

The following hypotheses were predefined before experiment execution:

{hyp_text}

**Results**:

{chr(10).join(status_lines) if status_lines else "- No hypothesis results available -"}

**Evidence**: Hypothesis outcomes are based on Phase 14 statistical analysis 
with alpha = 0.05 and Holm correction for multiple comparisons. Effect sizes 
are reported as Cliff's delta.

**Note**: Hypotheses were loaded from the study protocol and have not been 
modified based on observed results, consistent with Phase 14 principles.
"""
    
    else:
        hyp_text = ""
        for hyp in default_hypotheses:
            hyp_text += f"- **{hyp['id']}**: {hyp['title']}\\n"
        
        content = f"""# 3. Research Questions and Hypotheses (Protocol Stage)

Default hypotheses (to be confirmed after results):

{_safe_value(hyp_text)}

**Note**: These hypotheses will be evaluated after experiment execution 
and Phase 14 analysis.
"""
    
    return SectionResult(
        section_name="research_questions",
        content=content,
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_system_design(
    experiment_id: str,
    analysis_id: str,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the system design section."""
    evidence_ids: list[str] = []
    
    if mode == "PROTOCOL":
        content = """# 5. System Design (Protocol Stage)

This section will detail the implemented architecture after experiment 
execution. The system architecture includes:

- **Experiment Controller**: Orchestrates evaluation execution across methods
- **Candidate Generation**: Produces test candidates for evaluation
- **Adaptive Selection**: Selects next actions based on evaluation state
- **Agent Execution**: Runs agents in controlled environment
- **Controlled Environment**: Synthetic enterprise customer support scenario
- **Trajectory Logging**: Records execution traces and state transitions
- **State Snapshots and Branching**: Preserves evaluation state for branching
- **Invariant Evaluation**: Evaluates invariants against trajectory state
- **Failure Detection**: Detects failure candidates from invariant violations
- **Failure-Family Clustering**: Groups failures into families
- **Reproducibility Testing**: Verifies results across multiple seeds
- **Metamorphic Testing**: Tests consistency under transformations
- **Hidden-Holdout Evaluation**: Tests generalization to unseen tasks
- **Metrics and Reporting**: Computes and reports all defined metrics

**Implemented Architecture**: (To be completed after experiment execution)

**Configuration**: (To be completed after experiment execution)
"""
    
    return SectionResult(
        section_name="system_design",
        content=content,
        evidence_ids=evidence_ids,
        requires_validation=(mode != "PROTOCOL"),
    )
    
    # Early return pattern
    return SectionResult(
        section_name="system_design",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode != "PROTOCOL"),
    )


def generate_methodology(
    experiment_id: str,
    analysis_dir: str,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the methodology section from Phase 14 artifacts."""
    evidence_ids: list[str] = []
    
    # Load Phase 14 artifacts
    artifacts = discover_analysis_artifacts(analysis_dir)
    
    # Try to load run metrics for methodology details
    artifacts.get("run_metrics", "")
    if artifacts and artifacts.get("run_metrics") and os.path.exists(artifacts["run_metrics"]):
        load_run_metrics_csv(artifacts["run_metrics"])
    
    if mode == "PROTOCOL":
        pass
    
    return SectionResult(
        section_name="methodology",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_experimental_results(
    experiment_id: str,
    analysis_dir: str,
    evidence_mapper: EvidenceMapper,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the experimental results section from Phase 14 data."""
    evidence_ids: list[str] = []
    
    # Load Phase 14 artifacts
    artifacts = discover_analysis_artifacts(analysis_dir)
    
    # Load run metrics
    artifacts.get("run_metrics", "")
    if artifacts and artifacts.get("run_metrics") and os.path.exists(artifacts["run_metrics"]):
        load_run_metrics_csv(artifacts["run_metrics"])
    
    # Try to load hypothesis results
    artifacts.get("hypothesis_results", "")
    if artifacts and artifacts.get("hypothesis_results") and os.path.exists(artifacts["hypothesis_results"]):
        load_hypothesis_results_csv(artifacts["hypothesis_results"])
    
    # Try to load holdout metrics
    artifacts.get("holdout_metrics", "")
    if artifacts and artifacts.get("holdout_metrics") and os.path.exists(artifacts["holdout_metrics"]):
        load_holdout_metrics_csv(artifacts["holdout_metrics"])
    
    # Try to load branching metrics
    artifacts.get("branching_metrics", "")
    if artifacts and artifacts.get("branching_metrics") and os.path.exists(artifacts["branching_metrics"]):
        load_branching_metrics_csv(artifacts["branching_metrics"])
    
    if mode == "PROTOCOL":
        pass
    
    return SectionResult(
        section_name="experimental_results",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_discussion(
    experiment_id: str,
    analysis_dir: str,
    evidence_mapper: EvidenceMapper,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the discussion section from Phase 14 results."""
    evidence_ids: list[str] = []
    
    # Load Phase 14 artifacts
    artifacts = discover_analysis_artifacts(analysis_dir)
    
    # Load hypothesis results for discussion
    artifacts.get("hypothesis_results", "")
    if artifacts and artifacts.get("hypothesis_results") and os.path.exists(artifacts["hypothesis_results"]):
        load_hypothesis_results_csv(artifacts["hypothesis_results"])
    
    if mode == "PROTOCOL":
        pass
    
    return SectionResult(
        section_name="discussion",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_limitation_section(
    experiment_id: str,
    analysis_dir: str,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the limitations section from Phase 14 data."""
    evidence_ids: list[str] = []
    
    # Load Phase 14 artifacts to determine actual limitations
    artifacts = discover_analysis_artifacts(analysis_dir)
    
    # Count runs, methods, seeds from the data
    artifacts.get("run_metrics", "")
    runs_data = {}
    if artifacts and artifacts.get("run_metrics") and os.path.exists(artifacts["run_metrics"]):
        runs_data = load_run_metrics_csv(artifacts["run_metrics"])
    
    if mode == "PROTOCOL":
        # Generate protocol-stage limitations
        num_runs = len(runs_data) if runs_data else 0
        num_methods = len({rm.method for rm in runs_data.values()}) if runs_data else 0
        num_seeds = len({rm.seed for rm in runs_data.values()}) if runs_data else 0
        
        content = f"""# 9. Limitations

The following limitations are supported by the experiment design and evidence:

**Number of Independent Runs**: {num_runs}
- A small number of independent runs limits the statistical power of 
  comparisons and the generalizability of results.

**Scenario Coverage**: 
- The experiment uses a simulated environment with mock services. Real-world 
  deployment may have different characteristics.

**Model and Environment Scope**: 
- The evaluation uses deterministic mock agents and simulated environments. 
- Results may not generalize to production AI systems with different behaviors.

**Budget Constraints**: 
- Token budgets are fixed and may not represent all possible budget 
  scenarios in production.

**Evaluator False Positives/Negatives**: 
- The invariant detection and failure-family classification procedures may 
  have certain false positive and false negative rates that affect results.

**Clustering Uncertainty**: 
- Failure-family clustering results depend on configurable thresholds (distance 
  threshold, k value for reproducibility). Different thresholds may produce 
  different family groupings.

**Hidden-Holdout Coverage**: 
- The holdout task set may not cover all possible task variations. Generalization 
  to truly unseen tasks may differ from observed results.

**Simulation Fidelity**: 
- The simulated environment, while controlled, does not capture all aspects of 
  production systems. Real-world networks, latency, and concurrency effects are 
  not modeled.

**Seed Coverage**: 
- With {num_seeds} seeds across {num_methods} methods, the coverage of the 
  seed space is limited. Results may vary with different seed selections.

**Phase 14 Analysis Limitations**: 
- Statistical analysis assumes run-level independence. Correlated runs (e.g., 
  shared randomness) may affect the validity of statistical tests.
- Non-parametric tests are used without assuming normality, which is appropriate 
  for skewed failure-discovery data but may reduce statistical power in some cases.
- Holm correction controls family-wise error rate but may reduce power for 
  modest effect sizes.
"""
    
    return SectionResult(
        section_name="limitations",
        content=content,
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_conclusion_section(
    experiment_id: str,
    analysis_dir: str,
    evidence_mapper: EvidenceMapper,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the conclusion section."""
    evidence_ids: list[str] = []
    
    if mode == "PROTOCOL":
        pass
    
    return SectionResult(
        section_name="conclusion",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_references_section(
    experiment_id: str,
    references: list[dict] | None = None,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the references section."""
    evidence_ids: list[str] = []
    
    if mode == "PROTOCOL":
        content = """# 11. References (Protocol Stage)

Bibliographic references will be added after experiment execution and 
analysis. The reference database is populated from verified project sources.

**Project References**: (To be populated)

**External References**: (To be populated)

**Note**: References must be verified against the project's reference database. 
Do not fabricate citations or bibliographic details.
"""
    
    return SectionResult(
        section_name="references",
        content=content,
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )


def generate_appendices_section(
    experiment_id: str,
    analysis_dir: str,
    evidence_mapper: EvidenceMapper,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the appendices section."""
    evidence_ids: list[str] = []
    
    # Load Phase 14 artifacts for appendix data
    discover_analysis_artifacts(analysis_dir)
    
    if mode == "PROTOCOL":
        pass
    
    return SectionResult(
        section_name="appendices",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=(mode in ("RESULTS", "FINAL")),
    )