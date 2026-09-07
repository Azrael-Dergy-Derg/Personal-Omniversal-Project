"""Subject and Character Resolution Engine for OIPM.

The Subject and Character Resolution Engine (SCRE) is responsible for

resolving and maintaining subject identity within a VisualIntent.

The initial implementation is intentionally conservative. It establishes

the resolution boundary without inventing unspecified character

information, silently altering canon, or making independent artistic

decisions.

Future SCRE capabilities will include:

- canonical character resolution

- reference-assisted identity resolution

- species and anatomy consistency

- attribute conflict detection

- scene-specific overrides

- relationship-aware subject resolution

- ambiguity handling

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import CanonStatus, Subject, VisualIntent

@dataclass(frozen=True)

class SubjectResolutionResult:

    """Result produced by the Subject Resolution Engine."""

    visual_intent: VisualIntent

    resolved_subjects: tuple[Subject, ...] = ()

    warnings: tuple[str, ...] = ()

class SubjectResolver:

    """Resolve subjects within an OIPM VisualIntent.

    The resolver preserves supplied information and does not invent

    unspecified visual attributes.

    """

    name = "SubjectResolver"

    version = "0.1.0"

    def resolve(

        self,

        visual_intent: VisualIntent,

        *,

        identity: str | None = None,

        subject_type: str | None = None,

        species: str | None = None,

        canon_status: CanonStatus = CanonStatus.UNKNOWN,

    ) -> SubjectResolutionResult:

        """Resolve or register a subject in the VisualIntent.

        Args:

            visual_intent: The structured source-of-truth representation.

            identity: Optional subject identity.

            subject_type: Optional subject type.

            species: Optional species designation.

            canon_status: Canon relationship for the subject.

        Returns:

            A SubjectResolutionResult containing the updated

            VisualIntent and resolved subject collection.

        Raises:

            TypeError: If visual_intent is not a VisualIntent instance.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent instance."

            )

        warnings: list[str] = []

        subject = self._find_existing_subject(

            visual_intent,

            identity=identity,

        )

        if subject is None:

            subject = Subject(

                identity=identity,

                type=subject_type,

                species=species,

                canon_status=canon_status,

            )

            visual_intent.subjects.append(subject)

        else:

            warnings.extend(

                self._apply_explicit_identity_data(

                    subject,

                    subject_type=subject_type,

                    species=species,

                    canon_status=canon_status,

                )

            )

        return SubjectResolutionResult(

            visual_intent=visual_intent,

            resolved_subjects=(subject,),

            warnings=tuple(warnings),

        )

    @staticmethod

    def _find_existing_subject(

        visual_intent: VisualIntent,

        *,

        identity: str | None,

    ) -> Subject | None:

        """Find an existing subject by explicit identity."""

        if not identity:

            return None

        for subject in visual_intent.subjects:

            if subject.identity == identity:

                return subject

        return None

    @staticmethod

    def _apply_explicit_identity_data(

        subject: Subject,

        *,

        subject_type: str | None,

        species: str | None,

        canon_status: CanonStatus,

    ) -> list[str]:

        """Apply explicit subject data without inventing information."""

        warnings: list[str] = []

        if subject_type is not None:

            if subject.type is None:

                subject.type = subject_type

            elif subject.type != subject_type:

                warnings.append(

                    "Existing subject type conflicts with supplied "

                    "subject type; existing value was preserved."

                )

        if species is not None:

            if subject.species is None:

                subject.species = species

            elif subject.species != species:

                warnings.append(

                    "Existing subject species conflicts with supplied "

                    "species; existing value was preserved."

                )

        if (

            canon_status != CanonStatus.UNKNOWN

            and subject.canon_status == CanonStatus.UNKNOWN

        ):

            subject.canon_status = canon_status

        return warnings