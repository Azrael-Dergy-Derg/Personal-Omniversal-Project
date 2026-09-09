"""Tests for the OIPM Generator Adaptation Layer adapter registry."""

from __future__ import annotations

import pytest

from oipm.adapters import GeneratorAdapter, GeneratorAdapterResult

from oipm.adapters.adapter_registry import AdapterRegistry

from oipm.models import VisualIntent

class StubGeneratorAdapter(GeneratorAdapter):

    """Minimal adapter used for registry tests."""

    def __init__(self, name: str) -> None:

        self._name = name

    @property

    def generator_name(self) -> str:

        return self._name

    def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

        self._validate_input(visual_intent)

        return GeneratorAdapterResult(

            generator=self.generator_name,

            prompt="stub prompt",

            parameters={},

            warnings=[],

        )

def test_registry_starts_empty() -> None:

    registry = AdapterRegistry()

    assert registry.names() == ()

def test_registry_accepts_generator_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter("stub-generator")

    registry.register(adapter)

    assert registry.has("stub-generator")

    assert registry.get("stub-generator") is adapter

def test_registry_rejects_non_adapter() -> None:

    registry = AdapterRegistry()

    with pytest.raises(TypeError, match="adapter must be a GeneratorAdapter"):

        registry.register("not an adapter")  # type: ignore[arg-type]

def test_registry_rejects_empty_generator_name() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter("")

    with pytest.raises(

        ValueError,

        match="adapter generator_name must not be empty",

    ):

        registry.register(adapter)

def test_registry_rejects_duplicate_generator_name() -> None:

    registry = AdapterRegistry()

    first = StubGeneratorAdapter("stub-generator")

    second = StubGeneratorAdapter("stub-generator")

    registry.register(first)

    with pytest.raises(

        ValueError,

        match="adapter already registered for generator: stub-generator",

    ):

        registry.register(second)

    assert registry.get("stub-generator") is first

def test_registry_returns_registered_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter("stub-generator")

    registry.register(adapter)

    assert registry.get("stub-generator") is adapter

def test_registry_rejects_unknown_generator() -> None:

    registry = AdapterRegistry()

    with pytest.raises(

        KeyError,

        match="no adapter registered for generator: missing-generator",

    ):

        registry.get("missing-generator")

def test_registry_has_returns_false_for_unknown_generator() -> None:

    registry = AdapterRegistry()

    assert registry.has("missing-generator") is False

def test_registry_names_are_deterministically_sorted() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter("zeta"))

    registry.register(StubGeneratorAdapter("alpha"))

    registry.register(StubGeneratorAdapter("middle"))

    assert registry.names() == (

        "alpha",

        "middle",

        "zeta",

    )

def test_registry_remove_returns_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter("stub-generator")

    registry.register(adapter)

    removed = registry.remove("stub-generator")

    assert removed is adapter

    assert registry.has("stub-generator") is False

    assert registry.names() == ()

def test_registry_remove_rejects_unknown_generator() -> None:

    registry = AdapterRegistry()

    with pytest.raises(

        KeyError,

        match="no adapter registered for generator: missing-generator",

    ):

        registry.remove("missing-generator")

def test_registry_clear_removes_all_adapters() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter("alpha"))

    registry.register(StubGeneratorAdapter("beta"))

    registry.register(StubGeneratorAdapter("gamma"))

    registry.clear()

    assert registry.names() == ()

    assert registry.has("alpha") is False

    assert registry.has("beta") is False

    assert registry.has("gamma") is False

def test_registry_does_not_modify_registered_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter("stub-generator")

    registry.register(adapter)

    retrieved = registry.get("stub-generator")

    assert retrieved is adapter

    assert retrieved.generator_name == "stub-generator"