"""Core processing pipeline for the Omniversal Image Prompt Maker (OIPM).

The OIPMPipeline coordinates the currently implemented OIPM processing

stages without allowing any individual stage to redefine upstream intent.

Current pipeline:

    Raw User Input

        ↓

    InputInterpreter

        ↓

    VisualIntent

        ↓

    VisualIntentValidator

        ↓

    PromptAssembler

        ↓

    Prompt

This implementation represents the initial OIPM vertical slice.

Additional interpretation, reasoning, resolution, analysis, refinement,

and generator-adaptation stages will be integrated as they are built.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.assembly import PromptAssembler

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

        assembler: PromptAssembler | None = None,

    ) -> None:

        """Initialize the pipeline with its processing components."""

        self.interpreter = interpreter or InputInterpreter()

        self.validator = validator or VisualIntentValidator()

        self.assembler = assembler or PromptAssembler()

    def process(

        self,

        user_input: str,

        *,

        project: str | None = None,

        scene_id: str | None = None,

    ) -> PipelineResult:

        """Process raw user input through the current OIPM pipeline.

        Args:

            user_input: The user's original image-generation request.

            project: Optional project identifier.

            scene_id: Optional scene identifier.

        Returns:

            A PipelineResult containing interpretation, validation,

            and assembled prompt output.

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

        prompt = ""

        if validation.valid:

            prompt = self.assembler.assemble(

                interpretation.visual_intent

            )

        return PipelineResult(

            interpretation=interpretation,

            validation=validation,

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