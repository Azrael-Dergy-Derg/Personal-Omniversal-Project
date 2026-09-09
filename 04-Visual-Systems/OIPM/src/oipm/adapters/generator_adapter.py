"""Generator Adaptation Layer interface for OIPM.

This module defines the contract for generator-specific adapters.

The Generator Adaptation Layer (GAL) sits downstream of PAOE and

translates generator-neutral OIPM visual intent into a representation

understood by a specific image-generation system.

Adapters must preserve upstream intent. They must not become a second

interpretation, reasoning, or canon system.

"""

from __future__ import annotations

from abc import ABC, abstractmethod

from dataclasses import dataclass

from typing import Any

from oipm.models import VisualIntent

@dataclass(frozen=True)

class GeneratorAdapterResult:

    """Result produced by a generator-specific adapter.

    Attributes:

        generator: Stable identifier for the target generator.

        prompt: Generator-specific prompt representation.

        parameters: Generator-specific generation parameters.

        warnings: Non-fatal adaptation warnings.

    """

    generator: str

    prompt: str

    parameters: dict[str, Any]

    warnings: list[str]

class GeneratorAdapter(ABC):

    """Abstract interface for OIPM generator adapters.

    Implementations translate an existing VisualIntent into the syntax

    or parameter representation required by a specific generator.

    An adapter must not:

    - invent visual information,

    - modify canon,

    - silently resolve upstream conflicts,

    - replace VisualIntent as the source of truth,

    - reinterpret the user's creative intent,

    - or perform general prompt assembly that belongs to PAOE.

    """

    @property

    @abstractmethod

    def generator_name(self) -> str:

        """Return the stable identifier for the target generator."""

    @abstractmethod

    def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

        """Adapt VisualIntent for the target generator.

        Args:

            visual_intent: Validated, generator-neutral OIPM visual intent.

        Returns:

            GeneratorAdapterResult containing generator-specific output.

        Raises:

            TypeError: If the supplied value is not a VisualIntent.

        """

    def _validate_input(self, visual_intent: VisualIntent) -> None:

        """Validate the adapter input without modifying it.

        This shared guard prevents adapters from accepting arbitrary

        objects and accidentally becoming alternate interpretation layers.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent")