"""Main audit orchestration for Phase 17.

Runs all verification checks and produces a comprehensive audit report.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from agent_eval.audit.budget_audit import run_budget_audit
from agent_eval.audit.claims import run_claims_audit
from agent_eval.audit.fairness_audit import run_fairness_audit
from agent_eval.audit.ground_truth.test_runner import run_ground_truth_tests
from agent_eval.audit.integrity_audit import run_integrity_audit
from agent_eval.audit.reproducibility_audit import run_reproducibility_audit
from agent_eval.audit.selector_leakage import run_selector_leakage_audit
from agent_eval.audit.state_isolation import run_state_isolation_audit
from agent_eval.audit.statistical_audit import run_statistical_audit
from agent_eval.audit.visual_audit import run_visual_audit


def run_full_audit(
    experiment_id: str,
    analysis_dir: str,
    experiment_dir: str,
    config_path: str,
) -> dict[str, Any]:
    """Run the complete Phase 17 audit suite.

    Args:
        experiment_id: The experiment identifier
        analysis_dir: Path to Phase 14 analysis outputs
        experiment_dir: Path to the experiment directory
        config_path: Path to the experiment configuration

    Returns:
        Dict containing audit results and the release decision
    """
    start_time = datetime.now(UTC)
    
    passed_checks: int = 0
    total_checks: int = 0
    
    # Initialize audit result structure
    audit_result: dict[str, Any] = {
        "experiment_id": experiment_id,
        "audit_timestamp": start_time.isoformat(),
        "audit_version": "1.0.0",
        "component_status": {},
        "ground_truth_results": {},
        "budget_reconciliation": {},
        "selector_leakage_results": {},
        "statistical_audit": {},
        "fairness_results": {},
        "visual_audit": {},
        "integrity_results": {},
        "reproducibility_results": {},
        "security_findings": {},
        "claim_ledger": [],
        "unresolved_issues": [],
        "release_decision": "BLOCKED",
        "blocking_issues": [],
        "conditional_issues": [],
        "passed_checks": 0,
        "total_checks": 0,
    }
    
    # 1. Ground-truth evaluator validation
    total_checks += 1
    try:
        gt_results = run_ground_truth_tests(experiment_dir)
        audit_result["ground_truth_results"] = gt_results
        # Count passed/failing fixtures
        passed = sum(1 for v in gt_results.values() if v.get("status") == "PASS")
        failed = sum(1 for v in gt_results.values() if v.get("status") == "FAIL")
        audit_result["component_status"]["ground_truth"] = {
            "passed": passed,
            "failed": failed,
            "total": len(gt_results),
        }
        passed_checks += 1
    except Exception as e:
        audit_result["component_status"]["ground_truth"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 2. State snapshot and branch isolation
    total_checks += 1
    try:
        state_results = run_state_isolation_audit(experiment_dir)
        audit_result["component_status"]["state_isolation"] = state_results
        passed_checks += 1
    except Exception as e:
        audit_result["component_status"]["state_isolation"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 3. Adaptive selector leakage test
    total_checks += 1
    try:
        leakage_results = run_selector_leakage_audit(experiment_dir)
        audit_result["selector_leakage_results"] = leakage_results
        passed_checks += 1
    except Exception as e:
        audit_result["selector_leakage_results"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 4. Budget accounting audit
    total_checks += 1
    try:
        budget_results = run_budget_audit(experiment_dir)
        audit_result["budget_reconciliation"] = budget_results
        passed_checks += 1
    except Exception as e:
        audit_result["budget_reconciliation"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 4. Statistical audit
    total_checks += 1
    try:
        stat_results = run_statistical_audit(analysis_dir)
        audit_result["statistical_audit"] = stat_results
        passed_checks += 1
    except Exception as e:
        audit_result["statistical_audit"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 5. Fairness audit
    total_checks += 1
    try:
        fairness_results = run_fairness_audit(experiment_dir)
        audit_result["fairness_results"] = fairness_results
        passed_checks += 1
    except Exception as e:
        audit_result["fairness_results"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 6. Visualization audit
    total_checks += 1
    try:
        visual_results = run_visual_audit(analysis_dir)
        audit_result["visual_audit"] = visual_results
        passed_checks += 1
    except Exception as e:
        audit_result["visual_audit"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 6. Integrity audit
    total_checks += 1
    try:
        integrity_results = run_integrity_audit(experiment_dir, analysis_dir)
        audit_result["integrity_results"] = integrity_results
        passed_checks += 1
    except Exception as e:
        audit_result["integrity_results"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 6. Reproducibility audit
    total_checks += 1
    try:
        repro_results = run_reproducibility_audit(experiment_dir)
        audit_result["reproducibility_results"] = repro_results
        passed_checks += 1
    except Exception as e:
        audit_result["reproducibility_results"] = {
            "passed": 0,
            "failed": 1,
            "total": 1,
            "error": str(e),
        }
    
    # 7. Claims audit
    total_checks += 1
    try:
        claims_results = run_claims_audit(experiment_dir, analysis_dir)
        audit_result["claim_ledger"] = claims_results.get("claim_ledger", [])
        audit_result["unresolved_issues"] = claims_results.get("unresolved_issues", [])
        # Determine release decision
        blocking = claims_results.get("blocking_issues", [])
        conditional = claims_results.get("conditional_issues", [])
        if blocking:
            audit_result["release_decision"] = "BLOCKED"
        elif conditional:
            audit_result["release_decision"] = "CONDITIONALLY_READY"
        else:
            audit_result["release_decision"] = "READY_FOR_RESEARCH_REVIEW"
        passed_checks += 1
    except Exception as e:
        audit_result["claim_ledger"] = []
        audit_result["unresolved_issues"] = [str(e)]
        audit_result["release_decision"] = "BLOCKED"
    
    # 8. Finalize audit metadata
    end_time = datetime.now(UTC)
    audit_result["audit_duration_seconds"] = (end_time - start_time).total_seconds()
    audit_result["total_checks"] = total_checks
    audit_result["passed_checks"] = passed_checks
    audit_result["failed_checks"] = total_checks - passed_checks
    
    return audit_result