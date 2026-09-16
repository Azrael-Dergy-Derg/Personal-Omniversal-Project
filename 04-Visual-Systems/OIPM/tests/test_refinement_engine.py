"""Tests for the OIPM Iterative Refinement System planning engine."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from oipm.refinement.refinement_engine import (

    RefinementEngine,

    RefinementPlan,

)

from oipm.refinement.refinement_request import (

    RefinementAction,

    RefinementRequest,

    RefinementScope,

)

def make_request(

    *,

    request_id: str = "request-001",

    action: RefinementAction = RefinementAction.MODIFY,

    scope: RefinementScope = RefinementScope.SUBJECT,

    target: str = "azrael",

    instruction: str = "Make the armor darker.",

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

def test_plan_from_request_copies_request_data() -> None:

    request = make_request(

        reason="Improve visual separation.",

        preserve=(

            "black scales",

            "purple underbelly",

        ),

    )

    plan = RefinementPlan.from_request(request)

    assert plan.request_id == request.request_id

    assert plan.action is request.action

    assert plan.scope is request.scope

    assert plan.target == request.target

    assert plan.instruction == request.instruction

    assert plan.reason == request.reason

    assert plan.preserve == request.preserve

def test_plan_from_request_rejects_invalid_request() -> None:

    with pytest.raises(TypeError):

        RefinementPlan.from_request(

            "not-a-refinement-request",  # type: ignore[arg-type]

        )

def test_engine_creates_plan() -> None:

    engine = RefinementEngine()

    request = make_request()

    plan = engine.create_plan(request)

    assert isinstance(plan, RefinementPlan)

    assert plan.request_id == "request-001"

    assert plan.action is RefinementAction.MODIFY

    assert plan.scope is RefinementScope.SUBJECT

    assert plan.target == "azrael"

    assert plan.instruction == "Make the armor darker."

def test_engine_preserves_optional_request_data() -> None:

    engine = RefinementEngine()

    request = make_request(

        reason="Improve contrast.",

        preserve=(

            "black scales",

            "biological wings",

        ),

    )

    plan = engine.create_plan(request)

    assert plan.reason == "Improve contrast."

    assert plan.preserve == (

        "black scales",

        "biological wings",

    )

def test_engine_rejects_invalid_request() -> None:

    engine = RefinementEngine()

    with pytest.raises(TypeError):

        engine.create_plan(

            "not-a-refinement-request",  # type: ignore[arg-type]

        )

@pytest.mark.parametrize(

    "action",

    list(RefinementAction),

)

def test_engine_supports_each_refinement_action(

    action: RefinementAction,

) -> None:

    engine = RefinementEngine()

    request = make_request(action=action)

    plan = engine.create_plan(request)

    assert plan.action is action

@pytest.mark.parametrize(

    "scope",

    list(RefinementScope),

)

def test_engine_supports_each_refinement_scope(

    scope: RefinementScope,

) -> None:

    engine = RefinementEngine()

    request = make_request(scope=scope)

    plan = engine.create_plan(request)

    assert plan.scope is scope

def test_plan_is_immutable() -> None:

    request = make_request()

    plan = RefinementPlan.from_request(request)

    with pytest.raises(FrozenInstanceError):

        plan.target = "scene"  # type: ignore[misc]

def test_engine_does_not_modify_request() -> None:

    engine = RefinementEngine()

    request = make_request(

        reason="Improve readability.",

        preserve=(

            "black scales",

            "purple underbelly",

        ),

    )

    original = request

    engine.create_plan(request)

    assert request == original

def test_engine_does_not_resolve_refinement_request() -> None:

    engine = RefinementEngine()

    request = make_request(

        action=RefinementAction.RECONSIDER,

        scope=RefinementScope.REFERENCE,

        target="style-reference",

        instruction="Reconsider whether this reference should influence style.",

    )

    plan = engine.create_plan(request)

    assert plan.action is RefinementAction.RECONSIDER

    assert plan.scope is RefinementScope.REFERENCE

    assert plan.target == "style-reference"

    assert (

        plan.instruction

        == "Reconsider whether this reference should influence style."

    )

def test_plan_creation_is_deterministic() -> None:

    engine = RefinementEngine()

    request = make_request()

    first = engine.create_plan(request)

    second = engine.create_plan(request)

    assert first == second

def test_plan_from_request_and_engine_produce_equivalent_results() -> None:

    engine = RefinementEngine()

    request = make_request(

        reason="Preserve the established silhouette.",

        preserve=(

            "hood-up silhouette",

            "tail integration",

        ),

    )

    direct_plan = RefinementPlan.from_request(request)

    engine_plan = engine.create_plan(request)

    assert direct_plan == engine_plan