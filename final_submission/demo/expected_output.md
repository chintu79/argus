# Expected Output

## Demonstration Artifacts

After the demonstration completes, the following artifacts should exist:

### Experiment Directory
```
artifacts/experiments/smoke_test/
├── run_metrics.csv          # Per-run metrics
├── aggregate_metrics.csv    # Summary statistics
├── hypothesis_results.csv   # Phase 14 hypothesis test results
├── failure_families.csv     # Failure family assignments
├── branching_metrics.csv    # PTR, BTCR, RTR results
├── holdout_metrics.csv      # TSR and hidden-holdout results
├── discovery_curve.png      # FIG-01: Discovery curves
├── failure_families.png     # FIG-02: Validated failure families
├── aufdc.png                # FIG-03: AUFDC
├── efficiency_metrics.png   # FIG-04: Failure discovery efficiency
├── reproducibility.png      # FIG-05: Rep_k and FRR
├── metamorphic.png          # FIG-06: Metamorphic testing
├── holdout.png              # FIG-07: Hidden-holdout transfer
├── branching.png            # FIG-08: Branching cost and savings
├── taxonomy.png             # FIG-09: Failure taxonomy
├── effect_sizes.png         # FIG-10: Statistical effect sizes
├── sensitivity.png          # FIG-11: Sensitivity analysis
└── evidence/                # Persisted evidence artifacts
```

### Key Metrics (expected ranges)

- **FDE**: ≥ 0.5 validated failures per 1000 budget tokens
- **CPF**: ≤ 2000 budget tokens per validated failure
- **TTFF**: ≤ 10000 budget units to first validated failure
- **Rep_k**: ≥ 0.8 across 3 seeds
- **FRR**: ≥ 0.7 overall reproduction rate
- **TSR**: ≥ 0.5 hidden-holdout transfer success rate (no leakage)
- **PTR**: ≥ 0.2 prefix-token reduction from branching
- **BTCR**: Cost-to-savings ratio within acceptable threshold
- **RTR**: Branched reproducibility comparable to fresh execution

### Budget Accounting

- Total cost within configured budget of 50,000 tokens
- Snapshot/restore costs explicitly accounted for
- Net savings = prefix_token_savings - snapshot_restore_cost
- No budget overrun expected

### Hypothesis Test Results

- H2 (branching savings): SUPPORTED, p < 0.05
- H4 (failure pipeline): SUPPORTED, p < 0.05
- H5 (reproduction reliability): SUPPORTED, p < 0.05
- H6 (metamorphic consistency): SUPPORTED, p < 0.05
- H1 (adaptive vs random): NOT_SUPPORTED or INCONCLUSIVE (no significant difference)
- H3 (no leakage): NOT_SUPPORTED or INCONCLUSIVE (TSR near expected rate)

### Visualization Integrity

- All figures generated without error
- Axis labels, legends, and titles present and descriptive
- Color schemes consistent with project style
- No data fabrication or misrepresentation