"""Integration tests for the OIPM Iterative Refinement System."""

from __future__ import annotations

from oipm.models import VisualIntent

from oipm.refinement import (

    RefinementAction,

    RefinementEngine,

    RefinementEvaluator,

    RefinementRequest,

    RefinementScope,

    RefinementStatus,

)

def test_refinement_request_to_plan() -> None:

    request = RefinementRequest(

        request_id="integration-001",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.SUBJECT,

        target="azrael",

        instruction="Adjust the visible armor detailing.",

        preserve=("species anatomy", "eye colors"),

    )

    engine = RefinementEngine()

    plan = engine.create_plan(request)

    assert plan.request_id == request.request_id

    assert plan.action is request.action

    assert plan.scope is request.scope

    assert plan.target == request.target

    assert plan.instruction == request.instruction

    assert plan.preserve == request.preserve

def test_refinement_plan_to_evaluation() -> None:

    visual_intent = VisualIntent(

        metadata={

            "project": "integration-test",

        }

    )

    request = RefinementRequest(

        request_id="integration-002",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Refine the overall visual presentation.",

    )

    evaluator = RefinementEvaluator()

    result = evaluator.evaluate(

        request,

        visual_intent,

    )

    assert result.request_id == request.request_id

    assert result.status is RefinementStatus.PROPOSED

    assert result.has_changes is False

def test_missing_subject_is_rejected() -> None:

    visual_intent = VisualIntent(

        metadata={

            "project": "integration-test",

        }

    )

    request = RefinementRequest(

        request_id="integration-003",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.SUBJECT,

        target="missing-subject",

        instruction="Change the subject's appearance.",

    )

    evaluator = RefinementEvaluator()

    result = evaluator.evaluate(

        request,

        visual_intent,

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.has_unresolved is True

    assert "missing-subject" in result.unresolved[0]

def test_refinement_preserves_explicit_protected_information() -> None:

    visual_intent = VisualIntent(

        metadata={

            "project": "integration-test",

        }

    )

    request = RefinementRequest(

        request_id="integration-004",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Refine the presentation.",

        preserve=(

            "character identity",

            "species anatomy",

            "established canon",

        ),

    )

    evaluator = RefinementEvaluator()

    result = evaluator.evaluate(

        request,

        visual_intent,

    )

    assert result.status is RefinementStatus.PROPOSED

    assert result.preserved == request.preserve