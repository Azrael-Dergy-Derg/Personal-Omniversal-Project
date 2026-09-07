class VisualIntent(BaseModel):

    """Source-of-truth representation of an intended image."""

    model_config = ConfigDict(extra="forbid")

    metadata: Metadata = Field(default_factory=Metadata)

    subjects: list[Subject] = Field(default_factory=list)

    relationships: list[Relationship] = Field(default_factory=list)

    scene: Scene = Field(default_factory=Scene)

    composition: Composition = Field(default_factory=Composition)

    lighting: Lighting = Field(default_factory=Lighting)

    artistic_direction: ArtisticDirection = Field(default_factory=ArtisticDirection)

    constraints: list[Constraint] = Field(default_factory=list)

    references: list[Reference] = Field(default_factory=list)

    generator_target: GeneratorTarget = Field(default_factory=GeneratorTarget)

    state: State = Field(default_factory=State)