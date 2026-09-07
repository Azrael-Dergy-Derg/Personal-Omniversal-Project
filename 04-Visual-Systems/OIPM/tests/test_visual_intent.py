"""Tests for the OIPM VisualIntent data model."""

from __future__ import annotations

from uuid import uuid4

import pytest

from pydantic import ValidationError

from oipm.models import (

    Attribute,

    AttributeStatus,

    CanonStatus,

    Confidence,

    Priority,

    Source,

    Subject,

    VisualIntent,

)

def test_visual_intent_can_be_created_with_defaults() -> None:

    """VisualIntent should initialize all major sections by default."""

    intent = VisualIntent()

    assert intent.metadata is not None

    assert intent.subjects == []

    assert intent.relationships == []

    assert intent.scene is not None

    assert intent.composition is not None

    assert intent.lighting is not None

    assert intent.artistic_direction is not None

    assert intent.constraints == []

    assert intent.references == []

    assert intent.generator_target is not None

    assert intent.state is not None

def test_visual_intent_metadata_is_initialized() -> None:

    """Metadata should receive an ID and valid timestamps automatically."""

    intent = VisualIntent()

    assert intent.metadata.intent_id is not None

    assert intent.metadata.created_at is not None

    assert intent.metadata.modified_at is not None

    assert intent.metadata.oipm_version == "0.1.0"

def test_visual_intent_preserves_user_input() -> None:

    """User input should be stored as metadata without alteration."""

    user_input = "A dark fantasy dragon standing beneath a moonlit sky."

    intent = VisualIntent()

    intent.metadata.user_input = user_input

    assert intent.metadata.user_input == user_input

def test_subject_can_contain_structured_attributes() -> None:

    """Subjects should support provenance-aware visual attributes."""

    subject = Subject(

        identity="Azrael",

        type="character",

        species="dragon",

        canon_status=CanonStatus.CANONICAL,

        physical_attributes={

            "scale_color": Attribute(

                value="matte black",

                source=Source.CANON,

                confidence=Confidence.HIGH,

                priority=Priority.CRITICAL,

                status=AttributeStatus.LOCKED,

            )

        },

    )

    assert subject.identity == "Azrael"

    assert subject.species == "dragon"

    assert subject.canon_status == CanonStatus.CANONICAL

    scale_color = subject.physical_attributes["scale_color"]

    assert scale_color.value == "matte black"

    assert scale_color.source == Source.CANON

    assert scale_color.priority == Priority.CRITICAL

    assert scale_color.status == AttributeStatus.LOCKED

def test_subject_generates_unique_id() -> None:

    """Each subject should receive its own UUID automatically."""

    first = Subject()

    second = Subject()

    assert first.id != second.id

def test_relationship_ids_can_reference_subjects() -> None:

    """Subject relationship references should accept UUID values."""

    first_id = uuid4()

    second_id = uuid4()

    subject = Subject(

        id=first_id,

        relationships=[second_id],

    )

    assert subject.id == first_id

    assert subject.relationships == [second_id]

def test_visual_intent_serializes_to_dictionary() -> None:

    """VisualIntent should serialize into a standard Python dictionary."""

    intent = VisualIntent()

    data = intent.model_dump()

    assert isinstance(data, dict)

    assert "metadata" in data

    assert "subjects" in data

    assert "scene" in data

    assert "composition" in data

    assert "lighting" in data

    assert "artistic_direction" in data

    assert "constraints" in data

    assert "references" in data

    assert "generator_target" in data

    assert "state" in data

def test_visual_intent_rejects_unknown_fields() -> None:

    """The source-of-truth model must reject undeclared fields."""

    with pytest.raises(ValidationError):

        VisualIntent(

            unauthorized_field="this must not be accepted",

        )

def test_subject_rejects_unknown_fields() -> None:

    """Subject models must reject undeclared fields."""

    with pytest.raises(ValidationError):

        Subject(

            unauthorized_field="this must not be accepted",

        )

def test_attribute_defaults_are_stable() -> None:

    """Attribute defaults should preserve OIPM's conservative priority model."""

    attribute = Attribute(

        value="black",

        source=Source.EXPLICIT_USER,

    )

    assert attribute.confidence == Confidence.HIGH

    assert attribute.priority == Priority.MEDIUM

    assert attribute.status == AttributeStatus.REQUIRED

    assert attribute.override is False