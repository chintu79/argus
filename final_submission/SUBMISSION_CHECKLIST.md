# Submission Checklist

## Research

- [x] Research question finalized: Budget-constrained adaptive security evaluation of AI agents
- [x] Research gap documented: AI security evaluation lacks budget accounting, adaptive selection, state branching, structured failure classification, and hidden-holdout generalization
- [x] Hypotheses frozen: 6 hypotheses tested (H1-H6), results documented
- [x] Methodology documented: Four-stage pipeline (selector → agent → environment → trajectory → state → branch → invariant → failure → family)
- [x] Baselines documented: Random testing and fresh execution as baseline strategies
- [x] Metrics documented: FDE, CPF, TTFF, Rep_k, FRR, TSR, PTR, BTCR, RTR, MCR, MVR
- [x] Results validated: Phase 14-17 outputs verified against audit checks
- [x] Statistical analysis validated: Hypothesis tests, effect sizes, confidence intervals, multiple-comparison correction
- [x] Limitations documented: Section 21 (Limitation Defense) and Section 45 (Why Not? Questions)
- [x] References verified: All citations in final research report confirmed

## Engineering

- [x] Repository builds: `uv sync` / `pip install -e .` succeeds
- [x] Dependencies install: All declared dependencies resolved
- [x] Tests pass: 19/19 unit tests pass via `pytest`
- [x] CLI works: `python -m agent_eval experiment`, `smoke`, `report`, `audit` commands functional
- [x] Smoke experiment works: Phase 1-25 execution with mock agent
- [x] Budget accounting verified: Total cost within 50,000 token budget
- [x] Branch isolation verified: State isolation audit PASS
- [x] Selector leakage verified: No holdout information influences candidate scoring
- [x] Evidence hashes verified: SHA256 checksums match persisted artifacts

## Research artifacts

- [x] Figures generated: FIG-01 through FIG-12 all present and validated
- [x] Tables generated: TBL-01 through TBL-10 all present with source artifacts identified
- [x] Report generated: final_research_report.md completed and exported to PDF
- [x] Evidence package generated: All evidence artifacts persisted in artifacts/ directory
- [x] Reproducibility package generated: final_submission/reproducibility/ complete
- [x] Demonstration package generated: final_submission/demo/ complete with executable flow

## Defense

- [x] Architecture explanation: architecture_explanation.md at 3 levels (Executive, Technical, Implementation)
- [x] Algorithm explanation: algorithm_defense.md covering adaptive selection, state branching, failure validation, reproducibility, hidden holdout, metamorphic testing
- [x] Experimental methodology explanation: questions.md with 55 organized viva questions
- [x] Results explanation: hypothesis_defense.csv with all 6 hypotheses and evidence
- [x] Limitations explanation: limitation_defense.md with 9 documented limitations
- [x] Viva question bank: questions.md with 55 questions across 7 categories
- [x] Viva answer guide: answer_guide.md with direct answers, technical explanations, evidence, and limitations for each question