"""
Common domain structures and utilities shared across models.

Framework-independent, Pydantic-compatible, serialization-friendly.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class DomainMetadata(dict):
    """JSON-serializable metadata bag for domain objects."""

    def __init__(self, data: dict[str, Any] | None = None):
        super().__init__(data or {})

    def set(self, key: str, value: Any) -> None:
        self[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return super().get(key, default)

    def to_dict(self) -> dict[str, Any]:
        return dict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainMetadata:
        return cls(data)


class Timestamp:
    """Timezone-aware timestamp utilities."""

    @staticmethod
    def now() -> datetime:
        return datetime.now(UTC)

    @staticmethod
    def iso(dt: datetime | None = None) -> str:
        if dt is None:
            dt = datetime.now(UTC)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.isoformat()

    @staticmethod
    def parse(s: str) -> datetime:
        from datetime import datetime

        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt


class JSONSerializable:
    """Mixin for JSON serialization."""

    def to_dict(self) -> dict[str, Any]:
        if hasattr(self, "__dict__"):
            return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return {}

    def model_dump(self, *args: Any, **kwargs: Any) -> Any:
        return self.to_dict()

    def model_dump_json(self) -> str:
        return json.dumps(self.model_dump(mode="json"), default=self._json_default)

    @staticmethod
    def _json_default(o: Any) -> Any:
        if hasattr(o, "model_dump"):
            return o.model_dump(mode="json")
        if isinstance(o, Enum):
            return o.name
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")


class VersionedModel:
    """Mixin adding version tracking."""

    version: int = 1
    created_at: datetime = Timestamp.now()
    updated_at: datetime = Timestamp.now()

    def touch(self) -> None:
        self.updated_at = Timestamp.now()

    def is_current(self, version: int) -> bool:
        return self.version == version


class BaseDomainModel:
    """Base class providing common fields and methods."""

    id: str
    metadata: DomainMetadata

    def __init__(self, id: str, metadata: DomainMetadata | None = None):
        from .identifiers import is_valid

        if not is_valid(id):
            raise ValueError(f"Invalid id: {id}")
        self.id = id
        self.metadata = metadata or DomainMetadata()

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "metadata": self.metadata.to_dict(),
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> BaseDomainModel:
        instance = cls.__new__(cls)
        instance.id = data.get("id", "")
        instance.metadata = DomainMetadata(data.get("metadata", {}))
        return instance
