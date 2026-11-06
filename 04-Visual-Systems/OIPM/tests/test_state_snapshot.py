"""Tests for the OIPM state snapshot model."""

from __future__ import annotations

from copy import deepcopy

import pytest

from oipm.models import VisualIntent

from oipm.versioning.state_snapshot import StateSnapshot

from oipm.versioning.version_metadata import (

    VersionKind,

    VersionMetadata,

)

def make_visual_intent() -> VisualIntent:

    return VisualIntent(

        metadata={

            "project": "Personal Omniversal Project",

            "scene_id": "snapshot-test",

        },

    )

def make_metadata(

    kind: VersionKind = VersionKind.VISUAL_INTENT,

) -> VersionMetadata:

    return VersionMetadata(

        version_id="version-001",

        kind=kind,

    )

def test_state_snapshot_can_be_created() -> None:

    snapshot = StateSnapshot(

        metadata=make_metadata(),

        state={"scene": {"location": "forest"}},

    )

    assert snapshot.metadata.version_id == "version-001"

    assert snapshot.state["scene"]["location"] == "forest"

def test_state_snapshot_accepts_state_version_kind() -> None:

    snapshot = StateSnapshot(

        metadata=make_metadata(VersionKind.STATE),

        state={"status": "recorded"},

    )

    assert snapshot.metadata.kind is VersionKind.STATE

def test_state_snapshot_rejects_incompatible_version_kind() -> None:

    with pytest.raises(ValueError):

        StateSnapshot(

            metadata=make_metadata(VersionKind.PROMPT),

            state={"prompt": "example"},

        )

def test_state_snapshot_rejects_invalid_metadata() -> None:

    with pytest.raises(TypeError):

        StateSnapshot(

            metadata=object(),  # type: ignore[arg-type]

            state={},

        )

def test_state_snapshot_rejects_non_dictionary_state() -> None:

    with pytest.raises(TypeError):

        StateSnapshot(

            metadata=make_metadata(),

            state=[],  # type: ignore[arg-type]

        )

def test_from_visual_intent_creates_snapshot() -> None:

    visual_intent = make_visual_intent()

    snapshot = StateSnapshot.from_visual_intent(

        visual_intent,

        make_metadata(),

    )

    assert snapshot.state == visual_intent.model_dump(mode="json")

def test_from_visual_intent_rejects_invalid_visual_intent() -> None:

    with pytest.raises(TypeError):

        StateSnapshot.from_visual_intent(

            object(),  # type: ignore[arg-type]

            make_metadata(),

        )

def test_from_visual_intent_rejects_invalid_metadata() -> None:

    with pytest.raises(TypeError):

        StateSnapshot.from_visual_intent(

            make_visual_intent(),

            object(),  # type: ignore[arg-type]

        )

def test_snapshot_does_not_share_nested_state_with_input() -> None:

    original_state = {

        "scene": {

            "location": "forest",

            "weather": ["rain", "fog"],

        },

    }

    snapshot = StateSnapshot(

        metadata=make_metadata(),

        state=original_state,

    )

    original_state["scene"]["location"] = "desert"

    original_state["scene"]["weather"].append("snow")

    assert snapshot.state["scene"]["location"] == "forest"

    assert snapshot.state["scene"]["weather"] == ["rain", "fog"]

def test_to_dict_returns_an_independent_copy() -> None:

    snapshot = StateSnapshot(

        metadata=make_metadata(),

        state={

            "scene": {

                "location": "forest",

            },

        },

    )

    exported = snapshot.to_dict()

    exported["scene"]["location"] = "desert"

    assert snapshot.state["scene"]["location"] == "forest"

def test_to_dict_preserves_nested_values() -> None:

    original_state = {

        "subjects": [

            {"id": "azrael", "species": "dragon"},

        ],

    }

    snapshot = StateSnapshot(

        metadata=make_metadata(),

        state=original_state,

    )

    assert snapshot.to_dict() == deepcopy(original_state)