"""Unit tests for agent-eval unified CLI."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from agent_eval.cli import cli


def test_cli_help() -> None:
    """Test CLI root help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Budget-Constrained Adaptive Security Evaluation CLI." in result.output
    assert "db" in result.output
    assert "experiment" in result.output
    assert "audit" in result.output


def test_db_lifecycle(tmp_path: Path) -> None:
    """Test db init, db status, and db reset commands on an isolated SQLite database."""
    runner = CliRunner()
    db_file = tmp_path / "test.sqlite"
    url = f"sqlite:///{db_file}"

    # 1. db status before init
    result = runner.invoke(cli, ["db", "status", "--url", url])
    assert result.exit_code == 0
    assert "File Exists: False" in result.output

    # 2. db init
    result = runner.invoke(cli, ["db", "init", "--url", url])
    assert result.exit_code == 0
    assert "Database initialized successfully" in result.output
    assert "14 tables created" in result.output
    assert db_file.exists()

    # 3. db status after init
    result = runner.invoke(cli, ["db", "status", "--url", url])
    assert result.exit_code == 0
    assert "File Exists: True" in result.output
    assert "Existing Tables (14):" in result.output
    assert "executions" in result.output
    assert "validated_failures" in result.output

    # 4. db reset
    result = runner.invoke(cli, ["db", "reset", "--url", url, "--yes"])
    assert result.exit_code == 0
    assert "Database reset successfully" in result.output
    assert db_file.exists()


def test_audit_help() -> None:
    """Test audit subcommand group help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["audit", "--help"])
    assert result.exit_code == 0
    assert "Audit and validation commands" in result.output
    assert "inspect" in result.output
