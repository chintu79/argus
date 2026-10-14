"""Feature extraction for failure family clustering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent_eval.failure_families.models import (
    FailureFeatureExtractor,
    ValidatedFailureInput,
)


class FeatureExtractor:
    """Extracts structured features from validated failures for clustering."""

    def __init__(self):
        self.extractor = FailureFeatureExtractor()

    def extract_features(
        self, validated_failure: ValidatedFailureInput
    ) -> dict[str, Any]:
        """Extract structured features from a validated failure."""
        return self.extractor.extract(validated_failure)

    def extract_batch(
        self, validated_failures: list[ValidatedFailureInput]
    ) -> list[dict[str, Any]]:
        """Extract features for a batch of validated failures."""
        return [self.extract_features(vf) for vf in validated_failures]


@dataclass
class ExtractedFeatures:
    """Container for extracted features with metadata."""

    failure_id: str
    features: dict[str, Any]
    raw_evidence: dict[str, Any]

    def get_feature(self, key: str) -> Any:
        """Get a specific feature value."""
        return self.features.get(key)

    def has_feature(self, key: str) -> bool:
        """Check if a feature is present and non-null."""
        return key in self.features and self.features[key] is not None


class FeatureExtractorPipeline:
    """Pipeline for extracting features from multiple failures."""

    def __init__(self):
        self.extractor = FeatureExtractor()

    def process(
        self,
        validated_failures: list[Any],
    ) -> list[Any]:
        """Process a batch of validated failures into extracted features."""
        results = []
        for vf in validated_failures:
            features = self.extractor.extract_features(vf)
            results.append(
                ExtractedFeatures(
                    failure_id=vf.failure_id,
                    features=features,
                    raw_evidence={},
                )
            )
        return results


def extract_event_pattern(trajectory: Any) -> str | None:
    """Extract a compact event pattern from a trajectory."""
    if not hasattr(trajectory, "events"):
        return None

    events = trajectory.events
    pattern = []
    for event in events:
        if hasattr(event, "event_type"):
            etype = event.event_type
            if hasattr(etype, "name"):
                pattern.append(etype.name)
            else:
                pattern.append(str(etype))

    if not pattern:
        return None

    # Normalize common sequences
    pattern_str = "->".join(pattern)

    # Normalize common patterns
    pattern_str = pattern_str.replace(
        "TOOL_REQUEST->POLICY_DECISION->TOOL_RESPONSE", "TOOL_CALL"
    )
    pattern_str = pattern_str.replace("TOOL_REQUEST->TOOL_RESPONSE", "TOOL_CALL")

    return pattern_str


def extract_state_transitions(trajectory: Any) -> list[str]:
    """Extract state transitions from trajectory events."""
    transitions: list[str] = []
    if not hasattr(trajectory, "events"):
        return transitions

    for event in trajectory.events:
        if hasattr(event, "event_type"):
            etype = event.event_type
            if (
                hasattr(etype, "name")
                and etype.name == "STATE_TRANSITION"
                and hasattr(event, "payload")
                and isinstance(event.payload, dict)
            ):
                payload = event.payload
                if "changed_components" in payload:
                    components = payload.get("changed_components", [])
                    if isinstance(components, list) and components:
                        transitions.append(f"CHANGED({':'.join(components)})")

    return transitions


def normalize_tool_name(tool_name: str) -> str:
    """Normalize tool names to standard categories."""
    if not tool_name:
        return "UNKNOWN"

    tool = tool_name.lower()
    if "customer" in tool:
        return "CUSTOMER_LOOKUP"
    elif "account" in tool:
        return "ACCOUNT_LOOKUP"
    elif "transaction" in tool:
        return "TRANSACTION_LOOKUP"
    elif "ticket.search" in tool:
        return "TICKET_SEARCH"
    elif "ticket.update" in tool:
        return "TICKET_UPDATE"
    elif "notification" in tool:
        return "NOTIFICATION_SEND"
    elif "database" in tool:
        return "DATABASE_WRITE"
    return tool.upper()


def normalize_resource_type(resource_id: str) -> str:
    """Normalize resource IDs to standard types."""
    if not resource_id:
        return "UNKNOWN"

    rid = resource_id.upper()
    if "CUST" in rid:
        return "CUSTOMER"
    elif "ACC" in rid:
        return "ACCOUNT"
    elif "TXN" in rid:
        return "TRANSACTION"
    elif "TKT" in rid:
        return "TICKET"
    return rid


def extract_resource_scope(evidence: dict[str, Any]) -> str:
    """Extract resource scope from evidence."""
    if not isinstance(evidence, dict):
        return "protected"

    if "resource_scope" in evidence:
        return evidence["resource_scope"]

    # Infer from evidence
    if "resource_id" in evidence:
        rid = evidence.get("resource_id", "")
        if isinstance(rid, str) and ("CUST-002" in rid or "ACC-002" in rid):
            return "cross_customer"

    return "protected"
