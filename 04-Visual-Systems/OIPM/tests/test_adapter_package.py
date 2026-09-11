"""Tests for the public OIPM Generator Adaptation Layer package."""

from __future__ import annotations

from oipm.adapters import (

    AdapterExecutor,

    AdapterRegistry,

    GeneratorAdapter,

    GeneratorAdapterResult,

    StubGeneratorAdapter,

)

def test_adapter_executor_is_publicly_exported() -> None:

    registry = AdapterRegistry()

    executor = AdapterExecutor(registry)

    assert isinstance(executor, AdapterExecutor)

def test_adapter_registry_is_publicly_exported() -> None:

    registry = AdapterRegistry()

    assert isinstance(registry, AdapterRegistry)

def test_generator_adapter_is_publicly_exported() -> None:

    assert issubclass(GeneratorAdapter, object)

def test_generator_adapter_result_is_publicly_exported() -> None:

    result = GeneratorAdapterResult(

        generator="test-generator",

        prompt="test prompt",

        parameters={},

        warnings=[],

    )

    assert result.generator == "test-generator"

    assert result.prompt == "test prompt"

    assert result.parameters == {}

    assert result.warnings == []

def test_stub_generator_adapter_is_publicly_exported() -> None:

    adapter = StubGeneratorAdapter()

    assert isinstance(adapter, StubGeneratorAdapter)

    assert adapter.generator_name == "stub-generator"

def test_public_exports_are_available_from_expected_module() -> None:

    import oipm.adapters as adapters

    assert adapters.AdapterExecutor is AdapterExecutor

    assert adapters.AdapterRegistry is AdapterRegistry

    assert adapters.GeneratorAdapter is GeneratorAdapter

    assert adapters.GeneratorAdapterResult is GeneratorAdapterResult

    assert adapters.StubGeneratorAdapter is StubGeneratorAdapter