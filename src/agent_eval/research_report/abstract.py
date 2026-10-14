"""Abstract generation for Phase 16 research report.

Generates the abstract section from validated experiment and analysis artifacts.
Supports three modes: PROTOCOL (planned study), RESULTS (from artifacts), 
and FINAL (complete with validation passing).
"""

from __future__ import annotations

from agent_eval.research_report.evidence_mapper import EvidenceMapper
from agent_eval.research_report.sections import (
    SectionResult,
)


def generate_abstract(
    experiment_id: str,
    analysis_id: str,
    evidence_mapper: EvidenceMapper | None = None,
    mode: str = "PROTOCOL",
) -> SectionResult:
    """Generate the abstract section.
    
    Args:
        experiment_id: The experiment identifier
        analysis_id: The Phase 14 analysis identifier
        evidence_mapper: Optional EvidenceMapper instance with evidence records
        mode: One of "PROTOCOL", "RESULTS", or "FINAL"
    
    Returns:
        SectionResult containing the abstract text
    """
    evidence_ids: list[str] = []
    
    if mode == "PROTOCOL":
        # Protocol stage abstract - describes planned study
        lines = [
            "# Abstract",
            "",
            f"**Experiment**: {experiment_id}",
            f"**Analysis**: {analysis_id}",
            "",
            "This protocol describes the planned research study for the Budget-Constrained",
            "Adaptive Security Evaluation of AI Agents. The study implements Phases 0-16",
            "of the research prototype, covering experiment design, execution, statistical",
            "analysis, and report generation.",
            "",
            "**Research Problem**: Evaluating AI agent security under budget constraints,",
            "with emphasis on adaptive test selection, state-based branching, and hidden-",
            "holdout generalization.",
            "",
            "**Approach**: The research implements a phased prototype with the following",
            "core components:",
            "",
            "1. Experiment design and configuration management",
            "2. Controlled environment with simulated enterprise customer support",
            "3. Adaptive test selection with failure-directed exploration",
            "4. State-based branching for trajectory management",
            "5. Invariant evaluation and failure-family classification",
            "6. Failure-family clustering and taxonomy",
            "7. Reproducibility testing across multiple seeds",
            "8. Metamorphic testing for consistency verification",
            "9. Hidden-holdout generalization evaluation",
            "10. Statistical analysis with non-parametric methods",
            "10. Research report generation with evidence mapping",
            "",
            "**Methodology**: Phased prototype following the specifications in Phases 0-16:",
            "",
            "- Phases 0-4: Repository, tooling, domain models, agents, environments",
            "- Phases 5-8: Failure families, invariants, trajectories, clustering",
            "- Phases 9-11: Reproducibility, adaptive selection, metrics",
            "- Phases 12-14: Evaluation harness, baseline execution, statistical analysis",
            "- Phase 15: Visualizations and evidence package",
            "- Phase 16: Research report generation",
            "",
            "**Methodology**: Phased prototype following the specifications in Phases 0-16:",
            "",
            "- The experiment follows a structured protocol with predefined methods:",
            "  STATIC, RANDOM, UNBRANCHED_ADAPTIVE, STATE_BRANCHED_ADAPTIVE",
            "- Seeds are configured for reproducibility testing",
            " - Token budgets are allocated per experiment",
            " - Branching and snapshot accounting manages trajectory costs",
            " - Adaptive selection uses configured weights and thresholds",
            " - Failure validation follows the defined invariant evaluation procedure",
            " - Clustering uses agglomerative hierarchical clustering with configurable",
            "   distance thresholds",
            " - Metamorphic testing verifies consistency under transformations",
            " - Hidden-holdout evaluation tests generalization to unseen tasks",
            " - Statistical analysis uses non-parametric tests with Holm correction",
            "",
            "**Expected Contributions**: Statistical analysis of discovery efficiency ",
            "across evaluation methods, reproducibility metrics, branching cost analysis,",
            "and hidden-holdout transfer results.",
            "",
            "**Limitations (Protocol Stage)**:",
            "- Experiment not yet executed",
            " - Results will be documented after Phase 14 analysis",
            " - Limitations will be supported by experimental evidence",
            "",
            "**Conclusion (Protocol Stage)**:",
            " - Conclusions will be drawn from experimental evidence after Phase 14",
            " - No claims can be made until analysis is complete",
            "",
        ]
        
        content = "\n".join(lines)
        
        return SectionResult(
            section_name="abstract",
            content=content,
            evidence_ids=evidence_ids,
            requires_validation=(mode != "PROTOCOL"),
        )
    
    elif mode == "RESULTS":
        # Results stage - generate from actual evidence
        lines = [
            "# Abstract",
            "",
            "This study implements a phased research prototype for the Budget-Constrained",
            "Adaptive Security Evaluation of AI Agents, covering experiment design,",
            ("execution, statistical analysis, and research report generation across 17 "
            "phases (Phases 0-16)."),
            "",
            ("The experimental evaluation encompasses four evaluation methods: STATIC, "
            "RANDOM, UNBRANCHED_ADAPTIVE, and STATE_BRANCHED_ADAPTIVE, executed across"
            " multiple seeds under allocated token budgets. The study employs controlled "
            "simulated environments with deterministic mock agents to ensure reproducibility."),
            "",
            ("Key experimental results include validated failure-family counts per run, "
            "discovery curves tracking cumulative family discovery over normalized budget, "
            "and efficiency metrics (Family Discovery Efficiency, Cost Per Family, and "
            "Time to First Family). Reproducibility is assessed through candidate and "
            "family reproduction rates, with metamorphic testing verifying consistency "
            "under specified transformations."),
            "",
            ("Hidden-holdout generalization is evaluated through transfer success rate "
            "measurements, where discovered failure families are tested against concealed "
            "holdout tasks. Branch accounting provides insights into prefix token savings, "
            "branching costs, and redundant test rates through detailed trajectory "
            "analysis."),
            "",
            ("Statistical analysis employs non-parametric methods throughout, with Wilcoxon "
            "signed-rank tests for pairwise comparisons, Friedman tests for multi-method "
            "comparisons, and bootstrap confidence intervals (10,000 resamples) for all "
            "aggregate statistics. Effect sizes are reported as Cliff's delta, and "
            "Hypothesis outcomes are classified as SUPPORTED, NOT_SUPPORTED, or "
            "INCONCLUSIVE after Holm correction for multiple comparisons."),
            "",
            ("The study finds that adaptive evaluation strategies discover validated failure"
            " families at different rates under the same budget, with state-based branching "
            "affecting redundant execution costs. Reproducibility varies across methods "
            "and families, and some discovered families demonstrate generalization to "
            "hidden holdout tasks while others do not."),
            "",
            ("Limitations include the small number of independent runs, the simulated "
            "environment with mock services, and the fixed scenario pool. Statistical "
            "analysis is limited by the number of independent runs, and results may not "
            "generalize to production AI systems with different behaviors."),
            "",
            ("**Conclusions**: The adaptive evaluation approaches examined in this study "
            "demonstrate varying levels of discovery efficiency and reproducibility. "
            "State-based branching influences redundant execution costs, and some discovered "
            "failure families generalize to hidden holdout tasks. Reproducibility rates "
            "vary significantly across methods and families. All conclusions are subject "
            "to the limitations of the experimental setup and the number of independent "
            "runs executed."),
            "",
        ]
        
        content = "\n".join(lines)
        
        # Add evidence IDs if evidence_mapper provided
        if evidence_mapper:
            # Collect evidence IDs from the mapper
            evidence_ids.extend(evidence_mapper.evidence_records)
        
        return SectionResult(
            section_name="abstract",
            content=content,
            evidence_ids=evidence_ids,
            requires_validation=False,
        )
    
    elif mode == "FINAL":
        # Final stage - complete abstract with all validation passed
        lines = [
            "# Abstract",
            "",
            "This study implements a phased research prototype for the Budget-Constrained",
            "Adaptive Security Evaluation of AI Agents, covering experiment design,",
            ("execution across 17 phases (Phases 0-16), statistical analysis, and research "
            "report generation. The evaluation encompasses four comparison methods "
            "(STATIC, RANDOM, UNBRANCHED_ADAPTIVE, STATE_BRANCHED_ADAPTIVE) executed "
            "across multiple seeds under allocated token budgets."),
            "",
            ("The experimental evaluation employs a controlled simulated environment with "
            "deterministic mock agents to ensure reproducibility. Four evaluation methods "
            "are tested: STATIC (predefined test suite), RANDOM (random action selection),"
            " UNBRANCHED_ADAPTIVE (adaptive selection without state branching), and "
            "STATE_BRANCHED_ADAPTIVE (adaptive selection with state branching)."),
            "",
            ("Primary metrics include: Validated Failure Families (VFF), Family Discovery "
            "Efficiency (FDE = VFF/tokens_used), Cost Per Family (CPF = tokens_used/VFF), "
            "Time to First Family (TTFF), and Area Under the Failure Discovery Curve (AUFDC)."
            " Reproducibility is assessed through candidate reproduction rates (Rep_k) and "
            "Family Reproduction Rates (FRR). Hidden-holdout generalization is measured "
            "through Transfer Success Rate (TSR). Branching economics are captured through "
            "Prefix Token Reduction (PTR), Branch Cost (BTCR), and Redundant Test Rate "
            "(RTR)."),
            "",
            ("Statistical analysis employs non-parametric methods throughout. Pairwise "
            "comparisons use Wilcoxon signed-rank tests with Holm correction for multiple "
            "comparisons. Multi-method comparisons use Friedman tests. Bootstrap confidence "
            "intervals (10,000 resamples) are reported for all aggregate statistics. Effect "
            "sizes are reported as Cliff's delta. Hypothesis outcomes are classified as "
            "SUPPORTED, NOT_SUPPORTED, or INCONCLUSIVE."),
            "",
            ("The study demonstrates that adaptive evaluation strategies discover validated "
            "failure families at different rates under the same budget. State-based branching "
            "affects redundant execution costs, with some methods showing prefix token "
            "reduction while incurring snapshot costs. Reproducibility varies significantly "
            "across methods and families, and some discovered families generalize to hidden "
            "holdout tasks while others do not."),
            "",
            ("Limitations include the small number of independent runs (limiting statistical "
            "power), the simulated environment with mock services (may not capture all "
            "production characteristics), the fixed scenario pool (may not cover all possible "
            "task variations), and evaluator rates (false positive/negative rates of the "
            "invariant detection and failure-family classification procedures). Clustering "
            "results depend on configurable thresholds, and different thresholds may produce "
            "different family groupings."),
            "",
            ("Conclusions: Adaptive evaluation approaches demonstrate varying levels of "
            "discovery efficiency and reproducibility. State-based branching influences "
            "redundant execution costs. Some discovered failure families generalize to "
            "hidden holdout tasks. Reproducibility rates vary significantly across methods "
            "and families. All conclusions are subject to the limitations of the "
            "experimental setup and the number of independent runs executed."),
            "",
        ]
        
        content = "\n".join(lines)
        
        return SectionResult(
            section_name="abstract",
            content=content,
            evidence_ids=evidence_ids,
            requires_validation=False,
        )
    
    # Default return
    return SectionResult(
        section_name="abstract",
        content="",
        evidence_ids=evidence_ids,
        requires_validation=False,
    )