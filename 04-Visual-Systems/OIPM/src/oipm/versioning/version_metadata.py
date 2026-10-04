"""Version metadata for the OIPM Prompt & State Versioning System.

PSVS tracks structured state and generated representations over time.

Version metadata provides identity and provenance information for a version

without treating the versioned representation itself as the authoritative

source of creative intent.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

class VersionKind(str, Enum):

    """Kind of versioned OIPM artifact."""

    VISUAL_INTENT = "visual_intent"

    PROMPT = "prompt"

    STATE = "state"

    ANALYSIS = "analysis"

    REFINEMENT = "refinement"

    GENERATOR_OUTPUT = "generator_output"

@dataclass(frozen=True)

class VersionMetadata:

    """Immutable identity and provenance metadata for one version.

    Attributes:

        version_id: Unique identifier for the version.

        kind: Type of artifact represented by the version.

        parent_version_id: Optional immediate predecessor.

        created_by: Identifier for the process or actor that created it.

        description: Optional human-readable description.

        source: Optional provenance description.

    """

    version_id: str

    kind: VersionKind

    parent_version_id: str | None = None

    created_by: str = "oipm"

    description: str | None = None

    source: str | None = None

    def __post_init__(self) -> None:

        """Validate the structural requirements of version metadata."""

        if not self.version_id.strip():

            raise ValueError(

                "version_id must not be empty"

            )

        if not self.created_by.strip():

            raise ValueError(

                "created_by must not be empty"

            )

        if (

            self.parent_version_id is not None

            and not self.parent_version_id.strip()

        ):

            raise ValueError(

                "parent_version_id must be non-empty when provided"

            )

        if (

            self.description is not None

            and not self.description.strip()

        ):

            raise ValueError(

                "description must be non-empty when provided"

            )

        if self.source is not None and not self.source.strip():

            raise ValueError(

                "source must be non-empty when provided"

            )