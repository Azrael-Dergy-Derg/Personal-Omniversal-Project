from __future__ import annotations

from datetime import datetime, timezone

from enum import Enum

from typing import Any

from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

class Source(str, Enum):

    """Identifies where a piece of visual information originated."""

    EXPLICIT_USER = "explicit_user"

    SCENE_OVERRIDE = "scene_override"

    CANON = "canon"

    REFERENCE = "reference"

    PROJECT_DATA = "project_data"

    INFERENCE = "inference"

    GENERATOR_REQUIREMENT = "generator_requirement"

class Confidence(str, Enum):

    """Represents OIPM's confidence in an interpreted value."""

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"

class Priority(str, Enum):

    """Represents the importance of preserving a piece of information."""

    CRITICAL = "critical"

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"

class AttributeStatus(str, Enum):

    """Represents the current state of an attribute."""

    LOCKED = "locked"

    REQUIRED = "required"

    PREFERRED = "preferred"

    OPTIONAL = "optional"

    UNKNOWN = "unknown"

    CONFLICTING = "conflicting"

    DEPRECATED = "deprecated"

class CanonStatus(str, Enum):

    """Represents the relationship between subject data and project canon."""

    CANONICAL = "canonical"

    VARIABLE = "variable"

    SCENE_STATE = "scene_state"

    NON_CANON = "non_canon"

    UNKNOWN = "unknown"

class Attribute(BaseModel):

    """A structured visual attribute with provenance and priority."""

    model_config = ConfigDict(extra="forbid")

    value: Any

    source: Source

    confidence: Confidence = Confidence.HIGH

    priority: Priority = Priority.MEDIUM

    status: AttributeStatus = AttributeStatus.REQUIRED

    override: bool = False

class Relationship(BaseModel):

    """Represents a relationship between two subjects."""

    model_config = ConfigDict(extra="forbid")

    subject_a: UUID

    subject_b: UUID

    type: str

    direction: str | None = None

    intensity: str | None = None

    spatial_relation: str | None = None

    visual_evidence: list[str] = Field(default_factory=list)

class Subject(BaseModel):

    """Represents a subject or entity appearing in an intended image."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)

    identity: str | None = None

    type: str | None = None

    species: str | None = None

    physical_attributes: dict[str, Attribute] = Field(default_factory=dict)

    clothing: dict[str, Attribute] = Field(default_factory=dict)

    equipment: dict[str, Attribute] = Field(default_factory=dict)

    pose: dict[str, Attribute] = Field(default_factory=dict)

    expression: Attribute | None = None

    action: Attribute | None = None

    spatial_position: dict[str, Attribute] = Field(default_factory=dict)

    relationships: list[UUID] = Field(default_factory=list)

    canon_status: CanonStatus = CanonStatus.UNKNOWN

    references: list[UUID] = Field(default_factory=list)

    scene_overrides: dict[str, Attribute] = Field(default_factory=dict)

class Scene(BaseModel):

    """Represents the environment and contextual conditions of an image."""

    model_config = ConfigDict(extra="forbid")

    location: str | None = None

    structural_elements: list[str] = Field(default_factory=list)

    surface_properties: list[str] = Field(default_factory=list)

    environmental_conditions: list[str] = Field(default_factory=list)

    time: str | None = None

    weather: str | None = None

    narrative_context: str | None = None

    supporting_elements: list[str] = Field(default_factory=list)

    visual_story_cues: list[str] = Field(default_factory=list)

class Composition(BaseModel):

    """Represents camera, framing, spatial arrangement, and visual hierarchy."""

    model_config = ConfigDict(extra="forbid")

    shot_type: str | None = None

    camera_position: dict[str, Any] = Field(default_factory=dict)

    perspective: str | None = None

    subject_placement: dict[str, Any] = Field(default_factory=dict)

    focal_hierarchy: list[UUID] = Field(default_factory=list)

    foreground: list[str] = Field(default_factory=list)

    midground: list[str] = Field(default_factory=list)

    background: list[str] = Field(default_factory=list)

    depth_of_field: str | None = None

    motion: dict[str, Any] = Field(default_factory=dict)

    negative_space: str | None = None

class Lighting(BaseModel):

    """Represents lighting, shadows, atmosphere, and environmental interaction."""

    model_config = ConfigDict(extra="forbid")

    intent: str | None = None

    sources: list[dict[str, Any]] = Field(default_factory=list)

    direction: str | None = None

    intensity: str | None = None

    quality: str | None = None

    color_temperature: str | None = None

    shadows: dict[str, Any] = Field(default_factory=dict)

    atmosphere: list[str] = Field(default_factory=list)

    environmental_interaction: list[str] = Field(default_factory=list)

class ArtisticDirection(BaseModel):

    """Represents the intended artistic and rendering direction."""

    model_config = ConfigDict(extra="forbid")

    medium: str | None = None

    realism: str | None = None

    stylization: str | None = None

    linework: str | None = None

    shading: str | None = None

    texture: str | None = None

    color_treatment: str | None = None

    detail_distribution: str | None = None

    edge_hierarchy: str | None = None

    surface_rendering: str | None = None

class Constraint(BaseModel):

    """Represents a requirement, exclusion, or other image constraint."""

    model_config = ConfigDict(extra="forbid")

    type: str

    target: str | None = None

    requirement: str

    priority: Priority = Priority.HIGH

    source: Source = Source.EXPLICIT_USER

    resolution: str | None = None

class Reference(BaseModel):

    """Represents an authorized reference and the information it provides."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)

    type: str

    source: str

    authorization: str | None = None

    influence: dict[str, Any] = Field(default_factory=dict)

    attributes_provided: list[str] = Field(default_factory=list)

    priority: Priority = Priority.MEDIUM

    conflicts: list[str] = Field(default_factory=list)

class GeneratorTarget(BaseModel):

    """Represents the intended image-generation target."""

    model_config = ConfigDict(extra="forbid")

    generator: str | None = None

    model: str | None = None

    capabilities: list[str] = Field(default_factory=list)

    desired_aspect_ratio: str | None = None

    output_requirements: dict[str, Any] = Field(default_factory=dict)

    adapter_version: str | None = None

class State(BaseModel):

    """Represents versioning, approval, and canon-impact state."""

    model_config = ConfigDict(extra="forbid")

    version: str = "0.1.0"

    parent_version: str | None = None

    branch: str = "main"

    status: str = "draft"

    approval: str | None = None

    canon_impact: str | None = None

    change_history: list[dict[str, Any]] = Field(default_factory=list)

class Metadata(BaseModel):

    """Tracking metadata for a VisualIntent instance."""

    model_config = ConfigDict(extra="forbid")

    intent_id: UUID = Field(default_factory=uuid4)

    created_at: datetime = Field(

        default_factory=lambda: datetime.now(timezone.utc)

    )

    modified_at: datetime = Field(

        default_factory=lambda: datetime.now(timezone.utc)

    )

    oipm_version: str = "0.1.0"

    user_input: str = ""

    project: str | None = None

    scene_id: str | None = None

class VisualIntent(BaseModel):

    """Source-of-truth representation of an intended image.

    VisualIntent is the central structured data model used by OIPM.

    It represents visual intent independently from any particular

    image-generation model or prompt syntax. Prompt text is generated

    from this structured representation and is not itself the source

    of truth.

    """

    model_config = ConfigDict(extra="forbid")

    metadata: Metadata = Field(default_factory=Metadata)

    subjects: list[Subject] = Field(default_factory=list)

    relationships: list[Relationship] = Field(default_factory=list)

    scene: Scene = Field(default_factory=Scene)

    composition: Composition = Field(default_factory=Composition)

    lighting: Lighting = Field(default_factory=Lighting)

    artistic_direction: ArtisticDirection = Field(

        default_factory=ArtisticDirection

    )

    constraints: list[Constraint] = Field(default_factory=list)

    references: list[Reference] = Field(default_factory=list)

    generator_target: GeneratorTarget = Field(

        default_factory=GeneratorTarget

    )

    state: State = Field(default_factory=State)