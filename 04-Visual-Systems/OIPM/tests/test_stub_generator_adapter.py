"""Tests for the reference OIPM stub generator adapter."""

from __future__ import annotations

import pytest

from oipm.adapters import GeneratorAdapterResult

from oipm.adapters.stub_generator_adapter import StubGeneratorAdapter

from oipm.models import VisualIntent

def test_stub_adapter_implements_generator_adapter_contract() -> None:

    adapter = StubGeneratorAdapter()

    assert adapter.generator_name == "stub-generator"

def test_stub_adapter_accepts_visual_intent() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    result = adapter.adapt(visual_intent)

    assert isinstance(result, GeneratorAdapterResult)

    assert result.generator == "stub-generator"

def test_stub_adapter_returns_deterministic_reference_result() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    result = adapter.adapt(visual_intent)

    assert (

        result.prompt

        == (

            "stub-generator representation: "

            "subjects=0; "

            "scene=False; "

            "composition=False; "

            "lighting=False; "

            "artistic_direction=False; "

            "constraints=0"

        )

    )

    assert result.parameters == {

        "subject_count": 0,

        "has_scene": False,

        "has_composition": False,

        "has_lighting": False,

        "has_artistic_direction": False,

        "constraint_count": 0,

    }

    assert result.warnings == []

def test_stub_adapter_reflects_existing_visual_intent_structure() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    visual_intent.subjects.append(

        {

            "identity": "test-subject",

            "type": "character",

        }

    )

    result = adapter.adapt(visual_intent)

    assert "subjects=1" in result.prompt

    assert result.parameters["subject_count"] == 1

def test_stub_adapter_rejects_invalid_input() -> None:

    adapter = StubGeneratorAdapter()

    with pytest.raises(TypeError):

        adapter.adapt("not a visual intent")  # type: ignore[arg-type]

def test_stub_adapter_does_not_modify_visual_intent() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    before = visual_intent.model_dump()

    adapter.adapt(visual_intent)

    after = visual_intent.model_dump()

    assert after == before

def test_stub_adapter_result_is_independent_from_visual_intent() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    result = adapter.adapt(visual_intent)

    assert result is not visual_intent

def test_stub_adapter_does_not_invent_visual_information() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    result = adapter.adapt(visual_intent)

    assert "identity" not in result.prompt

    assert "species" not in result.prompt

    assert "camera" not in result.prompt

    assert "lighting_style" not in result.prompt

    assert "artistic_style" not in result.prompt