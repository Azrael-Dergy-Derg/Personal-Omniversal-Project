"""Tests for the OIPM Iterative Refinement System request model."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

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

def test_refinement_action_values() -> None:

    assert RefinementAction.MODIFY.value == "modify"

    assert RefinementAction.ADD.value == "add"

    assert RefinementAction.REMOVE.value == "remove"

    assert RefinementAction.PRESERVE.value == "preserve"

    assert RefinementAction.RECONSIDER.value == "reconsider"

def test_refinement_scope_values() -> None:

    assert RefinementScope.SUBJECT.value == "subject"

    assert RefinementScope.SCENE.value == "scene"

    assert RefinementScope.COMPOSITION.value == "composition"

    assert RefinementScope.LIGHTING.value == "lighting"

    assert (

        RefinementScope.ARTISTIC_DIRECTION.value

        == "artistic_direction"

    )

    assert RefinementScope.CONSTRAINT.value == "constraint"

    assert RefinementScope.REFERENCE.value == "reference"

    assert RefinementScope.RELATIONSHIP.value == "relationship"

    assert RefinementScope.GLOBAL.value == "global"

def test_request_stores_required_fields() -> None:

    request = make_request()

    assert request.request_id == "request-001"

    assert request.action is RefinementAction.MODIFY

    assert request.scope is RefinementScope.SUBJECT

    assert request.target == "azrael"

    assert request.instruction == "Make the armor darker."

def test_request_stores_optional_reason() -> None:

    request = make_request(

        reason="The armor is visually blending into the background.",

    )

    assert request.reason == (

        "The armor is visually blending into the background."

    )

def test_request_defaults_reason_to_none() -> None:

    request = make_request()

    assert request.reason is None

def test_request_stores_preservation_requirements() -> None:

    request = make_request(

        preserve=(

            "black scales",

            "purple underbelly",

            "biological wings",

        ),

    )

    assert request.preserve == (

        "black scales",

        "purple underbelly",

        "biological wings",

    )

def test_request_defaults_preserve_to_empty_tuple() -> None:

    request = make_request()

    assert request.preserve == ()

def test_request_rejects_empty_request_id() -> None:

    with pytest.raises(ValueError):

        make_request(request_id="")

def test_request_rejects_whitespace_request_id() -> None:

    with pytest.raises(ValueError):

        make_request(request_id="   ")

def test_request_rejects_empty_target() -> None:

    with pytest.raises(ValueError):

        make_request(target="")

def test_request_rejects_whitespace_target() -> None:

    with pytest.raises(ValueError):

        make_request(target="   ")

def test_request_rejects_empty_instruction() -> None:

    with pytest.raises(ValueError):

        make_request(instruction="")

def test_request_rejects_whitespace_instruction() -> None:

    with pytest.raises(ValueError):

        make_request(instruction="   ")

def test_request_rejects_empty_reason() -> None:

    with pytest.raises(ValueError):

        make_request(reason="")

def test_request_rejects_whitespace_reason() -> None:

    with pytest.raises(ValueError):

        make_request(reason="   ")

def test_request_allows_none_reason() -> None:

    request = make_request(reason=None)

    assert request.reason is None

def test_request_rejects_empty_preserve_entry() -> None:

    with pytest.raises(ValueError):

        make_request(

            preserve=("black scales", ""),

        )

def test_request_rejects_whitespace_preserve_entry() -> None:

    with pytest.raises(ValueError):

        make_request(

            preserve=("black scales", "   "),

        )

@pytest.mark.parametrize(

    "action",

    list(RefinementAction),

)

def test_request_accepts_each_refinement_action(

    action: RefinementAction,

) -> None:

    request = make_request(action=action)

    assert request.action is action

@pytest.mark.parametrize(

    "scope",

    list(RefinementScope),

)

def test_request_accepts_each_refinement_scope(

    scope: RefinementScope,

) -> None:

    request = make_request(scope=scope)

    assert request.scope is scope

def test_request_is_immutable() -> None:

    request = make_request()

    with pytest.raises(FrozenInstanceError):

        request.target = "scene"  # type: ignore[misc]

def test_request_does_not_mutate_preserve_data() -> None:

    preserve = (

        "black scales",

        "purple underbelly",

    )

    request = make_request(

        preserve=preserve,

    )

    assert request.preserve == preserve

    assert isinstance(request.preserve, tuple)

def test_request_is_deterministic() -> None:

    first = make_request()

    second = make_request()

    assert first == second