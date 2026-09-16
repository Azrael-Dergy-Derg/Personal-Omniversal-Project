"""Tests for the OIPM Iterative Refinement System result models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from oipm.refinement.refinement_result import (

    RefinementChange,

    RefinementResult,

    RefinementStatus,

)

def make_change(

    *,

    target: str = "azrael",

    field: str = "armor.color",

    previous_value: object | None = "black",

    new_value: object | None = "dark charcoal",

    reason: str | None = None,

) -> RefinementChange:

    """Create a representative refinement change."""

    return RefinementChange(

        target=target,

        field=field,

        previous_value=previous_value,

        new_value=new_value,

        reason=reason,

    )

def make_result(

    *,

    request_id: str = "request-001",

    status: RefinementStatus = RefinementStatus.PROPOSED,

    changes: tuple[RefinementChange, ...] = (),

    preserved: tuple[str, ...] = (),

    warnings: tuple[str, ...] = (),

    unresolved: tuple[str, ...] = (),

) -> RefinementResult:

    """Create a representative refinement result."""

    return RefinementResult(

        request_id=request_id,

        status=status,

        changes=changes,

        preserved=preserved,

        warnings=warnings,

        unresolved=unresolved,

    )

def test_refinement_status_values() -> None:

    assert RefinementStatus.PROPOSED.value == "proposed"

    assert RefinementStatus.APPLIED.value == "applied"

    assert RefinementStatus.PARTIAL.value == "partial"

    assert RefinementStatus.REJECTED.value == "rejected"

    assert RefinementStatus.NO_CHANGE.value == "no_change"

def test_change_stores_required_fields() -> None:

    change = make_change()

    assert change.target == "azrael"

    assert change.field == "armor.color"

    assert change.previous_value == "black"

    assert change.new_value == "dark charcoal"

def test_change_stores_optional_reason() -> None:

    change = make_change(

        reason="Improve contrast against the background.",

    )

    assert change.reason == (

        "Improve contrast against the background."

    )

def test_change_defaults_reason_to_none() -> None:

    change = make_change()

    assert change.reason is None

def test_change_rejects_empty_target() -> None:

    with pytest.raises(ValueError):

        make_change(target="")

def test_change_rejects_whitespace_target() -> None:

    with pytest.raises(ValueError):

        make_change(target="   ")

def test_change_rejects_empty_field() -> None:

    with pytest.raises(ValueError):

        make_change(field="")

def test_change_rejects_whitespace_field() -> None:

    with pytest.raises(ValueError):

        make_change(field="   ")

def test_change_rejects_empty_reason() -> None:

    with pytest.raises(ValueError):

        make_change(reason="")

def test_change_rejects_whitespace_reason() -> None:

    with pytest.raises(ValueError):

        make_change(reason="   ")

def test_change_allows_none_values() -> None:

    change = make_change(

        previous_value=None,

        new_value=None,

    )

    assert change.previous_value is None

    assert change.new_value is None

def test_result_stores_required_fields() -> None:

    result = make_result()

    assert result.request_id == "request-001"

    assert result.status is RefinementStatus.PROPOSED

def test_result_stores_changes() -> None:

    change = make_change()

    result = make_result(

        changes=(change,),

    )

    assert result.changes == (change,)

def test_result_stores_preserved_information() -> None:

    result = make_result(

        preserved=(

            "black scales",

            "purple underbelly",

        ),

    )

    assert result.preserved == (

        "black scales",

        "purple underbelly",

    )

def test_result_stores_warnings() -> None:

    result = make_result(

        warnings=(

            "Requested change conflicts with an existing constraint.",

        ),

    )

    assert result.warnings == (

        "Requested change conflicts with an existing constraint.",

    )

def test_result_stores_unresolved_issues() -> None:

    result = make_result(

        unresolved=(

            "User intent is ambiguous.",

        ),

    )

    assert result.unresolved == (

        "User intent is ambiguous.",

    )

def test_result_defaults_collections_to_empty_tuples() -> None:

    result = make_result()

    assert result.changes == ()

    assert result.preserved == ()

    assert result.warnings == ()

    assert result.unresolved == ()

def test_result_rejects_empty_request_id() -> None:

    with pytest.raises(ValueError):

        make_result(request_id="")

def test_result_rejects_whitespace_request_id() -> None:

    with pytest.raises(ValueError):

        make_result(request_id="   ")

def test_result_rejects_empty_preserved_entry() -> None:

    with pytest.raises(ValueError):

        make_result(

            preserved=("black scales", ""),

        )

def test_result_rejects_whitespace_preserved_entry() -> None:

    with pytest.raises(ValueError):

        make_result(

            preserved=("black scales", "   "),

        )

def test_result_rejects_empty_warning_entry() -> None:

    with pytest.raises(ValueError):

        make_result(

            warnings=("warning", ""),

        )

def test_result_rejects_whitespace_warning_entry() -> None:

    with pytest.raises(ValueError):

        make_result(

            warnings=("warning", "   "),

        )

def test_result_rejects_empty_unresolved_entry() -> None:

    with pytest.raises(ValueError):

        make_result(

            unresolved=("issue", ""),

        )

def test_result_rejects_whitespace_unresolved_entry() -> None:

    with pytest.raises(ValueError):

        make_result(

            unresolved=("issue", "   "),

        )

@pytest.mark.parametrize(

    "status",

    list(RefinementStatus),

)

def test_result_accepts_each_status(

    status: RefinementStatus,

) -> None:

    result = make_result(status=status)

    assert result.status is status

def test_change_is_immutable() -> None:

    change = make_change()

    with pytest.raises(FrozenInstanceError):

        change.target = "scene"  # type: ignore[misc]

def test_result_is_immutable() -> None:

    result = make_result()

    with pytest.raises(FrozenInstanceError):

        result.request_id = "changed"  # type: ignore[misc]

def test_change_count() -> None:

    changes = (

        make_change(field="armor.color"),

        make_change(field="armor.texture"),

    )

    result = make_result(

        changes=changes,

    )

    assert result.change_count == 2

def test_warning_count() -> None:

    result = make_result(

        warnings=(

            "warning one",

            "warning two",

        ),

    )

    assert result.warning_count == 2

def test_unresolved_count() -> None:

    result = make_result(

        unresolved=(

            "issue one",

            "issue two",

        ),

    )

    assert result.unresolved_count == 2

def test_has_changes() -> None:

    result = make_result(

        changes=(make_change(),),

    )

    assert result.has_changes is True

def test_has_no_changes() -> None:

    result = make_result()

    assert result.has_changes is False

def test_has_warnings() -> None:

    result = make_result(

        warnings=("warning",),

    )

    assert result.has_warnings is True

def test_has_no_warnings() -> None:

    result = make_result()

    assert result.has_warnings is False

def test_has_unresolved() -> None:

    result = make_result(

        unresolved=("issue",),

    )

    assert result.has_unresolved is True

def test_has_no_unresolved() -> None:

    result = make_result()

    assert result.has_unresolved is False