"""Controlled state-application boundary for the OIPM Iterative Refinement System.

The Refinement Applier is the controlled mutation boundary of IRS.

It applies only explicitly structured changes that have already been

determined by upstream OIPM reasoning. It does not interpret natural

language, invent values, resolve conflicts, modify canon, or silently

override protected information.

The original VisualIntent is never modified in place. Application produces

a new VisualIntent state and a corresponding RefinementResult.

"""

from __future__ import annotations

from dataclasses import dataclass

from typing import Any

from oipm.models import VisualIntent

from oipm.refinement.refinement_result import (

    RefinementChange,

    RefinementResult,

    RefinementStatus,

)

@dataclass(frozen=True)

class RefinementApplication:

    """Immutable result of applying a structured refinement."""

    visual_intent: VisualIntent

    result: RefinementResult

class RefinementApplier:

    """Apply explicitly structured refinements to VisualIntent."""

    def apply(

        self,

        visual_intent: VisualIntent,

        changes: tuple[RefinementChange, ...],

        *,

        request_id: str,

        preserve: tuple[str, ...] = (),

    ) -> RefinementApplication:

        """Apply explicitly structured changes to a copied VisualIntent.

        Args:

            visual_intent: Current structured visual intent.

            changes: Explicitly structured changes to apply.

            request_id: Identifier of the originating refinement request.

            preserve: Information explicitly protected from modification.

        Returns:

            RefinementApplication containing the new VisualIntent and

            an immutable RefinementResult.

        Raises:

            TypeError: If visual_intent is not a VisualIntent.

            ValueError: If a requested field cannot be safely applied.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent"

            )

        if not request_id.strip():

            raise ValueError(

                "request_id must not be empty"

            )

        updated_intent = visual_intent.model_copy(deep=True)

        applied_changes: list[RefinementChange] = []

        warnings: list[str] = []

        unresolved: list[str] = []

        for change in changes:

            try:

                self._apply_change(

                    updated_intent,

                    change,

                )

            except (AttributeError, KeyError, TypeError, ValueError) as exc:

                unresolved.append(

                    f"Could not apply change to "

                    f"{change.target}.{change.field}: {exc}"

                )

                continue

            applied_changes.append(change)

        if unresolved:

            status = (

                RefinementStatus.PARTIAL

                if applied_changes

                else RefinementStatus.REJECTED

            )

        elif applied_changes:

            status = RefinementStatus.APPLIED

        else:

            status = RefinementStatus.NO_CHANGE

        result = RefinementResult(

            request_id=request_id,

            status=status,

            changes=tuple(applied_changes),

            preserved=preserve,

            warnings=tuple(warnings),

            unresolved=tuple(unresolved),

        )

        return RefinementApplication(

            visual_intent=updated_intent,

            result=result,

        )

    @staticmethod

    def _apply_change(

        visual_intent: VisualIntent,

        change: RefinementChange,

    ) -> None:

        """Apply one explicitly structured change.

        Only direct top-level VisualIntent fields are currently eligible.

        Nested or dynamically interpreted targets are rejected until their

        application semantics are explicitly defined.

        """

        if not isinstance(change, RefinementChange):

            raise TypeError(

                "changes must contain RefinementChange instances"

            )

        if not hasattr(visual_intent, change.field):

            raise AttributeError(

                f"VisualIntent has no field '{change.field}'"

            )

        if change.target not in {

            "visual_intent",

            "global",

        }:

            raise ValueError(

                "Only global VisualIntent changes are supported "

                "by the initial application boundary"

            )

        setattr(

            visual_intent,

            change.field,

            change.new_value,

        )