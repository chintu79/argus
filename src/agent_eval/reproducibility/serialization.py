"""Serialization utilities for reproducibility verification."""

from __future__ import annotations

import json
from typing import Any

from agent_eval.reproducibility.models import (
    ReproducibilityRequest,
    ReproducibilityResult,
    VerificationRun,
)


def request_to_dict(request: ReproducibilityRequest) -> dict[str, Any]:
    """Convert ReproducibilityRequest to JSON-compatible dict."""
    return {
        "failure_id": request.failure_id,
        "trajectory_id": request.trajectory_id,
        "scenario_id": request.scenario_id,
        "verification_seeds": request.verification_seeds,
        "k": request.k,
        "temperature": request.temperature,
        "max_attempts": request.max_attempts,
        "timeout": request.timeout,
        "threshold": request.threshold,
        "metadata": request.metadata,
    }


def result_to_dict(result: ReproducibilityResult) -> dict[str, Any]:
    """Convert ReproducibilityResult to JSON-compatible dict."""
    return {
        "failure_id": result.failure_id,
        "verification_id": result.verification_id,
        "k": result.k,
        "successful_replications": result.successful_replications,
        "rep_k": result.rep_k,
        "threshold": result.threshold,
        "status": result.status.value
        if hasattr(result.status, "value")
        else str(result.status),
        "runs": [run_to_dict(r) for r in result.runs],
        "created_at": result.created_at.isoformat()
        if hasattr(result.created_at, "isoformat")
        else str(result.created_at),
        "completed_at": result.completed_at.isoformat()
        if result.completed_at and hasattr(result.completed_at, "isoformat")
        else str(result.completed_at)
        if result.completed_at
        else None,
        "verifier_version": result.verifier_version,
        "metadata": result.metadata,
    }


def run_to_dict(run: VerificationRun) -> dict[str, Any]:
    """Convert VerificationRun to JSON-compatible dict."""
    return {
        "run_id": run.run_id,
        "verification_id": run.verification_id,
        "seed": run.seed,
        "status": run.status.value if hasattr(run.status, "value") else str(run.status),
        "started_at": run.started_at.isoformat()
        if run.started_at and hasattr(run.started_at, "isoformat")
        else str(run.started_at)
        if run.started_at
        else None,
        "completed_at": run.completed_at.isoformat()
        if run.completed_at and hasattr(run.completed_at, "isoformat")
        else str(run.completed_at)
        if run.completed_at
        else None,
        "trajectory_id": run.trajectory_id,
        "target_matched": (
            run.target_matched.value
            if run.target_matched is not None
            else None
        ),
        "observed_signature": signature_to_dict(run.observed_signature)
        if run.observed_signature
        else None,
        "invariant_results": run.invariant_results,
        "token_count": run.token_count,
        "error": run.error,
    }


def signature_to_dict(signature: Any) -> dict[str, Any]:
    """Convert FailureSignature to dict."""
    if hasattr(signature, "model_dump"):
        return signature.model_dump()
    elif hasattr(signature, "to_canonical_string"):
        return {
            "invariant_id": signature.invariant_id,
            "reason_code": signature.reason_code,
            "action": signature.action,
            "resource": signature.resource,
            "state_transition": signature.state_transition,
            "resource_type": signature.resource_type,
            "policy_decision": signature.policy_decision,
        }
    return {}


def reproducibility_to_jsonl(results: list[Any]) -> str:
    """Convert a list of ReproducibilityResults to JSONL format."""
    lines = []
    for result in results:
        if hasattr(result, "model_dump"):
            d = result.model_dump()
        else:
            d = result_to_dict(result)
        lines.append(json.dumps(d, default=str))
    return "\n".join(lines)
