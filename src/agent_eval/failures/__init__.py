"""Failure detection and failure candidate generation for Budget-Constrained Adaptive Security Evaluation."""

from __future__ import annotations

from .detector import FailureDetector
from .evidence import EvidenceIntegrityError, EvidenceValidator
from .models import (
    FailureCandidate,
    FailureCandidateStatus,
    FailureDetectionContext,
    FailureReasonCode,
)
from .registry import FailureCandidateRegistry, get_failure_candidate_registry
from .rules import (
    applies_invariant,
    detect_from_invariant_result,
    rule_i1,
    rule_i2,
    rule_i3,
    rule_i4,
    rule_i5,
    rule_i6,
    rule_i7,
    rule_i8,
)
from .serialization import (
    candidate_fingerprint,
    candidate_from_dict,
    candidate_to_dict,
    candidates_to_jsonl,
    jsonl_to_candidates,
)
from .validation import (
    validate_candidate_creation,
    validate_failure_candidate,
)

__all__ = [
    "EvidenceIntegrityError",
    "EvidenceValidator",
    "FailureCandidate",
    "FailureCandidateRegistry",
    "FailureCandidateStatus",
    "FailureDetectionContext",
    "FailureDetector",
    "FailureReasonCode",
    "applies_invariant",
    "candidate_fingerprint",
    "candidate_from_dict",
    "candidate_to_dict",
    "candidates_to_jsonl",
    "detect_from_invariant_result",
    "detect_i1",
    "detect_i2",
    "detect_i3",
    "detect_i4",
    "detect_i5",
    "detect_i6",
    "detect_i7",
    "detect_i8",
    "get_failure_candidate_registry",
    "jsonl_to_candidates",
    "rule_i1",
    "rule_i2",
    "rule_i3",
    "rule_i4",
    "rule_i5",
    "rule_i6",
    "rule_i7",
    "rule_i8",
    "validate_candidate_creation",
    "validate_failure_candidate",
]
