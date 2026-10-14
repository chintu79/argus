"""Evidence mapper for Phase 16 research report.

Maps every quantitative claim in the report to an evidence record containing:
- evidence_id, claim_id, claim_type
- source_artifact, source_hash, source_metric
- experiment_id, analysis_id, population, denominator
- units, value, uncertainty, generation_method

Claim types:
  MEASURED
  STATISTICALLY_TESTED
  DESCRIPTIVE_INTERPRETATION
  LITERATURE_SUPPORTED
  IMPLEMENTATION_VERIFIED
  PROPOSED
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, validator


class EvidenceRecord(BaseModel):
    """Evidence record linking a claim to its source."""

    evidence_id: str = Field(..., description="Unique evidence identifier")
    claim_id: str = Field(..., description="Identifier of the claim in the report")
    claim_type: str = Field(
        ..., description="MEASURED/STATISTICALLY_TESTED/DESCRIPTIVE_INTERPRETATION/"
        "LITERATURE_SUPPORTED/IMPLEMENTATION_VERIFIED/PROPOSED"
    )
    source_artifact: str = Field(
        ..., description="Path to the source artifact"
    )
    source_hash: str = Field(
        ..., description="SHA256 hash of the source artifact"
    )
    source_metric: str = Field(..., description="Metric name from the source")
    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis identifier")
    population: int | None = Field(
        default=None, description="Population size"
    )
    denominator: int | None = Field(
        default=None, description="Denominator for ratios/rates"
    )
    units: str = Field(..., description="Units of measurement")
    value: Any = Field(..., description="The measured or computed value")
    uncertainty: dict[str, Any] | None = Field(
        default=None, description="Uncertainty representation (CI, etc.)"
    )
    generation_method: str = Field(
        ..., description="How the value was generated"
    )
    generated_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO timestamp when evidence was recorded"
    )

    @validator("claim_type")
    def _validate_claim_type(cls, v):
        allowed = {
            "MEASURED",
            "STATISTICALLY_TESTED",
            "DESCRIPTIVE_INTERPRETATION",
            "LITERATURE_SUPPORTED",
            "IMPLEMENTATION_VERIFIED",
            "PROPOSED",
        }
        if v not in allowed:
            raise ValueError(
                f"Invalid claim_type '{v}'. Must be one of {allowed}"
            )
        return v


class EvidenceMapper:
    """Maps claims to their source artifacts and metrics."""

    def __init__(self, experiment_id: str, analysis_id: str):
        self.experiment_id = experiment_id
        self.analysis_id = analysis_id
        self.evidence_records: dict[str, EvidenceRecord] = {}
        self.claim_counter = 0

    def add_evidence(
        self,
        claim_type: str,
        source_artifact: str,
        source_metric: str,
        value: Any,
        units: str,
        population: int | None = None,
        denominator: int | None = None,
        uncertainty: dict[str, Any] | None = None,
        generation_method: str = "computed_from_artifacts",
    ) -> EvidenceRecord:
        """Add an evidence record and return it."""
        self.claim_counter += 1
        evidence_id = f"E{self.claim_counter:04d}"

        # Compute hash of source artifact
        source_hash = ""
        if os.path.exists(source_artifact):
            source_hash = self._compute_sha256(source_artifact)

        record = EvidenceRecord(
            evidence_id=evidence_id,
            claim_id=f"C{self.claim_counter:04d}",
            claim_type=claim_type,
            source_artifact=source_artifact,
            source_hash=source_hash,
            source_metric=source_metric,
            experiment_id=self.experiment_id,
            analysis_id=self.analysis_id,
            population=population,
            denominator=denominator,
            units=units,
            value=value,
            uncertainty=uncertainty,
            generation_method=generation_method,
        )

        self.evidence_records[evidence_id] = record
        return record

    def _compute_sha256(self, filepath: str) -> str:
        """Compute SHA256 hash of a file."""
        h = __import__("hashlib").sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def get_evidence(self, claim_id: str) -> EvidenceRecord | None:
        """Get evidence record by claim ID."""
        # claim_id format: C0001, C0002, etc.
        prefix = "C"
        if claim_id.startswith(prefix):
            num = int(claim_id[len(prefix):])
            # Evidence IDs are 1-based, so adjust
            target_evidence_id = f"E{num:04d}"
            return self.evidence_records.get(target_evidence_id)
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON serialization."""
        return {
            "experiment_id": self.experiment_id,
            "analysis_id": self.analysis_id,
            "evidence_records": {
                k: v.dict() for k, v in self.evidence_records.items()
            },
            "total_claims": self.claim_counter,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvidenceMapper:
        """Create from dict (for deserialization)."""
        mapper = cls(data["experiment_id"], data["analysis_id"])
        mapper.claim_counter = data.get("total_claims", 0)
        for ev_data in data.get("evidence_records", {}).values():
            # Reconstruct EvidenceRecord
            # Need to handle the validator carefully
            pass
        return mapper