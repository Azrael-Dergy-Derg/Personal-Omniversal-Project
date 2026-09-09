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

def test_stub_adapter_returns_expected_reference_result() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    result = adapter.adapt(visual_intent)

    assert result.prompt == "stub prompt"

    assert result.parameters == {}

    assert result.warnings == []

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

def test_stub_adapter_returns_independent_result() -> None:

    adapter = StubGeneratorAdapter()

    visual_intent = VisualIntent()

    result = adapter.adapt(visual_intent)

    assert result is not visual_intent