"""Tests for the OIPM Iterative Refinement System application boundary."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.refinement import (

    RefinementApplier,

    RefinementChange,

    RefinementStatus,

)

def make_visual_intent() -> VisualIntent:

    return VisualIntent(

        metadata={

            "project": "refinement-test",

        }

    )

def test_applier_returns_new_visual_intent() -> None:

    original = make_visual_intent()

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=original.metadata,

        new_value={

            "project": "refinement-test",

            "refined": True,

        },

        reason="Test refinement.",

    )

    applier = RefinementApplier()

    application = applier.apply(

        original,

        (change,),

        request_id="apply-001",

    )

    assert application.visual_intent is not original

    assert original.metadata == {

        "project": "refinement-test",

    }

def test_applier_applies_explicit_top_level_change() -> None:

    original = make_visual_intent()

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=original.metadata,

        new_value={

            "project": "refinement-test",

            "version": 2,

        },

    )

    application = RefinementApplier().apply(

        original,

        (change,),

        request_id="apply-002",

    )

    assert application.visual_intent.metadata == {

        "project": "refinement-test",

        "version": 2,

    }

    assert application.result.status is RefinementStatus.APPLIED

    assert application.result.change_count == 1

def test_applier_preserves_explicit_protected_information() -> None:

    original = make_visual_intent()

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=original.metadata,

        new_value={

            "project": "refinement-test",

            "refined": True,

        },

    )

    application = RefinementApplier().apply(

        original,

        (change,),

        request_id="apply-003",

        preserve=(

            "character identity",

            "species anatomy",

        ),

    )

    assert application.result.preserved == (

        "character identity",

        "species anatomy",

    )

def test_applier_rejects_non_global_target() -> None:

    original = make_visual_intent()

    change = RefinementChange(

        target="azrael",

        field="metadata",

        previous_value=original.metadata,

        new_value={

            "changed": True,

        },

    )

    application = RefinementApplier().apply(

        original,

        (change,),

        request_id="apply-004",

    )

    assert application.result.status is RefinementStatus.REJECTED

    assert application.result.has_unresolved is True

    assert application.result.change_count == 0

def test_applier_rejects_unknown_field() -> None:

    original = make_visual_intent()

    change = RefinementChange(

        target="global",

        field="does_not_exist",

        previous_value=None,

        new_value="invalid",

    )

    application = RefinementApplier().apply(

        original,

        (change,),

        request_id="apply-005",

    )

    assert application.result.status is RefinementStatus.REJECTED

    assert application.result.has_unresolved is True

    assert application.result.change_count == 0

def test_applier_reports_partial_application() -> None:

    original = make_visual_intent()

    valid_change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=original.metadata,

        new_value={

            "project": "refinement-test",

            "valid": True,

        },

    )

    invalid_change = RefinementChange(

        target="invalid-target",

        field="metadata",

        previous_value=None,

        new_value={

            "invalid": True,

        },

    )

    application = RefinementApplier().apply(

        original,

        (

            valid_change,

            invalid_change,

        ),

        request_id="apply-006",

    )

    assert application.result.status is RefinementStatus.PARTIAL

    assert application.result.change_count == 1

    assert application.result.unresolved_count == 1

def test_applier_rejects_invalid_visual_intent() -> None:

    change = RefinementChange(

        target="global",

        field="metadata",

        previous_value=None,

        new_value={},

    )

    with pytest.raises(TypeError):

        RefinementApplier().apply(

            object(),

            (change,),

            request_id="apply-007",

        )

def test_applier_rejects_empty_request_id() -> None:

    original = make_visual_intent()

    with pytest.raises(ValueError):

        RefinementApplier().apply(

            original,

            (),

            request_id="",

        )

def test_no_changes_produce_no_change_status() -> None:

    original = make_visual_intent()

    application = RefinementApplier().apply(

        original,

        (),

        request_id="apply-008",

    )

    assert application.result.status is RefinementStatus.NO_CHANGE

    assert application.result.change_count == 0