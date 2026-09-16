"""Structured results for the OIPM Iterative Refinement System.

IRS separates refinement planning from refinement application.

A RefinementResult records what happened during a refinement operation.

It does not itself perform mutations and does not decide whether a proposed

change is authoritative.

This boundary allows later IRS components to distinguish:

- requested refinement,

- planned refinement,

- proposed changes,

- applied changes,

- preserved information,

- warnings,

- and unresolved issues.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

class RefinementStatus(str, Enum):

    """Outcome state of a refinement operation."""

    PROPOSED = "proposed"

    APPLIED = "applied"

    PARTIAL = "partial"

    REJECTED = "rejected"

    NO_CHANGE = "no_change"

@dataclass(frozen=True)

class RefinementChange:

    """One structured change associated with a refinement.

    Attributes:

        target: Structured target affected by the change.

        field: Field or attribute affected by the change.

        previous_value: Value before the change, when known.

        new_value: Proposed or resulting value.

        reason: Explanation for the change.

    This model records a change. It does not apply one.

    """

    target: str

    field: str

    previous_value: object | None

    new_value: object | None

    reason: str | None = None

    def __post_init__(self) -> None:

        """Validate the structural requirements of a change."""

        if not self.target.strip():

            raise ValueError(

                "target must not be empty"

            )

        if not self.field.strip():

            raise ValueError(

                "field must not be empty"

            )

        if self.reason is not None and not self.reason.strip():

            raise ValueError(

                "reason must be non-empty when provided"

            )

@dataclass(frozen=True)

class RefinementResult:

    """Immutable result of a refinement operation.

    Attributes:

        request_id: Identifier of the originating refinement request.

        status: Outcome of the refinement operation.

        changes: Structured changes proposed or applied.

        preserved: Information explicitly preserved during refinement.

        warnings: Non-fatal issues encountered during refinement.

        unresolved: Issues that remain unresolved and require further

            reasoning or user input.

    The result is informational. It does not itself mutate VisualIntent,

    references, or canon.

    """

    request_id: str

    status: RefinementStatus

    changes: tuple[RefinementChange, ...] = ()

    preserved: tuple[str, ...] = ()

    warnings: tuple[str, ...] = ()

    unresolved: tuple[str, ...] = ()

    def __post_init__(self) -> None:

        """Validate the structural requirements of a result."""

        if not self.request_id.strip():

            raise ValueError(

                "request_id must not be empty"

            )

        self._validate_text_collection(

            self.preserved,

            "preserved",

        )

        self._validate_text_collection(

            self.warnings,

            "warnings",

        )

        self._validate_text_collection(

            self.unresolved,

            "unresolved",

        )

    @staticmethod

    def _validate_text_collection(

        values: tuple[str, ...],

        field_name: str,

    ) -> None:

        """Validate a tuple of descriptive text values."""

        if any(not value.strip() for value in values):

            raise ValueError(

                f"{field_name} entries must not be empty"

            )

    @property

    def change_count(self) -> int:

        """Return the number of recorded changes."""

        return len(self.changes)

    @property

    def warning_count(self) -> int:

        """Return the number of warnings."""

        return len(self.warnings)

    @property

    def unresolved_count(self) -> int:

        """Return the number of unresolved issues."""

        return len(self.unresolved)

    @property

    def has_changes(self) -> bool:

        """Return whether the result contains recorded changes."""

        return bool(self.changes)

    @property

    def has_warnings(self) -> bool:

        """Return whether the result contains warnings."""

        return bool(self.warnings)

    @property

    def has_unresolved(self) -> bool:

        """Return whether unresolved issues remain."""

        return bool(self.unresolved)