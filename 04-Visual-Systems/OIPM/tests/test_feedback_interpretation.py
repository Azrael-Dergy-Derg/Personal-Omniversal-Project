"""Tests for the OIPM IAFIS feedback interpretation models."""

from __future__ import annotations

import pytest

from oipm.analysis.analysis_observation import (

    AnalysisObservation,

    ObservationConfidence,

    ObservationSource,

)

from oipm.analysis.feedback_interpretation import (

    FeedbackInterpretation,

    InterpretationInput,

    InterpretationType,

)

from oipm.analysis.feedback_item import (

    FeedbackItem,

    FeedbackSource,

    FeedbackType,

)

def make_observation() -> AnalysisObservation:

    return AnalysisObservation(

        observation_id="obs-001",

        source=ObservationSource.IMAGE,

        subject="azrael",

        attribute="mantle",

        value="dark hooded garment is visible",

        confidence=ObservationConfidence.HIGH,

    )

def make_feedback() -> FeedbackItem:

    return FeedbackItem(

        feedback_id="feedback-001",

        source=FeedbackSource.USER,

        feedback_type=FeedbackType.PRESERVATION,

        target="mantle",

        message="Keep the mantle visible.",

    )

def test_feedback_interpretation_can_be_created() -> None:

    interpretation = FeedbackInterpretation(

        interpretation_id="interp-001",

        interpretation_type=InterpretationType.MATCH,

        target="mantle",

        summary="Observed evidence agrees with the requested mantle.",

    )

    assert interpretation.interpretation_id == "interp-001"

    assert interpretation.interpretation_type is InterpretationType.MATCH

    assert interpretation.target == "mantle"

    assert interpretation.summary == (

        "Observed evidence agrees with the requested mantle."

    )

def test_feedback_interpretation_preserves_evidence_ids() -> None:

    interpretation = FeedbackInterpretation(

        interpretation_id="interp-002",

        interpretation_type=InterpretationType.CONSISTENT,

        target="azrael",

        summary="The observed identity remains visually consistent.",

        observation_ids=("obs-001", "obs-002"),

        feedback_ids=("feedback-001",),

    )

    assert interpretation.observation_ids == (

        "obs-001",

        "obs-002",

    )

    assert interpretation.feedback_ids == (

        "feedback-001",

    )

def test_feedback_interpretation_supports_confidence() -> None:

    interpretation = FeedbackInterpretation(

        interpretation_id="interp-003",

        interpretation_type=InterpretationType.MISMATCH,

        target="composition",

        summary="Observed framing differs from the requested framing.",

        confidence="medium",

    )

    assert interpretation.confidence == "medium"

def test_feedback_interpretation_requires_reasoning_by_default() -> None:

    interpretation = FeedbackInterpretation(

        interpretation_id="interp-004",

        interpretation_type=InterpretationType.POTENTIAL_CONFLICT,

        target="lighting",

        summary="Evidence suggests a possible lighting conflict.",

    )

    assert interpretation.requires_reasoning is True

def test_feedback_interpretation_can_mark_reasoning_as_not_required() -> None:

    interpretation = FeedbackInterpretation(

        interpretation_id="interp-005",

        interpretation_type=InterpretationType.CONSISTENT,

        target="lighting",

        summary="Lighting appears consistent with the requested intent.",

        requires_reasoning=False,

    )

    assert interpretation.requires_reasoning is False

def test_empty_interpretation_id_is_rejected() -> None:

    with pytest.raises(ValueError):

        FeedbackInterpretation(

            interpretation_id="",

            interpretation_type=InterpretationType.UNKNOWN,

            target="lighting",

            summary="Unknown lighting state.",

        )

def test_empty_target_is_rejected() -> None:

    with pytest.raises(ValueError):

        FeedbackInterpretation(

            interpretation_id="interp-006",

            interpretation_type=InterpretationType.UNKNOWN,

            target="",

            summary="Unknown state.",

        )

def test_empty_summary_is_rejected() -> None:

    with pytest.raises(ValueError):

        FeedbackInterpretation(

            interpretation_id="interp-007",

            interpretation_type=InterpretationType.UNKNOWN,

            target="lighting",

            summary="",

        )

def test_empty_observation_id_is_rejected() -> None:

    with pytest.raises(ValueError):

        FeedbackInterpretation(

            interpretation_id="interp-008",

            interpretation_type=InterpretationType.MATCH,

            target="mantle",

            summary="Evidence matches.",

            observation_ids=("obs-001", ""),

        )

def test_empty_feedback_id_is_rejected() -> None:

    with pytest.raises(ValueError):

        FeedbackInterpretation(

            interpretation_id="interp-009",

            interpretation_type=InterpretationType.MATCH,

            target="mantle",

            summary="Feedback agrees with evidence.",

            feedback_ids=("feedback-001", ""),

        )

def test_empty_confidence_is_rejected() -> None:

    with pytest.raises(ValueError):

        FeedbackInterpretation(

            interpretation_id="interp-010",

            interpretation_type=InterpretationType.UNKNOWN,

            target="lighting",

            summary="Unknown lighting state.",

            confidence="",

        )

def test_interpretation_input_can_be_created() -> None:

    observation = make_observation()

    feedback = make_feedback()

    evidence = InterpretationInput(

        observations=(observation,),

        feedback=(feedback,),

    )

    assert evidence.observations == (observation,)

    assert evidence.feedback == (feedback,)

def test_interpretation_input_can_be_empty() -> None:

    evidence = InterpretationInput()

    assert evidence.observations == ()

    assert evidence.feedback == ()

def test_interpretation_input_rejects_invalid_observation() -> None:

    with pytest.raises(TypeError):

        InterpretationInput(

            observations=(object(),),  # type: ignore[arg-type]

        )

def test_interpretation_input_rejects_invalid_feedback() -> None:

    with pytest.raises(TypeError):

        InterpretationInput(

            feedback=(object(),),  # type: ignore[arg-type]

        )

def test_feedback_interpretation_is_immutable() -> None:

    interpretation = FeedbackInterpretation(

        interpretation_id="interp-011",

        interpretation_type=InterpretationType.MATCH,

        target="mantle",

        summary="Evidence matches.",

    )

    with pytest.raises((AttributeError, TypeError)):

        interpretation.summary = "Changed."  # type: ignore[misc]

def test_interpretation_input_is_immutable() -> None:

    evidence = InterpretationInput(

        observations=(make_observation(),),

    )

    with pytest.raises((AttributeError, TypeError)):

        evidence.observations = ()  # type: ignore[misc]