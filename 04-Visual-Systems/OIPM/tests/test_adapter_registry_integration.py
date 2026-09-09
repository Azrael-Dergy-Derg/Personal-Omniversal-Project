"""Integration tests for the OIPM adapter registry and reference adapter."""

from __future__ import annotations

from oipm.adapters import AdapterRegistry, StubGeneratorAdapter

def test_registry_can_register_and_retrieve_stub_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter()

    registry.register(adapter)

    assert registry.has("stub-generator")

    assert registry.get("stub-generator") is adapter

def test_registry_names_include_registered_stub_adapter() -> None:

    registry = AdapterRegistry()

    registry.register(StubGeneratorAdapter())

    assert registry.names() == ("stub-generator",)

def test_registry_can_remove_registered_stub_adapter() -> None:

    registry = AdapterRegistry()

    adapter = StubGeneratorAdapter()

    registry.register(adapter)

    removed = registry.remove("stub-generator")

    assert removed is adapter

    assert not registry.has("stub-generator")

    assert registry.names() == ()