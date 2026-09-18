"""Tests for the OIPM IAFIS analysis batch model."""

from __future__ import annotations

import pytest

from oipm.analysis.analysis_batch import AnalysisBatch

from oipm.analysis.analysis_observation import (

    AnalysisObservation,

    ObservationConfidence,

    ObservationSource,

)

def make_observation(

    observation_id: str = "obs-001",

) -> AnalysisObservation:

    return AnalysisObservation(

        observation_id=observation_id,

        source=ObservationSource.IMAGE,

        subject="azrael",

        attribute="eye_color",

        value="emerald green",

        confidence=ObservationConfidence.HIGH,

    )

def test_analysis_batch_can_be_created_empty() -> None:

    batch = AnalysisBatch(

        batch_id="batch-001",

    )

    assert batch.batch_id == "batch-001"

    assert batch.observations == ()

    assert batch.observation_count == 0

    assert batch.is_empty is True

def test_analysis_batch_stores_observations() -> None:

    observation = make_observation()

    batch = AnalysisBatch(

        batch_id="batch-002",

        observations=(observation,),

    )

    assert batch.observations == (observation,)

    assert batch.observation_count == 1

    assert batch.is_empty is False

def test_analysis_batch_preserves_source_metadata() -> None:

    batch = AnalysisBatch(

        batch_id="batch-003",

        source_id="generated-image-001",

        notes="Initial visual analysis.",

    )

    assert batch.source_id == "generated-image-001"

    assert batch.notes == "Initial visual analysis."

def test_analysis_batch_rejects_empty_batch_id() -> None:

    with pytest.raises(ValueError):

        AnalysisBatch(

            batch_id="",

        )

def test_analysis_batch_rejects_invalid_observation() -> None:

    with pytest.raises(TypeError):

        AnalysisBatch(

            batch_id="batch-004",

            observations=(object(),),  # type: ignore[arg-type]

        )

def test_analysis_batch_rejects_empty_source_id() -> None:

    with pytest.raises(ValueError):

        AnalysisBatch(

            batch_id="batch-005",

            source_id="",

        )

def test_analysis_batch_rejects_empty_notes() -> None:

    with pytest.raises(ValueError):

        AnalysisBatch(

            batch_id="batch-006",

            notes="",

        )

def test_add_returns_new_batch() -> None:

    original = AnalysisBatch(

        batch_id="batch-007",

    )

    observation = make_observation()

    updated = original.add(observation)

    assert original.observations == ()

    assert original.observation_count == 0

    assert updated.observations == (observation,)

    assert updated.observation_count == 1

def test_add_preserves_batch_metadata() -> None:

    original = AnalysisBatch(

        batch_id="batch-008",

        source_id="image-008",

        notes="Analysis notes.",

    )

    updated = original.add(

        make_observation("obs-008"),

    )

    assert updated.batch_id == original.batch_id

    assert updated.source_id == original.source_id

    assert updated.notes == original.notes

def test_add_rejects_invalid_observation() -> None:

    batch = AnalysisBatch(

        batch_id="batch-009",

    )

    with pytest.raises(TypeError):

        batch.add(object())  # type: ignore[arg-type]

def test_analysis_batch_is_immutable() -> None:

    batch = AnalysisBatch(

        batch_id="batch-010",

        observations=(make_observation(),),

    )

    with pytest.raises((AttributeError, TypeError)):

        batch.batch_id = "changed"  # type: ignore[misc]