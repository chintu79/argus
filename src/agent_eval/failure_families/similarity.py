"""Similarity calculation for failure family clustering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent_eval.failure_families.models import SimilarityWeights


@dataclass
class FeatureComparison:
    """Result of comparing two feature values."""

    feature_name: str
    similarity: float
    feature_a: Any
    feature_b: Any
    matched: bool


class SimilarityCalculator:
    """Calculates similarity between two failure feature sets."""

    def __init__(self, weights: SimilarityWeights | None = None):
        self.weights = weights or SimilarityWeights().normalize()
        self._feature_comparators = {
            "invariant_id": self._compare_categorical,
            "reason_code": self._compare_categorical,
            "action": self._compare_categorical,
            "tool": self._compare_categorical,
            "tool_category": self._compare_categorical,
            "resource_type": self._compare_categorical,
            "resource_scope": self._compare_categorical,
            "authorization_decision": self._compare_categorical,
            "state_transition": self._compare_categorical,
            "process_stage": self._compare_categorical,
            "severity": self._compare_severity,
            "event_pattern": self._compare_categorical,
            "taxonomy_label": self._compare_taxonomy,
        }

    def calculate(
        self,
        features_a: dict[str, Any],
        features_b: dict[str, Any],
    ) -> tuple[float, list[str]]:
        """
        Calculate similarity between two feature sets.

        Returns:
            (overall_similarity, matched_features)
        """
        normalized_weights = self.weights.normalize()
        weight_dict = normalized_weights.dict()

        total_similarity = 0.0
        total_weight = 0.0
        feature_sims = {}
        matched_features = []

        for feature_name, weight in weight_dict.items():
            if weight == 0:
                continue

            value_a = features_a.get(feature_name)
            value_b = features_b.get(feature_name)

            # Handle missing values
            if value_a is None and value_b is None:
                # Both missing - exclude from calculation
                continue
            elif value_a is None or value_b is None:
                # One missing - exclude feature and renormalize
                # Could also assign 0 similarity
                similarity = 0.0
            else:
                # Both present - compare
                comparator = self._feature_comparators.get(
                    feature_name, self._compare_categorical
                )
                similarity = comparator(value_a, value_b)

            feature_sims[feature_name] = similarity
            total_similarity += similarity * weight
            total_weight += weight

            if similarity > 0.0:
                matched_features.append(feature_name)

        # Normalize by actual total weight used
        if total_weight > 0:
            overall = total_similarity / total_weight
        else:
            overall = 0.0

        # Clamp to [0, 1]
        overall = max(0.0, min(1.0, overall))

        return overall, matched_features

    def _compare_categorical(self, a: Any, b: Any) -> float:
        """Compare two categorical values."""
        if a == b:
            return 1.0
        return 0.0

    def _compare_severity(self, a: Any, b: Any) -> float:
        """Compare severity levels with ordinal similarity."""
        severity_order = {
            "INFO": 0,
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4,
        }

        try:
            a_val = severity_order.get(str(a).upper(), 0)
            b_val = severity_order.get(str(b).upper(), 0)
            diff = abs(a_val - b_val)
            # Normalize: max difference is 4 (CRITICAL vs INFO)
            return max(0.0, 1.0 - diff / 4.0)
        except (KeyError, AttributeError):
            return self._compare_categorical(a, b)

    def _compare_taxonomy(self, a: Any, b: Any) -> float:
        """Compare taxonomy labels with hierarchical similarity."""
        if a == b:
            return 1.0

        # Try hierarchical comparison
        a_parts = str(a).split("/")
        b_parts = str(b).split("/")

        # Find common prefix
        common = 0
        for i in range(min(len(a_parts), len(b_parts))):
            if a_parts[i] == b_parts[i]:
                common += 1
            else:
                break

        if common > 0:
            # Partial credit for shared hierarchy
            max_depth = max(len(a_parts), len(b_parts))
            return common / max_depth

        return 0.0


class FeatureSimilarityMatrix:
    """Computes and caches pairwise similarity matrix."""

    def __init__(self, calculator: SimilarityCalculator):
        self.calculator = calculator
        self._cache: dict[tuple[str, str], float] = {}

    def compute_matrix(
        self,
        failures: list[Any],
    ) -> dict[tuple[str, str], float]:
        """Compute pairwise similarity matrix."""
        n = len(failures)
        matrix = {}

        for i in range(n):
            for j in range(i, n):
                fi = failures[i]
                fj = failures[j]

                if i == j:
                    sim = 1.0
                else:
                    sim, _ = self.calculator.calculate(
                        failures[i],
                        failures[j],
                    )

                matrix[(fi.failure_id, fj.failure_id)] = sim
                matrix[(fj.failure_id, fi.failure_id)] = sim

        return matrix

    def get_similarity(self, failure_a: Any, failure_b: Any) -> float:
        """Get cached or compute similarity."""
        key = (failure_a.failure_id, failure_b.failure_id)
        if key in self._cache:
            return self._cache[key]

        sim, _ = self.calculator.calculate(
            failure_a,
            failure_b,
        )
        self._cache[key] = sim
        return sim


def calculate_feature_similarity(
    feature_a: Any,
    feature_b: Any,
    feature_name: str,
) -> float:
    """Standalone function for comparing two feature values."""
    calculator = SimilarityCalculator()
    comparator = calculator._feature_comparators.get(
        feature_name, calculator._compare_categorical
    )
    return comparator(feature_a, feature_b)


def compare_feature_sets(
    features_a: dict[str, Any],
    features_b: dict[str, Any],
    weights: SimilarityWeights,
) -> tuple[float, list[str]]:
    """Convenience function for one-off similarity calculations."""
    calculator = SimilarityCalculator(weights)
    return calculator.calculate(features_a, features_b)
