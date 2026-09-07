"""Natural-language input interpretation for OIPM.

The Input Interpreter is responsible for establishing the initial

structured VisualIntent from user-provided creative input.

This first implementation intentionally performs only conservative

normalization and metadata initialization. Advanced semantic

interpretation, canon resolution, ambiguity detection, and AI-assisted

extraction belong to later OIPM engines.

"""

from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime, timezone

from oipm.models import VisualIntent

@dataclass(frozen=True)

class InterpretationResult:

    """Result produced by the input interpretation stage."""

    visual_intent: VisualIntent

    warnings: tuple[str, ...] = ()

class InputInterpreter:

    """Convert raw user input into an initial VisualIntent.

    The interpreter establishes the structured source-of-truth object

    without prematurely inventing visual details that were not supplied

    by the user.

    """

    name = "InputInterpreter"

    version = "0.1.0"

    def process(

        self,

        user_input: str,

        *,

        project: str | None = None,

        scene_id: str | None = None,

    ) -> InterpretationResult:

        """Interpret raw user input into a VisualIntent.

        Args:

            user_input: The user's original image-generation request.

            project: Optional project identifier.

            scene_id: Optional scene identifier.

        Returns:

            An InterpretationResult containing the initial VisualIntent.

        Raises:

            ValueError: If user_input is empty or contains only whitespace.

        """

        normalized_input = self._normalize_input(user_input)

        visual_intent = VisualIntent()

        visual_intent.metadata.user_input = normalized_input

        visual_intent.metadata.project = project

        visual_intent.metadata.scene_id = scene_id

        visual_intent.metadata.modified_at = datetime.now(timezone.utc)

        warnings = self._collect_initial_warnings(normalized_input)

        return InterpretationResult(

            visual_intent=visual_intent,

            warnings=tuple(warnings),

        )

    def validate(self, result: InterpretationResult) -> list[str]:

        """Validate the interpreter's output.

        This method performs only interpreter-level validation.

        Comprehensive schema, consistency, ambiguity, and constraint

        validation belongs to later OIPM systems.

        """

        errors: list[str] = []

        if not result.visual_intent.metadata.user_input.strip():

            errors.append("VisualIntent contains no user input.")

        if not result.visual_intent.metadata.intent_id:

            errors.append("VisualIntent is missing an intent ID.")

        return errors

    @staticmethod

    def _normalize_input(user_input: str) -> str:

        """Perform conservative normalization of user input."""

        if not isinstance(user_input, str):

            raise ValueError("user_input must be a string.")

        normalized = " ".join(user_input.split())

        if not normalized:

            raise ValueError("user_input cannot be empty.")

        return normalized

    @staticmethod

    def _collect_initial_warnings(user_input: str) -> list[str]:

        """Identify conditions that may require later interpretation.

        These warnings do not modify the user's intent and do not

        constitute ambiguity resolution.

        """

        warnings: list[str] = []

        if len(user_input) < 10:

            warnings.append(

                "Input is very short and may require additional "

                "interpretation or clarification."

            )

        return warnings