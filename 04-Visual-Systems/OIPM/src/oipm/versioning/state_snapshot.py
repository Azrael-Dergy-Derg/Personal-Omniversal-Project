"""Immutable state snapshots for the OIPM versioning system.

A state snapshot captures a particular VisualIntent state for historical

reference and comparison.

Snapshots preserve the distinction between recorded state and current

authoritative creative intent.

"""

from __future__ import annotations

from copy import deepcopy

from dataclasses import dataclass

from typing import Any

from oipm.models import VisualIntent

from oipm.versioning.version_metadata import (

    VersionKind,

    VersionMetadata,

)

@dataclass(frozen=True)

class StateSnapshot:

    """Immutable record of a VisualIntent state.

    Attributes:

        metadata: Identity and provenance information for the snapshot.

        state: Deep-copied structured representation of VisualIntent.

    The snapshot does not modify the original VisualIntent.

    """

    metadata: VersionMetadata

    state: dict[str, Any]

    def __post_init__(self) -> None:

        """Validate and isolate the stored snapshot state."""

        if not isinstance(self.metadata, VersionMetadata):

            raise TypeError(

                "metadata must be VersionMetadata"

            )

        if self.metadata.kind not in (

            VersionKind.VISUAL_INTENT,

            VersionKind.STATE,

        ):

            raise ValueError(

                "metadata kind must be VISUAL_INTENT or STATE"

            )

        if not isinstance(self.state, dict):

            raise TypeError(

                "state must be a dictionary"

            )

        object.__setattr__(

            self,

            "state",

            deepcopy(self.state),

        )

    @classmethod

    def from_visual_intent(

        cls,

        visual_intent: VisualIntent,

        metadata: VersionMetadata,

    ) -> StateSnapshot:

        """Create a snapshot from a VisualIntent instance."""

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent"

            )

        if not isinstance(metadata, VersionMetadata):

            raise TypeError(

                "metadata must be VersionMetadata"

            )

        state = visual_intent.model_dump(mode="json")

        return cls(

            metadata=metadata,

            state=state,

        )

    def to_dict(self) -> dict[str, Any]:

        """Return an independent copy of the recorded state."""

        return deepcopy(self.state)