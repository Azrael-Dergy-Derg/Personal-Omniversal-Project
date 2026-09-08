"""Composition and Camera Engine for OIPM.

The Composition and Camera Engine (CCE) is responsible for organizing

explicitly supplied composition and camera information within a

VisualIntent.

The initial implementation is intentionally conservative. It does not

invent camera choices, framing, lens characteristics, perspective,

subject placement, or other visual decisions that were not explicitly

provided.

VisualIntent remains the source of truth.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import VisualIntent

@dataclass(frozen=True)

class CompositionResult:

    """Result produced by the Composition and Camera Engine."""

    visual_intent: VisualIntent

    composition: object

    warnings: tuple[str, ...] = ()

class CompositionEngine:

    """Conservatively construct composition information."""

    def construct(

        self,

        visual_intent: VisualIntent,

        *,

        framing: str | None = None,

        camera_angle: str | None = None,

        camera_distance: str | None = None,

        lens: str | None = None,

        perspective: str | None = None,

        depth_of_field: str | None = None,

    ) -> CompositionResult:

        """Apply explicitly supplied composition information.

        Existing values are preserved when a supplied value conflicts with

        an existing value. No unspecified composition information is

        invented.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent instance")

        composition = visual_intent.composition

        warnings: list[str] = []

        supplied_values = {

            "framing": framing,

            "camera_angle": camera_angle,

            "camera_distance": camera_distance,

            "lens": lens,

            "perspective": perspective,

            "depth_of_field": depth_of_field,

        }

        for field_name, supplied_value in supplied_values.items():

            if supplied_value is None:

                continue

            existing_value = getattr(composition, field_name)

            if existing_value is None:

                setattr(composition, field_name, supplied_value)

                continue

            if existing_value != supplied_value:

                warnings.append(

                    f"Existing composition {field_name} conflicts with "

                    f"supplied {field_name}; existing value was preserved."

                )

        return CompositionResult(

            visual_intent=visual_intent,

            composition=composition,

            warnings=tuple(warnings),

        )