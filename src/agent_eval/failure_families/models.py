"""Failure family and clustering domain models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, validator

from agent_eval.domain.identifiers import make_id
from agent_eval.failures.models import FailureCandidate
from agent_eval.reproducibility.models import ReproducibilityStatus


class ClusteringEligibilityStatus(str, Enum):
    """Eligibility status for clustering."""

    ELIGIBLE = "ELIGIBLE"
    EXCLUDED = "EXCLUDED"


class ValidatedFailure(BaseModel):
    """A failure candidate that has been validated through reproducibility testing."""

    failure_id: str = Field(..., description="Unique validated failure identifier")
    candidate: FailureCandidate = Field(..., description="Original failure candidate")
    reproducibility_result: Any = Field(
        ..., description="Reproducibility verification result"
    )
    rep_k: float = Field(..., description="Reproducibility rate")
    eligible: bool = Field(default=False, description="Whether eligible for clustering")
    eligibility_reason: str | None = Field(
        None, description="Reason for eligibility decision"
    )

    @validator("failure_id")
    def failure_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("failure_id must not be empty")
        return v


class FailureFamily(BaseModel):
    """A cluster of similar validated failures representing a failure family."""

    family_id: str = Field(..., description="Stable family identifier")
    member_failure_ids: list[str] = Field(
        default_factory=list, description="Member failure IDs"
    )
    representative_failure_id: str = Field(..., description="Representative failure ID")
    family_signature: str = Field(..., description="Canonical family signature")
    family_size: int = Field(default=0, description="Number of members")
    taxonomy_labels: list[str] = Field(
        default_factory=list, description="Assigned taxonomy labels"
    )
    coherence_score: float = Field(
        default=0.0, description="Average pairwise similarity"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    clustering_version: str = Field(
        default="1.0", description="Clustering configuration version"
    )
    severity_distribution: dict[str, int] = Field(default_factory=dict)
    invariant_distribution: dict[str, int] = Field(default_factory=dict)
    reason_code_distribution: dict[str, int] = Field(default_factory=dict)
    environment_distribution: dict[str, int] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @validator("family_id")
    def family_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("family_id must not be empty")
        return v

    @validator("representative_failure_id")
    def representative_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("representative_failure_id must not be empty")
        return v


class FailureFeatures(BaseModel):
    """Structured feature representation of a failure for clustering."""

    invariant_id: str | None = None
    reason_code: str | None = None
    action: str | None = None
    tool: str | None = None
    tool_category: str | None = None
    resource_type: str | None = None
    resource_scope: str | None = None
    authorization_decision: str | None = None
    state_transition: str | None = None
    process_stage: str | None = None
    severity: str | None = None
    event_pattern: str | None = None
    policy_violation_type: str | None = None
    taxonomy_label: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in self.dict().items() if v is not None}


class SimilarityWeights(BaseModel):
    """Configurable similarity weights for clustering."""

    invariant_id: float = 0.20
    reason_code: float = 0.25
    action: float = 0.10
    resource_type: float = 0.10
    state_transition: float = 0.15
    event_pattern: float = 0.10
    taxonomy: float = 0.10

    @validator("*")
    def weights_non_negative(cls, v):
        if v < 0:
            raise ValueError("Weights must be non-negative")
        return v

    def normalize(self) -> SimilarityWeights:
        """Return normalized weights that sum to 1.0."""
        total = sum(self.dict().values())
        if total == 0:
            return SimilarityWeights()
        return SimilarityWeights(**{k: v / total for k, v in self.dict().items()})


class ClusteringEligibilityPolicy(BaseModel):
    """Policy for determining which failures are eligible for clustering."""

    include_reproducible: bool = True
    include_partial: bool = False
    include_not_reproducible: bool = False
    include_inconclusive: bool = False
    include_error: bool = False
    minimum_rep_k: float = 0.75

    def is_eligible(self, validated_failure: ValidatedFailure) -> bool:
        """Check if a validated failure meets eligibility criteria."""
        status = validated_failure.reproducibility_result.status
        if status == ReproducibilityStatus.REPRODUCIBLE:
            return self.include_reproducible
        elif status == ReproducibilityStatus.PARTIAL:
            return self.include_partial
        elif status == ReproducibilityStatus.NOT_REPRODUCIBLE:
            return self.include_not_reproducible
        elif status == ReproducibilityStatus.INCONCLUSIVE:
            return self.include_inconclusive
        elif status == ReproducibilityStatus.ERROR:
            return self.include_error
        return False


class ClusteringConfig(BaseModel):
    """Configuration for failure family clustering."""

    algorithm: str = "agglomerative"
    distance_threshold: float = 0.25
    linkage: str = "average"
    minimum_family_size: int = 1
    similarity_weights: SimilarityWeights = Field(default_factory=SimilarityWeights)
    eligibility_policy: ClusteringEligibilityPolicy = Field(
        default_factory=ClusteringEligibilityPolicy
    )
    clustering_version: str = "1.0"
    early_stopping: bool = False

    @validator("distance_threshold")
    def threshold_valid(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("distance_threshold must be between 0 and 1")
        return v

    @validator("linkage")
    def linkage_valid(cls, v):
        if v not in {"ward", "complete", "average", "single"}:
            raise ValueError("linkage must be one of: ward, complete, average, single")
        return v

    @validator("minimum_family_size")
    def min_size_valid(cls, v):
        if v < 1:
            raise ValueError("minimum_family_size must be >= 1")
        return v


class ValidatedFailureInput(BaseModel):
    """Input for the clustering pipeline combining candidate and reproducibility."""

    failure_id: str
    candidate: FailureCandidate
    reproducibility_result: Any
    rep_k: float
    eligible: bool = False
    eligibility_reason: str | None = None


REASON_CODE_TO_TAXONOMY: dict[str, str] = {
    "UNAUTHORIZED_SENSITIVE_ACTION": "SECURITY/AUTHORIZATION_FAILURE",
    "DENIED_ACTION_MUTATED_STATE": "SECURITY/AUTHORIZATION_FAILURE/POLICY_BYPASS",
    "IDENTITY_MISMATCH": "SECURITY/AUTHORIZATION_FAILURE/IDENTITY_MISMATCH",
    "MISSING_REQUIRED_CAPABILITY": "SECURITY/AUTHORIZATION_FAILURE/CAPABILITY_VIOLATION",
    "POLICY_EXECUTION_CONTRADICTION": "SECURITY/POLICY_ENFORCEMENT_FAILURE",
    "RESOURCE_BOUNDARY_VIOLATION": "SECURITY/RESOURCE_BOUNDARY_FAILURE",
    "SENSITIVE_DATA_EXPOSURE": "SECURITY/DATA_EXPOSURE_FAILURE",
    "PROCESS_ORDER_VIOLATION": "RELIABILITY/PROCESS_ORDER_FAILURE",
}


class FailureFeatureExtractor(BaseModel):
    """Extracts structured features from validated failures."""

    def extract(self, validated_failure: ValidatedFailureInput) -> dict[str, Any]:
        """Extract structured features from a validated failure."""
        candidate = validated_failure.candidate

        features = {
            "invariant_id": candidate.invariant_id,
            "reason_code": candidate.reason_code.value
            if hasattr(candidate.reason_code, "value")
            else candidate.reason_code,
            "action": self._extract_action(candidate),
            "tool": self._extract_tool(candidate),
            "tool_category": self._extract_tool_category(candidate),
            "resource_type": self._extract_resource_type(candidate),
            "resource_scope": self._extract_resource_scope(candidate),
            "authorization_decision": self._extract_authorization_decision(candidate),
            "state_transition": self._extract_state_transition(candidate),
            "process_stage": self._extract_process_stage(candidate),
            "severity": candidate.severity.value
            if hasattr(candidate.severity, "value")
            else str(candidate.severity),
            "event_pattern": self._extract_event_pattern(candidate),
            "policy_violation_type": self._extract_policy_violation_type(candidate),
            "taxonomy_label": self._assign_taxonomy_label(candidate),
        }
        return features

    def _extract_action(self, candidate: FailureCandidate) -> str | None:
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict):
            return evidence.get("action") or evidence.get("tool_name")
        return None

    def _extract_tool(self, candidate: FailureCandidate) -> str | None:
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict):
            return evidence.get("tool_name")
        return None

    def _extract_tool_category(self, candidate: FailureCandidate) -> str | None:
        tool = self._extract_tool(candidate)
        if not tool:
            return None
        if "customer" in tool or "account" in tool or "transaction" in tool:
            return "data_query"
        elif "ticket" in tool:
            return "ticket_management"
        elif "notification" in tool:
            return "notification"
        elif "database" in tool:
            return "database_write"
        return "unknown"

    def _extract_resource_type(self, candidate: FailureCandidate) -> str | None:
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict):
            if "resource_type" in evidence:
                return evidence["resource_type"]
            if "resource_id" in evidence:
                rid = evidence["resource_id"]
                if isinstance(rid, str):
                    if "CUST" in rid:
                        return "customer"
                    elif "ACC" in rid:
                        return "account"
                    elif "TXN" in rid:
                        return "transaction"
                    elif "TKT" in rid:
                        return "ticket"
        return None

    def _extract_resource_scope(self, candidate: FailureCandidate) -> str | None:
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict):
            return evidence.get("resource_scope")
        return "protected"  # Default for security failures

    def _extract_authorization_decision(
        self, candidate: FailureCandidate
    ) -> str | None:
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict):
            if "authorization_result" in evidence:
                return evidence["authorization_result"]
            if "policy_decision" in evidence and isinstance(
                evidence["policy_decision"], dict
            ):
                return evidence["policy_decision"].get("decision")
        return None

    def _extract_state_transition(self, candidate: FailureCandidate) -> str | None:
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict):
            return evidence.get("state_transition")
        return None

    def _extract_process_stage(self, candidate: FailureCandidate) -> str | None:
        reason_code = candidate.reason_code
        if hasattr(reason_code, "value"):
            rc = reason_code.value
        else:
            rc = str(reason_code)

        if "UNAUTHORIZED" in rc or "SENSITIVE_ACTION" in rc:
            return "authorization"
        elif "DENIED_ACTION" in rc or "MUTATED_STATE" in rc:
            return "mutation"
        elif "IDENTITY_MISMATCH" in rc:
            return "identity"
        elif "MISSING_CAPABILITY" in rc:
            return "capability"
        elif "POLICY_EXECUTION" in rc:
            return "policy_enforcement"
        elif "RESOURCE_BOUNDARY" in rc:
            return "resource_access"
        elif "SENSITIVE_DATA" in rc or "EXPOSURE" in rc:
            return "data_exposure"
        elif "PROCESS_ORDER" in rc:
            return "process_order"
        return "unknown"

    def _extract_event_pattern(self, candidate: FailureCandidate) -> str | None:
        # Extract event sequence pattern from evidence
        evidence = candidate.evidence or {}
        if isinstance(evidence, dict) and "event_ids" in evidence:
            return f"EVT_PATTERN_{candidate.invariant_id}"
        return None

    def _extract_policy_violation_type(
        self, candidate: FailureCandidate
    ) -> str | None:
        reason_code = candidate.reason_code
        if hasattr(reason_code, "value"):
            rc = reason_code.value
        else:
            rc = str(reason_code)

        if "UNAUTHORIZED" in rc:
            return "unauthorized_access"
        elif "DENIED_ACTION" in rc:
            return "denied_mutation"
        elif "IDENTITY" in rc:
            return "identity_mismatch"
        elif "CAPABILITY" in rc:
            return "capability_violation"
        elif "POLICY" in rc:
            return "policy_contradiction"
        elif "RESOURCE" in rc:
            return "resource_boundary"
        elif "SENSITIVE" in rc or "EXPOSURE" in rc:
            return "data_exposure"
        elif "PROCESS" in rc:
            return "process_violation"
        return "unknown"

    def _assign_taxonomy_label(self, candidate: FailureCandidate) -> str | None:
        """Assign taxonomy label based on reason code."""
        reason_code = candidate.reason_code
        rc = reason_code.value if hasattr(reason_code, "value") else str(reason_code)
        return REASON_CODE_TO_TAXONOMY.get(rc, "UNCLASSIFIED")


class FailureTaxonomy(BaseModel):
    """Hierarchical failure taxonomy."""

    taxonomy_id: str
    label: str
    description: str | None = None
    parent: str | None = None
    children: list[str] = Field(default_factory=list)


class FailureSimilarity(BaseModel):
    """Result of similarity comparison between two failures."""

    similarity: float = 0.0
    matched_features: list[str] = Field(default_factory=list)
    feature_similarities: dict[str, float] = Field(default_factory=dict)


class FamilySignature(BaseModel):
    """Canonical signature for a failure family."""

    primary_invariant: str | None = None
    primary_reason_code: str | None = None
    taxonomy: str | None = None
    dominant_action: str | None = None
    dominant_resource_type: str | None = None
    dominant_state_transition: str | None = None
    canonical_event_pattern: str | None = None
    canonical_fingerprint: str = ""

    def to_canonical_string(self) -> str:
        parts = []
        if self.primary_invariant:
            parts.append(f"inv:{self.primary_invariant}")
        if self.primary_reason_code:
            parts.append(f"rc:{self.primary_reason_code}")
        if self.dominant_action:
            parts.append(f"act:{self.dominant_action}")
        if self.dominant_resource_type:
            parts.append(f"rtype:{self.dominant_resource_type}")
        if self.dominant_state_transition:
            parts.append(f"trans:{self.dominant_state_transition}")
        return "|".join(parts)


class FamilyCoherence(BaseModel):
    """Family coherence metrics."""

    coherence_score: float = 0.0
    average_pairwise_similarity: float = 0.0
    minimum_pairwise_similarity: float = 0.0
    maximum_pairwise_similarity: float = 0.0


class FamilyValidator:
    """Validates failure family integrity."""

    @classmethod
    def validate(cls, family: Any, all_families: list[Any]) -> tuple[bool, list[str]]:
        errors = []

        # Check family size
        if len(family.member_failure_ids) == 0:
            errors.append(f"Family {family.family_id} has no members")

        # Check coherence
        if family.coherence_score < 0 or family.coherence_score > 1:
            errors.append(
                f"Family {family.family_id} has invalid coherence score: {family.coherence_score}"
            )

        # Check duplicate membership across families
        all_members = []
        for f in all_families:
            all_members.extend(f.member_failure_ids)

        seen = set()
        duplicates = set()
        for m in all_members:
            if m in seen:
                duplicates.add(m)
            seen.add(m)

        if duplicates:
            errors.append(f"Duplicate membership found: {duplicates}")

        return len(errors) == 0, errors


class FamilyMembershipExplanation(BaseModel):
    """Explanation for why a failure was assigned to a family."""

    failure_id: str
    family_id: str
    similarity: float
    matched_features: list[str] = Field(default_factory=list)
    threshold: float


class ClusteringRun(BaseModel):
    """Record of a clustering execution."""

    run_id: str = Field(default_factory=lambda: make_id("clust"))
    configuration: dict[str, Any] = Field(default_factory=dict)
    input_failure_count: int = 0
    eligible_failure_count: int = 0
    family_count: int = 0
    singleton_count: int = 0
    average_family_size: float = 0.0
    average_coherence: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    clustering_version: str = "1.0"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClusteringRunResult(BaseModel):
    """Result of a clustering execution."""

    run: ClusteringRun
    families: list[Any] = Field(default_factory=list)
    validated_failures: list[ValidatedFailureInput] = Field(default_factory=list)
    excluded: list[ValidatedFailureInput] = Field(default_factory=list)


# Import Enum at top
from enum import Enum
