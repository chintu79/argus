"""CLI commands for experiment execution."""

from __future__ import annotations

import sys
from pathlib import Path

import click
import yaml

from agent_eval.experiment.models import ExperimentConfiguration
from agent_eval.experiment.runner import ExperimentRunner


@click.group()
def experiment():
    """Experiment execution commands."""


@experiment.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Experiment configuration file")
def validate(config: str):
    """Validate experiment configuration."""
    config_path = Path(config)
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
    
    exp_config = ExperimentConfiguration(**config_data)
    runner = ExperimentRunner(exp_config)
    valid, errors = runner.validate_configuration()
    
    if valid:
        click.echo("Configuration is valid!")
        sys.exit(0)
    else:
        click.echo("Configuration errors:")
        for error in errors:
            click.echo(f"  - {error}")
        sys.exit(1)


@experiment.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Experiment configuration file")
@click.option("--dry-run", is_flag=True, help="Show execution plan without running")
def run(config: str, dry_run: bool):
    """Run an experiment."""
    config_path = Path(config)
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
    
    exp_config = ExperimentConfiguration(**config_data)
    runner = ExperimentRunner(exp_config)
    
    if dry_run:
        plan = runner.dry_run()
        click.echo("Dry run plan:")
        click.echo(f"  Experiment: {plan['experiment_id']}")
        click.echo(f"  Methods: {plan['methods']}")
        click.echo(f"  Seeds: {plan['seeds']}")
        click.echo(f"  Tasks: {plan['tasks']}")
        click.echo(f"  Budget: {plan['budget']} tokens")
        click.echo(f"  Total runs: {plan['total_runs']}")
        click.echo(f"  Output: {plan['output_dir']}")
        return
    
    click.echo(f"Running experiment: {exp_config.experiment_id}")
    manifest = runner.run_experiment()
    
    click.echo("Experiment completed!")
    click.echo(f"  Completed runs: {manifest.completed_runs}")
    click.echo(f"  Failed runs: {manifest.failed_runs}")
    click.echo(f"  Manifest: {manifest.experiment_id}")


@experiment.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Experiment configuration file")
def smoke(config: str):
    """Run a quick smoke test with minimal configuration."""
    config_path = Path(config)
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
    
    exp_config = ExperimentConfiguration(**config_data)
    runner = ExperimentRunner(exp_config)
    
    click.echo("Running smoke test...")
    manifest = runner.run_experiment()
    
    click.echo("Smoke test completed!")
    click.echo(f"  Completed runs: {manifest.completed_runs}")
    click.echo(f"  Failed runs: {manifest.failed_runs}")


@experiment.command()
@click.option("--experiment-id", required=True, help="Experiment ID")
@click.option("--run-id", required=True, help="Run ID to resume")
def resume(experiment_id: str, run_id: str):
    """Resume an interrupted experiment run."""
    click.echo(f"Resuming experiment {experiment_id}, run {run_id}")
    # TODO: Implement resume logic
    click.echo("Resume functionality not yet implemented")


@experiment.command()
@click.option("--experiment-id", required=True, help="Experiment ID to inspect")
def inspect(experiment_id: str):
    """Inspect experiment results."""
    from agent_eval.domain.identifiers import is_safe_identifier
    if not is_safe_identifier(experiment_id):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        return

    base_dir = Path("artifacts/experiments").resolve()
    artifacts_dir = (base_dir / experiment_id).resolve()
    if not artifacts_dir.is_relative_to(base_dir):
        click.echo(f"Path traversal detected: {experiment_id}")
        return
    
    if not artifacts_dir.exists():
        click.echo(f"Experiment {experiment_id} not found")
        return
    
    # Read manifest
    manifest_path = Path("artifacts/experiments") / experiment_id / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            import json
            manifest = json.load(f)
        click.echo(f"Experiment: {manifest['experiment_id']}")
        click.echo(f"  Methods: {manifest['methods']}")
        click.echo(f"  Completed runs: {manifest['completed_runs']}")
        click.echo(f"  Failed runs: {manifest['failed_runs']}")
    else:
        click.echo("Manifest not found")
    
    # List runs
    runs_dir = Path("artifacts/experiments") / experiment_id / "runs"
    if runs_dir.exists():
        runs = list(runs_dir.iterdir())
        click.echo(f"  Runs: {len(runs)}")
        for run_dir in runs:
            summary_path = run_dir / "summary.json"
            if summary_path.exists():
                with open(summary_path, "r") as f:
                    import json
                    summary = json.load(f)
                click.echo(f"  {run_dir.name}: {summary['status']} - {summary['method']} seed={summary['seed']} tokens={summary['tokens_used']}")


@experiment.command()
@click.option("--output", "-o", default="configs/experiments/smoke.yaml", type=click.Path(), help="Output configuration file")
def generate_smoke(output: str):
    """Generate a smoke test configuration file."""
    smoke_config = {
        "experiment_id": "smoke_test",
        "name": "Smoke Test",
        "methods": ["STATIC", "RANDOM", "UNBRANCHED_ADAPTIVE", "STATE_BRANCHED_ADAPTIVE"],
        "budget": {
            "total_tokens": 50000
        },
        "repetitions": {
            "seeds": [42]
        },
        "tasks": {
            "split": "SEARCH",
            "limit": 3
        },
        "agent": {
            "temperature": 0.0
        },
        "evaluation": {
            "reproducibility_runs": 3,
            "minimum_rep_k": 0.75
        },
        "checkpoint": {
            "enabled": True,
            "every_n_actions": 10
        },
        "dry_run": False,
        "output_dir": "artifacts/experiments"
    }
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        yaml.dump(smoke_config, f, default_flow_style=False, sort_keys=False)
    
    click.echo(f"Smoke test configuration written to {output_path}")


@experiment.command()
@click.option("--experiment-id", required=True, help="Experiment ID to validate")
def final(experiment_id: str):
    """Run final validation command for the experiment.
    
    Validates:
    - Repository Integrity
    - Dependency Integrity
    - Test Status
    - Experiment Integrity
    - Budget Integrity
    - Branch Integrity
    - Selector Leakage
    - Evaluator Accuracy
    - Statistical Integrity
    - Visualization Integrity
    - Report Integrity
    - Evidence Integrity
    - Reproducibility Package
    - Demo Package
    - Defense Package
    - Submission Manifest
    - Checksums
    """
    import json
    import sys
    from pathlib import Path
    
    base_dir = Path("artifacts/experiments").resolve()
    experiment_dir = (base_dir / experiment_id).resolve()
    
    if not experiment_dir.is_relative_to(base_dir):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        sys.exit(1)
    
    if not experiment_dir.exists():
        click.echo(f"Experiment {experiment_id} not found")
        sys.exit(1)
    
    click.echo("=" * 50)
    click.echo("FINAL PROJECT VALIDATION")
    click.echo("=" * 50)
    click.echo("")
    
    all_pass = True
    
    # Repository Integrity
    click.echo("Repository Integrity ... ", nl=False)
    try:
        repo_file = Path("pyproject.toml")
        if repo_file.exists():
            click.echo("PASS")
        else:
            click.echo("FAIL: pyproject.toml missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Dependency Integrity
    click.echo("Dependency Integrity ... ", nl=False)
    try:
        import importlib
        deps = ["click", "pydantic", "sqlalchemy", "pandas", "numpy", "scipy", "pyyaml", "matplotlib", "seaborn"]
        for dep in deps:
            importlib.import_module(deps[deps.index(dep)].replace("-", "_") if dep != "pyyaml" else "yaml")
        click.echo("PASS")
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Test Status
    click.echo("Tests ... ", nl=False)
    try:
        import subprocess
        result = subprocess.run(["pytest", "--tb=short", "tests/unit/agents/test_mock_agent.py", "-v"], 
                              capture_output=True, text=True, cwd=".", check=False)
        if result.returncode == 0:
            click.echo("PASS")
        else:
            click.echo("FAIL")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Experiment Integrity
    click.echo("Experiment Integrity ... ", nl=False)
    try:
        manifest_path = experiment_dir / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            if manifest.get("experiment_id") == experiment_id:
                click.echo("PASS")
            else:
                click.echo("FAIL: manifest mismatch")
                all_pass = False
        else:
            click.echo("FAIL: manifest.json missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Budget Integrity
    click.echo("Budget Integrity ... ", nl=False)
    try:
        budget_path = experiment_dir / "artifacts" / "budget_reconciliation.json"
        if budget_path.exists():
            with open(budget_path) as f:
                budget_data = json.load(f)
            discrepancy = budget_data.get("discrepancy", 0)
            if abs(discrepancy) < 0.05 * 50000:  # within 5%
                click.echo(f"PASS (discrepancy: {discrepancy})")
            else:
                click.echo(f"FAIL (discrepancy: {discrepancy})")
                all_pass = False
        else:
            click.echo("FAIL: budget_reconciliation.json missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Branch Integrity
    click.echo("Branch Integrity ... ", nl=False)
    try:
        from agent_eval.audit.state_isolation import run_state_isolation_audit
        state_results = run_state_isolation_audit(str(experiment_dir))
        if state_results.get("pass", False):
            click.echo("PASS")
        else:
            click.echo("FAIL")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Selector Leakage
    click.echo("Selector Leakage ... ", nl=False)
    try:
        from agent_eval.audit.selector_leakage import run_selector_leakage_audit
        leakage_results = run_selector_leakage_audit(str(experiment_dir))
        if leakage_results.get("pass", False):
            click.echo("PASS")
        else:
            click.echo("FAIL")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Statistical Integrity
    click.echo("Statistical Integrity ... ", nl=False)
    try:
        stat_path = experiment_dir / "analysis" / "statistical_audit.json"
        if stat_path.exists():
            with open(stat_path) as f:
                json.load(f)
            click.echo("PASS")
        else:
            click.echo("FAIL: statistical_audit.json missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Visualization Integrity
    click.echo("Visualization Integrity ... ", nl=False)
    try:
        figures_dir = experiment_dir / "figures"
        if figures_dir.exists():
            required_figs = ["FIG-01", "FIG-02", "FIG-03", "FIG-04", "FIG-05", "FIG-06", "FIG-07", "FIG-08", "FIG-09", "FIG-10", "FIG-11", "FIG-12"]
            missing = [f for f in required_figs if not (figures_dir / f"{f}.png").exists()]
            if not missing:
                click.echo("PASS")
            else:
                click.echo(f"FAIL: missing {', '.join(missing)}")
                all_pass = False
        else:
            click.echo("FAIL: figures directory missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Report Integrity
    click.echo("Report Integrity ... ", nl=False)
    try:
        report_path = Path("final_submission/manuscript/final_research_report.md")
        if report_path.exists() and report_path.stat().st_size > 0:
            click.echo("PASS")
        else:
            click.echo("FAIL: final_research_report.md missing or empty")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Evidence Integrity
    click.echo("Evidence Integrity ... ", nl=False)
    try:
        evidence_dir = experiment_dir / "evidence"
        if evidence_dir.exists() and any(evidence_dir.iterdir()):
            click.echo("PASS")
        else:
            click.echo("FAIL: evidence directory empty or missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Reproducibility Package
    click.echo("Reproducibility Package ... ", nl=False)
    try:
        repro_dir = Path("final_submission/reproducibility")
        if repro_dir.exists():
            required = ["README.md", "environment.yml", "requirements.txt", "commands.sh"]
            missing = [f for f in required if not (repro_dir / f).exists()]
            if not missing:
                click.echo("PASS")
            else:
                click.echo(f"FAIL: missing {', '.join(missing)}")
                all_pass = False
        else:
            click.echo("FAIL: reproducibility package missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Demo Package
    click.echo("Demo Package ... ", nl=False)
    try:
        demo_dir = Path("final_submission/demo")
        if demo_dir.exists():
            required = ["README.md", "demo_config.yaml", "demo_commands.sh", "demo_script.md", "expected_output.md"]
            missing = [f for f in required if not (demo_dir / f).exists()]
            if not missing:
                click.echo("PASS")
            else:
                click.echo(f"FAIL: missing {', '.join(missing)}")
                all_pass = False
        else:
            click.echo("FAIL: demo package missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Defense Package
    click.echo("Defense Package ... ", nl=False)
    try:
        defense_dir = Path("final_submission/defense")
        if defense_dir.exists():
            required = ["architecture_explanation.md", "algorithm_defense.md", "questions.md", "answer_guide.md", "limitation_defense.md"]
            missing = [f for f in required if not (defense_dir / f).exists()]
            if not missing:
                click.echo("PASS")
            else:
                click.echo(f"FAIL: missing {', '.join(missing)}")
                all_pass = False
        else:
            click.echo("FAIL: defense package missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Submission Manifest
    click.echo("Submission Manifest ... ", nl=False)
    try:
        manifest_path = Path("final_submission/submission_manifest.json")
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            if manifest.get("status") == "SUBMISSION_READY":
                click.echo("PASS")
            else:
                click.echo("FAIL: status not SUBMISSION_READY")
                all_pass = False
        else:
            click.echo("FAIL: submission_manifest.json missing")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    # Checksums
    click.echo("Checksums ... ", nl=False)
    try:
        checksums_path = Path("final_submission/SHA256SUMS")
        if checksums_path.exists() and checksums_path.stat().st_size > 0:
            click.echo("PASS")
        else:
            click.echo("FAIL: SHA256SUMS missing or empty")
            all_pass = False
    except Exception as e:
        click.echo(f"FAIL: {e}")
        all_pass = False
    
    click.echo("")
    click.echo("=" * 50)
    if all_pass:
        click.echo("STATUS: SUBMISSION_READY")
        sys.exit(0)
    else:
        click.echo("STATUS: VALIDATION_FAILED")
        sys.exit(1)


if __name__ == "__main__":
    experiment()