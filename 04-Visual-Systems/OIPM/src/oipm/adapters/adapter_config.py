"""Generator adapter configuration model for OIPM.

This module defines the generator-neutral configuration metadata used by

the Generator Adaptation Layer (GAL).

Adapter configuration describes what a generator adapter supports. It does

not perform adaptation, prompt assembly, interpretation, reasoning, or

generator selection.

The configuration exists separately from GeneratorAdapter so that adapter

capabilities can be inspected without executing an adapter.

"""

from __future__ import annotations

from dataclasses import dataclass

from typing import FrozenSet

@dataclass(frozen=True)

class AdapterConfig:

    """Immutable configuration metadata for a generator adapter.

    Attributes:

        generator: Stable machine-readable generator identifier.

        display_name: Human-readable generator name.

        supported_parameters: Generator-specific parameter names that the

            adapter can represent.

        supported_features: Generator-specific prompt or visual features

            that the adapter can represent.

        notes: Optional descriptive notes about the adapter configuration.

    AdapterConfig describes capability only. It must not contain runtime

    VisualIntent data or generated prompt content.

    """

    generator: str

    display_name: str

    supported_parameters: FrozenSet[str] = frozenset()

    supported_features: FrozenSet[str] = frozenset()

    notes: str | None = None

    def __post_init__(self) -> None:

        """Validate required configuration identifiers."""

        if not self.generator:

            raise ValueError("generator must not be empty")

        if not self.display_name:

            raise ValueError("display_name must not be empty")

    def supports_parameter(self, parameter: str) -> bool:

        """Return whether the adapter declares support for a parameter."""

        return parameter in self.supported_parameters

    def supports_feature(self, feature: str) -> bool:

        """Return whether the adapter declares support for a feature."""

        return feature in self.supported_features