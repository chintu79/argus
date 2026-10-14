"""Failure candidate serialization and hashing.

Provides deterministic JSON serialization and fingerprint computation
for candidate identity and integrity verification.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC
from typing import Any

from agent_eval.domain.enums import InvariantSeverity
from agent_eval.domain.identifiers import make_id
from agent_eval.failures.models import FailureCandidate, FailureReasonCode


def candidate_to_dict(candidate: FailureCandidate) -> dict[str, Any]:
    """Convert a FailureCandidate to a JSON-compatible dict."""
    return {
        "failure_id": candidate.failure_id,
        "trajectory_id": candidate.trajectory_id,
        "invariant_result_id": candidate.invariant_result_id,
        "invariant_id": candidate.invariant_id,
        "status": candidate.status.value,
        "severity": candidate.severity.value,
        "reason_code": candidate.reason_code.value,
        "description": candidate.description,
        "evidence": candidate.evidence,
        "detected_at": candidate.detected_at.isoformat()
        if hasattr(candidate.detected_at, "isoformat")
        else str(candidate.detected_at),
        "detector_version": candidate.detector_version,
        "metadata": candidate.metadata,
    }


def candidate_from_dict(data: dict[str, Any]) -> FailureCandidate:
    """Convert a dict to a FailureCandidate.

    Ensures required fields are present and validates IDs.
    """
    from datetime import datetime

    # Parse detected_at
    detected_at_str = data.get("detected_at", "")
    if isinstance(detected_at_str, str):
        try:
            from datetime import datetime

            detected_at = datetime.fromisoformat(detected_at_str)
            if detected_at.tzinfo is None:
                detected_at = detected_at.replace(tzinfo=UTC)
        except (ValueError, TypeError):
            detected_at = datetime.now(UTC)
    else:
        detected_at = datetime.now(UTC)

    # Extract reason code
    reason_code_str = data.get("reason_code", "")
    try:
        reason_code = FailureReasonCode(reason_code_str)
    except ValueError:
        reason_code = FailureReasonCode.UNAUTHORIZED_SENSITIVE_ACTION

    # Extract status
    status_str = data.get("status", "")
    from agent_eval.failures.models import FailureCandidateStatus

    try:
        status = FailureCandidateStatus(status_str)
    except ValueError:
        status = FailureCandidateStatus.CANDIDATE

    # Build evidence dict
    evidence = data.get("evidence", {})

    candidate = FailureCandidate(
        failure_id=data.get("failure_id", make_id("fc")),
        trajectory_id=data.get("trajectory_id", "unknown"),
        invariant_result_id=data.get("invariant_result_id", "unknown"),
        invariant_id=data.get("invariant_id", "unknown"),
        status=status,
        severity=InvariantSeverity(
            data.get("severity", "MEDIUM").upper()
            if isinstance(data.get("severity"), str)
            else "MEDIUM"
        ),
        reason_code=reason_code,
        description=data.get("description", "Failure candidate"),
        evidence=evidence,
        detected_at=detected_at,
        detector_version=data.get("detector_version", "1.0"),
        metadata=data.get("metadata", {}),
        event_ids=evidence.get("event_ids", []),
        state_ids=evidence.get("state_ids", []),
        scenario_id=data.get("scenario_id"),
        agent_id=data.get("agent_id"),
        environment_id=data.get("environment_id"),
    )

    return candidate


def candidate_fingerprint(candidate: FailureCandidate) -> str:
    """Compute a deterministic fingerprint for a failure candidate.

    Based on semantic evidence, not timestamps or random values.
    Same evidence = same fingerprint.
    Different evidence = different fingerprint.
    """

    canonical_parts = [
        f"inv:{candidate.invariant_id}",
        f"rc:{candidate.reason_code.value}",
        f"evt:{':'.join(sorted(candidate.evidence.get('event_ids', [])))}"
        if candidate.evidence.get("event_ids")
        else "evt:none",
        f"st:{':'.join(sorted(candidate.evidence.get('state_ids', [])))}"
        if candidate.evidence.get("state_ids")
        else "st:none",
    ]
    canonical_string = "|".join(canonical_parts)
    return hashlib.sha256(canonical_string.encode("utf-8")).hexdigest()


def candidates_to_jsonl(candidates: list[FailureCandidate]) -> str:
    """Convert a list of FailureCandidates to JSONL format.

    Each line is a JSON object representing one candidate.
    """
    lines = []
    for candidate in candidates:
        d = candidate_to_dict(candidate)
        lines.append(json.dumps(d, default=str))
    return "\n".join(lines)


def jsonl_to_candidates(jsonl_text: str) -> list[FailureCandidate]:
    """Convert JSONL text to a list of FailureCandidates.

    Each line should be a JSON object as produced by candidates_to_jsonl.
    """
    import json

    candidates = []
    for line in jsonl_text.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            candidate = candidate_from_dict(data)
            candidates.append(candidate)
        except (json.JSONDecodeError, ValueError, KeyError):
            # Skip malformed lines rather than crashing
            continue
    return candidates
