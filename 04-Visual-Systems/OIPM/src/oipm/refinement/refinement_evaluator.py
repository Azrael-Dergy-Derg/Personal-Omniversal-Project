"""Evaluation boundary for the OIPM Iterative Refinement System.

The refinement evaluator determines whether a structured refinement request

can be evaluated against the current VisualIntent.

It does not:

- mutate VisualIntent,

- modify canon,

- modify references,

- silently resolve conflicts,

- invent missing information,

- or assemble a replacement prompt.

Evaluation produces an explicit RefinementResult that downstream IRS

components can use to decide whether and how a state change should occur.

"""

from __future__ import annotations

from oipm.models import VisualIntent

from oipm.refinement.refinement_engine import (

    RefinementEngine,

    RefinementPlan,

)

from oipm.refinement.refinement_request import (

    RefinementRequest,

    RefinementScope,

)

from oipm.refinement.refinement_result import (

    RefinementResult,

    RefinementStatus,

)

class RefinementEvaluator:

    """Evaluate refinement requests without mutating visual state."""

    def __init__(

        self,

        engine: RefinementEngine | None = None,

    ) -> None:

        """Initialize the refinement evaluator.

        Args:

            engine: Optional refinement planning engine.

        Raises:

            TypeError: If engine is not a RefinementEngine.

        """

        if engine is not None and not isinstance(

            engine,

            RefinementEngine,

        ):

            raise TypeError(

                "engine must be a RefinementEngine"

            )

        self.engine = engine or RefinementEngine()

    def evaluate(

        self,

        request: RefinementRequest,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a refinement request against VisualIntent.

        The evaluator creates a refinement plan and then determines whether

        the requested target can be located in the current structured

        visual state.

        No state mutation occurs.

        Args:

            request: Structured refinement request.

            visual_intent: Current structured visual intent.

        Returns:

            Immutable RefinementResult.

        Raises:

            TypeError: If request or visual_intent has the wrong type.

        """

        if not isinstance(request, RefinementRequest):

            raise TypeError(

                "request must be a RefinementRequest"

            )

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent"

            )

        plan = self.engine.create_plan(request)

        return self._evaluate_plan(

            plan,

            visual_intent,

        )

    def _evaluate_plan(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate an existing refinement plan."""

        if plan.scope is RefinementScope.SUBJECT:

            return self._evaluate_subject(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.SCENE:

            return self._evaluate_scene(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.COMPOSITION:

            return self._evaluate_composition(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.LIGHTING:

            return self._evaluate_lighting(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.ARTISTIC_DIRECTION:

            return self._evaluate_artistic_direction(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.CONSTRAINT:

            return self._evaluate_constraint(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.REFERENCE:

            return self._evaluate_reference(

                plan,

                visual_intent,

            )

        if plan.scope is RefinementScope.RELATIONSHIP:

            return self._evaluate_relationship(

                plan,

                visual_intent,

            )

        return self._evaluate_global(

            plan,

            visual_intent,

        )

    def _evaluate_subject(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a subject-scoped refinement."""

        subject = next(

            (

                item

                for item in visual_intent.subjects

                if item.subject_id == plan.target

            ),

            None,

        )

        if subject is None:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    f"Subject '{plan.target}' was not found.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_scene(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a scene-scoped refinement."""

        if visual_intent.scene is None:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No scene is currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_composition(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a composition-scoped refinement."""

        if visual_intent.composition is None:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No composition is currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_lighting(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a lighting-scoped refinement."""

        if visual_intent.lighting is None:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No lighting specification is currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_artistic_direction(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate an artistic-direction refinement."""

        if visual_intent.artistic_direction is None:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No artistic direction is currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_constraint(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a constraint-scoped refinement."""

        if not visual_intent.constraints:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No constraints are currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_reference(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a reference-scoped refinement."""

        if not visual_intent.references:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No references are currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_relationship(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a relationship-scoped refinement."""

        if not visual_intent.relationships:

            return RefinementResult(

                request_id=plan.request_id,

                status=RefinementStatus.REJECTED,

                unresolved=(

                    "No relationships are currently defined.",

                ),

            )

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )

    def _evaluate_global(

        self,

        plan: RefinementPlan,

        visual_intent: VisualIntent,

    ) -> RefinementResult:

        """Evaluate a global refinement."""

        return RefinementResult(

            request_id=plan.request_id,

            status=RefinementStatus.PROPOSED,

            preserved=plan.preserve,

        )