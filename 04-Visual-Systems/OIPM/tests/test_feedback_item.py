"""Tests for the OIPM IAFIS feedback item model."""

from __future__ import annotations

import pytest

from oipm.analysis.feedback_item import (

    FeedbackItem,

    FeedbackSource,

    FeedbackType,

)

def test_feedback_item_can_be_created() -> None:

    feedback = FeedbackItem(

        feedback_id="feedback-001",

        source=FeedbackSource.USER,

        feedback_type=FeedbackType.CORRECTION,

        target="azrael",

        message="The character's mantle should remain visible.",

    )

    assert feedback.feedback_id == "feedback-001"

    assert feedback.source is FeedbackSource.USER

    assert feedback.feedback_type is FeedbackType.CORRECTION

    assert feedback.target == "azrael"

    assert feedback.message == (

        "The character's mantle should remain visible."

    )

def test_feedback_item_supports_optional_evidence() -> None:

    feedback = FeedbackItem(

        feedback_id="feedback-002",

        source=FeedbackSource.EXTERNAL_EVALUATOR,

        feedback_type=FeedbackType.PROBLEM,

        target="composition",

        message="The subject is too close to the frame edge.",

        evidence="The right side of the subject is visibly cropped.",

    )

    assert feedback.evidence == (

        "The right side of the subject is visibly cropped."

    )

def test_feedback_item_supports_optional_confidence() -> None:

    feedback = FeedbackItem(

        feedback_id="feedback-003",

        source=FeedbackSource.ANALYSIS_PROCESS,

        feedback_type=FeedbackType.OBSERVATION,

        target="lighting",

        message="The lighting appears directional.",

        confidence="medium",

    )

    assert feedback.confidence == "medium"

def test_feedback_item_allows_no_target() -> None:

    feedback = FeedbackItem(

        feedback_id="feedback-004",

        source=FeedbackSource.USER,

        feedback_type=FeedbackType.PREFERENCE,

        target=None,

        message="Keep the overall visual style consistent.",

    )

    assert feedback.target is None

def test_feedback_item_rejects_empty_id() -> None:

    with pytest.raises(ValueError):

        FeedbackItem(

            feedback_id="",

            source=FeedbackSource.USER,

            feedback_type=FeedbackType.CORRECTION,

            target="azrael",

            message="Change the armor.",

        )

def test_feedback_item_rejects_empty_message() -> None:

    with pytest.raises(ValueError):

        FeedbackItem(

            feedback_id="feedback-005",

            source=FeedbackSource.USER,

            feedback_type=FeedbackType.CORRECTION,

            target="azrael",

            message="",

        )

def test_feedback_item_rejects_empty_target() -> None:

    with pytest.raises(ValueError):

        FeedbackItem(

            feedback_id="feedback-006",

            source=FeedbackSource.USER,

            feedback_type=FeedbackType.CORRECTION,

            target="",

            message="Change the armor.",

        )

def test_feedback_item_rejects_empty_evidence() -> None:

    with pytest.raises(ValueError):

        FeedbackItem(

            feedback_id="feedback-007",

            source=FeedbackSource.USER,

            feedback_type=FeedbackType.PROBLEM,

            target="lighting",

            message="The lighting is incorrect.",

            evidence="",

        )

def test_feedback_item_rejects_empty_confidence() -> None:

    with pytest.raises(ValueError):

        FeedbackItem(

            feedback_id="feedback-008",

            source=FeedbackSource.ANALYSIS_PROCESS,

            feedback_type=FeedbackType.OBSERVATION,

            target="composition",

            message="Composition differs from the requested framing.",

            confidence="",

        )

def test_feedback_item_is_immutable() -> None:

    feedback = FeedbackItem(

        feedback_id="feedback-009",

        source=FeedbackSource.USER,

        feedback_type=FeedbackType.PRESERVATION,

        target="azrael",

        message="Preserve established character identity.",

    )

    with pytest.raises((AttributeError, TypeError)):

        feedback.message = "Changed."  # type: ignore[misc]