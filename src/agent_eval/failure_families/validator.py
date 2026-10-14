"""Family validation and integrity checking."""

from __future__ import annotations

from typing import Any

from agent_eval.domain.identifiers import is_valid
from agent_eval.failure_families.models import (
    FamilyMembershipExplanation,
)


class FamilyValidatorImpl:
    """Implementation of family validation logic."""

    @classmethod
    def validate_family(cls, family: Any) -> tuple[bool, list[str]]:
        """Validate a single family's internal consistency."""
        errors = []

        # Check family ID
        if not family.family_id or not family.family_id.strip():
            errors.append("Family ID is empty")
        elif not family.family_id.startswith("FF-"):
            errors.append(
                f"Family ID {family.family_id} does not follow FF- prefix convention"
            )

        # Check members
        if not family.member_failure_ids:
            errors.append("Family has no members")
        else:
            # Check all member IDs are valid
            for mid in family.member_failure_ids:
                if not mid or not is_valid(mid):
                    errors.append(f"Invalid member failure ID: {mid}")

            # Check for duplicates
            if len(family.member_failure_ids) != len(set(family.member_failure_ids)):
                errors.append("Family contains duplicate member IDs")

        # Check representative
        if (
            not family.representative_failure_id
            or not family.representative_failure_id.strip()
        ):
            errors.append("Representative failure ID is empty")
        elif family.representative_failure_id not in family.member_failure_ids:
            errors.append("Representative failure ID is not a member of the family")

        # Check family size matches member count
        if family.family_size != len(family.member_failure_ids):
            errors.append(
                f"Family size ({family.family_size}) does not match "
                f"member count ({len(family.member_failure_ids)})"
            )

        # Check coherence score
        if family.coherence_score < 0 or family.family.coherence_score > 1:
            errors.append(f"Invalid coherence score: {family.coherence_score}")

        # Check taxonomy labels
        for label in family.taxonomy_labels:
            if not label or not label.strip():
                errors.append("Empty taxonomy label found")

        return len(errors) == 0, errors

    @classmethod
    def validate_all_families(cls, families: list[Any]) -> tuple[bool, list[str]]:
        """Validate all families for cross-family constraints."""
        errors = []

        # Check for duplicate family IDs
        family_ids = [f.family_id for f in families]
        if len(family_ids) != len(set(family_ids)):
            duplicates = [fid for fid in family_ids if family_ids.count(fid) > 1]
            errors.append(f"Duplicate family IDs: {duplicates}")

        # Check for overlapping memberships
        all_members: dict[str, str] = {}
        for family in families:
            for mid in family.member_failure_ids:
                if mid in all_members:
                    errors.append(
                        f"Failure {mid} appears in multiple families: "
                        f"{all_members[mid]} and {family.family_id}"
                    )
                all_members[mid] = family.family_id

        # Validate each family individually
        for family in families:
            valid, errors_list = cls.validate_family(family)
            if not valid:
                errors.extend([f"Family {family.family_id}: {e}" for e in errors_list])

        # Check for empty families
        empty_families = [
            f.family_id for f in families if len(f.member_failure_ids) == 0
        ]
        if empty_families:
            errors.append(f"Empty families found: {empty_families}")

        return len(errors) == 0, errors

    @classmethod
    def validate_membership_explanations(
        cls,
        explanations: list[Any],
        families: list[Any],
    ) -> tuple[bool, list[str]]:
        """Validate membership explanations match family assignments."""
        errors = []

        family_lookup = {f.family_id: f for f in families}

        for exp in explanations:
            family = family_lookup.get(exp.family_id)
            if family is None:
                errors.append(
                    f"Explanation references non-existent family: {exp.family_id}"
                )
                continue

            # Check failure is actually a member
            if exp.failure_id not in family.member_failure_ids:
                errors.append(
                    f"Explanation for {exp.failure_id} claims membership in "
                    f"{exp.family_id} but failure is not a member"
                )

            # Check similarity is reasonable
            if exp.similarity < 0 or exp.similarity > 1:
                errors.append(f"Invalid similarity value: {exp.similarity}")

            # Check threshold
            if exp.similarity < exp.threshold:
                errors.append(
                    f"Similarity {exp.similarity} below threshold {exp.threshold} "
                    f"for {exp.failure_id} -> {exp.family_id}"
                )

        return len(errors) == 0, errors

    @classmethod
    def generate_membership_explanation(
        cls,
        failure_id: str,
        family: Any,
        similarity: float,
        matched_features: list[str],
        threshold: float,
    ) -> Any:
        """Generate a membership explanation for a failure."""
        return FamilyMembershipExplanation(
            failure_id=failure_id,
            family_id=family.family_id,
            similarity=similarity,
            matched_features=matched_features,
            threshold=threshold,
        )

    @classmethod
    def validate_coherence(
        cls, family: Any, similarities: dict[tuple[str, str], float]
    ) -> tuple[bool, list[str]]:
        """Validate family coherence matches pairwise similarities."""
        errors = []

        if len(family.member_failure_ids) <= 1:
            if family.coherence_score != 1.0:
                errors.append(
                    f"Singleton family should have coherence 1.0, got {family.coherence_score}"
                )
            return len(errors) == 0, errors

        # Compute expected coherence from similarity matrix
        member_ids = family.member_failure_ids
        pair_similarities: list[float] = []

        for i, mid1 in enumerate(member_ids):
            for mid2 in member_ids[i + 1 :]:
                key = tuple(sorted([mid1, mid2]))
                if key in similarities:
                    pair_similarities.append(similarities[key])

        if pair_similarities:
            expected_coherence = sum(pair_similarities) / len(pair_similarities)
            if abs(family.coherence_score - expected_coherence) > 0.01:
                errors.append(
                    f"Coherence mismatch: stored={family.coherence_score:.4f}, "
                    f"expected={expected_coherence:.4f}"
                )

        return len(errors) == 0, errors

    @classmethod
    def validate_against_threshold(
        cls,
        families: list[Any],
        distance_threshold: float,
        similarity_matrix: dict[tuple[str, str], float],
    ) -> tuple[bool, list[str]]:
        """Validate that no two members within a family exceed distance threshold."""
        errors = []

        for family in families:
            member_ids = family.member_failure_ids
            for i, mid1 in enumerate(family.member_failure_ids):
                for mid2 in member_ids[i + 1 :]:
                    key = tuple(sorted([mid1, mid2]))
                    if key in similarity_matrix:
                        sim = similarity_matrix[key]
                        dist = 1.0 - sim
                        if dist > distance_threshold + 1e-6:  # Small epsilon
                            errors.append(
                                f"Members {mid1} and {mid2} in family {family.family_id} "
                                f"have distance {dist:.4f} > threshold {distance_threshold}"
                            )

        return len(errors) == 0, errors


def validate_clustering_output(
    families: list[Any],
    similarity_matrix: dict[tuple[str, str], float],
    config: Any,
) -> tuple[bool, list[str]]:
    """Comprehensive validation of clustering output."""
    all_errors = []

    # Validate families
    _valid, errors = FamilyValidatorImpl.validate_all_families(families)
    all_errors.extend(errors)

    # Validate against threshold
    _valid, errors = FamilyValidatorImpl.validate_against_threshold(
        families, config.distance_threshold, similarity_matrix
    )
    all_errors.extend(errors)

    return len(all_errors) == 0, all_errors


# Alias for compatibility
FamilyValidator = FamilyValidatorImpl

