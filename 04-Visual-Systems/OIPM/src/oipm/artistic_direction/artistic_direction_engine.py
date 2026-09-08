"""Artistic Direction and Rendering Engine for OIPM.

The Artistic Direction and Rendering Engine (ADRE) is responsible for

organizing explicitly supplied artistic and rendering information within

a VisualIntent.

The initial implementation is intentionally conservative. It does not

invent artistic mediums, realism levels, stylization, linework, shading,

texture, color treatment, detail distribution, edge hierarchy, surface

rendering, or other visual decisions that were not explicitly provided.

VisualIntent remains the source of truth.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import VisualIntent

@dataclass(frozen=True)

class ArtisticDirectionResult:

    """Result produced by the Artistic Direction and Rendering Engine."""

    visual_intent: VisualIntent

    artistic_direction: object

    warnings: tuple[str, ...] = ()

class ArtisticDirectionEngine:

    """Conservatively construct artistic and rendering direction."""

    def construct(

        self,

        visual_intent: VisualIntent,

        *,

        medium: str | None = None,

        realism: str | None = None,

        stylization: str | None = None,

        linework: str | None = None,

        shading: str | None = None,

        texture: str | None = None,

        color_treatment: str | None = None,

        detail_distribution: str | None = None,

        edge_hierarchy: str | None = None,

        surface_rendering: str | None = None,

    ) -> ArtisticDirectionResult:

        """Apply explicitly supplied artistic direction.

        Existing values are preserved when a supplied value conflicts with

        an existing value. No unspecified artistic or rendering

        information is invented.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent instance")

        artistic_direction = visual_intent.artistic_direction

        warnings: list[str] = []

        supplied_values = {

            "medium": medium,

            "realism": realism,

            "stylization": stylization,

            "linework": linework,

            "shading": shading,

            "texture": texture,

            "color_treatment": color_treatment,

            "detail_distribution": detail_distribution,

            "edge_hierarchy": edge_hierarchy,

            "surface_rendering": surface_rendering,

        }

        for field_name, supplied_value in supplied_values.items():

            if supplied_value is None:

                continue

            existing_value = getattr(artistic_direction, field_name)

            if existing_value is None:

                setattr(artistic_direction, field_name, supplied_value)

                continue

            if existing_value != supplied_value:

                warnings.append(

                    f"Existing artistic direction {field_name} conflicts "

                    f"with supplied {field_name}; existing value was "

                    f"preserved."

                )

        return ArtisticDirectionResult(

            visual_intent=visual_intent,

            artistic_direction=artistic_direction,

            warnings=tuple(warnings),

        )