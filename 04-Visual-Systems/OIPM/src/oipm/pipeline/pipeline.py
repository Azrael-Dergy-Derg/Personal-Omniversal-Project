"""Core processing pipeline for the Omniversal Image Prompt Maker (OIPM).

The pipeline coordinates the current OIPM processing stages while preserving

VisualIntent as the authoritative internal representation.

Current flow:

Raw User Input

    ↓

Input Interpretation

    ↓

Visual Intent Validation

    ↓

Subject Resolution

    ↓

Scene Construction

    ↓

Composition & Camera Construction

    ↓

Lighting & Atmosphere Construction

    ↓

Artistic Direction & Rendering Construction

    ↓

Constraint, Conflict & Consistency Processing

    ↓

Prompt Assembly

    ↓

Pipeline Result

Each subsystem is intentionally conservative. Components may organize or

apply explicitly supplied information, but they must not silently invent

visual decisions or overwrite higher-priority existing information.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.artistic_direction import (

    ArtisticDirectionEngine,

    ArtisticDirectionResult,

)

from oipm.assembly import PromptAssembler

from oipm.composition import CompositionEngine, CompositionResult

from oipm.constraints import ConstraintEngine, ConstraintResult

from oipm.interpretation import InputInterpreter, InterpretationResult

from oipm.lighting import LightingEngine, LightingResult

from oipm.models import Priority, Source, VisualIntent

from oipm.scene import SceneConstructionResult, SceneConstructor

from oipm.subjects import SubjectResolutionResult, SubjectResolver

from oipm.validation import (

    ValidationResult,

    VisualIntentValidator,

)

@dataclass(frozen=True)

class PipelineResult:

    """Complete result produced by the OIPM processing pipeline."""

    visual_intent: VisualIntent

    interpretation: InterpretationResult

    validation: ValidationResult

    subject_resolution: SubjectResolutionResult | None = None

    scene_construction: SceneConstructionResult | None = None

    composition: CompositionResult | None = None

    lighting: LightingResult | None = None

    artistic_direction: ArtisticDirectionResult | None = None

    constraint_processing: ConstraintResult | None = None

    prompt: str = ""

class OIPMPipeline:

    """Coordinate the current OIPM processing stages."""

    def __init__(

        self,

        *,

        interpreter: InputInterpreter | None = None,

        validator: VisualIntentValidator | None = None,

        subject_resolver: SubjectResolver | None = None,

        scene_constructor: SceneConstructor | None = None,

        composition_engine: CompositionEngine | None = None,

        lighting_engine: LightingEngine | None = None,

        artistic_direction_engine: ArtisticDirectionEngine | None = None,

        constraint_engine: ConstraintEngine | None = None,

        assembler: PromptAssembler | None = None,

    ) -> None:

        """Initialize the pipeline with optional component overrides."""

        self.interpreter = interpreter or InputInterpreter()

        self.validator = validator or VisualIntentValidator()

        self.subject_resolver = subject_resolver or SubjectResolver()

        self.scene_constructor = scene_constructor or SceneConstructor()

        self.composition_engine = composition_engine or CompositionEngine()

        self.lighting_engine = lighting_engine or LightingEngine()

        self.artistic_direction_engine = (

            artistic_direction_engine or ArtisticDirectionEngine()

        )

        self.constraint_engine = constraint_engine or ConstraintEngine()

        self.assembler = assembler or PromptAssembler()

    def process(

        self,

        user_input: str,

        *,

        project_id: str | None = None,

        scene_id: str | None = None,

        subject_identity: str | None = None,

        subject_type: str | None = None,

        species: str | None = None,

        location: str | None = None,

        time: str | None = None,

        weather: str | None = None,

        narrative_context: str | None = None,

        framing: str | None = None,

        camera_angle: str | None = None,

        camera_distance: str | None = None,

        lens: str | None = None,

        perspective: str | None = None,

        depth_of_field: str | None = None,

        light_source: str | None = None,

        direction: str | None = None,

        intensity: str | None = None,

        color_temperature: str | None = None,

        contrast: str | None = None,

        atmospheric_effects: str | None = None,

        volumetric_effects: str | None = None,

        environmental_interaction: str | None = None,

        medium: str | None = None,

        realism: str | None = None,

        stylization: str | None = None,

        linework: str | None = None,

        shading: str | None = None,

        texture: str | None = None,

        color_treatment: str | None = None,

        detail_distribution: str | None = None,

        edge_hierarchy: str | None = None,

        surface_rendering: str | None = None,

        constraint_type: str | None = None,

        constraint_target: str | None = None,

        constraint_requirement: str | None = None,

        constraint_priority: Priority = Priority.HIGH,

        constraint_source: Source = Source.EXPLICIT_USER,

        constraint_resolution: str | None = None,

    ) -> PipelineResult:

        """Process user input through the current OIPM pipeline."""

        interpretation = self.interpreter.interpret(

            user_input,

            project_id=project_id,

            scene_id=scene_id,

        )

        visual_intent = interpretation.visual_intent

        validation = self.validator.validate(visual_intent)

        if not validation.is_valid:

            return PipelineResult(

                visual_intent=visual_intent,

                interpretation=interpretation,

                validation=validation,

            )

        subject_resolution = self.subject_resolver.resolve(

            visual_intent,

            identity=subject_identity,

            subject_type=subject_type,

            species=species,

        )

        scene_construction = self.scene_constructor.construct(

            visual_intent,

            location=location,

            time=time,

            weather=weather,

            narrative_context=narrative_context,

        )

        composition = self.composition_engine.construct(

            visual_intent,

            framing=framing,

            camera_angle=camera_angle,

            camera_distance=camera_distance,

            lens=lens,

            perspective=perspective,

            depth_of_field=depth_of_field,

        )

        lighting = self.lighting_engine.construct(

            visual_intent,

            light_source=light_source,

            direction=direction,

            intensity=intensity,

            color_temperature=color_temperature,

            contrast=contrast,

            atmospheric_effects=atmospheric_effects,

            volumetric_effects=volumetric_effects,

            environmental_interaction=environmental_interaction,

        )

        artistic_direction = self.artistic_direction_engine.construct(

            visual_intent,

            medium=medium,

            realism=realism,

            stylization=stylization,

            linework=linework,

            shading=shading,

            texture=texture,

            color_treatment=color_treatment,

            detail_distribution=detail_distribution,

            edge_hierarchy=edge_hierarchy,

            surface_rendering=surface_rendering,

        )

        constraint_processing = self.constraint_engine.construct(

            visual_intent,

            constraint_type=constraint_type,

            target=constraint_target,

            requirement=constraint_requirement,

            priority=constraint_priority,

            source=constraint_source,

            resolution=constraint_resolution,

        )

        prompt = self.assembler.assemble(visual_intent)

        return PipelineResult(

            visual_intent=visual_intent,

            interpretation=interpretation,

            validation=validation,

            subject_resolution=subject_resolution,

            scene_construction=scene_construction,

            composition=composition,

            lighting=lighting,

            artistic_direction=artistic_direction,

            constraint_processing=constraint_processing,

            prompt=prompt,

        )