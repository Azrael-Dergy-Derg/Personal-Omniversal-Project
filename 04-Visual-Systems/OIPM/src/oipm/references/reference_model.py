"""Reference data model for the OIPM Reference & Consistency System.

This module defines the structured representation of a visual reference.

References provide evidence or guidance to OIPM. They are not themselves

canon, VisualIntent, or authoritative truth.

The Reference & Consistency System (RCS) may later use these objects to

compare references against VisualIntent, identify inconsistencies, and

support controlled visual continuity.

A reference must never silently:

- become canon,

- overwrite VisualIntent,

- invent missing information,

- resolve conflicts without an explicit rule,

- or redefine user intent.

"""

from __future__ import annotations

from dataclasses import dataclass, field

from enum import Enum

from typing import FrozenSet

class ReferenceType(str, Enum):

    """Classification of what a reference primarily represents."""

    CHARACTER = "character"

    ENVIRONMENT = "environment"

    PROP = "prop"

    POSE = "pose"

    COMPOSITION = "composition"

    LIGHTING = "lighting"

    COLOR = "color"

    MATERIAL = "material"

    STYLE = "style"

    ANATOMY = "anatomy"

    COSTUME = "costume"

    GENERAL = "general"

class ReferenceRole(str, Enum):

    """Role a reference plays during visual consistency processing."""

    IDENTITY = "identity"

    APPEARANCE = "appearance"

    ANATOMY = "anatomy"

    CLOTHING = "clothing"

    EQUIPMENT = "equipment"

    POSE = "pose"

    COMPOSITION = "composition"

    LIGHTING = "lighting"

    STYLE = "style"

    COLOR = "color"

    ENVIRONMENT = "environment"

    MATERIAL = "material"

    INSPIRATION = "inspiration"

    CONTINUITY = "continuity"

@dataclass(frozen=True)

class Reference:

    """Immutable structured metadata describing a visual reference.

    Attributes:

        reference_id: Stable identifier for the reference.

        reference_type: Primary category represented by the reference.

        source: Origin or description of where the reference came from.

        roles: Visual consistency roles served by the reference.

        description: Optional human-readable description.

        tags: Optional searchable descriptors.

        authoritative: Whether the reference has been explicitly

            designated as authoritative for its stated purpose.

        notes: Optional additional context.

    Authoritative means authoritative *for the stated reference purpose*.

    It does not grant the reference authority over VisualIntent, canon, or

    unrelated visual attributes.

    """

    reference_id: str

    reference_type: ReferenceType

    source: str

    roles: FrozenSet[ReferenceRole] = field(default_factory=frozenset)

    description: str | None = None

    tags: FrozenSet[str] = field(default_factory=frozenset)

    authoritative: bool = False

    notes: str | None = None

    def __post_init__(self) -> None:

        """Validate required reference identifiers."""

        if not self.reference_id:

            raise ValueError("reference_id must not be empty")

        if not self.source:

            raise ValueError("source must not be empty")

    def serves_role(self, role: ReferenceRole) -> bool:

        """Return whether this reference serves the requested role."""

        return role in self.roles

    def has_tag(self, tag: str) -> bool:

        """Return whether the reference contains the supplied tag."""

        return tag in self.tags