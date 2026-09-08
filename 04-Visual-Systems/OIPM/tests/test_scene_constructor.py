"""Tests for the OIPM Scene Construction Engine."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.scene.scene_constructor import (

    SceneConstructionResult,

    SceneConstructor,

)

def test_scene_constructor_returns_result() -> None:

    """Scene construction should return a structured result."""

    intent = VisualIntent()

    result = SceneConstructor().construct(intent)

    assert isinstance(result, SceneConstructionResult)

    assert result.visual_intent is intent

    assert result.scene is intent.scene

def test_scene_constructor_applies_explicit_scene_data() -> None:

    """Explicit scene information should be preserved exactly."""

    intent = VisualIntent()

    result = SceneConstructor().construct(

        intent,

        location="an ancient ruined temple",

        time="midnight",

        weather="heavy rain",

        narrative_context="The aftermath of a brutal battle.",

    )

    scene = result.scene

    assert scene.location == "an ancient ruined temple"

    assert scene.time == "midnight"

    assert scene.weather == "heavy rain"

    assert scene.narrative_context == "The aftermath of a brutal battle."

    assert result.warnings == ()

def test_scene_constructor_preserves_existing_scene_data() -> None:

    """Existing scene information should not be silently overwritten."""

    intent = VisualIntent()

    intent.scene.location = "a ruined castle"

    result = SceneConstructor().construct(

        intent,

        location="an ancient temple",

    )

    assert intent.scene.location == "a ruined castle"

    assert (

        "Existing scene location conflicts with supplied location; "

        "existing value was preserved."

        in result.warnings

    )

def test_scene_constructor_applies_missing_fields() -> None:

    """Explicit values should populate previously unspecified fields."""

    intent = VisualIntent()

    intent.scene.location = "a ruined castle"

    result = SceneConstructor().construct(

        intent,

        location="a ruined castle",

        weather="heavy rain",

        time="night",

    )

    assert result.scene.location == "a ruined castle"

    assert result.scene.weather == "heavy rain"

    assert result.scene.time == "night"

    assert result.warnings == ()

def test_scene_constructor_handles_multiple_conflicts() -> None:

    """Multiple conflicting fields should produce independent warnings."""

    intent = VisualIntent(

        scene={

            "location": "a forest",

            "time": "dawn",

            "weather": "clear skies",

            "narrative_context": "A peaceful morning.",

        }

    )

    result = SceneConstructor().construct(

        intent,

        location="a battlefield",

        time="midnight",

        weather="storm",

        narrative_context="The aftermath of war.",

    )

    assert result.scene.location == "a forest"

    assert result.scene.time == "dawn"

    assert result.scene.weather == "clear skies"

    assert result.scene.narrative_context == "A peaceful morning."

    assert len(result.warnings) == 4

def test_scene_constructor_does_not_modify_unspecified_scene_data() -> None:

    """Unspecified scene fields should remain unchanged."""

    intent = VisualIntent()

    result = SceneConstructor().construct(

        intent,

        location="an ancient ruin",

    )

    assert result.scene.location == "an ancient ruin"

    assert result.scene.time is None

    assert result.scene.weather is None

    assert result.scene.narrative_context is None

    assert result.scene.structural_elements == []

    assert result.scene.surface_properties == []

    assert result.scene.environmental_conditions == []

    assert result.scene.supporting_elements == []

    assert result.scene.visual_story_cues == []

def test_scene_constructor_does_not_invent_environmental_details() -> None:

    """The constructor should not create unspecified environmental data."""

    intent = VisualIntent()

    result = SceneConstructor().construct(

        intent,

        location="an ancient ruin",

    )

    scene = result.scene

    assert scene.location == "an ancient ruin"

    assert scene.structural_elements == []

    assert scene.surface_properties == []

    assert scene.environmental_conditions == []

    assert scene.supporting_elements == []

    assert scene.visual_story_cues == []

    assert result.warnings == ()

def test_scene_constructor_rejects_non_visual_intent_input() -> None:

    """The constructor should reject objects of the wrong type."""

    with pytest.raises(TypeError):

        SceneConstructor().construct(

            "not a visual intent",  # type: ignore[arg-type]

        )

def test_scene_constructor_preserves_visual_intent_identity() -> None:

    """Scene construction should operate on the supplied VisualIntent."""

    intent = VisualIntent()

    result = SceneConstructor().construct(

        intent,

        location="a moonlit forest",

    )

    assert result.visual_intent is intent

    assert result.visual_intent.scene is result.scene