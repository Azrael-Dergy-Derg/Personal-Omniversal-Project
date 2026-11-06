"""Tests for the OIPM version metadata model."""

from __future__ import annotations

import pytest

from oipm.versioning.version_metadata import (

    VersionKind,

    VersionMetadata,

)

def test_version_metadata_can_be_created() -> None:

    metadata = VersionMetadata(

        version_id="version-001",

        kind=VersionKind.VISUAL_INTENT,

    )

    assert metadata.version_id == "version-001"

    assert metadata.kind is VersionKind.VISUAL_INTENT

    assert metadata.created_by == "oipm"

def test_version_metadata_supports_parent_version() -> None:

    metadata = VersionMetadata(

        version_id="version-002",

        kind=VersionKind.STATE,

        parent_version_id="version-001",

    )

    assert metadata.parent_version_id == "version-001"

def test_version_metadata_preserves_provenance() -> None:

    metadata = VersionMetadata(

        version_id="version-003",

        kind=VersionKind.PROMPT,

        created_by="prompt_assembler",

        description="Initial assembled prompt.",

        source="visual_intent:version-001",

    )

    assert metadata.created_by == "prompt_assembler"

    assert metadata.description == "Initial assembled prompt."

    assert metadata.source == "visual_intent:version-001"

@pytest.mark.parametrize(

    "kind",

    [

        VersionKind.VISUAL_INTENT,

        VersionKind.PROMPT,

        VersionKind.STATE,

        VersionKind.ANALYSIS,

        VersionKind.REFINEMENT,

        VersionKind.GENERATOR_OUTPUT,

    ],

)

def test_version_metadata_accepts_all_version_kinds(

    kind: VersionKind,

) -> None:

    metadata = VersionMetadata(

        version_id=f"version-{kind.value}",

        kind=kind,

    )

    assert metadata.kind is kind

def test_empty_version_id_is_rejected() -> None:

    with pytest.raises(ValueError):

        VersionMetadata(

            version_id="",

            kind=VersionKind.STATE,

        )

def test_empty_created_by_is_rejected() -> None:

    with pytest.raises(ValueError):

        VersionMetadata(

            version_id="version-004",

            kind=VersionKind.STATE,

            created_by="",

        )

def test_empty_parent_version_id_is_rejected() -> None:

    with pytest.raises(ValueError):

        VersionMetadata(

            version_id="version-005",

            kind=VersionKind.STATE,

            parent_version_id="",

        )

def test_empty_description_is_rejected() -> None:

    with pytest.raises(ValueError):

        VersionMetadata(

            version_id="version-006",

            kind=VersionKind.STATE,

            description="",

        )

def test_empty_source_is_rejected() -> None:

    with pytest.raises(ValueError):

        VersionMetadata(

            version_id="version-007",

            kind=VersionKind.STATE,

            source="",

        )

def test_version_metadata_is_immutable() -> None:

    metadata = VersionMetadata(

        version_id="version-008",

        kind=VersionKind.STATE,

    )

    with pytest.raises((AttributeError, TypeError)):

        metadata.version_id = "changed"  # type: ignore[misc]