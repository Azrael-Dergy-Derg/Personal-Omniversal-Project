"""Tests for the OIPM IAFIS analysis observation model."""

from __future__ import annotations

import pytest

from oipm.analysis.analysis_observation import (

    AnalysisObservation,

    ObservationConfidence,

    ObservationSource,

)

def test_observation_requires_identifier_attribute_and_value() -> None:

    observation = AnalysisObservation(

        observation_id="obs-001",

        source=ObservationSource.IMAGE,

        subject="azrael",

        attribute="eye_color",

        value="left eye appears emerald green",

    )

    assert observation.observation_id == "obs-001"

    assert observation.subject == "azrael"

    assert observation.attribute == "eye_color"

    assert observation.value == "left eye appears emerald green"

def test_observation_defaults_to_unknown_confidence() -> None:

    observation = AnalysisObservation(

        observation_id="obs-002",

        source=ObservationSource.IMAGE,

        subject=None,

        attribute="weather",

        value="rain appears visible",

    )

    assert observation.confidence is ObservationConfidence.UNKNOWN

def test_observation_accepts_explicit_confidence() -> None:

    observation = AnalysisObservation(

        observation_id="obs-003",

        source=ObservationSource.ANALYSIS_PROCESS,

        subject="azrael",

        attribute="species",

        value="anthropomorphic dragon",

        confidence=ObservationConfidence.HIGH,

    )

    assert observation.confidence is ObservationConfidence.HIGH

def test_observation_preserves_evidence_and_notes() -> None:

    observation = AnalysisObservation(

        observation_id="obs-004",

        source=ObservationSource.IMAGE,

        subject="azrael",

        attribute="mantle",

        value="dark hooded outer garment is visible",

        confidence=ObservationConfidence.MEDIUM,

        evidence="Visible garment surrounding the torso and arms.",

        notes="Hood appears raised.",

    )

    assert observation.evidence == (

        "Visible garment surrounding the torso and arms."

    )

    assert observation.notes == "Hood appears raised."

def test_empty_observation_id_is_rejected() -> None:

    with pytest.raises(ValueError):

        AnalysisObservation(

            observation_id="",

            source=ObservationSource.IMAGE,

            subject=None,

            attribute="lighting",

            value="soft lighting",

        )

def test_empty_attribute_is_rejected() -> None:

    with pytest.raises(ValueError):

        AnalysisObservation(

            observation_id="obs-005",

            source=ObservationSource.IMAGE,

            subject=None,

            attribute="",

            value="soft lighting",

        )

def test_empty_value_is_rejected() -> None:

    with pytest.raises(ValueError):

        AnalysisObservation(

            observation_id="obs-006",

            source=ObservationSource.IMAGE,

            subject=None,

            attribute="lighting",

            value="",

        )

def test_empty_optional_subject_is_rejected() -> None:

    with pytest.raises(ValueError):

        AnalysisObservation(

            observation_id="obs-007",

            source=ObservationSource.IMAGE,

            subject="",

            attribute="lighting",

            value="soft lighting",

        )

def test_empty_optional_evidence_is_rejected() -> None:

    with pytest.raises(ValueError):

        AnalysisObservation(

            observation_id="obs-008",

            source=ObservationSource.IMAGE,

            subject=None,

            attribute="lighting",

            value="soft lighting",

            evidence="",

        )

def test_empty_optional_notes_are_rejected() -> None:

    with pytest.raises(ValueError):

        AnalysisObservation(

            observation_id="obs-009",

            source=ObservationSource.IMAGE,

            subject=None,

            attribute="lighting",

            value="soft lighting",

            notes="",

        )

def test_observation_is_immutable() -> None:

    observation = AnalysisObservation(

        observation_id="obs-010",

        source=ObservationSource.IMAGE,

        subject="azrael",

        attribute="eye_color",

        value="emerald green",

    )

    with pytest.raises((AttributeError, TypeError)):

        observation.value = "crimson red"  # type: ignore[misc]