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

Prompt Assembly

    ↓

Pipeline Result

Each subsystem is intentionally conservative. Components may organize or

apply explicitly supplied information, but they must not silently invent

visual decisions or overwrite higher-priority existing information.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.assembly import PromptAssembler

from oipm.composition import CompositionEngine, CompositionResult

from oipm.interpretation import InputInterpreter, InterpretationResult

from oipm.lighting import LightingEngine, LightingResult

from oipm.models import VisualIntent

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

        assembler: PromptAssembler | None = None,

    ) -> None:

        """Initialize the pipeline with optional component overrides."""

        self.interpreter = interpreter or InputInterpreter()

        self.validator = validator or VisualIntentValidator()

        self.subject_resolver = subject_resolver or SubjectResolver()

        self.scene_constructor = scene_constructor or SceneConstructor()

        self.composition_engine = composition_engine or CompositionEngine()

        self.lighting_engine = lighting_engine or LightingEngine()

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

        prompt = self.assembler.assemble(visual_intent)

        return PipelineResult(

            visual_intent=visual_intent,

            interpretation=interpretation,

            validation=validation,

            subject_resolution=subject_resolution,

            scene_construction=scene_construction,

            composition=composition,

            lighting=lighting,

            prompt=prompt,

        )