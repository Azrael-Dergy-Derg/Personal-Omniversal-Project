"""Reference generator adapter for OIPM.

This module provides a minimal concrete GeneratorAdapter implementation

used to establish and test the concrete-adapter pattern.

The adapter intentionally remains generator-neutral and does not represent

a real external image-generation service.

The purpose of this adapter is to demonstrate the Generator Adaptation

Layer boundary:

    VisualIntent -> generator-specific representation

It must not:

- reinterpret visual intent,

- invent visual information,

- modify canon,

- resolve upstream conflicts,

- assemble a production prompt,

- or optimize for a real image generator.

"""

from __future__ import annotations

from oipm.adapters.generator_adapter import (

    GeneratorAdapter,

    GeneratorAdapterResult,

)

from oipm.models import VisualIntent

class StubGeneratorAdapter(GeneratorAdapter):

    """Minimal concrete adapter for development and testing.

    This adapter demonstrates how a concrete generator adapter can

    translate existing VisualIntent data into a deterministic output

    representation without becoming another interpretation or prompt

    assembly layer.

    """

    @property

    def generator_name(self) -> str:

        """Return the stable identifier for this adapter."""

        return "stub-generator"

    def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

        """Adapt VisualIntent into a deterministic test representation.

        The adapter reads existing VisualIntent data only. It does not

        infer missing information, alter the supplied model, or assemble

        a production prompt.

        Args:

            visual_intent: Validated, generator-neutral OIPM visual intent.

        Returns:

            GeneratorAdapterResult containing a deterministic

            generator-neutral test representation.

        Raises:

            TypeError: If the supplied value is not a VisualIntent.

        """

        self._validate_input(visual_intent)

        subject_count = len(visual_intent.subjects)

        has_scene = visual_intent.scene is not None

        has_composition = visual_intent.composition is not None

        has_lighting = visual_intent.lighting is not None

        has_artistic_direction = (

            visual_intent.artistic_direction is not None

        )

        constraint_count = len(visual_intent.constraints)

        prompt = (

            "stub-generator representation: "

            f"subjects={subject_count}; "

            f"scene={has_scene}; "

            f"composition={has_composition}; "

            f"lighting={has_lighting}; "

            f"artistic_direction={has_artistic_direction}; "

            f"constraints={constraint_count}"

        )

        return GeneratorAdapterResult(

            generator=self.generator_name,

            prompt=prompt,

            parameters={

                "subject_count": subject_count,

                "has_scene": has_scene,

                "has_composition": has_composition,

                "has_lighting": has_lighting,

                "has_artistic_direction": has_artistic_direction,

                "constraint_count": constraint_count,

            },

            warnings=[],

        )