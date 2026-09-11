"""Tests for the OIPM Reference & Consistency System reference model."""

from __future__ import annotations

import pytest

from oipm.references.reference_model import (

    Reference,

    ReferenceRole,

    ReferenceType,

)

def test_reference_requires_reference_id() -> None:

    with pytest.raises(ValueError):

        Reference(

            reference_id="",

            reference_type=ReferenceType.CHARACTER,

            source="test-source",

        )

def test_reference_requires_source() -> None:

    with pytest.raises(ValueError):

        Reference(

            reference_id="test-reference",

            reference_type=ReferenceType.CHARACTER,

            source="",

        )

def test_reference_stores_required_metadata() -> None:

    reference = Reference(

        reference_id="azrael-main",

        reference_type=ReferenceType.CHARACTER,

        source="approved character reference",

    )

    assert reference.reference_id == "azrael-main"

    assert reference.reference_type == ReferenceType.CHARACTER

    assert reference.source == "approved character reference"

def test_reference_defaults_are_non_authoritative() -> None:

    reference = Reference(

        reference_id="test-reference",

        reference_type=ReferenceType.GENERAL,

        source="test-source",

    )

    assert reference.roles == frozenset()

    assert reference.description is None

    assert reference.tags == frozenset()

    assert reference.authoritative is False

    assert reference.notes is None

def test_reference_stores_roles() -> None:

    reference = Reference(

        reference_id="azrael-appearance",

        reference_type=ReferenceType.CHARACTER,

        source="approved appearance reference",

        roles=frozenset(

            {

                ReferenceRole.IDENTITY,

                ReferenceRole.APPEARANCE,

                ReferenceRole.ANATOMY,

            }

        ),

    )

    assert reference.serves_role(ReferenceRole.IDENTITY)

    assert reference.serves_role(ReferenceRole.APPEARANCE)

    assert reference.serves_role(ReferenceRole.ANATOMY)

    assert not reference.serves_role(ReferenceRole.LIGHTING)

def test_reference_stores_tags() -> None:

    reference = Reference(

        reference_id="test-reference",

        reference_type=ReferenceType.STYLE,

        source="test-source",

        tags=frozenset(

            {

                "dark-fantasy",

                "graphic-novel",

                "comic",

            }

        ),

    )

    assert reference.has_tag("dark-fantasy")

    assert reference.has_tag("graphic-novel")

    assert reference.has_tag("comic")

    assert not reference.has_tag("photorealistic")

def test_reference_stores_optional_metadata() -> None:

    reference = Reference(

        reference_id="test-reference",

        reference_type=ReferenceType.ENVIRONMENT,

        source="project reference",

        description="Border Realm fortress environment.",

        authoritative=True,

        notes="Approved for environmental continuity.",

    )

    assert reference.description == "Border Realm fortress environment."

    assert reference.authoritative is True

    assert reference.notes == "Approved for environmental continuity."

def test_reference_is_immutable() -> None:

    reference = Reference(

        reference_id="test-reference",

        reference_type=ReferenceType.CHARACTER,

        source="test-source",

    )

    with pytest.raises(AttributeError):

        reference.reference_id = "changed"  # type: ignore[misc]

def test_reference_does_not_contain_visual_intent() -> None:

    reference = Reference(

        reference_id="test-reference",

        reference_type=ReferenceType.CHARACTER,

        source="test-source",

    )

    assert not hasattr(reference, "visual_intent")

def test_reference_does_not_contain_prompt() -> None:

    reference = Reference(

        reference_id="test-reference",

        reference_type=ReferenceType.CHARACTER,

        source="test-source",

    )

    assert not hasattr(reference, "prompt")

def test_reference_authority_is_explicit() -> None:

    non_authoritative = Reference(

        reference_id="reference-a",

        reference_type=ReferenceType.CHARACTER,

        source="inspiration",

    )

    authoritative = Reference(

        reference_id="reference-b",

        reference_type=ReferenceType.CHARACTER,

        source="approved character sheet",

        authoritative=True,

    )

    assert non_authoritative.authoritative is False

    assert authoritative.authoritative is True

def test_reference_roles_are_limited_to_declared_purpose() -> None:

    reference = Reference(

        reference_id="appearance-reference",

        reference_type=ReferenceType.CHARACTER,

        source="approved appearance reference",

        roles=frozenset({ReferenceRole.APPEARANCE}),

        authoritative=True,

    )

    assert reference.authoritative is True

    assert reference.serves_role(ReferenceRole.APPEARANCE)

    assert not reference.serves_role(ReferenceRole.IDENTITY)

    assert not reference.serves_role(ReferenceRole.COSTUME)

    assert not reference.serves_role(ReferenceRole.STYLE)