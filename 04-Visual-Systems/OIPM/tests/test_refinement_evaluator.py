"""Tests for the OIPM Iterative Refinement System evaluator."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.refinement.refinement_engine import RefinementEngine

from oipm.refinement.refinement_evaluator import RefinementEvaluator

from oipm.refinement.refinement_request import (

    RefinementAction,

    RefinementRequest,

    RefinementScope,

)

from oipm.refinement.refinement_result import RefinementStatus

def make_visual_intent() -> VisualIntent:

    """Create a minimal valid VisualIntent."""

    return VisualIntent(

        user_input="Create a dark-fantasy character portrait.",

    )

def make_request(

    *,

    request_id: str = "request-001",

    action: RefinementAction = RefinementAction.MODIFY,

    scope: RefinementScope = RefinementScope.GLOBAL,

    target: str = "visual-intent",

    instruction: str = "Increase visual contrast.",

    reason: str | None = None,

    preserve: tuple[str, ...] = (),

) -> RefinementRequest:

    """Create a representative refinement request."""

    return RefinementRequest(

        request_id=request_id,

        action=action,

        scope=scope,

        target=target,

        instruction=instruction,

        reason=reason,

        preserve=preserve,

    )

def test_evaluator_creates_default_engine() -> None:

    evaluator = RefinementEvaluator()

    assert isinstance(evaluator.engine, RefinementEngine)

def test_evaluator_accepts_existing_engine() -> None:

    engine = RefinementEngine()

    evaluator = RefinementEvaluator(engine)

    assert evaluator.engine is engine

def test_evaluator_rejects_invalid_engine() -> None:

    with pytest.raises(TypeError):

        RefinementEvaluator("not-an-engine")  # type: ignore[arg-type]

def test_evaluator_rejects_invalid_request() -> None:

    evaluator = RefinementEvaluator()

    with pytest.raises(TypeError):

        evaluator.evaluate(

            "not-a-request",  # type: ignore[arg-type]

            make_visual_intent(),

        )

def test_evaluator_rejects_invalid_visual_intent() -> None:

    evaluator = RefinementEvaluator()

    with pytest.raises(TypeError):

        evaluator.evaluate(

            make_request(),

            "not-a-visual-intent",  # type: ignore[arg-type]

        )

def test_global_refinement_is_proposed() -> None:

    evaluator = RefinementEvaluator()

    result = evaluator.evaluate(

        make_request(),

        make_visual_intent(),

    )

    assert result.request_id == "request-001"

    assert result.status is RefinementStatus.PROPOSED

def test_global_refinement_preserves_explicit_preservation_requirements() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        preserve=(

            "black scales",

            "purple underbelly",

        ),

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.PROPOSED

    assert result.preserved == (

        "black scales",

        "purple underbelly",

    )

def test_subject_refinement_rejects_missing_subject() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.SUBJECT,

        target="missing-subject",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "Subject 'missing-subject' was not found.",

    )

def test_scene_refinement_rejects_missing_scene() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.SCENE,

        target="scene",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No scene is currently defined.",

    )

def test_composition_refinement_rejects_missing_composition() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.COMPOSITION,

        target="composition",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No composition is currently defined.",

    )

def test_lighting_refinement_rejects_missing_lighting() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.LIGHTING,

        target="lighting",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No lighting specification is currently defined.",

    )

def test_artistic_direction_refinement_rejects_missing_direction() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.ARTISTIC_DIRECTION,

        target="artistic-direction",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No artistic direction is currently defined.",

    )

def test_constraint_refinement_rejects_missing_constraints() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.CONSTRAINT,

        target="constraints",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No constraints are currently defined.",

    )

def test_reference_refinement_rejects_missing_references() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.REFERENCE,

        target="reference",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No references are currently defined.",

    )

def test_relationship_refinement_rejects_missing_relationships() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        scope=RefinementScope.RELATIONSHIP,

        target="relationship",

    )

    result = evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.unresolved == (

        "No relationships are currently defined.",

    )

def test_evaluator_does_not_mutate_visual_intent() -> None:

    evaluator = RefinementEvaluator()

    visual_intent = make_visual_intent()

    original_user_input = visual_intent.user_input

    original_metadata = dict(visual_intent.metadata)

    evaluator.evaluate(

        make_request(),

        visual_intent,

    )

    assert visual_intent.user_input == original_user_input

    assert visual_intent.metadata == original_metadata

def test_evaluator_does_not_mutate_request() -> None:

    evaluator = RefinementEvaluator()

    request = make_request(

        preserve=(

            "black scales",

            "purple underbelly",

        ),

    )

    original = request

    evaluator.evaluate(

        request,

        make_visual_intent(),

    )

    assert request == original

def test_evaluator_does_not_apply_changes() -> None:

    evaluator = RefinementEvaluator()

    visual_intent = make_visual_intent()

    result = evaluator.evaluate(

        make_request(

            instruction="Change the entire visual style.",

        ),

        visual_intent,

    )

    assert result.status is RefinementStatus.PROPOSED

    assert result.changes == ()

def test_evaluator_preserves_unresolved_state() -> None:

    evaluator = RefinementEvaluator()

    result = evaluator.evaluate(

        make_request(

            scope=RefinementScope.SUBJECT,

            target="unknown-character",

        ),

        make_visual_intent(),

    )

    assert result.status is RefinementStatus.REJECTED

    assert result.has_unresolved is True

    assert result.unresolved_count == 1