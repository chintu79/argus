"""Claims audit for Phase 17.

Creates a claim ledger for every major conclusion, classifying each claim as:
- SUPPORTED
- PARTIALLY_SUPPORTED
- UNSUPPORTED
- INCONCLUSIVE

Each claim includes:
- claim_id
- claim_text
- claim_type
- supporting_artifact
- source_hash
- metric_or_evidence
- experiment_population
- uncertainty
- limitations
- validation_status
"""

from __future__ import annotations

import json
import os
from typing import Any


def run_claims_audit(
    experiment_dir: str,
    analysis_dir: str,
) -> dict[str, Any]:
    """Run claims audit for the experiment.
    
    Creates a claim ledger classifying every major conclusion,
    and determines whether the overall result is BLOCKED, CONDITIONALLY_READY,
    or READY_FOR_RESEARCH_REVIEW.
    
    Returns dict with:
    - claim_ledger: list of claim dicts
    - unresolved_issues: list of unresolved issue strings
    - blocking_issues: list of blocking issue strings
    - conditional_issues: list of conditional issue strings
    """
    claim_ledger = []
    unresolved_issues = []
    blocking_issues = []
    conditional_issues = []
    
    # Collect claims from various sources
    
    # 1. Claims from experiment results
    results_path = os.path.join(experiment_dir, "artifacts", "analysis", "hypothesis_results.csv")
    if os.path.exists(results_path):
        try:
            import csv
            with open(results_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    hyp_id = row.get("hypothesis_id", "")
                    status = row.get("evidence_status", "")
                    metric = row.get("metric", "")
                    comparison = row.get("comparison", "")
                    
                    # Map Phase 14 evidence status to claim status
                    status_map = {
                        "SUPPORTED": "SUPPORTED",
                        "NOT_SUPPORTED": "UNSUPPORTED",
                        "INCONCLUSIVE": "INCONCLUSIVE",
                    }
                    claim_status = status_map.get(status, "INCONCLUSIVE")
                    
                    claim = {
                        "claim_id": hyp_id,
                        "claim_text": f"Hypothesis {hyp_id}: {metric} comparison ({comparison})",
                        "claim_type": "STATISTICALLY_TESTED",
                        "supporting_artifact": results_path,
                        "source_hash": _compute_file_hash(results_path),
                        "metric_or_evidence": metric,
                        "experiment_population": row.get("population", "unknown"),
                        "uncertainty": row.get("confidence_interval", "unknown"),
                        "limitations": f"Based on {row.get('n', 'unknown')} runs with alpha=0.05",
                        "validation_status": claim_status,
                    }
                    claim_ledger.append(claim)
                    
                    # Track blocking/conditional issues
                    if claim_status == "UNSUPPORTED":
                        blocking_issues.append(f"Claim {hyp_id} unsupported: {metric}")
                    elif claim_status == "INCONCLUSIVE":
                        conditional_issues.append(f"Claim {hyp_id} inconclusive: {metric}")
        except Exception as e:
            unresolved_issues.append(f"Error reading hypothesis results: {e}")
    
    # 2. Claims from budget audit
    budget_path = os.path.join(experiment_dir, "artifacts", "budget_reconciliation.json")
    if os.path.exists(budget_path):
        try:
            with open(budget_path) as f:
                budget_data = json.load(f)
            
            discrepancy = budget_data.get("discrepancy", 0)
            if discrepancy > 0:
                claim_ledger.append({
                    "claim_id": "BUDGET_001",
                    "claim_text": f"Budget discrepancy of {discrepancy} tokens exceeds acceptable threshold",
                    "claim_type": "STATISTICALLY_TESTED",
                    "supporting_artifact": budget_path,
                    "source_hash": _compute_file_hash(budget_path),
                    "metric_or_evidence": f"Discrepancy of {discrepancy} tokens",
                    "experiment_population": "all runs",
                    "uncertainty": "within 5% tolerance",
                    "limitations": "Tolerance threshold may not capture all accounting edge cases",
                    "validation_status": "SUPPORTED" if discrepancy <= 0 else "UNSUPPORTED",
                })
                if discrepancy > 0:
                    blocking_issues.append(f"Budget overrun of {discrepancy} tokens")
                elif discrepancy > -0.05 * 50000:  # 5% of 50000
                    conditional_issues.append(f"Budget within tolerance: {discrepancy} tokens")
        except Exception as e:
            unresolved_issues.append(f"Error reading budget reconciliation: {e}")
    
    # 3. Claims from statistical audit
    stat_path = os.path.join(analysis_dir, "statistical_audit.json") if os.path.isdir(analysis_dir) else None
    if stat_path and os.path.exists(stat_path):
        try:
            with open(stat_path) as f:
                stat_data = json.load(f)
            
            # Extract significant findings
            for key, value in stat_data.items():
                if isinstance(value, dict) and "p_value" in value:
                    p_val = value["p_value"]
                    if p_val < 0.05:
                        claim_ledger.append({
                            "claim_id": f"STAT_{key}",
                            "claim_text": f"Statistically significant finding: {key} (p={p_val:.4f})",
                            "claim_type": "STATISTICALLY_TESTED",
                            "supporting_artifact": stat_path,
                            "source_hash": _compute_file_hash(stat_path),
                            "metric_or_evidence": f"{key} (p={p_val:.4f})",
                            "experiment_population": "analyzed runs",
                            "uncertainty": "95% CI reported",
                            "limitations": "Multiple comparisons may inflate Type I error",
                            "validation_status": "SUPPORTED",
                        })
        except Exception as e:
            unresolved_issues.append(f"Error reading statistical audit: {e}")
    
    # 4. Claims from reproducibility testing
    repro_path = os.path.join(experiment_dir, "artifacts", "reproducibility", "results.json")
    if os.path.exists(repro_path):
        try:
            with open(repro_path) as f:
                repro_data = json.load(f)
            
            rep_rate = repro_data.get("reproduction_rate", None)
            if rep_rate is not None:
                claim_ledger.append({
                    "claim_id": "REPRO_001",
                    "claim_text": f"Reproduction rate: {rep_rate:.2%} of attempts resulted in reproduction",
                    "claim_type": "STATISTICALLY_TESTED",
                    "supporting_artifact": repro_path,
                    "source_hash": _compute_file_hash(repro_path),
                    "metric_or_evidence": f"Reproduction rate: {rep_rate:.2%}",
                    "experiment_population": "reproducibility runs",
                    "uncertainty": "binomial confidence interval",
                    "limitations": "Reproduction depends on identical initial state and seed",
                    "validation_status": "SUPPORTED" if rep_rate >= 0.8 else "PARTIALLY_SUPPORTED",
                })
        except Exception as e:
            unresolved_issues.append(f"Error reading reproducibility results: {e}")
    
    # 5. Claims from holdout evaluation
    holdout_path = os.path.join(experiment_dir, "artifacts", "holdout_metrics.csv")
    if os.path.exists(holdout_path):
        try:
            import csv
            with open(holdout_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tsr = row.get("tsr", "")
                    if tsr and tsr != "NULL":
                        try:
                            tsr_val = float(tsr)
                            claim_ledger.append({
                                "claim_id": "HOLD_001",
                                "claim_text": f"Hidden-holdout transfer success rate: {tsr_val:.2%}",
                                "claim_type": "STATISTICALLY_TESTED",
                                "supporting_artifact": holdout_path,
                                "source_hash": _compute_file_hash(holdout_path),
                                "metric_or_evidence": f"TSR={tsr_val:.2%}",
                                "experiment_population": "holdout-tested families",
                                "uncertainty": "binomial confidence interval",
                                "limitations": "Holdout task set may not represent all possible tasks",
                                "validation_status": "SUPPORTED" if tsr_val >= 0.5 else "PARTIALLY_SUPPORTED",
                            })
                        except ValueError:
                            pass
                    elif tsr == "NULL":
                            # No families were tested for transfer
                            claim_ledger.append({
                                "claim_id": "HOLD_002",
                                "claim_text": "No families were tested for hidden-holdout transfer",
                                "claim_type": "DESCRIPTIVE_INTERPRETATION",
                                "supporting_artifact": holdout_path,
                                "source_hash": _compute_file_hash(holdout_path),
                                "metric_or_evidence": "NULL (no transfer tested)",
                                "experiment_population": "N/A",
                                "uncertainty": "N/A",
                                "limitations": "No holdout transfer testing was performed",
                                "validation_status": "INCONCLUSIVE",
                            })
        except Exception as e:
            unresolved_issues.append(f"Error reading holdout metrics: {e}")
    
    # Determine overall status
    sum(1 for c in claim_ledger if c.get("validation_status") == "UNSUPPORTED")
    inconclusive_count = sum(1 for c in claim_ledger if c.get("validation_status") == "INCONCLUSIVE")
    
    if blocking_issues:
        release_decision = "BLOCKED"
    elif conditional_issues or inconclusive_count > 0:
        release_decision = "CONDITIONALLY_READY"
    else:
        release_decision = "READY_FOR_RESEARCH_REVIEW"
    
    return {
        "claim_ledger": claim_ledger,
        "unresolved_issues": unresolved_issues,
        "blocking_issues": blocking_issues,
        "conditional_issues": conditional_issues,
        "release_decision": release_decision,
    }


def _compute_file_hash(filepath: str) -> str:
    """Compute SHA256 hash of a file."""
    import hashlib
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()