"""Core refinement planning engine for the OIPM Iterative Refinement System.

The IRS operates on structured visual intent rather than directly rewriting

assembled prompt text.

This module provides the first refinement boundary: converting a validated

RefinementRequest into an explicit refinement plan.

The engine does not:

- mutate VisualIntent,

- mutate references,

- modify canon,

- silently resolve conflicts,

- invent visual information,

- reinterpret unrelated creative intent,

- or generate a replacement prompt.

Actual state mutation, when supported by the broader IRS architecture, must

be explicit, controlled, and separately testable.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.refinement.refinement_request import (

    RefinementAction,

    RefinementRequest,

    RefinementScope,

)

@dataclass(frozen=True)

class RefinementPlan:

    """Immutable plan describing how a refinement request is scoped.

    Attributes:

        request_id: Identifier of the originating refinement request.

        action: Requested refinement action.

        scope: Structured domain targeted by the request.

        target: Specific target identified by the request.

        instruction: User's requested refinement instruction.

        reason: Optional reason supplied with the request.

        preserve: Information explicitly protected from modification.

    The plan records intent for downstream processing. It does not itself

    perform any modification.

    """

    request_id: str

    action: RefinementAction

    scope: RefinementScope

    target: str

    instruction: str

    reason: str | None

    preserve: tuple[str, ...]

    @classmethod

    def from_request(

        cls,

        request: RefinementRequest,

    ) -> RefinementPlan:

        """Create a refinement plan from a validated request.

        Args:

            request: Structured refinement request.

        Returns:

            Immutable refinement plan.

        Raises:

            TypeError: If request is not a RefinementRequest.

        """

        if not isinstance(request, RefinementRequest):

            raise TypeError(

                "request must be a RefinementRequest"

            )

        return cls(

            request_id=request.request_id,

            action=request.action,

            scope=request.scope,

            target=request.target,

            instruction=request.instruction,

            reason=request.reason,

            preserve=request.preserve,

        )

class RefinementEngine:

    """Create explicit refinement plans from user requests."""

    def create_plan(

        self,

        request: RefinementRequest,

    ) -> RefinementPlan:

        """Create a refinement plan without modifying visual state.

        Args:

            request: Structured refinement request.

        Returns:

            Immutable RefinementPlan.

        Raises:

            TypeError: If request is not a RefinementRequest.

        """

        return RefinementPlan.from_request(request)