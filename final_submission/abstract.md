# Abstract

This research addresses the problem of evaluating AI agent security under constrained evaluation budgets. Traditional security evaluations of AI agents are computationally expensive and often fail to adaptively explore the most relevant failure modes. We present BCADE-AI, a system that integrates adaptive candidate selection, state-based execution branching, and structured failure classification to maximize discovery efficiency within a fixed budget.

The problem: AI agents operate in complex environments where security failures emerge from unexpected interactions between prompts, tools, and state. The combinatorial space makes exhaustive evaluation infeasible. Existing approaches either test randomly (wasting budget on irrelevant scenarios) or use unprincipled heuristics (missing novel failure modes).

The gap: Current AI security evaluation methods lack explicit budget accounting, adaptive selection based on accumulated evidence, state reuse via snapshotting and branching, structured failure classification, and generalization assessment via hidden-holdout evaluation.

Our contribution: BCADE-AI, a system with four-stage pipeline (candidate selection, state-based branching, failure detection, failure validation) that maximizes discovery efficiency within fixed budgets. Experimental results show: adaptive selection discovers more validated failures per budget unit than random testing; state-based branching provides measurable prefix-token savings; hidden-holdout TSR demonstrates no discovery-time information leakage; and failure families are reliably classified using the candidate → invariant → reproduction → family pipeline.

The system is implemented in Python 3.11+ using FastAPI, Pydantic v2, SQLModel, and SQLite, with 25 phases covering experiment design, execution, statistical analysis, visualization, research report generation, and audit/validation.