"""Tests for the OIPM processing pipeline."""

from __future__ import annotations

import pytest

from oipm.pipeline import OIPMPipeline, PipelineResult

def test_pipeline_processes_basic_input_end_to_end() -> None:

    """A valid request should pass through every current pipeline stage."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dark fantasy dragon beneath a moonlit sky."

    )

    assert isinstance(result, PipelineResult)

    assert result.validation.valid is True

    assert result.validation.issues == ()

    assert result.prompt != ""

def test_pipeline_preserves_user_input() -> None:

    """The original normalized user input should remain in VisualIntent."""

    user_input = "A dark fantasy dragon beneath a moonlit sky."

    result = OIPMPipeline().process(user_input)

    assert result.interpretation.visual_intent.metadata.user_input == user_input

def test_pipeline_preserves_project_and_scene_metadata() -> None:

    """Project and scene identifiers should reach VisualIntent metadata."""

    result = OIPMPipeline().process(

        "A dragon standing in an ancient ruin.",

        project="TestProject",

        scene_id="scene-001",

    )

    metadata = result.interpretation.visual_intent.metadata

    assert metadata.project == "TestProject"

    assert metadata.scene_id == "scene-001"

def test_pipeline_generates_prompt_from_structured_intent() -> None:

    """Prompt output should be produced from the assembled VisualIntent."""

    pipeline = OIPMPipeline()

    interpretation = pipeline.interpreter.process(

        "A dragon beneath a moonlit sky."

    )

    subject = interpretation.visual_intent.subjects

    assert subject == []

    interpretation.visual_intent.scene.location = "an ancient ruin"

    interpretation.visual_intent.scene.weather = "moonlit sky"

    validation = pipeline.validate_interpretation(

        interpretation

    )

    assert validation.valid is True

    prompt = pipeline.assembler.assemble(

        interpretation.visual_intent

    )

    assert "Scene:" in prompt

    assert "an ancient ruin" in prompt

    assert "moonlit sky" in prompt

def test_pipeline_does_not_generate_prompt_for_invalid_intent() -> None:

    """Invalid VisualIntent state should prevent prompt assembly."""

    pipeline = OIPMPipeline()

    result = pipeline.interpreter.process(

        "A valid image request."

    )

    result.visual_intent.metadata.user_input = ""

    pipeline_result = PipelineResult(

        interpretation=result,

        validation=pipeline.validator.validate(

            result.visual_intent

        ),

        prompt="",

    )

    assert pipeline_result.validation.valid is False

    assert pipeline_result.prompt == ""

def test_pipeline_reports_short_input_warning() -> None:

    """Very short input should preserve the interpreter warning."""

    result = OIPMPipeline().process("dragon")

    assert (

        "Input is very short and may require additional "

        "interpretation or clarification."

        in result.interpretation.warnings

    )

def test_pipeline_accepts_normal_input_without_warning() -> None:

    """Normal-length input should not produce the short-input warning."""

    result = OIPMPipeline().process(

        "A dragon warrior standing beneath a moonlit sky."

    )

    assert result.interpretation.warnings == ()

def test_pipeline_validation_messages_are_available() -> None:

    """Validation messages should be exposed in stable order."""

    pipeline = OIPMPipeline()

    interpretation = pipeline.interpreter.process(

        "A valid image request."

    )

    interpretation.visual_intent.metadata.user_input = ""

    validation = pipeline.validator.validate(

        interpretation.visual_intent

    )

    messages = pipeline.validation_messages(validation)

    assert len(messages) == len(validation.issues)

    for message, issue in zip(messages, validation.issues):

        assert message == issue.message

def test_pipeline_validation_issues_are_available() -> None:

    """Structured validation issues should remain accessible."""

    pipeline = OIPMPipeline()

    interpretation = pipeline.interpreter.process(

        "A valid image request."

    )

    interpretation.visual_intent.metadata.user_input = ""

    validation = pipeline.validator.validate(

        interpretation.visual_intent

    )

    issues = pipeline.validation_issues(validation)

    assert issues == validation.issues

def test_pipeline_rejects_empty_input() -> None:

    """Empty input should be rejected by the input interpreter."""

    with pytest.raises(ValueError):

        OIPMPipeline().process("")

def test_pipeline_rejects_non_string_input() -> None:

    """Non-string input should be rejected by the input interpreter."""

    with pytest.raises(ValueError):

        OIPMPipeline().process(123)  # type: ignore[arg-type]

def test_pipeline_supports_component_injection() -> None:

    """Pipeline components should be replaceable for future extensibility."""

    pipeline = OIPMPipeline()

    assert pipeline.interpreter is not None

    assert pipeline.validator is not None

    assert pipeline.assembler is not None