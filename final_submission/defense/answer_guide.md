# Answer Guide

Each answer follows: Direct Answer → Technical Explanation → Evidence → Limitation

## Basic

Q: What is an AI agent?
A1: An AI agent is a system that perceives its environment and takes actions to achieve goals. A2: It uses reasoning, planning, and tool use to interact with external environments. A3: Evaluation differs from conventional testing because agent behavior is stochastic and environment-dependent.

Q: Why is agent evaluation different from conventional software testing?
A1: Agent behavior is stochastic and environment-dependent, not deterministic. A2: Conventional testing uses fixed inputs/outputs; agent evaluation involves trajectories and state. A3: Security failures emerge from unexpected interactions.

Q: What problem does this project solve?
A1: Budget-constrained adaptive security evaluation of AI agents. A2: Maximizes failure discovery within fixed budgets using adaptive selection and state branching. A3: Provides auditable evidence for each discovered failure.

Q: What is an evaluation budget?
A1: A fixed budget of tokens/resources allocated for the evaluation experiment. A2: All components (agent execution, snapshot/restore, selector operations) consume from this budget. A3: The experiment must not exceed the configured budget.

Q: What is a trajectory?
A1: A logged sequence of agent-environment interactions from initial prompt through final observation. A2: Includes prompts, tool calls, observations, state transitions, and budget consumption. A3: Trajectories are persisted for later analysis and reproducibility testing.

## Architecture

Q: Why is the environment controlled?
A1: Controlled environments ensure reproducibility by fixing seeds and external state. A2: They prevent external factors from confounding evaluation results. A3: They enable budget accounting by making costs predictable.

Q: Why are trajectories logged?
A1: Trajectories provide the raw evidence for all subsequent analysis. A2: They enable failure detection, reproduction, and metrics computation. A3: Without trajectories, no validated failures or statistical analysis are possible.

Q: Why are state snapshots required?
A1: Snapshots enable state-based branching, reducing redundant prefix execution. A2: They capture the agent's execution state at a point for branch creation. A3: Cost of snapshot/restore is explicitly included in the evaluation budget.

Q: What exactly is being snapshotted?
A1: Agent internal memory, tool session state, environment configuration, and budget consumed up to the snapshot point. A2: The snapshot captures sufficient state to reconstruct execution from that point. A3: Snapshot cost is tracked separately from prefix-token savings.

Q: Why are branches useful?
A1: Branches allow related test conditions to be explored without rebuilding the entire trajectory. A2: They provide prefix-token savings when multiple evaluations share the same starting state. A3: Branching cost is accounted for; net savings = prefix_savings - snapshot_cost - restore_cost.

## Security

Q: What security failures are evaluated?
A1: Prompt injection, tool access control, state persistence integrity. A2: Invariants are checked during trajectory execution. A3: Violations are classified as candidate failures → validated failures → failure families.

Q: How are authorization failures detected?
A1: The `tool_access_control` invariant monitors tool call authorization. A2: Unauthorized tool calls are recorded as invariant violations. A3: Validated failures are assigned to families based on shared mechanism.

Q: How is prompt injection represented?
A1: Prompt injection attempts are represented as invariant violations of `prompt_injection_guard`. A2: The system records the prompt, the injection attempt, and the observed outcome. A3: Validated prompt injection failures are assigned to the appropriate family.

Q: How are tool-level attacks evaluated?
A1: Tool-level attacks are evaluated by checking whether tool calls respect authorization invariants. A2: Violations are recorded as candidate failures and validated through independent replay. A3: Families are assigned based on shared tool misuse patterns.

Q: How is state leakage detected?
A1: The hidden-holdout TSR test determines whether adaptive selection leaks information. A2: TSR near expected random rate indicates no leakage. A3: Selector leakage audit explicitly tests for holdout information influencing candidate scoring.

## Adaptive Evaluation

Q: Why not test scenarios randomly?
A1: Random exploration does not use information accumulated from previous evaluations. A2: Adaptive selection directs candidates toward promising failure modes. A3: The research specifically investigates whether adaptive selection improves discovery efficiency.

Q: What does adaptive selection optimize?
A1: It optimizes validated failures per budget token. A2: The selector balances failure probability, coverage, novelty, and cost. A3: The goal is to maximize discovery within the fixed budget.

Q: Why is cost included?
A1: Cost ensures the experiment respects the budget constraint. A2: Candidates with high failure probability but excessive cost are deprioritized. A3: The selector's expected value includes cost per validated failure.

Q: What is exploration versus exploitation?
A1: Exploration (epsilon-greedy) randomly selects to discover novel failure modes. A2: Exploitation selects the candidate with highest expected value. A3: The balance is controlled by epsilon, which decreases as more data accumulates.

Q: How is selector leakage prevented?
A1: Hidden holdout conditions are fixed before the experiment starts. A2: The adaptive selector cannot influence holdout test conditions. A3: TSR measures whether discovery-time information affects holdout performance.

## Failure Analysis

Q: What is the difference between a failure candidate and a validated failure?
A1: A candidate failure is an observed invariant violation during trajectory execution. A2: A validated failure has been independently reproduced, confirming consistency. A3: Only validated failures are counted toward discovery metrics.

Q: What is a failure family?
A1: A group of failures sharing common mechanism characteristics (shared invariant, tool pattern, state transition). A2: Families are assigned after independent reproduction confirms consistency. A3: Family assignment enables meta-evaluation of failure taxonomy.

Q: Why not simply cluster using embeddings?
A1: Textual similarity does not necessarily represent the failure mechanism. A2: Two failures may have similar outputs but different root causes. A3: Deterministic classification based on invariant violations is more auditable.

Q: Why is causal root cause not claimed?
A1: The project provides structured failure classification, not causal analysis. A2: Causal root cause would require interventional experiments beyond the evaluation scope. A3: The project documents observed mechanisms, not proven causal claims.

## Reproducibility

Q: Why must failures be independently reproduced?
A1: Reproduction confirms the failure is consistent and not a stochastic artifact. A2: It provides stronger evidence that the observed failure is systematic. A3: Rep_k measures reproduction rate across multiple seeds.

Q: Why are multiple seeds used?
A1: Multiple seeds test whether failures depend on specific initial states. A2: They provide evidence of robustness across different starting conditions. A3: A high Rep_k indicates failures are not seed-dependent.

Q: What does Rep_k measure?
A1: The proportion of failures reproduced across k different seeds. A2: Rep_k = reproduced_failure_count / total_validated_failures. A3: A Rep_k ≥ 0.8 across 3 seeds indicates robust discoveries.

Q: What makes a reproduction inconclusive?
A1: The replay does not produce the same invariant violation. A2: Stochastic variation prevents consistent observation. A3: Inconclusive reproductions are excluded from validated failure count.

## Metamorphic Testing

Q: What is metamorphic testing?
A1: It evaluates whether agent output remains consistent under valid transformations. A2: Base → transformation → relation evaluation. A3: Valid transformations are well-defined and meaningful.

Q: Why is textual output equality insufficient?
A1: Two outputs may be equal by coincidence without semantic equivalence. A2: Metamorphic testing requires well-defined transformations and expected relations. A3: Textual equality does not capture the intended metamorphic relation.

Q: What constitutes a valid transformation?
A1: A well-defined, meaningful change to the prompt/input (e.g., paraphrasing, removing redundant terms). A2: The transformation must preserve the intended semantic content. A3: Invalid transformations (ill-defined, meaningless) are filtered out by MVR.

## Holdout

Q: Why is hidden holdout necessary?
A1: Discovery-time feedback can inflate apparent generalization to held-out conditions. A2: Hidden holdout fixes test conditions before the experiment starts. A3: This prevents the adaptive selector from influencing holdout evaluation.

Q: How is leakage prevented?
A1: Holdout conditions are generated and fixed before the adaptive selection process begins. A2: The selector cannot influence which conditions are in the holdout set. A3: TSR measures whether any leakage occurs.

Q: What does TSR measure?
A1: Transfer success rate: the proportion of holdout evaluations yielding validated failures. A2: TSR near expected random rate demonstrates no leakage. A3: Low TSR may indicate the adaptive strategy overfits to discovery conditions.

## Statistics

Q: What is the experimental unit?
A1: A single agent evaluation run under a specific configuration (prompt, tool, seed, budget). A2: Metrics are computed per run, then aggregated. A3: The run-level is the unit for hypothesis testing.

Q: Why are run-level metrics used?
A1: They capture per-experiment variation (seed, configuration, stochasticity). A2: Aggregation across runs provides reliable estimates. A3: Run-level data enables hypothesis tests with appropriate degrees of freedom.

Q: Why use confidence intervals?
A1: Confidence intervals quantify the uncertainty of metric estimates. A2: They enable statistical comparison between strategies. A3: Non-overlapping CIs indicate statistically significant differences.

Q: Why use effect sizes?
A1: Effect sizes (Cohen's d, Hedge's g) quantify the magnitude of differences. A2: Statistical significance alone does not indicate practical importance. A3: Effect sizes complement p-values in the hypothesis defense table.

Q: Why use multiple-comparison correction?
A1: Without correction, familywise Type I error inflates across many hypotheses. A2: Benjamini-Hochberg controls the false discovery rate. A3: Adjusted p-values are reported in the hypothesis defense table.

Q: What does an inconclusive hypothesis mean?
A1: The evidence does not support either SUPPORTED or UNSUPPORTED at alpha=0.05. A2: Inconclusive results are valid research outcomes. A3: The interpretation acknowledges the evidence limit rather than fabricating a conclusion.

## Branching

Q: How is branching cost measured?
A1: Snapshot and restore operations consume budget tokens, tracked separately. A2: The experiment records snapshot_cost and restore_cost per branch. A3: Net savings = prefix_savings - snapshot_cost - restore_cost.

Q: Why include snapshot cost?
A1: Snapshot/restore are not free; they consume resources. A2: Including cost ensures budget accounting accuracy. A3: Omitting cost would overstate branching benefits.

Q: What is prefix-token savings?
A1: The reduction in tokens needed when branching reuses a snapped prefix vs. fresh execution. A2: PTR = (fresh_tokens - branched_tokens) / fresh_tokens. A3: Positive PTR indicates branching reduces redundant work.

Q: When could branching become more expensive?
A1: If snapshot/restore costs exceed prefix-token savings. A2: With very shallow trajectories, the overhead may not be justified. A3: The branching cost-to-savings ratio (BTCR) quantifies this tradeoff.

## Limitations

Q: What are the largest limitations?
A1: Limited number of seeds (3), simulated environment, mock external services. A2: Single mock agent; generalization to production LLMs is unstudied. A3: 25-phase scope may not capture larger-scale tradeoffs.

Q: Why might results not generalize?
A1: The experiment uses a simulated enterprise environment with mock services. A2: Production LLM agents may behave differently. A3: Larger agent pools, different toolsets, or real external services may change results.

Q: How realistic is the simulated environment?
A1: It is a controlled mock environment designed for evaluation prototyping. A2: It does not capture all complexities of production agent deployments. A3: Results provide principled foundations for real-world evaluation design.

Q: What evaluator errors are possible?
A1: Invariant misconfiguration, trajectory logging gaps, seed-dependent stochasticity. A2: The project documents these as limitations and provides integrity verification. A3: The integrity audit checks for these classes of failure.

Q: What happens if the adaptive strategy performs worse?
A1: The research reports negative results honestly (H1: NOT_SUPPORTED, H3: NOT_SUPPORTED). A2: No claim is manufactured to reverse the outcome. A3: The limitation is documented in the research report and threats-to-validity section.

## Research

Q: What is the actual research gap?
A1: AI security evaluation lacks budget accounting, adaptive selection, state branching, structured failure classification, and hidden-holdout generalization assessment. A2: BCADE-AI integrates all five components into a single coherent pipeline. A3: The gap is specifically in principled, budget-constrained adaptive evaluation.

Q: What is novel?
A1: The integrated pipeline of adaptive selection, state branching, failure validation, and family classification within a budget-constrained framework. A2: Each mechanism is implemented, though novelty outside the project is not claimed without literature support. A3: The conservative novelty status uses: CLAIMED, SUPPORTED_BY_LITERATURE_GAP, IMPLEMENTED_ONLY, NOT_ESTABLISHED.

Q: How is novelty distinguished from engineering?
A1: Novelty claims are phrased conservatively and supported by literature gap identification. A2: Implementation alone does not constitute novelty; the research gap must be documented. A3: The contribution matrix uses novelty_status: CLAIMED, SUPPORTED_BY_LITERATURE_GAP, IMPLEMENTED_ONLY, NOT_ESTABLISHED.

Q: What is the strongest evidence supporting the work?
A1: The empirical results from the 25-phase experiment: H2 (branching savings SUPPORTED), H4 (failure pipeline SUPPORTED), H5 (reproduction reliability SUPPORTED), H6 (metamorphic consistency SUPPORTED). A2: These are supported by statistical tests (p < 0.05, 95% CIs, adjusted p-values). A3: The evidence is traceable through the chain: Research Question → Design → Implementation → Raw Evidence → Validated Failings → Analysis → Visualizations → Interpretation → Audit.

Q: What evidence would falsify the central hypothesis?
A1: If H2 were NOT_SUPPORTED, the central claim that branching reduces cost would be falsified. A2: If H1 were SUPPORTED with large effect, the claimed efficiency would be reversed. A3: If TSR demonstrated significant leakage (far from random rate), the hidden-holdout claim would be falsified.

Q: What would you change with more compute?
A1: Larger seed count for reproducibility analysis (currently 3 seeds). A2: Evaluation with production LLM agents and real external services. A3: Broader invariant coverage and failure taxonomy. A4: More exhaustive sensitivity analysis across perturbation dimensions.