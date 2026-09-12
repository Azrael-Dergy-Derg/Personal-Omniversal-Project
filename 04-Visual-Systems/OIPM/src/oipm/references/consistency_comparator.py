"""Attribute-level consistency comparison for OIPM references.

This module provides the first attribute-level comparison layer of the

Reference & Consistency System (RCS).

The comparator compares explicitly supplied reference metadata against

corresponding VisualIntent data when a direct comparison is possible.

It does not:

- modify VisualIntent,

- modify references,

- invent missing information,

- infer unspecified reference attributes,

- promote references to canon,

- resolve conflicts,

- choose which source is correct,

- or rewrite VisualIntent to match a reference.

VisualIntent remains the source of truth for the OIPM processing pipeline.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

from typing import Any

from oipm.models import VisualIntent

from oipm.references.reference_model import Reference

class ComparisonStatus(str, Enum):

    """Outcome of comparing one reference attribute."""

    MATCH = "match"

    MISMATCH = "mismatch"

    UNAVAILABLE = "unavailable"

@dataclass(frozen=True)

class ComparisonFinding:

    """Structured result of comparing one reference attribute.

    Attributes:

        reference_id: Identifier of the reference being compared.

        attribute: Name of the reference attribute being compared.

        status: Result of the comparison.

        reference_value: Value supplied by the reference.

        visual_intent_value: Corresponding VisualIntent value.

        message: Human-readable explanation of the finding.

    A finding reports comparison state only. It does not determine

    authority or resolve a mismatch.

    """

    reference_id: str

    attribute: str

    status: ComparisonStatus

    reference_value: Any

    visual_intent_value: Any

    message: str

class ConsistencyComparator:

    """Compare explicit reference metadata against VisualIntent."""

    def compare(

        self,

        reference: Reference,

        visual_intent: VisualIntent,

    ) -> tuple[ComparisonFinding, ...]:

        """Compare directly comparable reference metadata.

        The initial comparator compares only reference metadata that has

        an explicit corresponding field in VisualIntent.

        Currently supported comparisons are:

            - description -> metadata.reference_description

            - tags -> metadata.reference_tags

        These comparisons are intentionally conservative. If the

        corresponding VisualIntent metadata is absent, the result is

        UNAVAILABLE rather than an inferred match or mismatch.

        Args:

            reference: Structured visual reference.

            visual_intent: Generator-neutral OIPM visual intent.

        Returns:

            Deterministically ordered comparison findings.

        Raises:

            TypeError: If either argument has an invalid type.

        """

        if not isinstance(reference, Reference):

            raise TypeError("reference must be a Reference")

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent")

        findings: list[ComparisonFinding] = []

        self._compare_description(

            reference,

            visual_intent,

            findings,

        )

        self._compare_tags(

            reference,

            visual_intent,

            findings,

        )

        return tuple(findings)

    def _compare_description(

        self,

        reference: Reference,

        visual_intent: VisualIntent,

        findings: list[ComparisonFinding],

    ) -> None:

        """Compare an explicitly supplied reference description."""

        if reference.description is None:

            return

        metadata = visual_intent.metadata

        visual_intent_value = metadata.get("reference_description")

        if visual_intent_value is None:

            findings.append(

                ComparisonFinding(

                    reference_id=reference.reference_id,

                    attribute="description",

                    status=ComparisonStatus.UNAVAILABLE,

                    reference_value=reference.description,

                    visual_intent_value=None,

                    message=(

                        "VisualIntent does not contain an explicit "

                        "reference_description value for comparison."

                    ),

                )

            )

            return

        status = (

            ComparisonStatus.MATCH

            if reference.description == visual_intent_value

            else ComparisonStatus.MISMATCH

        )

        findings.append(

            ComparisonFinding(

                reference_id=reference.reference_id,

                attribute="description",

                status=status,

                reference_value=reference.description,

                visual_intent_value=visual_intent_value,

                message=self._comparison_message(

                    "description",

                    status,

                ),

            )

        )

    def _compare_tags(

        self,

        reference: Reference,

        visual_intent: VisualIntent,

        findings: list[ComparisonFinding],

    ) -> None:

        """Compare explicitly supplied reference tags."""

        if not reference.tags:

            return

        metadata = visual_intent.metadata

        visual_intent_value = metadata.get("reference_tags")

        if visual_intent_value is None:

            findings.append(

                ComparisonFinding(

                    reference_id=reference.reference_id,

                    attribute="tags",

                    status=ComparisonStatus.UNAVAILABLE,

                    reference_value=reference.tags,

                    visual_intent_value=None,

                    message=(

                        "VisualIntent does not contain an explicit "

                        "reference_tags value for comparison."

                    ),

                )

            )

            return

        normalized_reference = frozenset(reference.tags)

        normalized_visual_intent = self._normalize_tags(

            visual_intent_value

        )

        status = (

            ComparisonStatus.MATCH

            if normalized_reference == normalized_visual_intent

            else ComparisonStatus.MISMATCH

        )

        findings.append(

            ComparisonFinding(

                reference_id=reference.reference_id,

                attribute="tags",

                status=status,

                reference_value=reference.tags,

                visual_intent_value=visual_intent_value,

                message=self._comparison_message(

                    "tags",

                    status,

                ),

            )

        )

    @staticmethod

    def _normalize_tags(value: object) -> frozenset[str]:

        """Normalize an explicitly supplied tag collection.

        Values that cannot be interpreted as a collection of strings are

        preserved as an empty set for comparison purposes. The comparator

        does not attempt to infer or repair malformed data.

        """

        if isinstance(value, str):

            return frozenset({value})

        if isinstance(value, (list, tuple, set, frozenset)):

            return frozenset(

                item

                for item in value

                if isinstance(item, str)

            )

        return frozenset()

    @staticmethod

    def _comparison_message(

        attribute: str,

        status: ComparisonStatus,

    ) -> str:

        """Build a deterministic comparison message."""

        if status is ComparisonStatus.MATCH:

            return f"reference {attribute} matches VisualIntent"

        if status is ComparisonStatus.MISMATCH:

            return f"reference {attribute} differs from VisualIntent"

        return (

            f"reference {attribute} could not be compared with "

            "VisualIntent"

        )