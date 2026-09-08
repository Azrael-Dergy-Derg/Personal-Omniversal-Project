"""Tests for the Artistic Direction and Rendering Engine."""

import pytest

from oipm.artistic_direction import (

    ArtisticDirectionEngine,

    ArtisticDirectionResult,

)

from oipm.models import VisualIntent

def test_artistic_direction_engine_returns_result() -> None:

    """ADRE should return a structured result."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    engine = ArtisticDirectionEngine()

    result = engine.construct(visual_intent)

    assert isinstance(result, ArtisticDirectionResult)

def test_artistic_direction_engine_preserves_visual_intent_identity() -> None:

    """ADRE should operate on the existing VisualIntent."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        medium="digital painting",

    )

    assert result.visual_intent is visual_intent

    assert result.artistic_direction is visual_intent.artistic_direction

def test_artistic_direction_engine_applies_explicit_values() -> None:

    """Explicit artistic direction should be applied."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        medium="digital painting",

        realism="semi-realistic",

        stylization="cinematic",

        linework="bold inked contours",

        shading="controlled cel-shading",

        texture="rich textured brushwork",

        color_treatment="deep blacks and purple accents",

        detail_distribution="high detail on the subject",

        edge_hierarchy="strong focal edges",

        surface_rendering="painterly rendering",

    )

    assert result.artistic_direction.medium == "digital painting"

    assert result.artistic_direction.realism == "semi-realistic"

    assert result.artistic_direction.stylization == "cinematic"

    assert result.artistic_direction.linework == "bold inked contours"

    assert result.artistic_direction.shading == "controlled cel-shading"

    assert result.artistic_direction.texture == "rich textured brushwork"

    assert (

        result.artistic_direction.color_treatment

        == "deep blacks and purple accents"

    )

    assert (

        result.artistic_direction.detail_distribution

        == "high detail on the subject"

    )

    assert (

        result.artistic_direction.edge_hierarchy

        == "strong focal edges"

    )

    assert (

        result.artistic_direction.surface_rendering

        == "painterly rendering"

    )

def test_artistic_direction_engine_applies_missing_fields() -> None:

    """Only explicitly supplied fields should be populated."""

    visual_intent = VisualIntent(metadata={"user_input": "A warrior."})

    visual_intent.artistic_direction.medium = "digital painting"

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        realism="semi-realistic",

    )

    assert result.artistic_direction.medium == "digital painting"

    assert result.artistic_direction.realism == "semi-realistic"

    assert result.artistic_direction.stylization is None

def test_artistic_direction_engine_preserves_conflicts() -> None:

    """Existing artistic direction should remain authoritative."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    visual_intent.artistic_direction.medium = "oil painting"

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        medium="digital painting",

    )

    assert result.artistic_direction.medium == "oil painting"

    assert len(result.warnings) == 1

    assert "medium" in result.warnings[0]

    assert "preserved" in result.warnings[0]

def test_artistic_direction_engine_preserves_multiple_conflicts() -> None:

    """Multiple conflicts should each generate a warning."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    visual_intent.artistic_direction.medium = "oil painting"

    visual_intent.artistic_direction.realism = "photorealistic"

    visual_intent.artistic_direction.shading = "soft shading"

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        medium="digital painting",

        realism="stylized",

        shading="cel-shading",

    )

    assert result.artistic_direction.medium == "oil painting"

    assert result.artistic_direction.realism == "photorealistic"

    assert result.artistic_direction.shading == "soft shading"

    assert len(result.warnings) == 3

def test_artistic_direction_engine_does_not_invent_values() -> None:

    """Unspecified artistic direction should remain unspecified."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    engine = ArtisticDirectionEngine()

    result = engine.construct(visual_intent)

    assert result.artistic_direction.medium is None

    assert result.artistic_direction.realism is None

    assert result.artistic_direction.stylization is None

    assert result.artistic_direction.linework is None

    assert result.artistic_direction.shading is None

    assert result.artistic_direction.texture is None

    assert result.artistic_direction.color_treatment is None

    assert result.artistic_direction.detail_distribution is None

    assert result.artistic_direction.edge_hierarchy is None

    assert result.artistic_direction.surface_rendering is None

def test_artistic_direction_engine_accepts_partial_direction() -> None:

    """ADRE should support partial artistic direction."""

    visual_intent = VisualIntent(metadata={"user_input": "A warrior."})

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        linework="bold ink",

        texture="painterly",

    )

    assert result.artistic_direction.linework == "bold ink"

    assert result.artistic_direction.texture == "painterly"

    assert result.artistic_direction.medium is None

    assert result.artistic_direction.realism is None

def test_artistic_direction_engine_rejects_invalid_input() -> None:

    """ADRE should reject objects that are not VisualIntent instances."""

    engine = ArtisticDirectionEngine()

    with pytest.raises(TypeError):

        engine.construct(None)  # type: ignore[arg-type]

def test_artistic_direction_engine_returns_no_warnings_without_conflicts() -> None:

    """A clean construction should not generate warnings."""

    visual_intent = VisualIntent(metadata={"user_input": "A dragon."})

    engine = ArtisticDirectionEngine()

    result = engine.construct(

        visual_intent,

        medium="digital painting",

        realism="semi-realistic",

    )

    assert result.warnings == ()