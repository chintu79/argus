"""Failure taxonomy definitions and management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaxonomyNode:
    """Node in the failure taxonomy tree."""

    taxonomy_id: str
    label: str
    description: str = ""
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class FailureTaxonomy:
    """Hierarchical failure taxonomy for classification."""

    def __init__(self):
        self.nodes: dict[str, TaxonomyNode] = {}
        self._build_default_taxonomy()

    def _build_default_taxonomy(self):
        """Build the default MAST/AgentRx inspired taxonomy."""
        # Root
        self._add_node("ROOT", "FAILURE", "Root of failure taxonomy")

        # Level 1: Domains
        self._add_node(
            "SECURITY", "SECURITY_FAILURE", "Security-related failures", parent="ROOT"
        )
        self._add_node(
            "RELIABILITY",
            "RELIABILITY_FAILURE",
            "Reliability-related failures",
            parent="ROOT",
        )
        self._add_node(
            "ROBUSTNESS",
            "ROBUSTNESS_FAILURE",
            "Robustness-related failures",
            parent="ROOT",
        )
        self._add_node(
            "POLICY", "POLICY_FAILURE", "Policy-related failures", parent="ROOT"
        )
        self._add_node(
            "EVALUATOR", "EVALUATOR_FAILURE", "Evaluator failures", parent="ROOT"
        )
        self._add_node(
            "ENVIRONMENT", "ENVIRONMENT_FAILURE", "Environment failures", parent="ROOT"
        )
        self._add_node(
            "INFRASTRUCTURE",
            "INFRASTRUCTURE_FAILURE",
            "Infrastructure failures",
            parent="ROOT",
        )
        self._add_node(
            "SCENARIO", "SCENARIO_FAILURE", "Scenario failures", parent="ROOT"
        )

        # Level 2: Security subcategories
        self._add_node(
            "AUTHORIZATION",
            "AUTHORIZATION_FAILURE",
            "Authorization failures",
            parent="SECURITY",
        )
        self._add_node(
            "DATA_EXPOSURE",
            "DATA_EXPOSURE_FAILURE",
            "Data exposure failures",
            parent="SECURITY",
        )
        self._add_node(
            "STATE_INTEGRITY",
            "STATE_INTEGRITY_FAILURE",
            "State integrity failures",
            parent="SECURITY",
        )
        self._add_node(
            "RESOURCE", "RESOURCE_FAILURE", "Resource failures", parent="SECURITY"
        )
        self._add_node(
            "POLICY_ENFORCEMENT",
            "POLICY_ENFORCEMENT_FAILURE",
            "Policy enforcement failures",
            parent="SECURITY",
        )

        # Level 3: Authorization subcategories
        self._add_node(
            "UNAUTHORIZED_ACCESS",
            "UNAUTHORIZED_ACCESS",
            "Unauthorized access",
            parent="AUTHORIZATION",
        )
        self._add_node(
            "POLICY_BYPASS", "POLICY_BYPASS", "Policy bypass", parent="AUTHORIZATION"
        )
        self._add_node(
            "IDENTITY_MISMATCH",
            "IDENTITY_MISMATCH",
            "Identity mismatch",
            parent="AUTHORIZATION",
        )
        self._add_node(
            "CAPABILITY_VIOLATION",
            "CAPABILITY_VIOLATION",
            "Capability violation",
            parent="AUTHORIZATION",
        )

        # Level 3: Policy enforcement
        self._add_node(
            "POLICY_CONTRADICTION",
            "POLICY_CONTRADICTION",
            "Policy contradiction",
            parent="POLICY_ENFORCEMENT",
        )

        # Level 3: Data exposure
        self._add_node(
            "SENSITIVE_DATA_EXPOSURE",
            "SENSITIVE_DATA_EXPOSURE",
            "Sensitive data exposure",
            parent="DATA_EXPOSURE",
        )

        # Level 3: State integrity
        self._add_node(
            "STATE_MUTATION",
            "STATE_MUTATION",
            "Unauthorized state mutation",
            parent="STATE_INTEGRITY",
        )

        # Level 3: Resource
        self._add_node(
            "RESOURCE_BOUNDARY",
            "RESOURCE_BOUNDARY",
            "Resource boundary violation",
            parent="RESOURCE",
        )
        self._add_node(
            "RESOURCE_EXHAUSTION",
            "RESOURCE_EXHAUSTION",
            "Resource exhaustion",
            parent="RESOURCE",
        )

        # Level 2: Reliability subcategories
        self._add_node(
            "PROCESS_ORDER",
            "PROCESS_ORDER_FAILURE",
            "Process order failure",
            parent="RELIABILITY",
        )
        self._add_node(
            "RECOVERY", "RECOVERY_FAILURE", "Recovery failure", parent="RELIABILITY"
        )
        self._add_node(
            "FAULT_TOLERANCE",
            "FAULT_TOLERANCE_FAILURE",
            "Fault tolerance failure",
            parent="RELIABILITY",
        )

        # Level 2: Robustness
        self._add_node(
            "TOOL_ROBUSTNESS",
            "TOOL_ROBUSTNESS_FAILURE",
            "Tool robustness failure",
            parent="ROBUSTNESS",
        )
        self._add_node(
            "PROMPT_INJECTION",
            "PROMPT_INJECTION",
            "Prompt injection",
            parent="ROBUSTNESS",
        )

        # Build reverse mapping
        self._build_reverse_mapping()

    def _add_node(
        self,
        taxonomy_id: str,
        label: str,
        description: str = "",
        parent: str | None = None,
    ):
        """Add a node to the taxonomy."""
        if taxonomy_id in self.nodes:
            return

        node = TaxonomyNode(
            taxonomy_id=taxonomy_id,
            label=label,
            description=description,
            parent=parent,
        )
        self.nodes[taxonomy_id] = node

        if parent and parent in self.nodes:
            self.nodes[parent].children.append(taxonomy_id)

    def _build_reverse_mapping(self):
        """Build reverse mapping from labels to taxonomy IDs."""
        self._label_to_id = {}
        for tid, node in self.nodes.items():
            self._label_to_id[node.label] = tid
            # Also map by taxonomy_id
            self._label_to_id[tid] = tid

    def get_node(self, taxonomy_id: str) -> TaxonomyNode | None:
        """Get a taxonomy node by ID."""
        return self.nodes.get(taxonomy_id)

    def get_by_label(self, label: str) -> TaxonomyNode | None:
        """Get a taxonomy node by label."""
        tid = self._label_to_id.get(label)
        if tid:
            return self.nodes.get(tid)
        return None

    def get_path(self, taxonomy_id: str) -> list[str]:
        """Get the path from root to a taxonomy node."""
        path = []
        node = self.nodes.get(taxonomy_id)
        while node:
            path.append(node.taxonomy_id)
            if node.parent:
                node = self.nodes.get(node.parent)
            else:
                break
        return list(reversed(path))

    def get_label_path(self, taxonomy_id: str) -> list[str]:
        """Get the path of labels from root to a taxonomy node."""
        path = []
        node = self.nodes.get(taxonomy_id)
        while node:
            path.append(node.label)
            if node.parent:
                node = self.nodes.get(node.parent)
            else:
                break
        return list(reversed(path))

    def get_children(self, taxonomy_id: str) -> list[TaxonomyNode]:
        """Get direct children of a taxonomy node."""
        node = self.nodes.get(taxonomy_id)
        if not node:
            return []
        return [self.nodes[child] for child in node.children if child in self.nodes]

    def get_ancestors(self, taxonomy_id: str) -> list[TaxonomyNode]:
        """Get all ancestors of a taxonomy node."""
        ancestors = []
        node = self.nodes.get(taxonomy_id)
        while node and node.parent:
            parent = self.nodes.get(node.parent)
            if parent:
                ancestors.append(parent)
                node = parent
            else:
                break
        return ancestors

    def get_descendants(self, taxonomy_id: str) -> list[TaxonomyNode]:
        """Get all descendants of a taxonomy node."""
        descendants = []
        node = self.nodes.get(taxonomy_id)
        if not node:
            return []

        for child_id in node.children:
            child = self.nodes.get(child_id)
            if child:
                descendants.append(child)
                descendants.extend(self.get_descendants(child_id))
        return descendants

    def find_lca(self, tax_id_a: str, tax_id_b: str) -> str | None:
        """Find lowest common ancestor of two taxonomy nodes."""
        path_a = set(self.get_path(tax_id_a))
        path_b = self.get_path(tax_id_b)

        for tid in path_b:
            if tid in path_a:
                return tid
        return None

    def hierarchical_similarity(self, tax_id_a: str, tax_id_b: str) -> float:
        """Compute hierarchical similarity between two taxonomy nodes."""
        lca = self.find_lca(tax_id_a, tax_id_b)
        if not lca:
            return 0.0

        path_a = self.get_path(tax_id_a)
        path_b = self.get_path(tax_id_b)

        lca_depth = path_a.index(lca) + 1
        max_depth = max(len(path_a), len(path_b))

        if max_depth == 0:
            return 0.0

        return lca_depth / max_depth

    def assign_taxonomy(self, failure_data: dict[str, Any]) -> str:
        """Assign taxonomy label based on failure data."""
        # Map reason codes to taxonomy
        reason_code = failure_data.get("reason_code", "")

        reason_to_taxonomy = {
            "UNAUTHORIZED_SENSITIVE_ACTION": "UNAUTHORIZED_ACCESS",
            "DENIED_ACTION_MUTATED_STATE": "POLICY_BYPASS",
            "IDENTITY_MISMATCH": "IDENTITY_MISMATCH",
            "MISSING_REQUIRED_CAPABILITY": "CAPABILITY_VIOLATION",
            "POLICY_EXECUTION_CONTRADICTION": "POLICY_CONTRADICTION",
            "RESOURCE_BOUNDARY_VIOLATION": "RESOURCE_BOUNDARY",
            "SENSITIVE_DATA_EXPOSURE": "SENSITIVE_DATA_EXPOSURE",
            "PROCESS_ORDER_VIOLATION": "PROCESS_ORDER",
        }

        if reason_code in reason_to_taxonomy:
            return reason_to_taxonomy[reason_code]

        # Fallback to invariant-based
        invariant_id = failure_data.get("invariant_id", "")
        invariant_to_taxonomy = {
            "I1": "UNAUTHORIZED_ACCESS",
            "I2": "POLICY_BYPASS",
            "I3": "IDENTITY_MISMATCH",
            "I4": "CAPABILITY_VIOLATION",
            "I5": "POLICY_CONTRADICTION",
            "I6": "RESOURCE_BOUNDARY",
            "I7": "SENSITIVE_DATA_EXPOSURE",
            "I8": "PROCESS_ORDER",
        }

        if invariant_id in invariant_to_taxonomy:
            return invariant_to_taxonomy[invariant_id]

        return "UNCLASSIFIED"

    def get_all_labels(self) -> list[str]:
        """Get all taxonomy labels."""
        return [node.label for node in self.nodes.values()]

    def get_all_ids(self) -> list[str]:
        """Get all taxonomy IDs."""
        return list(self.nodes.keys())


# Global taxonomy instance
_DEFAULT_TAXONOMY: FailureTaxonomy | None = None


def get_default_taxonomy() -> FailureTaxonomy:
    """Get the default taxonomy instance (singleton)."""
    global _DEFAULT_TAXONOMY
    if _DEFAULT_TAXONOMY is None:
        _DEFAULT_TAXONOMY = FailureTaxonomy()
    return _DEFAULT_TAXONOMY


def assign_taxonomy_label(failure_data: dict[str, Any]) -> str:
    """Assign a taxonomy label to failure data."""
    taxonomy = get_default_taxonomy()
    return taxonomy.assign_taxonomy(failure_data)


def get_taxonomy_path(taxonomy_id: str) -> list[str]:
    """Get the path from root to a taxonomy node."""
    taxonomy = get_default_taxonomy()
    return taxonomy.get_path(taxonomy_id)


def hierarchical_similarity(tax_a: str, tax_b: str) -> float:
    """Compute hierarchical similarity between two taxonomy labels."""
    taxonomy = get_default_taxonomy()
    return taxonomy.hierarchical_similarity(tax_a, tax_b)
