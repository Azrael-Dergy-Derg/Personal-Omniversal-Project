"""Tests for the OIPM Iterative Refinement System orchestration layer."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.refinement import (

    RefinementAction,

    RefinementChange,

    RefinementRequest,

    RefinementScope,

    RefinementStatus,

    RefinementSystem,

)

def make_visual_intent() -> VisualIntent:

    return VisualIntent(

        metadata={

            "project": "refinement-system-test",

        }

    )

def make_global_request() -> RefinementRequest:

    return RefinementRequest(

        request_id="system-001",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Refine the overall visual presentation.",

        preserve=("character identity",),

    )

def test_system_creates_plan() -> None:

    system = RefinementSystem()

    request = make_global_request()

    plan = system.create_plan(request)

    assert plan.request_id == request.request_id

    assert plan.scope is request.scope

    assert plan.target == request.target

def test_system_evaluates_without_applying() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = make_global_request()

    result = system.evaluate(

        request,

        visual_intent,

    )

    assert result.status is RefinementStatus.PROPOSED

def test_system_execute_defaults_to_evaluation_only() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = make_global_request()

    execution = system.execute(

        request,

        visual_intent,

    )

    assert execution.application is None

    assert execution.visual_intent is None

    assert execution.evaluation.status is RefinementStatus.PROPOSED

def test_system_execute_applies_explicit_changes() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = make_global_request()

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=visual_intent.metadata,

        new_value={

            "project": "refinement-system-test",

            "refined": True,

        },

        reason="Explicit integration-test refinement.",

    )

    execution = system.execute(

        request,

        visual_intent,

        changes=(change,),

        apply_changes=True,

    )

    assert execution.application is not None

    assert execution.visual_intent is not None

    assert execution.visual_intent.metadata["refined"] is True

    assert execution.application.result.status is RefinementStatus.APPLIED

def test_system_does_not_mutate_original_visual_intent() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    original_metadata = dict(visual_intent.metadata)

    request = make_global_request()

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=visual_intent.metadata,

        new_value={

            "project": "refinement-system-test",

            "refined": True,

        },

    )

    execution = system.execute(

        request,

        visual_intent,

        changes=(change,),

        apply_changes=True,

    )

    assert execution.visual_intent is not visual_intent

    assert visual_intent.metadata == original_metadata

def test_system_requires_changes_for_explicit_application() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = make_global_request()

    with pytest.raises(ValueError):

        system.execute(

            request,

            visual_intent,

            apply_changes=True,

        )

def test_system_apply_delegates_to_applier() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=visual_intent.metadata,

        new_value={

            "project": "refinement-system-test",

            "delegated": True,

        },

    )

    application = system.apply(

        visual_intent,

        (change,),

        request_id="system-002",

    )

    assert application.result.status is RefinementStatus.APPLIED

    assert application.visual_intent.metadata["delegated"] is True