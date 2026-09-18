"""Tests for the OIPM IAFIS feedback batch model."""

from __future__ import annotations

import pytest

from oipm.analysis.feedback_batch import FeedbackBatch

from oipm.analysis.feedback_item import (

    FeedbackItem,

    FeedbackSource,

    FeedbackType,

)

def make_feedback(

    feedback_id: str = "feedback-001",

) -> FeedbackItem:

    return FeedbackItem(

        feedback_id=feedback_id,

        source=FeedbackSource.USER,

        feedback_type=FeedbackType.CORRECTION,

        target="azrael",

        message="Preserve the established character identity.",

    )

def test_feedback_batch_can_be_created_empty() -> None:

    batch = FeedbackBatch(

        batch_id="batch-001",

    )

    assert batch.batch_id == "batch-001"

    assert batch.feedback == ()

    assert batch.feedback_count == 0

    assert batch.is_empty is True

def test_feedback_batch_stores_feedback() -> None:

    feedback = make_feedback()

    batch = FeedbackBatch(

        batch_id="batch-002",

        feedback=(feedback,),

    )

    assert batch.feedback == (feedback,)

    assert batch.feedback_count == 1

    assert batch.is_empty is False

def test_feedback_batch_preserves_source_metadata() -> None:

    batch = FeedbackBatch(

        batch_id="batch-003",

        source_id="generated-image-003",

        notes="User feedback after generation.",

    )

    assert batch.source_id == "generated-image-003"

    assert batch.notes == "User feedback after generation."

def test_feedback_batch_rejects_empty_batch_id() -> None:

    with pytest.raises(ValueError):

        FeedbackBatch(

            batch_id="",

        )

def test_feedback_batch_rejects_invalid_feedback() -> None:

    with pytest.raises(TypeError):

        FeedbackBatch(

            batch_id="batch-004",

            feedback=(object(),),  # type: ignore[arg-type]

        )

def test_feedback_batch_rejects_empty_source_id() -> None:

    with pytest.raises(ValueError):

        FeedbackBatch(

            batch_id="batch-005",

            source_id="",

        )

def test_feedback_batch_rejects_empty_notes() -> None:

    with pytest.raises(ValueError):

        FeedbackBatch(

            batch_id="batch-006",

            notes="",

        )

def test_add_returns_new_batch() -> None:

    original = FeedbackBatch(

        batch_id="batch-007",

    )

    feedback = make_feedback()

    updated = original.add(feedback)

    assert original.feedback == ()

    assert original.feedback_count == 0

    assert updated.feedback == (feedback,)

    assert updated.feedback_count == 1

def test_add_preserves_batch_metadata() -> None:

    original = FeedbackBatch(

        batch_id="batch-008",

        source_id="image-008",

        notes="Feedback notes.",

    )

    updated = original.add(

        make_feedback("feedback-008"),

    )

    assert updated.batch_id == original.batch_id

    assert updated.source_id == original.source_id

    assert updated.notes == original.notes

def test_add_rejects_invalid_feedback() -> None:

    batch = FeedbackBatch(

        batch_id="batch-009",

    )

    with pytest.raises(TypeError):

        batch.add(object())  # type: ignore[arg-type]

def test_feedback_batch_is_immutable() -> None:

    batch = FeedbackBatch(

        batch_id="batch-010",

        feedback=(make_feedback(),),

    )

    with pytest.raises((AttributeError, TypeError)):

        batch.batch_id = "changed"  # type: ignore[misc]