"""Lighting and Atmosphere Engine for OIPM.

The Lighting and Atmosphere Engine (LAE) is responsible for organizing

explicitly supplied lighting and atmospheric information within a

VisualIntent.

The initial implementation is intentionally conservative. It does not

invent light sources, lighting direction, color temperature, intensity,

contrast, atmospheric effects, volumetric effects, weather interaction,

or other visual decisions that were not explicitly provided.

VisualIntent remains the source of truth.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import VisualIntent

@dataclass(frozen=True)

class LightingResult:

    """Result produced by the Lighting and Atmosphere Engine."""

    visual_intent: VisualIntent

    lighting: object

    warnings: tuple[str, ...] = ()

class LightingEngine:

    """Conservatively construct lighting and atmosphere information."""

    def construct(

        self,

        visual_intent: VisualIntent,

        *,

        light_source: str | None = None,

        direction: str | None = None,

        intensity: str | None = None,

        color_temperature: str | None = None,

        contrast: str | None = None,

        atmospheric_effects: str | None = None,

        volumetric_effects: str | None = None,

        environmental_interaction: str | None = None,

    ) -> LightingResult:

        """Apply explicitly supplied lighting information.

        Existing values are preserved when a supplied value conflicts with

        an existing value. No unspecified lighting or atmospheric

        information is invented.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent instance")

        lighting = visual_intent.lighting

        warnings: list[str] = []

        supplied_values = {

            "light_source": light_source,

            "direction": direction,

            "intensity": intensity,

            "color_temperature": color_temperature,

            "contrast": contrast,

            "atmospheric_effects": atmospheric_effects,

            "volumetric_effects": volumetric_effects,

            "environmental_interaction": environmental_interaction,

        }

        for field_name, supplied_value in supplied_values.items():

            if supplied_value is None:

                continue

            existing_value = getattr(lighting, field_name)

            if existing_value is None:

                setattr(lighting, field_name, supplied_value)

                continue

            if existing_value != supplied_value:

                warnings.append(

                    f"Existing lighting {field_name} conflicts with "

                    f"supplied {field_name}; existing value was preserved."

                )

        return LightingResult(

            visual_intent=visual_intent,

            lighting=lighting,

            warnings=tuple(warnings),

        )