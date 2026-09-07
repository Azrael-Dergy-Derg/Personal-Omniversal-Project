"""Tests for the OIPM VisualIntentValidator."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from uuid import uuid4

import pytest

from oipm.models import Relationship, Subject, VisualIntent

from oipm.validation.visual_intent_validator import (

    ValidationIssue,

    VisualIntentValidator,

)

def test_valid_visual_intent_passes_validation() -> None:

    """A structurally valid VisualIntent should pass validation."""

    intent = VisualIntent()

    intent.metadata.user_input = "A dark fantasy dragon beneath a moonlit sky."

    result = VisualIntentValidator().validate(intent)

    assert result.valid is True

    assert result.issues == ()

def test_empty_user_input_is_reported() -> None:

    """An empty user input should produce a validation issue."""

    intent = VisualIntent()

    result = VisualIntentValidator().validate(intent)

    assert result.valid is False

    assert any(

        issue.code == "EMPTY_USER_INPUT"

        for issue in result.issues

    )

def test_invalid_metadata_timestamps_are_reported() -> None:

    """created_at later than modified_at should be rejected."""

    intent = VisualIntent()

    intent.metadata.user_input = "A valid image request."

    now = datetime.now(timezone.utc)

    intent.metadata.created_at = now

    intent.metadata.modified_at = now - timedelta(seconds=1)

    result = VisualIntentValidator().validate(intent)

    assert result.valid is False

    assert any(

        issue.code == "INVALID_METADATA_TIMESTAMPS"

        for issue in result.issues

    )

def test_duplicate_subject_ids_are_reported() -> None:

    """Subject IDs must be unique within a VisualIntent."""

    shared_id = uuid4()

    first = Subject(id=shared_id)

    second = Subject(id=shared_id)

    intent = VisualIntent(

        subjects=[first, second],

    )

    intent.metadata.user_input = "Two subjects with duplicated IDs."

    result = VisualIntentValidator().validate(intent)

    assert result.valid is False

    assert any(

        issue.code == "DUPLICATE_SUBJECT_IDS"

        for issue in result.issues

    )

def test_valid_relationship_references_pass_validation() -> None:

    """Relationships referencing existing subjects should pass."""

    first = Subject()

    second = Subject()

    relationship = Relationship(

        subject_a=first.id,

        subject_b=second.id,

        type="ally",

    )

    intent = VisualIntent(

        subjects=[first, second],

        relationships=[relationship],

    )

    intent.metadata.user_input = "Two allied subjects."

    result = VisualIntentValidator().validate(intent)

    assert result.valid is True

    assert result.issues == ()

def test_unknown_relationship_subject_is_reported() -> None:

    """Relationships referencing unknown subjects should fail."""

    first = Subject()

    relationship = Relationship(

        subject_a=first.id,

        subject_b=uuid4(),

        type="ally",

    )

    intent = VisualIntent(

        subjects=[first],

        relationships=[relationship],

    )

    intent.metadata.user_input = "A subject with an invalid relationship."

    result = VisualIntentValidator().validate(intent)

    assert result.valid is False

    matching_issues = [

        issue

        for issue in result.issues

        if issue.code == "UNKNOWN_RELATIONSHIP_SUBJECT"

    ]

    assert len(matching_issues) == 1

    assert matching_issues[0].path == "relationships[0].subject_b"

def test_validator_rejects_non_visual_intent_input() -> None:

    """The validator should reject objects of the wrong type."""

    validator = VisualIntentValidator()

    with pytest.raises(TypeError):

        validator.validate("not a visual intent")  # type: ignore[arg-type]

def test_validation_issue_contains_structured_information() -> None:

    """ValidationIssue should preserve code, message, and path."""

    issue = ValidationIssue(

        code="TEST_ERROR",

        message="Example validation error.",

        path="metadata.user_input",

    )

    assert issue.code == "TEST_ERROR"

    assert issue.message == "Example validation error."

    assert issue.path == "metadata.user_input"