# Limitation Defense

## Limited Number of Seeds

Only 3 seeds were used for reproducibility testing (Rep_k, FRR). A larger seed count may change the reproduction rate and the statistical power of the hypothesis tests. This limitation is documented; results should be interpreted with the seed count in mind. More seeds would increase confidence in the reproducibility claims.

## Simulated Enterprise Environment

The evaluation is conducted in a simulated enterprise environment with mock external services. Production LLM agents and real services may exhibit different behavior. The simulated environment is designed for controlled prototyping, not end-to-end production realism. Results provide a principled foundation for real-world evaluation design but do not guarantee identical outcomes.

## Mock External Services

All external service interactions are mocked. Real-world tool calls, API responses, and system interactions are simulated. Mock assumptions (e.g., response formats, latency, error modes) may not hold in production. The project documents mock configurations; alternative configurations should be tested independently.

## Model-Specific Behavior

The mock agent may not represent the behavior of production LLMs. Different models have different failure modes, prompt sensitivities, and tool usage patterns. Model-specific evaluation requires separate investigation. The project's findings are agent-architecture-agnostic in principle but empirically validated on the mock agent.

## Scenario-Pool Limitations

The candidate pool is finite and may not exhaust the full evaluation space. Adaptive selection can only discover failures within the pool; unseen scenarios may yield different results. The pool size and composition are documented; extension to larger pools is straightforward in principle but requires computational investment.

## Evaluator Assumptions

Invariant definitions and violation detection assume specific evaluator logic. Different invariant implementations may produce different results. The project's invariant set (prompt_injection_guard, tool_access_control, state_persistence_integrity) is documented; alternative invariant sets should be tested for coverage and consistency.

## Clustering Assumptions

Failure family assignment relies on shared mechanism characteristics (invariant violations, tool patterns, state transitions). Clustering via embeddings or unsupervised methods was not attempted; the deterministic classification pipeline provides a more auditable baseline. Different clustering assumptions may produce different family assignments.

## Budget Constraints

The evaluation uses a fixed budget of 50,000 tokens. Different budget sizes may produce different discoveries, tradeoffs, or conclusions. The budget of 50,000 tokens is configured in the smoke test; other budgets should be tested to assess generality.

## Hidden-Holdout Size

The holdout set size is determined by the configuration and may not represent all possible held-out conditions. A larger or differently composed holdout set may yield different TSR results. The holdout size and composition are documented; extension is straightforward.

## Computational Constraints

The 25-phase experiment scope is limited by the available compute. Larger phase counts, more candidates per phase, or finer-grained metrics would increase computational cost. The experiment documents all parameter choices; replication with different resources is possible but may produce different results due to stochastic variation.

## No Apology

Each limitation is explained for how it affects interpretation. The project does not apologize for legitimate constraints but documents them so reviewers can assess the evidence's strength and the claims' robustness.