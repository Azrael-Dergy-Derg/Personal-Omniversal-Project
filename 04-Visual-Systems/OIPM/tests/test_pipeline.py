"""Tests for the OIPM processing pipeline."""

import pytest

from oipm.lighting import LightingEngine

from oipm.models import VisualIntent

from oipm.pipeline import OIPMPipeline, PipelineResult

def test_pipeline_returns_pipeline_result() -> None:

    """The pipeline should return a structured PipelineResult."""

    pipeline = OIPMPipeline()

    result = pipeline.process("A dragon standing in a ruined castle.")

    assert isinstance(result, PipelineResult)

def test_pipeline_preserves_input() -> None:

    """The pipeline should preserve the original user input."""

    user_input = "A dragon standing in a ruined castle."

    pipeline = OIPMPipeline()

    result = pipeline.process(user_input)

    assert result.visual_intent.metadata.user_input == user_input

def test_pipeline_preserves_project_and_scene_metadata() -> None:

    """Project and scene identifiers should reach VisualIntent metadata."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A warrior standing in a forest.",

        project_id="project-001",

        scene_id="scene-001",

    )

    assert result.visual_intent.metadata.project_id == "project-001"

    assert result.visual_intent.metadata.scene_id == "scene-001"

def test_pipeline_executes_subject_resolution() -> None:

    """Subject information should be processed through SCRE."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon standing in a ruined castle.",

        subject_identity="Azrael",

        subject_type="character",

        species="dragon",

    )

    assert result.subject_resolution is not None

    assert len(result.visual_intent.subjects) == 1

    assert result.visual_intent.subjects[0].identity == "Azrael"

    assert result.visual_intent.subjects[0].subject_type == "character"

    assert result.visual_intent.subjects[0].species == "dragon"

def test_pipeline_executes_scene_construction() -> None:

    """Explicit scene information should be processed through SCE."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A warrior standing in a forest.",

        location="ancient forest",

        time="night",

        weather="rain",

        narrative_context="The warrior is searching for a lost companion.",

    )

    assert result.scene_construction is not None

    assert result.visual_intent.scene.location == "ancient forest"

    assert result.visual_intent.scene.time == "night"

    assert result.visual_intent.scene.weather == "rain"

    assert (

        result.visual_intent.scene.narrative_context

        == "The warrior is searching for a lost companion."

    )

def test_pipeline_executes_composition_engine() -> None:

    """Explicit composition information should reach CCE."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon standing in a ruined castle.",

        framing="medium shot",

        camera_angle="low angle",

        camera_distance="close",

        lens="50mm",

        perspective="dramatic perspective",

        depth_of_field="shallow",

    )

    assert result.composition is not None

    assert result.visual_intent.composition.framing == "medium shot"

    assert result.visual_intent.composition.camera_angle == "low angle"

    assert result.visual_intent.composition.camera_distance == "close"

    assert result.visual_intent.composition.lens == "50mm"

    assert (

        result.visual_intent.composition.perspective

        == "dramatic perspective"

    )

    assert result.visual_intent.composition.depth_of_field == "shallow"

def test_pipeline_executes_lighting_engine() -> None:

    """Explicit lighting information should reach LAE."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon standing in a ruined castle.",

        light_source="moonlight",

        direction="from camera left",

        intensity="low",

        color_temperature="cool",

        contrast="high",

        atmospheric_effects="light mist",

        volumetric_effects="subtle",

        environmental_interaction="light catches wet stone",

    )

    assert result.lighting is not None

    assert result.visual_intent.lighting.light_source == "moonlight"

    assert result.visual_intent.lighting.direction == "from camera left"

    assert result.visual_intent.lighting.intensity == "low"

    assert result.visual_intent.lighting.color_temperature == "cool"

    assert result.visual_intent.lighting.contrast == "high"

    assert result.visual_intent.lighting.atmospheric_effects == "light mist"

    assert result.visual_intent.lighting.volumetric_effects == "subtle"

    assert (

        result.visual_intent.lighting.environmental_interaction

        == "light catches wet stone"

    )

def test_pipeline_exposes_lighting_result() -> None:

    """PipelineResult should expose the LAE result."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A warrior beneath moonlight.",

        light_source="moonlight",

        intensity="moderate",

    )

    assert result.lighting is not None

    assert result.lighting.visual_intent is result.visual_intent

    assert result.lighting.lighting is result.visual_intent.lighting

def test_pipeline_accepts_custom_lighting_engine() -> None:

    """The pipeline should support dependency injection for LAE."""

    class TrackingLightingEngine(LightingEngine):

        def __init__(self) -> None:

            self.called = False

        def construct(

            self,

            visual_intent: VisualIntent,

            *,

            light_source: str | None = None,

            direction: str | None = None,

            intensity: str | None = None,

            color_temperature: str | None = None,

            contrast: str | None = None,

            atmospheric_effects: str | None = None,

            volumetric_effects: str | None = None,

            environmental_interaction: str | None = None,

        ):

            self.called = True

            return super().construct(

                visual_intent,

                light_source=light_source,

                direction=direction,

                intensity=intensity,

                color_temperature=color_temperature,

                contrast=contrast,

                atmospheric_effects=atmospheric_effects,

                volumetric_effects=volumetric_effects,

                environmental_interaction=environmental_interaction,

            )

    lighting_engine = TrackingLightingEngine()

    pipeline = OIPMPipeline(

        lighting_engine=lighting_engine,

    )

    result = pipeline.process(

        "A warrior beneath moonlight.",

        light_source="moonlight",

    )

    assert lighting_engine.called is True

    assert result.lighting is not None

    assert result.visual_intent.lighting.light_source == "moonlight"

def test_pipeline_preserves_lighting_conflicts() -> None:

    """Existing lighting values should remain authoritative on conflict."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A warrior beneath sunlight.",

        light_source="moonlight",

    )

    result.visual_intent.lighting.light_source = "sunlight"

    second_result = pipeline.lighting_engine.construct(

        result.visual_intent,

        light_source="moonlight",

    )

    assert second_result.lighting.light_source == "sunlight"

    assert len(second_result.warnings) == 1

def test_pipeline_assembles_structured_prompt() -> None:

    """The pipeline should produce a prompt from the structured intent."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon standing in a ruined castle.",

        subject_identity="Azrael",

        subject_type="character",

        species="dragon",

        location="ruined castle",

        framing="medium shot",

        light_source="moonlight",

        intensity="low",

    )

    assert isinstance(result.prompt, str)

    assert result.prompt != ""

    assert "Azrael" in result.prompt

    assert "dragon" in result.prompt

    assert "ruined castle" in result.prompt

    assert "medium shot" in result.prompt

    assert "moonlight" in result.prompt

def test_pipeline_rejects_invalid_input() -> None:

    """The pipeline should reject invalid user input."""

    pipeline = OIPMPipeline()

    with pytest.raises(TypeError):

        pipeline.process(None)  # type: ignore[arg-type]

def test_pipeline_returns_validation_failure() -> None:

    """Invalid VisualIntent state should stop downstream processing."""

    class InvalidatingValidator:

        def validate(self, visual_intent: VisualIntent):

            from oipm.validation import ValidationResult

            return ValidationResult(

                is_valid=False,

                issues=[],

            )

    pipeline = OIPMPipeline(

        validator=InvalidatingValidator(),  # type: ignore[arg-type]

    )

    result = pipeline.process("A dragon.")

    assert result.validation.is_valid is False

    assert result.subject_resolution is None

    assert result.scene_construction is None

    assert result.composition is None

    assert result.lighting is None

    assert result.prompt == ""

def test_pipeline_short_input_preserves_warning() -> None:

    """Short input warnings should survive the complete pipeline."""

    pipeline = OIPMPipeline()

    result = pipeline.process("Hi")

    assert any(

        "short" in warning.lower()

        for warning in result.interpretation.warnings

    )

def test_pipeline_does_not_invent_lighting() -> None:

    """A pipeline call without lighting input should not invent lighting."""

    pipeline = OIPMPipeline()

    result = pipeline.process("A warrior standing in a field.")

    assert result.lighting is not None

    assert result.visual_intent.lighting.light_source is None

    assert result.visual_intent.lighting.direction is None

    assert result.visual_intent.lighting.intensity is None

    assert result.visual_intent.lighting.color_temperature is None

    assert result.visual_intent.lighting.contrast is None

    assert result.visual_intent.lighting.atmospheric_effects is None

    assert result.visual_intent.lighting.volumetric_effects is None

    assert result.visual_intent.lighting.environmental_interaction is None

def test_pipeline_preserves_visual_intent_identity() -> None:

    """All pipeline stages should operate on the same VisualIntent."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon beneath moonlight.",

        subject_identity="Azrael",

        location="ancient ruins",

        framing="close-up",

        light_source="moonlight",

    )

    assert result.interpretation.visual_intent is result.visual_intent

    assert result.subject_resolution is not None

    assert result.subject_resolution.visual_intent is result.visual_intent

    assert result.scene_construction is not None

    assert result.scene_construction.visual_intent is result.visual_intent

    assert result.composition is not None

    assert result.composition.visual_intent is result.visual_intent

    assert result.lighting is not None

    assert result.lighting.visual_intent is result.visual_intent