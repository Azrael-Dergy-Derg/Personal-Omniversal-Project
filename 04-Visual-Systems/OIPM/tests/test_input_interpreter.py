"""Tests for the OIPM InputInterpreter."""

from __future__ import annotations

import pytest

from oipm.interpretation.input_interpreter import (

    InputInterpreter,

    InterpretationResult,

)

def test_interpreter_creates_visual_intent() -> None:

    """The interpreter should produce a structured VisualIntent."""

    interpreter = InputInterpreter()

    result = interpreter.process(

        "A dark fantasy dragon beneath a moonlit sky."

    )

    assert isinstance(result, InterpretationResult)

    assert result.visual_intent is not None

    assert (

        result.visual_intent.metadata.user_input

        == "A dark fantasy dragon beneath a moonlit sky."

    )

def test_interpreter_normalizes_whitespace() -> None:

    """Input normalization should collapse unnecessary whitespace."""

    interpreter = InputInterpreter()

    result = interpreter.process(

        "  A   dark fantasy dragon\n"

        "beneath a moonlit sky.  "

    )

    assert (

        result.visual_intent.metadata.user_input

        == "A dark fantasy dragon beneath a moonlit sky."

    )

def test_interpreter_preserves_project_metadata() -> None:

    """Project metadata should be transferred into VisualIntent."""

    interpreter = InputInterpreter()

    result = interpreter.process(

        "A dragon standing in a ruined fortress.",

        project="Personal-Omniversal-Project",

        scene_id="scene-001",

    )

    assert (

        result.visual_intent.metadata.project

        == "Personal-Omniversal-Project"

    )

    assert result.visual_intent.metadata.scene_id == "scene-001"

def test_interpreter_rejects_empty_input() -> None:

    """Whitespace-only input should be rejected."""

    interpreter = InputInterpreter()

    with pytest.raises(ValueError):

        interpreter.process("   ")

def test_interpreter_rejects_non_string_input() -> None:

    """Non-string input should be rejected."""

    interpreter = InputInterpreter()

    with pytest.raises(ValueError):

        interpreter.process(123)  # type: ignore[arg-type]

def test_short_input_produces_warning() -> None:

    """Very short input should produce a conservative warning."""

    interpreter = InputInterpreter()

    result = interpreter.process("Dragon")

    assert (

        "Input is very short and may require additional "

        "interpretation or clarification."

        in result.warnings

    )

def test_normal_input_does_not_produce_short_input_warning() -> None:

    """Normal-length input should not trigger the short-input warning."""

    interpreter = InputInterpreter()

    result = interpreter.process(

        "A black dragon standing beneath a purple moon."

    )

    assert result.warnings == ()

def test_interpreter_validation_accepts_valid_result() -> None:

    """Interpreter-level validation should accept a valid result."""

    interpreter = InputInterpreter()

    result = interpreter.process(

        "A dark fantasy dragon beneath a moonlit sky."

    )

    errors = interpreter.validate(result)

    assert errors == []

def test_interpreter_validation_detects_missing_user_input() -> None:

    """Interpreter validation should detect missing user input."""

    interpreter = InputInterpreter()

    result = interpreter.process(

        "A dark fantasy dragon beneath a moonlit sky."

    )

    result.visual_intent.metadata.user_input = ""

    errors = interpreter.validate(result)

    assert "VisualIntent contains no user input." in errors

def test_interpreter_does_not_invent_visual_details() -> None:

    """The initial interpreter should not invent unspecified details."""

    interpreter = InputInterpreter()

    result = interpreter.process("A dragon.")

    intent = result.visual_intent

    assert intent.subjects == []

    assert intent.scene.location is None

    assert intent.composition.shot_type is None

    assert intent.lighting.intent is None

    assert intent.artistic_direction.medium is None