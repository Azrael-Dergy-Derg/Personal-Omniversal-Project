"""High-level orchestration boundary for the OIPM Iterative Refinement System.

IRS coordinates refinement requests, planning, evaluation, and controlled

application of explicitly structured changes.

The orchestration layer does not:

- interpret natural-language changes into arbitrary field mutations,

- modify canon,

- modify references,

- silently resolve conflicts,

- invent missing visual information,

- or mutate the caller's original VisualIntent in place.

The evaluator remains responsible for determining whether a requested

refinement can be evaluated. The applier remains the only component allowed

to produce a changed VisualIntent state.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import VisualIntent

from oipm.refinement.refinement_applier import (

    RefinementApplier,

    RefinementApplication,

)

from oipm.refinement.refinement_engine import (

    RefinementEngine,

    RefinementPlan,

)

from oipm.refinement.refinement_evaluator import RefinementEvaluator

from oipm.refinement.refinement_request import RefinementRequest

from oipm.refinement.refinement_result import (

    RefinementChange,

    RefinementResult,

)

@dataclass(frozen=True)

class RefinementExecution:

    """Complete result of one IRS refinement execution.

    Attributes:

        plan: Structured refinement plan.

        evaluation: Result of evaluating the requested refinement.

        application: Optional application result when explicit changes were

            supplied and application was attempted.

    The original VisualIntent supplied to the system is never mutated.

    """

    plan: RefinementPlan

    evaluation: RefinementResult

    application: RefinementApplication | None = None

    @property

    def visual_intent(self) -> VisualIntent | None:

        """Return the refined VisualIntent when application occurred."""

        if self.application is None:

            return None

        return self.application.visual_intent

class RefinementSystem:

    """Coordinate the OIPM Iterative Refinement System."""

    def __init__(

        self,

        engine: RefinementEngine | None = None,

        evaluator: RefinementEvaluator | None = None,

        applier: RefinementApplier | None = None,

    ) -> None:

        """Initialize the IRS orchestration boundary.

        Args:

            engine: Optional refinement planning engine.

            evaluator: Optional refinement evaluator.

            applier: Optional controlled refinement applier.

        Raises:

            TypeError: If a supplied component has the wrong type.

        """

        if engine is not None and not isinstance(

            engine,

            RefinementEngine,

        ):

            raise TypeError(

                "engine must be a RefinementEngine"

            )

        if evaluator is not None and not isinstance(

            evaluator,

            RefinementEvaluator,

        ):

            raise TypeError(

                "evaluator must be a RefinementEvaluator"

            )

        if applier is not None and not isinstance(

            applier,

            RefinementApplier,

        ):

            raise TypeError(

                "applier must be a RefinementApplier"

            )

        self.engine = engine or RefinementEngine()

        self.evaluator = evaluator or RefinementEvaluator(

            engine=self.engine,

        )

        self.applier = applier or RefinementApplier()

    def create_plan(

        self,

        request: RefinementRequest,

    ) -> RefinementPlan:

        """Create a structured refinement plan."""

        return self.engine.create_plan(request)

    def evaluate(

        self,

        request: RefinementRequest,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a refinement without applying changes."""

        return self.evaluator.evaluate(

            request,

            visual_intent,

        )

    def apply(

        self,

        visual_intent: VisualIntent,

        changes: tuple[RefinementChange, ...],

        *,

        request_id: str,

        preserve: tuple[str, ...] = (),

    ) -> RefinementApplication:

        """Apply explicitly structured changes.

        This method delegates directly to the controlled application

        boundary. It does not reinterpret the changes.

        """

        return self.applier.apply(

            visual_intent,

            changes,

            request_id=request_id,

            preserve=preserve,

        )

    def execute(

        self,

        request: RefinementRequest,

        visual_intent: VisualIntent,

        *,

        changes: tuple[RefinementChange, ...] = (),

        apply_changes: bool = False,

    ) -> RefinementExecution:

        """Execute the structured IRS workflow.

        By default, execution performs planning and evaluation only.

        Application occurs only when:

        - explicit structured changes are supplied, and

        - ``apply_changes`` is explicitly True.

        This prevents evaluation from implicitly becoming mutation.

        Args:

            request: Structured refinement request.

            visual_intent: Current VisualIntent.

            changes: Explicitly structured changes, if application is

                requested.

            apply_changes: Explicit authorization to apply those changes.

        Returns:

            Complete immutable RefinementExecution.

        Raises:

            TypeError: If request or visual_intent has the wrong type.

            ValueError: If application is requested without changes.

        """

        plan = self.engine.create_plan(request)

        evaluation = self.evaluator.evaluate(

            request,

            visual_intent,

        )

        if not apply_changes:

            return RefinementExecution(

                plan=plan,

                evaluation=evaluation,

            )

        if not changes:

            raise ValueError(

                "changes must be provided when apply_changes is True"

            )

        application = self.applier.apply(

            visual_intent,

            changes,

            request_id=request.request_id,

            preserve=request.preserve,

        )

        return RefinementExecution(

            plan=plan,

            evaluation=evaluation,

            application=application,

        )