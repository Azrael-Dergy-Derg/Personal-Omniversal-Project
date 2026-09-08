"""Core processing pipeline for the Omniversal Image Prompt Maker (OIPM).

The OIPMPipeline coordinates OIPM processing stages while preserving

upstream visual intent and structured state.

Current pipeline:

    Raw User Input

        ↓

    InputInterpreter

        ↓

    VisualIntent

        ↓

    VisualIntentValidator

        ↓

    CompositionEngine

        ↓

    PromptAssembler

        ↓

    Prompt

The pipeline is intentionally incremental. Individual visual-intelligence

engines are integrated as they become stable rather than being simulated

through prompt text.

VisualIntent remains the source of truth.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.assembly import PromptAssembler

from oipm.composition import CompositionEngine, CompositionResult

from oipm.interpretation.input_interpreter import (

    InputInterpreter,

    InterpretationResult,

)

from oipm.validation import (

    ValidationIssue,

    ValidationResult,

    VisualIntentValidator,

)

@dataclass(frozen=True)

class PipelineResult:

    """Complete result produced by the current OIPM pipeline."""

    interpretation: InterpretationResult

    validation: ValidationResult

    composition: CompositionResult | None

    prompt: str

class OIPMPipeline:

    """Coordinate the currently implemented OIPM processing stages."""

    name = "OIPMPipeline"

    version = "0.1.0"

    def __init__(

        self,

        *,

        interpreter: InputInterpreter | None = None,

        validator: VisualIntentValidator | None = None,

        composition_engine: CompositionEngine | None = None,

        assembler: PromptAssembler | None = None,

    ) -> None:

        """Initialize the pipeline with its processing components."""

        self.interpreter = interpreter or InputInterpreter()

        self.validator = validator or VisualIntentValidator()

        self.composition_engine = (

            composition_engine or CompositionEngine()

        )

        self.assembler = assembler or PromptAssembler()

    def process(

        self,

        user_input: str,

        *,

        project: str | None = None,

        scene_id: str | None = None,

        framing: str | None = None,

        camera_angle: str | None = None,

        camera_distance: str | None = None,

        lens: str | None = None,

        perspective: str | None = None,

        depth_of_field: str | None = None,

    ) -> PipelineResult:

        """Process raw user input through the current OIPM pipeline.

        Args:

            user_input: The user's original image-generation request.

            project: Optional project identifier.

            scene_id: Optional scene identifier.

            framing: Optional explicit framing instruction.

            camera_angle: Optional explicit camera-angle instruction.

            camera_distance: Optional explicit camera-distance instruction.

            lens: Optional explicit lens instruction.

            perspective: Optional explicit perspective instruction.

            depth_of_field: Optional explicit depth-of-field instruction.

        Returns:

            A PipelineResult containing interpretation, validation,

            composition, and assembled prompt output.

        Raises:

            ValueError: If the input interpreter rejects the user input.

        """

        interpretation = self.interpreter.process(

            user_input,

            project=project,

            scene_id=scene_id,

        )

        validation = self.validator.validate(

            interpretation.visual_intent

        )

        composition: CompositionResult | None = None

        prompt = ""

        if validation.valid:

            composition = self.composition_engine.construct(

                interpretation.visual_intent,

                framing=framing,

                camera_angle=camera_angle,

                camera_distance=camera_distance,

                lens=lens,

                perspective=perspective,

                depth_of_field=depth_of_field,

            )

            prompt = self.assembler.assemble(

                interpretation.visual_intent

            )

        return PipelineResult(

            interpretation=interpretation,

            validation=validation,

            composition=composition,

            prompt=prompt,

        )

    def validate_interpretation(

        self,

        interpretation: InterpretationResult,

    ) -> ValidationResult:

        """Validate an existing interpretation result."""

        return self.validator.validate(

            interpretation.visual_intent

        )

    @staticmethod

    def validation_messages(

        validation: ValidationResult,

    ) -> tuple[str, ...]:

        """Return validation issue messages in stable order."""

        return tuple(

            issue.message

            for issue in validation.issues

        )

    @staticmethod

    def validation_issues(

        validation: ValidationResult,

    ) -> tuple[ValidationIssue, ...]:

        """Return structured validation issues."""

        return validation.issues