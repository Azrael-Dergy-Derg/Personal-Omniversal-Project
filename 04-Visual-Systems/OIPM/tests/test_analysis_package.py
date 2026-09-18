"""Tests for the OIPM IAFIS analysis package exports."""

from __future__ import annotations

import oipm.analysis as analysis

def test_analysis_package_exports_observation_models() -> None:

    assert analysis.AnalysisObservation is not None

    assert analysis.ObservationConfidence is not None

    assert analysis.ObservationSource is not None

def test_analysis_package_exports_analysis_batch() -> None:

    assert analysis.AnalysisBatch is not None

def test_analysis_package_exports_feedback_models() -> None:

    assert analysis.FeedbackItem is not None

    assert analysis.FeedbackSource is not None

    assert analysis.FeedbackType is not None

    assert analysis.FeedbackBatch is not None

def test_analysis_package_exports_interpretation_models() -> None:

    assert analysis.FeedbackInterpretation is not None

    assert analysis.InterpretationInput is not None

    assert analysis.InterpretationType is not None

def test_analysis_package_exports_interpreter() -> None:

    assert analysis.AnalysisInterpreter is not None

def test_analysis_package_all_contains_public_api() -> None:

    expected = {

        "AnalysisBatch",

        "AnalysisInterpreter",

        "AnalysisObservation",

        "FeedbackBatch",

        "FeedbackInterpretation",

        "FeedbackItem",

        "FeedbackSource",

        "FeedbackType",

        "InterpretationInput",

        "InterpretationType",

        "ObservationConfidence",

        "ObservationSource",

    }

    assert set(analysis.__all__) == expected