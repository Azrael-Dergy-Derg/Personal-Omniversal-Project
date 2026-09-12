"""Reference consistency checking for OIPM.

This module establishes the initial comparison boundary for the Reference

& Consistency System (RCS).

The checker determines whether a reference's declared visual roles have a

corresponding area of VisualIntent available for comparison.

This is intentionally a structural consistency check. It does not:

- modify VisualIntent,

- modify references,

- promote references to canon,

- invent missing visual information,

- resolve conflicts,

- decide which source is correct,

- or silently reinterpret reference meaning.

VisualIntent remains the source of truth.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

from oipm.models import VisualIntent

from oipm.references.reference_model import Reference, ReferenceRole

class ConsistencyStatus(str, Enum):

    """Result status for a reference consistency check."""

    MATCHABLE = "matchable"

    UNMATCHABLE = "unmatchable"

    NOT_APPLICABLE = "not_applicable"

@dataclass(frozen=True)

class ConsistencyFinding:

    """Structured result produced by a consistency check.

    Attributes:

        reference_id: Identifier of the reference being evaluated.

        role: Reference role being evaluated.

        status: Structural consistency status.

        message: Human-readable explanation of the finding.

    A finding describes the comparison state. It does not determine which

    source is authoritative or modify either source.

    """

    reference_id: str

    role: ReferenceRole

    status: ConsistencyStatus

    message: str

_ROLE_TARGETS: dict[ReferenceRole, str] = {

    ReferenceRole.IDENTITY: "subjects",

    ReferenceRole.APPEARANCE: "subjects",

    ReferenceRole.ANATOMY: "subjects",

    ReferenceRole.CLOTHING: "subjects",

    ReferenceRole.EQUIPMENT: "subjects",

    ReferenceRole.POSE: "subjects",

    ReferenceRole.COMPOSITION: "composition",

    ReferenceRole.LIGHTING: "lighting",

    ReferenceRole.STYLE: "artistic_direction",

    ReferenceRole.COLOR: "artistic_direction",

    ReferenceRole.ENVIRONMENT: "scene",

    ReferenceRole.MATERIAL: "artistic_direction",

    ReferenceRole.INSPIRATION: "artistic_direction",

    ReferenceRole.CONTINUITY: "subjects",

}

class ConsistencyChecker:

    """Perform structural reference-to-VisualIntent checks."""

    def check(

        self,

        reference: Reference,

        visual_intent: VisualIntent,

    ) -> tuple[ConsistencyFinding, ...]:

        """Check whether a reference's roles can be compared.

        Args:

            reference: Structured visual reference.

            visual_intent: Generator-neutral OIPM visual intent.

        Returns:

            Deterministically ordered consistency findings.

        Raises:

            TypeError: If either input has the wrong type.

        Notes:

            A MATCHABLE finding means the relevant VisualIntent area exists

            and can therefore be examined by a later, more detailed RCS

            comparison stage.

            An UNMATCHABLE finding means the reference declares a role for

            which the current VisualIntent does not contain applicable

            structured data.

            A NOT_APPLICABLE finding is reserved for roles that do not yet

            have a defined structural comparison target.

        """

        if not isinstance(reference, Reference):

            raise TypeError("reference must be a Reference")

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent")

        findings: list[ConsistencyFinding] = []

        for role in sorted(reference.roles, key=lambda item: item.value):

            target = _ROLE_TARGETS.get(role)

            if target is None:

                findings.append(

                    ConsistencyFinding(

                        reference_id=reference.reference_id,

                        role=role,

                        status=ConsistencyStatus.NOT_APPLICABLE,

                        message=(

                            f"no structural comparison target is defined "

                            f"for role: {role.value}"

                        ),

                    )

                )

                continue

            value = getattr(visual_intent, target, None)

            if self._has_comparable_data(value):

                findings.append(

                    ConsistencyFinding(

                        reference_id=reference.reference_id,

                        role=role,

                        status=ConsistencyStatus.MATCHABLE,

                        message=(

                            f"VisualIntent contains structured data for "

                            f"reference role '{role.value}' in "

                            f"'{target}'"

                        ),

                    )

                )

            else:

                findings.append(

                    ConsistencyFinding(

                        reference_id=reference.reference_id,

                        role=role,

                        status=ConsistencyStatus.UNMATCHABLE,

                        message=(

                            f"VisualIntent contains no structured data "

                            f"available for comparison under reference "

                            f"role '{role.value}' in '{target}'"

                        ),

                    )

                )

        return tuple(findings)

    @staticmethod

    def _has_comparable_data(value: object) -> bool:

        """Return whether a VisualIntent field contains comparable data."""

        if value is None:

            return False

        if isinstance(value, (list, tuple, set, frozenset, dict)):

            return bool(value)

        return True