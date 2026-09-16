"""Integration tests for the complete OIPM Iterative Refinement System."""

from __future__ import annotations

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

            "project": "irs-integration",

        }

    )

def test_complete_evaluation_workflow() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = RefinementRequest(

        request_id="irs-integration-001",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Refine the overall visual presentation.",

        preserve=(

            "character identity",

            "established canon",

        ),

    )

    execution = system.execute(

        request,

        visual_intent,

    )

    assert execution.plan.request_id == request.request_id

    assert execution.evaluation.request_id == request.request_id

    assert execution.evaluation.status is RefinementStatus.PROPOSED

    assert execution.application is None

    assert execution.visual_intent is None

def test_complete_explicit_application_workflow() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = RefinementRequest(

        request_id="irs-integration-002",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Add an explicit project-state marker.",

    )

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=visual_intent.metadata,

        new_value={

            "project": "irs-integration",

            "refined": True,

        },

        reason="Explicitly authorized test change.",

    )

    execution = system.execute(

        request,

        visual_intent,

        changes=(change,),

        apply_changes=True,

    )

    assert execution.application is not None

    assert execution.visual_intent is not None

    assert execution.evaluation.status is RefinementStatus.PROPOSED

    assert execution.application.result.status is RefinementStatus.APPLIED

    assert execution.visual_intent.metadata["refined"] is True

    assert visual_intent.metadata == {

        "project": "irs-integration",

    }

def test_application_failure_does_not_corrupt_original_state() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    request = RefinementRequest(

        request_id="irs-integration-003",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Attempt an unsupported refinement.",

    )

    change = RefinementChange(

        target="unsupported-target",

        field="metadata",

        previous_value=None,

        new_value={

            "should_not_apply": True,

        },

    )

    execution = system.execute(

        request,

        visual_intent,

        changes=(change,),

        apply_changes=True,

    )

    assert execution.application is not None

    assert execution.application.result.status is RefinementStatus.REJECTED

    assert execution.application.result.has_unresolved is True

    assert visual_intent.metadata == {

        "project": "irs-integration",

    }

def test_preservation_requirements_survive_full_workflow() -> None:

    system = RefinementSystem()

    visual_intent = make_visual_intent()

    preserved = (

        "character identity",

        "species anatomy",

        "canon-established equipment",

    )

    request = RefinementRequest(

        request_id="irs-integration-004",

        action=RefinementAction.MODIFY,

        scope=RefinementScope.GLOBAL,

        target="visual_intent",

        instruction="Refine presentation while preserving established identity.",

        preserve=preserved,

    )

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=visual_intent.metadata,

        new_value={

            "project": "irs-integration",

            "refined": True,

        },

    )

    execution = system.execute(

        request,

        visual_intent,

        changes=(change,),

        apply_changes=True,

    )

    assert execution.evaluation.status is RefinementStatus.PROPOSED

    assert execution.application is not None

    assert execution.application.result.status is RefinementStatus.APPLIED

    assert execution.application.result.preserved == preserved