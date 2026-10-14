"""Data models for Phase 15 visualization layer.

Defines the data structures consumed by visualizations from Phase 14
analysis outputs and experiment artifacts.

All values must originate from experiment artifacts or Phase 14 analysis
outputs - never manually typed or hard-coded.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class VisualizationManifest(BaseModel):
    """Metadata for a generated visualization."""

    figure_id: str = Field(..., description="Stable figure identifier")
    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis identifier")
    metric: str = Field(..., description="Primary metric visualized")
    source_file: str = Field(..., description="Source data file path")
    source_hash: str = Field(..., description="SHA256 hash of source data")
    method_filter: str | None = Field(
        default=None, description="Applied method filter"
    )
    seed_filter: str | None = Field(
        default=None, description="Applied seed filter"
    )
    generated_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO timestamp when figure was generated"
    )
    visualization_version: str = Field(
        ..., description="Visualization code version"
    )


class FigureSpec(BaseModel):
    """Specification for a research figure."""

    figure_id: str = Field(..., description="Stable figure identifier")
    title: str = Field(..., description="Neutral figure title")
    kind: str = Field(..., description="Figure type (discovery, distribution, etc.)")
    methods: list[str] = Field(
        default_factory=list, description="Methods included in figure"
    )
    x_label: str = Field(..., description="X-axis label with units")
    y_label: str = Field(..., description="Y-axis label with units")
    x_scale: str = Field(default="linear", description="X-axis scale")
    y_scale: str = Field(default="linear", description="Y-axis scale")
    export_formats: list[str] = Field(
        default=["png", "svg", "pdf"], description="Export formats"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class TableSpec(BaseModel):
    """Specification for a research table."""

    table_id: str = Field(..., description="Stable table identifier")
    title: str = Field(..., description="Neutral table title")
    columns: list[str] = Field(..., description="Column names")
    methods: list[str] = Field(
        default_factory=list, description="Methods included"
    )
    export_formats: list[str] = Field(
        default=["csv", "json", "markdown"], description="Export formats"
    )


class DashboardConfig(BaseModel):
    """Configuration for the read-only research dashboard."""

    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis identifier")
    methods: list[str] = Field(
        default_factory=list, description="Methods to display"
    )
    seeds: list[str] = Field(
        default_factory=list, description="Seeds to display"
    )
    show_individual: bool = Field(
        default=True, description="Show individual seed curves"
    )
    show_aggregate: bool = Field(
        default=True, description="Show aggregate/representative curves"
    )
    theme: str = Field(default="professional", description="Color theme")
    palette: str = Field(
        default="colorblind_safe", description="Color palette name"
    )


class EvidencePackage(BaseModel):
    """Structural definition of the final evidence package."""

    experiment_id: str = Field(..., description="Experiment identifier")
    analysis_id: str = Field(..., description="Phase 14 analysis ID")
    visualization_id: str = Field(..., description="Visualization batch ID")
    code_version: str = Field(..., description="Software version")
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO timestamp"
    )
    hashes: dict[str, str] = Field(
        default_factory=dict, description="SHA256 hashes of artifacts"
    )
    configs: dict[str, str] = Field(
        default_factory=dict, description="Configuration files"
    )
    manifests: dict[str, str] = Field(
        default_factory=dict, description="Manifest files"
    )
    figures: dict[str, str] = Field(
        default_factory=dict, description="Generated figures"
    )
    tables: dict[str, str] = Field(
        default_factory=dict, description="Generated tables"
    )
    reports: dict[str, str] = Field(
        default_factory=dict, description="Generated reports"
    )
    reproducibility: dict[str, str] = Field(
        default_factory=dict, description="Reproducibility bundle"
    )
    integrity: dict[str, str] = Field(
        default_factory=dict, description="Integrity verification"
    )