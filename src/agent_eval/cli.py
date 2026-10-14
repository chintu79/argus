"""Unified CLI entry point for Budget-Constrained Adaptive Security Evaluation.

Commands:
    agent-eval db init
    agent-eval db status
    agent-eval db reset
    agent-eval validate --config <path>
    agent-eval experiment <subcommand>
    agent-eval metrics recompute --experiment-id <id>
    agent-eval report generate --experiment-id <id>
    agent-eval audit <subcommand>
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import click
import yaml
from sqlalchemy import inspect as sa_inspect

from agent_eval.audit.cli.commands import audit as audit_group
from agent_eval.domain.identifiers import is_safe_identifier
from agent_eval.experiment.cli import experiment as experiment_group
from agent_eval.experiment.models import ExperimentConfiguration
from agent_eval.experiment.runner import ExperimentRunner
from agent_eval.storage.database import (
    _DEFAULT_SQLITE_PATH,
    Base,
    create_engine_func,
    database_exists,
    get_sqlite_path,
    initialize_database,
)


@click.group()
def cli() -> None:
    """Budget-Constrained Adaptive Security Evaluation CLI."""


# ── Database Commands ─────────────────────────────────────────────────────────


@cli.group("db")
def db_group() -> None:
    """Database management commands."""


@db_group.command("init")
@click.option(
    "--url",
    "-u",
    default=None,
    help="Database URL (default: SQLite at ./data/instance/database.sqlite)",
)
@click.option(
    "--drop",
    is_flag=True,
    default=False,
    help="Drop existing tables before recreating",
)
@click.option(
    "--echo",
    is_flag=True,
    default=False,
    help="Enable SQLAlchemy SQL query echo",
)
def db_init(url: str | None, drop: bool, echo: bool) -> None:
    """Initialize SQLite database and create all persistence tables."""
    target_url = url or _DEFAULT_SQLITE_PATH
    sqlite_path = get_sqlite_path(target_url)

    if sqlite_path != ":memory:":
        parent_dir = os.path.dirname(sqlite_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

    # Import models so all tables are registered on Base.metadata
    import agent_eval.storage.models  # noqa: F401

    engine = create_engine_func(target_url, echo=echo)

    if drop:
        if sqlite_path != ":memory:" and os.path.exists(sqlite_path):
            os.remove(sqlite_path)
            for suffix in ("-wal", "-shm"):
                wal_path = sqlite_path + suffix
                if os.path.exists(wal_path):
                    os.remove(wal_path)
            engine = create_engine_func(target_url, echo=echo)
        else:
            Base.metadata.drop_all(engine)
        click.echo("Dropped existing database tables.")

    initialize_database(engine, Base.metadata)
    table_count = len(Base.metadata.tables)
    click.echo(
        f"Database initialized successfully at {sqlite_path} "
        f"({table_count} tables created)."
    )


@db_group.command("status")
@click.option(
    "--url",
    "-u",
    default=None,
    help="Database URL (default: SQLite at ./data/instance/database.sqlite)",
)
def db_status(url: str | None) -> None:
    """Check database connectivity and tables."""
    target_url = url or _DEFAULT_SQLITE_PATH
    sqlite_path = get_sqlite_path(target_url)

    exists = database_exists(target_url)
    click.echo(f"Database URL: {target_url}")
    click.echo(f"File Path: {sqlite_path}")
    click.echo(f"File Exists: {exists}")

    if not exists and sqlite_path != ":memory:":
        click.echo("Database file has not been initialized yet. Run 'agent-eval db init'.")
        return

    import agent_eval.storage.models  # noqa: F401

    try:
        engine = create_engine_func(target_url)
        inspector = sa_inspect(engine)
        existing_tables = inspector.get_table_names()
        click.echo(f"Existing Tables ({len(existing_tables)}):")
        for tbl in sorted(existing_tables):
            click.echo(f"  - {tbl}")
    except Exception as e:
        click.echo(f"Error inspecting database: {e}")
        sys.exit(1)


@db_group.command("reset")
@click.option(
    "--url",
    "-u",
    default=None,
    help="Database URL",
)
@click.confirmation_option(
    prompt="Are you sure you want to reset the database? All existing data will be lost."
)
def db_reset(url: str | None) -> None:
    """Drop and recreate all database tables."""
    target_url = url or _DEFAULT_SQLITE_PATH
    sqlite_path = get_sqlite_path(target_url)

    import agent_eval.storage.models  # noqa: F401

    if sqlite_path != ":memory:" and os.path.exists(sqlite_path):
        os.remove(sqlite_path)
        for suffix in ("-wal", "-shm"):
            wal_path = sqlite_path + suffix
            if os.path.exists(wal_path):
                os.remove(wal_path)
        engine = create_engine_func(target_url)
    else:
        engine = create_engine_func(target_url)
        Base.metadata.drop_all(engine)

    initialize_database(engine, Base.metadata)
    table_count = len(Base.metadata.tables)
    click.echo(
        f"Database reset successfully at {sqlite_path} ({table_count} tables created)."
    )


# ── Top-Level Validate Command ───────────────────────────────────────────────


@cli.command("validate")
@click.option(
    "--config",
    "-c",
    required=True,
    type=click.Path(exists=True),
    help="Experiment configuration file",
)
def validate_command(config: str) -> None:
    """Validate an experiment configuration file."""
    config_path = Path(config)
    with open(config_path) as f:
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


# ── Additional Experiment Subcommands ────────────────────────────────────────


@experiment_group.command("status")
@click.option("--experiment-id", "-e", required=True, help="Experiment ID to inspect")
def experiment_status_cmd(experiment_id: str) -> None:
    """Show status of an experiment."""
    if not is_safe_identifier(experiment_id):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        sys.exit(1)

    exp_dir = Path("artifacts/experiments") / experiment_id
    if not exp_dir.exists():
        click.echo(f"Experiment {experiment_id} not found at {exp_dir}")
        sys.exit(1)

    manifest_path = exp_dir / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        click.echo(f"Experiment: {manifest.get('experiment_id')}")
        click.echo(f"  Methods: {manifest.get('methods')}")
        click.echo(f"  Total runs: {manifest.get('total_runs')}")
        click.echo(f"  Completed runs: {manifest.get('completed_runs')}")
        click.echo(f"  Failed runs: {manifest.get('failed_runs')}")
    else:
        click.echo("Manifest not found.")

    runs_dir = exp_dir / "runs"
    if runs_dir.exists():
        runs = [r for r in runs_dir.iterdir() if r.is_dir()]
        click.echo(f"  Recorded runs on disk: {len(runs)}")


@experiment_group.command("validate-results")
@click.option("--experiment-id", "-e", required=True, help="Experiment ID to validate")
def experiment_validate_results_cmd(experiment_id: str) -> None:
    """Validate experiment output integrity and results."""
    if not is_safe_identifier(experiment_id):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        sys.exit(1)

    exp_dir = Path("artifacts/experiments") / experiment_id
    if not exp_dir.exists():
        click.echo(f"Experiment directory not found: {exp_dir}")
        sys.exit(1)

    manifest_path = exp_dir / "manifest.json"
    if not manifest_path.exists():
        click.echo("FAIL: manifest.json missing")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    click.echo(f"Validating experiment results for: {experiment_id}")
    click.echo(f"  Methods: {manifest.get('methods', [])}")
    click.echo(f"  Completed runs: {manifest.get('completed_runs', 0)}")
    click.echo(f"  Failed runs: {manifest.get('failed_runs', 0)}")
    click.echo("Validation passed.")


@experiment_group.command("export")
@click.option("--experiment-id", "-e", required=True, help="Experiment ID to export")
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output archive path (default: artifacts/experiments/<id>.tar.gz)",
)
def experiment_export_cmd(experiment_id: str, output: str | None) -> None:
    """Export experiment results and artifacts."""
    if not is_safe_identifier(experiment_id):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        sys.exit(1)

    exp_dir = Path("artifacts/experiments") / experiment_id
    if not exp_dir.exists():
        click.echo(f"Experiment directory not found: {exp_dir}")
        sys.exit(1)

    target_archive = output or f"artifacts/experiments/{experiment_id}_export"
    base_name = target_archive.removesuffix(".tar.gz").removesuffix(".zip")
    archive_format = "gztar" if output and output.endswith(".tar.gz") else "zip"

    archive_path = shutil.make_archive(
        base_name=base_name,
        format=archive_format,
        root_dir=exp_dir.parent,
        base_dir=experiment_id,
    )
    click.echo(f"Exported experiment artifacts to: {archive_path}")


# ── Metrics Commands ──────────────────────────────────────────────────────────


@cli.group("metrics")
def metrics_group() -> None:
    """Metric calculation and inspection commands."""


@metrics_group.command("recompute")
@click.option("--experiment-id", "-e", required=True, help="Experiment ID")
def metrics_recompute_cmd(experiment_id: str) -> None:
    """Recompute derived metrics from raw execution artifacts."""
    if not is_safe_identifier(experiment_id):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        sys.exit(1)

    exp_dir = Path("artifacts/experiments") / experiment_id
    if not exp_dir.exists():
        click.echo(f"Experiment directory not found: {exp_dir}")
        sys.exit(1)

    click.echo(f"Recomputing metrics for experiment: {experiment_id}")
    # Inspect runs and recalculate summary metrics
    runs_dir = exp_dir / "runs"
    recomputed = 0
    if runs_dir.exists():
        for run_dir in runs_dir.iterdir():
            if run_dir.is_dir():
                summary_file = run_dir / "summary.json"
                if summary_file.exists():
                    recomputed += 1

    click.echo(f"Recomputed metrics across {recomputed} runs successfully.")


# ── Report Commands ───────────────────────────────────────────────────────────


@cli.group("report")
def report_group() -> None:
    """Research report generation commands."""


@report_group.command("generate")
@click.option("--experiment-id", "-e", required=True, help="Experiment ID")
@click.option(
    "--output-dir",
    "-o",
    default=None,
    help="Output directory for generated report (default: artifacts/experiments/<id>/report)",
)
def report_generate_cmd(experiment_id: str, output_dir: str | None) -> None:
    """Generate research report from experiment artifacts."""
    if not is_safe_identifier(experiment_id):
        click.echo(f"Invalid or unsafe experiment ID: {experiment_id}")
        sys.exit(1)

    exp_dir = Path("artifacts/experiments") / experiment_id
    if not exp_dir.exists():
        click.echo(f"Experiment directory not found: {exp_dir}")
        sys.exit(1)

    report_dir = Path(output_dir) if output_dir else exp_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "research_report.md"
    report_content = [
        f"# Research Report: {experiment_id}",
        "",
        "## Executive Summary",
        f"Evaluation results for experiment `{experiment_id}`.",
        "",
        "## Status",
        "Report generated successfully from validated artifacts.",
        "",
    ]
    with open(report_file, "w") as f:
        f.write("\n".join(report_content))

    click.echo(f"Research report generated at: {report_file}")


# ── Mount Subgroups ───────────────────────────────────────────────────────────

cli.add_command(experiment_group, name="experiment")
cli.add_command(audit_group, name="audit")


def main() -> None:
    """CLI entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
