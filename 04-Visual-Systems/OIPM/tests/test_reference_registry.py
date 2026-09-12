"""Tests for the OIPM Reference & Consistency System registry."""

from __future__ import annotations

import pytest

from oipm.references.reference_model import Reference, ReferenceType

from oipm.references.reference_registry import ReferenceRegistry

def make_reference(

    reference_id: str = "test-reference",

) -> Reference:

    """Create a minimal test reference."""

    return Reference(

        reference_id=reference_id,

        reference_type=ReferenceType.GENERAL,

        source="test-source",

    )

def test_registry_starts_empty() -> None:

    registry = ReferenceRegistry()

    assert registry.ids() == ()

def test_registry_registers_reference() -> None:

    registry = ReferenceRegistry()

    reference = make_reference()

    registry.register(reference)

    assert registry.has("test-reference")

    assert registry.get("test-reference") is reference

def test_registry_rejects_non_reference() -> None:

    registry = ReferenceRegistry()

    with pytest.raises(TypeError):

        registry.register("not-a-reference")  # type: ignore[arg-type]

def test_registry_rejects_duplicate_reference_id() -> None:

    registry = ReferenceRegistry()

    registry.register(make_reference("reference-a"))

    with pytest.raises(ValueError):

        registry.register(make_reference("reference-a"))

def test_registry_get_missing_reference_raises_key_error() -> None:

    registry = ReferenceRegistry()

    with pytest.raises(KeyError):

        registry.get("missing-reference")

def test_registry_has_returns_false_for_missing_reference() -> None:

    registry = ReferenceRegistry()

    assert registry.has("missing-reference") is False

def test_registry_ids_are_deterministic() -> None:

    registry = ReferenceRegistry()

    registry.register(make_reference("reference-c"))

    registry.register(make_reference("reference-a"))

    registry.register(make_reference("reference-b"))

    assert registry.ids() == (

        "reference-a",

        "reference-b",

        "reference-c",

    )

def test_registry_remove_returns_reference() -> None:

    registry = ReferenceRegistry()

    reference = make_reference()

    registry.register(reference)

    removed = registry.remove("test-reference")

    assert removed is reference

    assert not registry.has("test-reference")

    assert registry.ids() == ()

def test_registry_remove_missing_reference_raises_key_error() -> None:

    registry = ReferenceRegistry()

    with pytest.raises(KeyError):

        registry.remove("missing-reference")

def test_registry_clear_removes_all_references() -> None:

    registry = ReferenceRegistry()

    registry.register(make_reference("reference-a"))

    registry.register(make_reference("reference-b"))

    registry.register(make_reference("reference-c"))

    registry.clear()

    assert registry.ids() == ()

    assert not registry.has("reference-a")

    assert not registry.has("reference-b")

    assert not registry.has("reference-c")

def test_registry_does_not_modify_reference() -> None:

    registry = ReferenceRegistry()

    reference = make_reference()

    original_id = reference.reference_id

    original_type = reference.reference_type

    original_source = reference.source

    registry.register(reference)

    stored = registry.get(reference.reference_id)

    assert stored.reference_id == original_id

    assert stored.reference_type == original_type

    assert stored.source == original_source

def test_registry_does_not_create_visual_intent() -> None:

    registry = ReferenceRegistry()

    registry.register(make_reference())

    reference = registry.get("test-reference")

    assert not hasattr(reference, "visual_intent")

def test_registry_does_not_promote_reference_to_canon() -> None:

    registry = ReferenceRegistry()

    reference = make_reference()

    registry.register(reference)

    stored = registry.get("test-reference")

    assert not hasattr(stored, "canon")

    assert stored.authoritative is False

def test_registry_preserves_authoritative_flag_without_interpreting_it() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="authoritative-reference",

        reference_type=ReferenceType.CHARACTER,

        source="approved appearance reference",

        authoritative=True,

    )

    registry.register(reference)

    stored = registry.get("authoritative-reference")

    assert stored.authoritative is True

def test_registry_remove_does_not_affect_other_references() -> None:

    registry = ReferenceRegistry()

    reference_a = make_reference("reference-a")

    reference_b = make_reference("reference-b")

    registry.register(reference_a)

    registry.register(reference_b)

    removed = registry.remove("reference-a")

    assert removed is reference_a

    assert registry.get("reference-b") is reference_b

    assert registry.ids() == ("reference-b",)