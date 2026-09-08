"""Tests for the OIPM Composition and Camera Engine."""

from __future__ import annotations

import pytest

from oipm.composition.composition_engine import (

    CompositionEngine,

    CompositionResult,

)

from oipm.models import VisualIntent

def test_composition_engine_returns_result() -> None:

    """Composition construction should return a structured result."""

    intent = VisualIntent()

    result = CompositionEngine().construct(intent)

    assert isinstance(result, CompositionResult)

    assert result.visual_intent is intent

    assert result.composition is intent.composition

def test_composition_engine_applies_explicit_composition_data() -> None:

    """Explicit composition information should be preserved exactly."""

    intent = VisualIntent()

    result = CompositionEngine().construct(

        intent,

        framing="medium shot",

        camera_angle="low angle",

        camera_distance="close",

        lens="85mm",

        perspective="shallow perspective",

        depth_of_field="shallow depth of field",

    )

    composition = result.composition

    assert composition.framing == "medium shot"

    assert composition.camera_angle == "low angle"

    assert composition.camera_distance == "close"

    assert composition.lens == "85mm"

    assert composition.perspective == "shallow perspective"

    assert composition.depth_of_field == "shallow depth of field"

    assert result.warnings == ()

def test_composition_engine_preserves_existing_values() -> None:

    """Existing composition information should not be silently overwritten."""

    intent = VisualIntent()

    intent.composition.framing = "wide shot"

    result = CompositionEngine().construct(

        intent,

        framing="close-up",

    )

    assert intent.composition.framing == "wide shot"

    assert (

        "Existing composition framing conflicts with supplied framing; "

        "existing value was preserved."

        in result.warnings

    )

def test_composition_engine_applies_missing_fields() -> None:

    """Explicit values should populate previously unspecified fields."""

    intent = VisualIntent()

    intent.composition.framing = "wide shot"

    result = CompositionEngine().construct(

        intent,

        framing="wide shot",

        camera_angle="high angle",

        lens="35mm",

    )

    assert result.composition.framing == "wide shot"

    assert result.composition.camera_angle == "high angle"

    assert result.composition.lens == "35mm"

    assert result.warnings == ()

def test_composition_engine_handles_multiple_conflicts() -> None:

    """Multiple conflicting fields should produce independent warnings."""

    intent = VisualIntent(

        composition={

            "framing": "wide shot",

            "camera_angle": "eye level",

            "camera_distance": "medium",

            "lens": "50mm",

        }

    )

    result = CompositionEngine().construct(

        intent,

        framing="close-up",

        camera_angle="low angle",

        camera_distance="close",

        lens="85mm",

    )

    assert result.composition.framing == "wide shot"

    assert result.composition.camera_angle == "eye level"

    assert result.composition.camera_distance == "medium"

    assert result.composition.lens == "50mm"

    assert len(result.warnings) == 4

def test_composition_engine_does_not_modify_unspecified_values() -> None:

    """Unspecified composition fields should remain unchanged."""

    intent = VisualIntent()

    result = CompositionEngine().construct(

        intent,

        framing="medium shot",

    )

    composition = result.composition

    assert composition.framing == "medium shot"

    assert composition.camera_angle is None

    assert composition.camera_distance is None

    assert composition.lens is None

    assert composition.perspective is None

    assert composition.depth_of_field is None

def test_composition_engine_does_not_invent_camera_information() -> None:

    """The engine should not create unspecified camera information."""

    intent = VisualIntent()

    result = CompositionEngine().construct(intent)

    composition = result.composition

    assert composition.framing is None

    assert composition.camera_angle is None

    assert composition.camera_distance is None

    assert composition.lens is None

    assert composition.perspective is None

    assert composition.depth_of_field is None

    assert result.warnings == ()

def test_composition_engine_rejects_non_visual_intent_input() -> None:

    """The engine should reject objects of the wrong type."""

    with pytest.raises(TypeError):

        CompositionEngine().construct(

            "not a visual intent",  # type: ignore[arg-type]

        )

def test_composition_engine_preserves_visual_intent_identity() -> None:

    """Composition construction should operate on the supplied VisualIntent."""

    intent = VisualIntent()

    result = CompositionEngine().construct(

        intent,

        framing="medium shot",

    )

    assert result.visual_intent is intent

    assert result.visual_intent.composition is result.composition