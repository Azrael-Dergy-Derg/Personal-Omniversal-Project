"""Structured refinement requests for the OIPM Iterative Refinement System.

The Iterative Refinement System (IRS) operates on structured visual intent

rather than treating an assembled prompt as the source of truth.

A refinement request describes what the user wants changed, preserved, or

reconsidered. It does not itself perform the change.

IRS must preserve explicit user intent, canon, references, and existing

visual decisions unless the requested refinement explicitly authorizes a

change.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

class RefinementAction(str, Enum):

    """Type of refinement requested."""

    MODIFY = "modify"

    ADD = "add"

    REMOVE = "remove"

    PRESERVE = "preserve"

    RECONSIDER = "reconsider"

class RefinementScope(str, Enum):

    """Structured scope targeted by a refinement request."""

    SUBJECT = "subject"

    SCENE = "scene"

    COMPOSITION = "composition"

    LIGHTING = "lighting"

    ARTISTIC_DIRECTION = "artistic_direction"

    CONSTRAINT = "constraint"

    REFERENCE = "reference"

    RELATIONSHIP = "relationship"

    GLOBAL = "global"

@dataclass(frozen=True)

class RefinementRequest:

    """Immutable description of one requested visual refinement.

    Attributes:

        request_id: Unique identifier for the refinement request.

        action: Operation requested by the user.

        scope: Visual-intent domain affected by the request.

        target: Specific target within the selected scope.

        instruction: Natural-language description of the requested change.

        reason: Optional explanation supplied by the user.

        preserve: Explicitly identified information that must remain

            unchanged during refinement.

    The request is declarative. It does not mutate VisualIntent and does

    not decide how the requested refinement should be implemented.

    """

    request_id: str

    action: RefinementAction

    scope: RefinementScope

    target: str

    instruction: str

    reason: str | None = None

    preserve: tuple[str, ...] = ()

    def __post_init__(self) -> None:

        """Validate the structural requirements of the request."""

        if not self.request_id.strip():

            raise ValueError(

                "request_id must not be empty"

            )

        if not self.target.strip():

            raise ValueError(

                "target must not be empty"

            )

        if not self.instruction.strip():

            raise ValueError(

                "instruction must not be empty"

            )

        if self.reason is not None and not self.reason.strip():

            raise ValueError(

                "reason must be non-empty when provided"

            )

        if any(

            not item.strip()

            for item in self.preserve

        ):

            raise ValueError(

                "preserve entries must not be empty"

            )