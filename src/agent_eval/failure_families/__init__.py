"""Failure family classification and clustering for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

from agent_eval.failure_families.clustering import (
    AgglomerativeClusterer,
    ClusteringConfig,
    build_family_signature,
    create_clustering_run,
)
from agent_eval.failure_families.features import (
    ExtractedFeatures,
    FeatureExtractor,
    FeatureExtractorPipeline,
    extract_event_pattern,
    extract_resource_scope,
    extract_state_transitions,
    normalize_resource_type,
    normalize_tool_name,
)
from agent_eval.failure_families.models import (
    REASON_CODE_TO_TAXONOMY,
    ClusteringEligibilityPolicy,
    ClusteringRun,
    ClusteringRunResult,
    FailureFamily,
    FailureFeatureExtractor,
    FailureFeatures,
    FailureSimilarity,
    FamilyCoherence,
    FamilySignature,
    SimilarityWeights,
    ValidatedFailure,
    ValidatedFailureInput,
)
from agent_eval.failure_families.registry import (
    ClusteringRunRegistry,
    FailureFamilyRegistry,
    create_failure_family,
    get_clustering_run_registry,
    get_failure_family_registry,
)
from agent_eval.failure_families.repository import (
    FailureFamilyRepository,
    FailureFamilyRepositoryImpl,
    get_failure_family_repository,
)
from agent_eval.failure_families.serialization import (
    coherence_from_dict,
    coherence_to_dict,
    explanation_from_dict,
    explanation_to_dict,
    families_to_jsonl,
    family_from_dict,
    family_to_dict,
    jsonl_to_families,
    jsonl_to_runs,
    run_from_dict,
    run_result_from_dict,
    run_result_to_dict,
    run_to_dict,
    runs_to_jsonl,
    signature_to_dict,
)
from agent_eval.failure_families.similarity import (
    FeatureComparison,
    FeatureSimilarityMatrix,
    SimilarityCalculator,
    calculate_feature_similarity,
    compare_feature_sets,
)
from agent_eval.failure_families.taxonomy import (
    FailureTaxonomy,
    TaxonomyNode,
    assign_taxonomy_label,
    get_default_taxonomy,
    get_taxonomy_path,
    hierarchical_similarity,
)
from agent_eval.failure_families.validator import (
    FamilyMembershipExplanation,
    FamilyValidator,
    FamilyValidatorImpl,
    validate_clustering_output,
)

__all__ = [
    "REASON_CODE_TO_TAXONOMY",
    # Clustering
    "AgglomerativeClusterer",
    "ClusteringConfig",
    "ClusteringEligibilityPolicy",
    "ClusteringRun",
    "ClusteringRunRegistry",
    "ClusteringRunResult",
    "ExtractedFeatures",
    "FailureFamily",
    # Registry
    "FailureFamilyRegistry",
    # Repository
    "FailureFamilyRepository",
    "FailureFamilyRepositoryImpl",
    "FailureFeatureExtractor",
    "FailureFeatures",
    "FailureSimilarity",
    "FailureTaxonomy",
    "FamilyCoherence",
    "FamilyMembershipExplanation",
    "FamilySignature",
    "FamilyValidator",
    # Validator
    "FamilyValidatorImpl",
    "FeatureComparison",
    # Features
    "FeatureExtractor",
    "FeatureExtractorPipeline",
    "FeatureSimilarityMatrix",
    # Similarity
    "SimilarityCalculator",
    "SimilarityWeights",
    # Taxonomy
    "TaxonomyNode",
    # Models
    "ValidatedFailure",
    "ValidatedFailureInput",
    "assign_taxonomy_label",
    "build_family_signature",
    "calculate_feature_similarity",
    "coherence_from_dict",
    "coherence_to_dict",
    "compare_feature_sets",
    "create_clustering_run",
    "create_failure_family",
    "explanation_from_dict",
    "explanation_to_dict",
    "extract_event_pattern",
    "extract_resource_scope",
    "extract_state_transitions",
    "families_to_jsonl",
    "family_from_dict",
    # Serialization
    "family_to_dict",
    "get_clustering_run_registry",
    "get_default_taxonomy",
    "get_failure_family_registry",
    "get_failure_family_repository",
    "get_taxonomy_path",
    "hierarchical_similarity",
    "jsonl_to_families",
    "jsonl_to_runs",
    "normalize_resource_type",
    "normalize_tool_name",
    "run_from_dict",
    "run_result_from_dict",
    "run_result_to_dict",
    "run_to_dict",
    "runs_to_jsonl",
    "signature_to_dict",
    "validate_clustering_output",
]
