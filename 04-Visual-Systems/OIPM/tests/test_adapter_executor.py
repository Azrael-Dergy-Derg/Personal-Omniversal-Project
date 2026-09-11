"""Tests for the OIPM generator adapter executor."""

from __future__ import annotations

import pytest

from oipm.adapters import AdapterRegistry, GeneratorAdapterResult

from oipm.adapters.adapter_executor import AdapterExecutor

from oipm.adapters.stub_generator_adapter import StubGeneratorAdapter

from oipm.models import VisualIntent

def test_executor_requires_adapter_registry() -> None:

    with pytest.raises(TypeError):

        AdapterExecutor("not a registry")  # type: ignore[arg-type]

def test_executor_stores_registry() -> None:

    registry = AdapterRegistry()

    executor = AdapterExecutor(registry)

    assert executor.registry is registry

def test_executor_requires_explicit_generator_name() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter())

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    with pytest.raises(ValueError):

        executor.execute(

            visual_intent,

            generator_name="",

        )

def test_executor_rejects_invalid_visual_intent() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter())

    executor = AdapterExecutor(registry)

    with pytest.raises(TypeError):

        executor.execute(

            "not a visual intent",  # type: ignore[arg-type]

            generator_name="stub-generator",

        )

def test_executor_rejects_unregistered_generator() -> None:

    registry = AdapterRegistry()

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    with pytest.raises(KeyError):

        executor.execute(

            visual_intent,

            generator_name="missing-generator",

        )

def test_executor_executes_registered_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter()

    registry.register(adapter)

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    result = executor.execute(

        visual_intent,

        generator_name="stub-generator",

    )

    assert isinstance(result, GeneratorAdapterResult)

    assert result.generator == "stub-generator"

def test_executor_uses_explicitly_selected_adapter() -> None:

    registry = AdapterRegistry()

    first_adapter = StubGeneratorAdapter()

    second_adapter = StubGeneratorAdapter()

    registry.register(first_adapter)

    class AlternateStubAdapter(StubGeneratorAdapter):

        @property

        def generator_name(self) -> str:

            return "alternate-stub-generator"

    alternate_adapter = AlternateStubAdapter()

    registry.register(alternate_adapter)

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    result = executor.execute(

        visual_intent,

        generator_name="alternate-stub-generator",

    )

    assert result.generator == "alternate-stub-generator"

def test_executor_preserves_visual_intent_identity() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter())

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    result = executor.execute(

        visual_intent,

        generator_name="stub-generator",

    )

    assert result is not visual_intent

def test_executor_does_not_modify_visual_intent() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter())

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    before = visual_intent.model_dump()

    executor.execute(

        visual_intent,

        generator_name="stub-generator",

    )

    after = visual_intent.model_dump()

    assert after == before

def test_executor_does_not_select_generator_implicitly() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter())

    executor = AdapterExecutor(registry)

    visual_intent = VisualIntent()

    with pytest.raises(TypeError):

        executor.execute(visual_intent)  # type: ignore[call-arg]