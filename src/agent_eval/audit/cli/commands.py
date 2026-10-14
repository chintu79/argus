"""CLI commands for Phase 17 audit and validation.

Commands:
  python -m agent_eval audit inspect --experiment <experiment_id>
  python -m agent_eval audit test --experiment <experiment_id>
  python -m agent_eval audit smoke --config <config_path>
  python -m agent_eval audit budget --experiment <experiment_id>
  python -m agent_eval audit leakage --experiment <experiment_id>
  python -m agent_eval audit claims --experiment <experiment_id>
  python -m agent_eval audit release --experiment <experiment_id>
"""
from __future__ import annotations

import os
import sys

import click

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


@click.group()
def audit():
    """Audit and validation commands for the research prototype."""


@audit.command()
@click.option("--experiment", "-e", required=True, help="Experiment ID")
def inspect(experiment: str):
    """Inspect experiment and audit status."""
    experiment_dir = os.path.join("artifacts", "experiments", experiment)
    analysis_dir = os.path.join(experiment_dir, "analysis") if os.path.isdir(
        os.path.join(experiment_dir, "analysis")
    ) else None
    
    if not os.path.isdir(experiment_dir):
        click.echo(f"Experiment directory not found: {experiment_dir}")
        sys.exit(1)
    
    # Run quick checks
    click.echo(f"Experiment: {experiment}")
    click.echo(f"Experiment directory: {experiment_dir}")
    
    if analysis_dir:
        click.echo(f"Analysis directory: {analysis_dir}")
        
        # List available analysis artifacts
        artifacts = ["run_metrics.csv", "aggregate_metrics.csv", 
                     "pairwise_comparisons.csv", "hypothesis_results.csv",
                     "bootstrap_results.csv", "effect_sizes.csv",
                     "holdout_metrics.csv", "branching_metrics.csv",
                     "sensitivity_results.csv", "analysis_manifest.json"]
        
        click.echo("Available analysis artifacts:")
        for artifact in artifacts:
            path = os.path.join(analysis_dir, artifact)
            exists = os.path.exists(path)
            click.echo(f"  {'✓' if exists else '✗'} {artifact}")
    else:
        click.echo("No analysis directory found")
    
    # Run ground-truth tests
    try:
        gt_results = run_ground_truth_tests(experiment_dir)
        click.echo("\nGround-truth evaluator results:")
        for fixture, result in gt_results.items():
            status = result.get("actual_outcome", "UNTESTED")
            click.echo(f"  {fixture}: {status}")
    except Exception as e:
        click.echo(f"\nError running ground-truth tests: {e}")
    
    # Run budget audit
    try:
        budget_results = run_budget_audit(experiment_dir)
        click.echo("\nBudget audit:")
        click.echo(f"  Total cost: {budget_results['total_cost']}")
        click.echo(f"  Configured budget: {budget_results['configured_budget']}")
        click.echo(f"  Discrepancy: {budget_results['discrepancy']}")
        click.echo(f"  Pass: {budget_results['pass']}")
    except Exception as e:
        click.echo(f"\nError running budget audit: {e}")
    
    # Run state isolation audit
    try:
        state_results = run_state_isolation_audit(experiment_dir)
        click.echo(f"\nState isolation audit: {'PASS' if state_results['pass'] else 'FAIL'}")
        for check_name, check_result in state_results.get("checks", {}).items():
            check_pass = check_result.get("pass", False)
            click.echo(f"  {check_name}: {'PASS' if check_pass else 'FAIL'}")
    except Exception as e:
        click.echo(f"\nError running state isolation audit: {e}")
    
    # Run selector leakage test
    try:
        leakage_results = run_selector_leakage_audit(experiment_dir)
        click.echo(f"\nSelector leakage audit: {'PASS' if leakage_results['pass'] else 'FAIL'}")
        for check_name, check_result in leakage_results.get("checks", {}).items():
            check_pass = check_result.get("pass", False)
            click.echo(f"  {check_name}: {'PASS' if check_pass else 'FAIL'}")
    except Exception as e:
        click.echo(f"\nError running selector leakage audit: {e}")
    
    # Run claims audit
    try:
        claims_results = run_claims_audit(experiment_dir, analysis_dir or "")
        click.echo("\nClaims audit:")
        click.echo(f"  Release decision: {claims_results['release_decision']}")
        click.echo(f"  Total claims: {len(claims_results['claim_ledger'])}")
        click.echo(f"  Blocking issues: {len(claims_results.get('blocking_issues', []))}")
        click.echo(f"  Conditional issues: {len(claims_results.get('conditional_issues', []))}")
        for claim in claims_results['claim_ledger'][:3]:  # Show first 3
            click.echo(f"  Claim {claim['claim_id']}: {claim['validation_status']}")
    except Exception as e:
        click.echo(f"\nError running claims audit: {e}")
    
    # Run statistical audit
    try:
        stat_results = run_statistical_audit(analysis_dir) if analysis_dir else {"error": "no analysis dir"}
        click.echo(f"\nStatistical audit: {stat_results}")
    except Exception as e:
        click.echo(f"\nError running statistical audit: {e}")
    
    # Run fairness audit
    try:
        fairness_results = run_fairness_audit(experiment_dir)
        click.echo(f"\nFairness audit: {fairness_results}")
    except Exception as e:
        click.echo(f"\nError running fairness audit: {e}")
    
    # Run integrity audit
    try:
        integrity_results = run_integrity_audit(experiment_dir, analysis_dir or "")
        click.echo(f"\nIntegrity audit: {'PASS' if integrity_results['is_valid'] else 'FAIL'}")
        for violation in integrity_results.get('violations', []):
            click.echo(f"  Violation: {violation.detail}")
    except Exception as e:
        click.echo(f"\nError running integrity audit: {e}")
    
    # Run reproducibility audit
    try:
        repro_results = run_reproducibility_audit(experiment_dir)
        click.echo(f"\nReproducibility audit: {'PASS' if repro_results['pass'] else 'FAIL'}")
        for check, result in repro_results.get('checks', {}).items():
            click.echo(f"  {check}: {'PASS' if result['pass'] else 'FAIL'}")
    except Exception as e:
        click.echo(f"\nError running reproducibility audit: {e}")
    
    # Run visual audit
    try:
        visual_results = run_visual_audit(analysis_dir) if analysis_dir else {"error": "no analysis dir"}
        click.echo(f"\nVisual audit: {visual_results}")
    except Exception as e:
        click.echo(f"\nError running visual audit: {e}")
    
    # Final release decision
    click.echo(f"\nRelease decision: {claims_results['release_decision'] if 'claims_results' in dir() else 'N/A'}")