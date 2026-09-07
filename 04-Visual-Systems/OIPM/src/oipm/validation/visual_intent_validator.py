"""Validation of OIPM VisualIntent instances.

The VisualIntentValidator performs conservative structural validation

of the OIPM source-of-truth representation.

It does not:

- invent missing information

- resolve creative ambiguity

- alter canon

- make artistic decisions

- generate prompts

- silently repair invalid state

More advanced semantic, consistency, conflict, and constraint validation

belongs to later OIPM systems.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import VisualIntent

@dataclass(frozen=True)

class ValidationIssue:

    """Represents a single validation issue."""

    code: str

    message: str

    path: str | None = None

@dataclass(frozen=True)

class ValidationResult:

    """Result produced by the VisualIntentValidator."""

    valid: bool

    issues: tuple[ValidationIssue, ...] = ()

class VisualIntentValidator:

    """Validate the structural integrity of a VisualIntent."""

    name = "VisualIntentValidator"

    version = "0.1.0"

    def validate(self, visual_intent: VisualIntent) -> ValidationResult:

        """Validate a VisualIntent instance.

        Args:

            visual_intent: The VisualIntent to validate.

        Returns:

            A ValidationResult containing any detected issues.

        Raises:

            TypeError: If visual_intent is not a VisualIntent instance.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent instance.")

        issues: list[ValidationIssue] = []

        self._validate_metadata(visual_intent, issues)

        self._validate_subjects(visual_intent, issues)

        self._validate_relationships(visual_intent, issues)

        return ValidationResult(

            valid=not issues,

            issues=tuple(issues),

        )

    @staticmethod

    def _validate_metadata(

        visual_intent: VisualIntent,

        issues: list[ValidationIssue],

    ) -> None:

        """Validate required metadata state."""

        metadata = visual_intent.metadata

        if metadata.intent_id is None:

            issues.append(

                ValidationIssue(

                    code="MISSING_INTENT_ID",

                    message="VisualIntent is missing an intent ID.",

                    path="metadata.intent_id",

                )

            )

        if not metadata.user_input.strip():

            issues.append(

                ValidationIssue(

                    code="EMPTY_USER_INPUT",

                    message="VisualIntent contains no user input.",

                    path="metadata.user_input",

                )

            )

        if metadata.created_at > metadata.modified_at:

            issues.append(

                ValidationIssue(

                    code="INVALID_METADATA_TIMESTAMPS",

                    message="created_at cannot be later than modified_at.",

                    path="metadata",

                )

            )

    @staticmethod

    def _validate_subjects(

        visual_intent: VisualIntent,

        issues: list[ValidationIssue],

    ) -> None:

        """Validate subject identity and collection integrity."""

        subject_ids = [subject.id for subject in visual_intent.subjects]

        if len(subject_ids) != len(set(subject_ids)):

            issues.append(

                ValidationIssue(

                    code="DUPLICATE_SUBJECT_IDS",

                    message="Subject IDs must be unique within a VisualIntent.",

                    path="subjects",

                )

            )

    @staticmethod

    def _validate_relationships(

        visual_intent: VisualIntent,

        issues: list[ValidationIssue],

    ) -> None:

        """Validate relationship references against known subjects."""

        subject_ids = {subject.id for subject in visual_intent.subjects}

        for index, relationship in enumerate(visual_intent.relationships):

            if relationship.subject_a not in subject_ids:

                issues.append(

                    ValidationIssue(

                        code="UNKNOWN_RELATIONSHIP_SUBJECT",

                        message=(

                            "Relationship references a subject that does "

                            "not exist in the VisualIntent."

                        ),

                        path=f"relationships[{index}].subject_a",

                    )

                )

            if relationship.subject_b not in subject_ids:

                issues.append(

                    ValidationIssue(

                        code="UNKNOWN_RELATIONSHIP_SUBJECT",

                        message=(

                            "Relationship references a subject that does "

                            "not exist in the VisualIntent."

                        ),

                        path=f"relationships[{index}].subject_b",

                    )

                )