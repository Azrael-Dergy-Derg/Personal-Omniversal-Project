"""Reference generator adapter for OIPM.

This module provides a minimal concrete GeneratorAdapter implementation

used to establish and test the concrete-adapter pattern.

It is intentionally not tied to any external image-generation service.

"""

from __future__ import annotations

from oipm.adapters.generator_adapter import (

    GeneratorAdapter,

    GeneratorAdapterResult,

)

from oipm.models import VisualIntent

class StubGeneratorAdapter(GeneratorAdapter):

    """Minimal concrete adapter for development and testing.

    This adapter demonstrates the expected shape of a generator-specific

    implementation without introducing generator-specific behavior into

    the core OIPM pipeline.

    """

    @property

    def generator_name(self) -> str:

        """Return the stable identifier for this adapter."""

        return "stub-generator"

    def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

        """Adapt VisualIntent into a minimal generator representation.

        The adapter performs no interpretation or visual invention. It

        simply demonstrates the concrete GeneratorAdapter contract.

        """

        self._validate_input(visual_intent)

        return GeneratorAdapterResult(

            generator=self.generator_name,

            prompt="stub prompt",

            parameters={},

            warnings=[],

        )