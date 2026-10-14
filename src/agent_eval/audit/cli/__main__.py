"""CLI entry point for Phase 17 audit commands."""

from __future__ import annotations

import sys

from agent_eval.audit.cli.commands import audit

if __name__ == "__main__":
    try:
        audit()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)