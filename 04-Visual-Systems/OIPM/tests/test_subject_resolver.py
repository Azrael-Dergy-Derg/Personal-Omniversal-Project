"""Tests for the OIPM Subject and Character Resolution Engine."""

from __future__ import annotations

from uuid import uuid4

import pytest

from oipm.models import CanonStatus, Subject, VisualIntent

from oipm.subjects.subject_resolver import (

    SubjectResolutionResult,

    SubjectResolver,

)

def test_resolver_registers_new_subject() -> None:

    """A new subject should be added to the VisualIntent."""

    intent = VisualIntent()

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

        subject_type="character",

        species="dragon",

    )

    assert isinstance(result, SubjectResolutionResult)

    assert result.visual_intent is intent

    assert len(intent.subjects) == 1

    assert result.resolved_subjects == (intent.subjects[0],)

def test_resolver_preserves_explicit_subject_data() -> None:

    """Explicit subject information should be preserved exactly."""

    intent = VisualIntent()

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

        subject_type="character",

        species="dragon",

        canon_status=CanonStatus.CANONICAL,

    )

    subject = result.resolved_subjects[0]

    assert subject.identity == "Azrael"

    assert subject.type == "character"

    assert subject.species == "dragon"

    assert subject.canon_status == CanonStatus.CANONICAL

def test_resolver_finds_existing_subject_by_identity() -> None:

    """An existing identity should not create a duplicate subject."""

    existing = Subject(

        identity="Azrael",

        type="character",

        species="dragon",

    )

    intent = VisualIntent(subjects=[existing])

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

    )

    assert len(intent.subjects) == 1

    assert result.resolved_subjects == (existing,)

def test_resolver_applies_missing_subject_data() -> None:

    """Missing fields on an existing subject may receive explicit data."""

    existing = Subject(

        identity="Azrael",

    )

    intent = VisualIntent(subjects=[existing])

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

        subject_type="character",

        species="dragon",

        canon_status=CanonStatus.CANONICAL,

    )

    subject = result.resolved_subjects[0]

    assert subject.type == "character"

    assert subject.species == "dragon"

    assert subject.canon_status == CanonStatus.CANONICAL

    assert result.warnings == ()

def test_resolver_preserves_existing_type_on_conflict() -> None:

    """Conflicting explicit type information should not silently overwrite."""

    existing = Subject(

        identity="Azrael",

        type="character",

    )

    intent = VisualIntent(subjects=[existing])

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

        subject_type="creature",

    )

    assert existing.type == "character"

    assert (

        "Existing subject type conflicts with supplied subject type; "

        "existing value was preserved."

        in result.warnings

    )

def test_resolver_preserves_existing_species_on_conflict() -> None:

    """Conflicting species information should preserve existing data."""

    existing = Subject(

        identity="Azrael",

        species="dragon",

    )

    intent = VisualIntent(subjects=[existing])

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

        species="argonian",

    )

    assert existing.species == "dragon"

    assert (

        "Existing subject species conflicts with supplied species; "

        "existing value was preserved."

        in result.warnings

    )

def test_resolver_does_not_change_known_canon_status() -> None:

    """Known canon status should not be silently downgraded or replaced."""

    existing = Subject(

        identity="Azrael",

        canon_status=CanonStatus.CANONICAL,

    )

    intent = VisualIntent(subjects=[existing])

    result = SubjectResolver().resolve(

        intent,

        identity="Azrael",

        canon_status=CanonStatus.NON_CANON,

    )

    assert existing.canon_status == CanonStatus.CANONICAL

    assert result.warnings == ()

def test_resolver_rejects_non_visual_intent_input() -> None:

    """The resolver should reject objects of the wrong type."""

    with pytest.raises(TypeError):

        SubjectResolver().resolve(

            "not a visual intent",  # type: ignore[arg-type]

            identity="Azrael",

        )

def test_resolver_does_not_invent_subject_attributes() -> None:

    """Unspecified subject information should remain unspecified."""

    intent = VisualIntent()

    result = SubjectResolver().resolve(

        intent,

        identity="Unknown Subject",

    )

    subject = result.resolved_subjects[0]

    assert subject.identity == "Unknown Subject"

    assert subject.type is None

    assert subject.species is None

    assert subject.physical_attributes == {}

    assert subject.clothing == {}

    assert subject.equipment == {}

    assert subject.pose == {}

    assert subject.expression is None

    assert subject.action is None

def test_resolver_assigns_unique_subject_ids() -> None:

    """Newly registered subjects should receive unique IDs."""

    intent = VisualIntent()

    first = SubjectResolver().resolve(

        intent,

        identity="First",

    )

    second = SubjectResolver().resolve(

        intent,

        identity="Second",

    )

    assert first.resolved_subjects[0].id != second.resolved_subjects[0].id

    assert first.resolved_subjects[0].id != uuid4()