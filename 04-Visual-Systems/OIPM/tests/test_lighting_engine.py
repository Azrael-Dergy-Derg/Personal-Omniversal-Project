"""Tests for the OIPM Lighting and Atmosphere Engine."""

import pytest

from oipm.lighting import LightingEngine, LightingResult

from oipm.models import VisualIntent

def test_construct_returns_lighting_result() -> None:

    """The engine should return a structured lighting result."""

    visual_intent = VisualIntent()

    engine = LightingEngine()

    result = engine.construct(visual_intent)

    assert isinstance(result, LightingResult)

def test_construct_preserves_visual_intent_identity() -> None:

    """The result should reference the original VisualIntent."""

    visual_intent = VisualIntent()

    engine = LightingEngine()

    result = engine.construct(visual_intent)

    assert result.visual_intent is visual_intent

def test_explicit_lighting_values_are_applied() -> None:

    """Explicit lighting information should be stored."""

    visual_intent = VisualIntent()

    engine = LightingEngine()

    result = engine.construct(

        visual_intent,

        light_source="moonlight",

        direction="from camera left",

        intensity="low",

        color_temperature="cool",

        contrast="high",

        atmospheric_effects="light mist",

        volumetric_effects="subtle",

        environmental_interaction="light catches wet surfaces",

    )

    assert result.lighting.light_source == "moonlight"

    assert result.lighting.direction == "from camera left"

    assert result.lighting.intensity == "low"

    assert result.lighting.color_temperature == "cool"

    assert result.lighting.contrast == "high"

    assert result.lighting.atmospheric_effects == "light mist"

    assert result.lighting.volumetric_effects == "subtle"

    assert (

        result.lighting.environmental_interaction

        == "light catches wet surfaces"

    )

def test_existing_lighting_values_are_preserved_on_conflict() -> None:

    """Existing lighting information should not be silently overwritten."""

    visual_intent = VisualIntent()

    visual_intent.lighting.light_source = "sunlight"

    engine = LightingEngine()

    result = engine.construct(

        visual_intent,

        light_source="moonlight",

    )

    assert result.lighting.light_source == "sunlight"

    assert len(result.warnings) == 1

    assert "light_source" in result.warnings[0]

def test_missing_lighting_values_are_applied_without_warning() -> None:

    """Explicit values should fill previously unspecified fields."""

    visual_intent = VisualIntent()

    engine = LightingEngine()

    result = engine.construct(

        visual_intent,

        intensity="moderate",

        contrast="soft",

    )

    assert result.lighting.intensity == "moderate"

    assert result.lighting.contrast == "soft"

    assert result.warnings == ()

def test_multiple_conflicts_are_reported() -> None:

    """Multiple conflicting fields should produce multiple warnings."""

    visual_intent = VisualIntent()

    visual_intent.lighting.light_source = "sunlight"

    visual_intent.lighting.direction = "from above"

    engine = LightingEngine()

    result = engine.construct(

        visual_intent,

        light_source="moonlight",

        direction="from below",

    )

    assert result.lighting.light_source == "sunlight"

    assert result.lighting.direction == "from above"

    assert len(result.warnings) == 2

def test_unspecified_lighting_values_remain_unchanged() -> None:

    """The engine should not invent unspecified lighting information."""

    visual_intent = VisualIntent()

    engine = LightingEngine()

    result = engine.construct(visual_intent)

    assert result.lighting.light_source is None

    assert result.lighting.direction is None

    assert result.lighting.intensity is None

    assert result.lighting.color_temperature is None

    assert result.lighting.contrast is None

    assert result.lighting.atmospheric_effects is None

    assert result.lighting.volumetric_effects is None

    assert result.lighting.environmental_interaction is None

def test_engine_does_not_invent_lighting() -> None:

    """A blank VisualIntent should remain visually unspecified."""

    visual_intent = VisualIntent()

    engine = LightingEngine()

    result = engine.construct(visual_intent)

    lighting = result.lighting

    assert all(

        getattr(lighting, field_name) is None

        for field_name in (

            "light_source",

            "direction",

            "intensity",

            "color_temperature",

            "contrast",

            "atmospheric_effects",

            "volumetric_effects",

            "environmental_interaction",

        )

    )

def test_wrong_input_type_is_rejected() -> None:

    """The engine should reject objects that are not VisualIntent."""

    engine = LightingEngine()

    with pytest.raises(TypeError):

        engine.construct("not a visual intent")  # type: ignore[arg-type]