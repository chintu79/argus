"""Serialization utilities for failure families."""

from __future__ import annotations

import json
from datetime import UTC
from typing import Any

from agent_eval.failure_families.models import (
    ClusteringRun,
    ClusteringRunResult,
    FailureFamily,
    FamilyCoherence,
    FamilyMembershipExplanation,
)


def family_to_dict(family: Any) -> dict[str, Any]:
    """Convert FailureFamily to JSON-compatible dict."""
    return {
        "family_id": family.family_id,
        "member_failure_ids": family.member_failure_ids,
        "representative_failure_id": family.representative_failure_id,
        "family_signature": family.family_signature,
        "family_size": family.family_size,
        "taxonomy_labels": family.taxonomy_labels,
        "coherence_score": family.coherence_score,
        "created_at": family.created_at.isoformat()
        if hasattr(family.created_at, "isoformat")
        else str(family.created_at),
        "clustering_version": family.clustering_version,
        "severity_distribution": family.severity_distribution,
        "invariant_distribution": family.invariant_distribution,
        "reason_code_distribution": family.reason_code_distribution,
        "environment_distribution": family.environment_distribution,
        "metadata": family.metadata,
    }


def family_from_dict(data: dict[str, Any]) -> Any:
    """Convert a dict to a FailureFamily."""
    from datetime import datetime

    # Parse created_at
    created_at_str = data.get("created_at", "")
    if isinstance(created_at_str, str) and created_at_str:
        try:
            created_at = datetime.fromisoformat(created_at_str)
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)
        except (ValueError, TypeError):
            created_at = datetime.now(UTC)
    else:
        created_at = datetime.now(UTC)

    return FailureFamily(
        family_id=data.get("family_id", ""),
        member_failure_ids=data.get("member_failure_ids", []),
        representative_failure_id=data.get("representative_failure_id", ""),
        family_signature=data.get("family_signature", ""),
        family_size=data.get("family_size", 0),
        taxonomy_labels=data.get("taxonomy_labels", []),
        coherence_score=data.get("coherence_score", 0.0),
        created_at=created_at,
        clustering_version=data.get("clustering_version", "1.0"),
        severity_distribution=data.get("severity_distribution", {}),
        invariant_distribution=data.get("invariant_distribution", {}),
        reason_code_distribution=data.get("reason_code_distribution", {}),
        environment_distribution=data.get("environment_distribution", {}),
        metadata=data.get("metadata", {}),
    )


def run_to_dict(run: Any) -> dict[str, Any]:
    """Convert ClusteringRun to dict."""
    return {
        "run_id": run.run_id,
        "configuration": run.configuration,
        "input_failure_count": run.input_failure_count,
        "eligible_failure_count": run.eligible_failure_count,
        "family_count": run.family_count,
        "singleton_count": run.singleton_count,
        "average_family_size": run.average_family_size,
        "average_coherence": run.average_coherence,
        "created_at": run.created_at.isoformat()
        if hasattr(run.created_at, "isoformat")
        else str(run.created_at),
        "clustering_version": run.clustering_version,
        "metadata": run.metadata,
    }


def run_from_dict(data: dict[str, Any]) -> Any:
    """Convert dict to ClusteringRun."""
    from datetime import datetime

    created_at_str = data.get("created_at", "")
    if isinstance(created_at_str, str) and created_at_str:
        try:
            created_at = datetime.fromisoformat(created_at_str)
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)
        except (ValueError, TypeError):
            created_at = datetime.now(UTC)
    else:
        created_at = datetime.now(UTC)

    return ClusteringRun(
        run_id=data.get("run_id", ""),
        configuration=data.get("configuration", {}),
        input_failure_count=data.get("input_failure_count", 0),
        eligible_failure_count=data.get("eligible_failure_count", 0),
        family_count=data.get("family_count", 0),
        singleton_count=data.get("singleton_count", 0),
        average_family_size=data.get("average_family_size", 0.0),
        average_coherence=data.get("average_coherence", 0.0),
        created_at=created_at,
        clustering_version=data.get("clustering_version", "1.0"),
        metadata=data.get("metadata", {}),
    )


def explanation_to_dict(explanation: Any) -> dict[str, Any]:
    """Convert FamilyMembershipExplanation to dict."""
    return {
        "failure_id": explanation.failure_id,
        "family_id": explanation.family_id,
        "similarity": explanation.similarity,
        "matched_features": explanation.matched_features,
        "threshold": explanation.threshold,
    }


def explanation_from_dict(data: dict[str, Any]) -> Any:
    """Convert dict to FamilyMembershipExplanation."""
    return FamilyMembershipExplanation(
        failure_id=data.get("failure_id", ""),
        family_id=data.get("family_id", ""),
        similarity=data.get("similarity", 0.0),
        matched_features=data.get("matched_features", []),
        threshold=data.get("threshold", 0.0),
    )


def families_to_jsonl(families: list[Any]) -> str:
    """Convert a list of families to JSONL format."""
    lines = []
    for family in families:
        d = family_to_dict(family)
        lines.append(json.dumps(d, default=str))
    return "\n".join(lines)


def jsonl_to_families(jsonl_text: str) -> list[Any]:
    """Convert JSONL text to list of FailureFamilies."""
    families = []
    for line in jsonl_text.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            family = family_from_dict(data)
            families.append(family)
        except (json.JSONDecodeError, ValueError, KeyError):
            # Skip malformed lines
            continue
    return families


def runs_to_jsonl(runs: list[Any]) -> str:
    """Convert a list of clustering runs to JSONL."""
    lines = []
    for run in runs:
        d = run_to_dict(run)
        lines.append(json.dumps(d, default=str))
    return "\n".join(lines)


def jsonl_to_runs(jsonl_text: str) -> list[Any]:
    """Convert JSONL text to list of ClusteringRuns."""
    runs = []
    for line in jsonl_text.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            run = run_from_dict(data)
            runs.append(run)
        except (json.JSONDecodeError, ValueError, KeyError):
            continue
    return runs


def signature_to_dict(signature: Any) -> dict[str, Any]:
    """Convert FamilySignature to dict."""
    if hasattr(signature, "to_canonical_string"):
        return {
            "primary_invariant": signature.primary_invariant,
            "primary_reason_code": signature.primary_reason_code,
            "taxonomy": signature.taxonomy,
            "dominant_action": signature.dominant_action,
            "dominant_resource_type": signature.dominant_resource_type,
            "dominant_state_transition": signature.dominant_state_transition,
            "canonical_event_pattern": signature.canonical_event_pattern,
            "canonical_fingerprint": signature.canonical_fingerprint,
        }
    return {}


def coherence_to_dict(coherence: Any) -> dict[str, Any]:
    """Convert FamilyCoherence to dict."""
    return {
        "coherence_score": coherence.coherence_score,
        "average_pairwise_similarity": coherence.average_pairwise_similarity,
        "minimum_pairwise_similarity": coherence.minimum_pairwise_similarity,
        "maximum_pairwise_similarity": coherence.maximum_pairwise_similarity,
    }


def coherence_from_dict(data: dict[str, Any]) -> Any:
    """Convert dict to FamilyCoherence."""
    return FamilyCoherence(
        coherence_score=data.get("coherence_score", 0.0),
        average_pairwise_similarity=data.get("average_pairwise_similarity", 0.0),
        minimum_pairwise_similarity=data.get("minimum_pairwise_similarity", 0.0),
        maximum_pairwise_similarity=data.get("maximum_pairwise_similarity", 0.0),
    )


def run_result_to_dict(result: Any) -> dict[str, Any]:
    """Convert ClusteringRunResult to dict."""
    return {
        "run": run_to_dict(result.run),
        "families": [family_to_dict(f) for f in result.families],
        "validated_failures": [
            {"failure_id": vf.failure_id} for vf in result.validated_failures
        ],
        "excluded": [{"failure_id": vf.failure_id} for vf in result.excluded],
    }


def run_result_from_dict(data: dict[str, Any]) -> Any:
    """Convert dict to ClusteringRunResult."""
    return ClusteringRunResult(
        run=run_from_dict(data.get("run", {})),
        families=[family_from_dict(f) for f in data.get("families", [])],
        validated_failures=[],  # Would need full objects
        excluded=[],  # Would need full objects
    )
