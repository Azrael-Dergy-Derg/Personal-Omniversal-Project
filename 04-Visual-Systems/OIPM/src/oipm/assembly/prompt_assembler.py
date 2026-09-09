"""Prompt assembly for the Omniversal Image Prompt Maker (OIPM).

The PromptAssembler converts structured VisualIntent data into a

deterministic natural-language image-generation prompt.

PAOE is intentionally downstream of interpretation, validation, subject

resolution, scene construction, composition, lighting, artistic direction,

and constraint processing.

This implementation:

- treats VisualIntent as the authoritative source of truth

- preserves explicitly supplied structured information

- emits deterministic output

- preserves section ordering

- includes structured composition and lighting data

- preserves constraint metadata when useful to the prompt

- does not invent unspecified visual information

- does not resolve ambiguity

- does not alter canon

- does not make independent artistic decisions

- does not apply generator-specific syntax

- does not optimize for a specific image generator

Generator-specific optimization belongs to the Generator Adaptation Layer

(GAL), which is downstream of PAOE.

"""

from __future__ import annotations

from typing import Any

from oipm.models import Attribute, VisualIntent

class PromptAssembler:

    """Assemble a deterministic prompt from an OIPM VisualIntent."""

    name = "PromptAssembler"

    version = "0.2.0"

    def assemble(self, visual_intent: VisualIntent) -> str:

        """Convert a VisualIntent into a deterministic prompt.

        Args:

            visual_intent: The structured source-of-truth representation.

        Returns:

            A natural-language image-generation prompt.

        Raises:

            TypeError: If visual_intent is not a VisualIntent instance.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent instance."

            )

        sections: list[str] = []

        subject_section = self._assemble_subjects(visual_intent)

        if subject_section:

            sections.append(subject_section)

        scene_section = self._assemble_scene(visual_intent)

        if scene_section:

            sections.append(scene_section)

        composition_section = self._assemble_composition(visual_intent)

        if composition_section:

            sections.append(composition_section)

        lighting_section = self._assemble_lighting(visual_intent)

        if lighting_section:

            sections.append(lighting_section)

        artistic_section = self._assemble_artistic_direction(

            visual_intent

        )

        if artistic_section:

            sections.append(artistic_section)

        constraint_section = self._assemble_constraints(visual_intent)

        if constraint_section:

            sections.append(constraint_section)

        return " ".join(sections)

    @staticmethod

    def _assemble_subjects(visual_intent: VisualIntent) -> str:

        """Assemble explicitly defined subject information."""

        subject_descriptions: list[str] = []

        for subject in visual_intent.subjects:

            parts: list[str] = []

            if subject.identity:

                parts.append(subject.identity)

            if subject.type:

                parts.append(subject.type)

            if subject.species:

                parts.append(subject.species)

            parts.extend(

                PromptAssembler._attribute_values(

                    subject.physical_attributes

                )

            )

            parts.extend(

                PromptAssembler._attribute_values(

                    subject.clothing

                )

            )

            parts.extend(

                PromptAssembler._attribute_values(

                    subject.equipment

                )

            )

            if subject.expression:

                parts.append(str(subject.expression.value))

            if subject.action:

                parts.append(str(subject.action.value))

            if subject.spatial_position:

                parts.append(

                    PromptAssembler._format_mapping(

                        subject.spatial_position

                    )

                )

            if parts:

                subject_descriptions.append(" ".join(parts))

        if not subject_descriptions:

            return ""

        return "Subjects: " + "; ".join(subject_descriptions) + "."

    @staticmethod

    def _assemble_scene(visual_intent: VisualIntent) -> str:

        """Assemble explicitly defined scene information."""

        scene = visual_intent.scene

        parts: list[str] = []

        if scene.location:

            parts.append(scene.location)

        parts.extend(scene.structural_elements)

        parts.extend(scene.surface_properties)

        parts.extend(scene.environmental_conditions)

        if scene.time:

            parts.append(scene.time)

        if scene.weather:

            parts.append(scene.weather)

        if scene.narrative_context:

            parts.append(scene.narrative_context)

        parts.extend(scene.supporting_elements)

        parts.extend(scene.visual_story_cues)

        if not parts:

            return ""

        return "Scene: " + ", ".join(parts) + "."

    @staticmethod

    def _assemble_composition(visual_intent: VisualIntent) -> str:

        """Assemble explicitly defined composition information."""

        composition = visual_intent.composition

        parts: list[str] = []

        if composition.shot_type:

            parts.append(composition.shot_type)

        if composition.camera_position:

            parts.append(

                PromptAssembler._format_mapping(

                    composition.camera_position

                )

            )

        if composition.perspective:

            parts.append(composition.perspective)

        if composition.subject_placement:

            parts.append(

                PromptAssembler._format_mapping(

                    composition.subject_placement

                )

            )

        if composition.focal_hierarchy:

            parts.append(

                "focal hierarchy: "

                + ", ".join(str(item) for item in composition.focal_hierarchy)

            )

        if composition.foreground:

            parts.append(

                "foreground: "

                + ", ".join(composition.foreground)

            )

        if composition.midground:

            parts.append(

                "midground: "

                + ", ".join(composition.midground)

            )

        if composition.background:

            parts.append(

                "background: "

                + ", ".join(composition.background)

            )

        if composition.depth_of_field:

            parts.append(composition.depth_of_field)

        if composition.motion:

            parts.append(

                PromptAssembler._format_mapping(

                    composition.motion

                )

            )

        if composition.negative_space:

            parts.append(composition.negative_space)

        if not parts:

            return ""

        return "Composition: " + ", ".join(parts) + "."

    @staticmethod

    def _assemble_lighting(visual_intent: VisualIntent) -> str:

        """Assemble explicitly defined lighting information."""

        lighting = visual_intent.lighting

        parts: list[str] = []

        if lighting.intent:

            parts.append(lighting.intent)

        if lighting.sources:

            parts.append(

                "sources: "

                + "; ".join(

                    PromptAssembler._format_mapping(source)

                    for source in lighting.sources

                )

            )

        if lighting.direction:

            parts.append(lighting.direction)

        if lighting.intensity:

            parts.append(lighting.intensity)

        if lighting.quality:

            parts.append(lighting.quality)

        if lighting.color_temperature:

            parts.append(lighting.color_temperature)

        if lighting.shadows:

            parts.append(

                PromptAssembler._format_mapping(

                    lighting.shadows

                )

            )

        parts.extend(lighting.atmosphere)

        parts.extend(lighting.environmental_interaction)

        if not parts:

            return ""

        return "Lighting: " + ", ".join(parts) + "."

    @staticmethod

    def _assemble_artistic_direction(

        visual_intent: VisualIntent,

    ) -> str:

        """Assemble explicitly defined artistic direction."""

        artistic = visual_intent.artistic_direction

        parts: list[str] = []

        if artistic.medium:

            parts.append(artistic.medium)

        if artistic.realism:

            parts.append(artistic.realism)

        if artistic.stylization:

            parts.append(artistic.stylization)

        if artistic.linework:

            parts.append(artistic.linework)

        if artistic.shading:

            parts.append(artistic.shading)

        if artistic.texture:

            parts.append(artistic.texture)

        if artistic.color_treatment:

            parts.append(artistic.color_treatment)

        if artistic.detail_distribution:

            parts.append(artistic.detail_distribution)

        if artistic.edge_hierarchy:

            parts.append(artistic.edge_hierarchy)

        if artistic.surface_rendering:

            parts.append(artistic.surface_rendering)

        if not parts:

            return ""

        return "Artistic direction: " + ", ".join(parts) + "."

    @staticmethod

    def _assemble_constraints(visual_intent: VisualIntent) -> str:

        """Assemble explicitly defined image constraints."""

        constraints: list[str] = []

        for constraint in visual_intent.constraints:

            parts: list[str] = []

            if constraint.type:

                parts.append(constraint.type)

            if constraint.target:

                parts.append("target=" + constraint.target)

            if constraint.requirement:

                parts.append(constraint.requirement)

            if constraint.resolution:

                parts.append("resolution=" + constraint.resolution)

            if parts:

                constraints.append(" ".join(parts))

        if not constraints:

            return ""

        return "Constraints: " + "; ".join(constraints) + "."

    @staticmethod

    def _attribute_values(

        attributes: dict[str, Attribute],

    ) -> list[str]:

        """Extract attribute values without inventing additional detail."""

        return [

            str(attribute.value)

            for attribute in attributes.values()

            if attribute.value is not None

        ]

    @staticmethod

    def _format_mapping(values: dict[str, Any]) -> str:

        """Format structured values deterministically.

        Dictionary insertion order is preserved by Python, while keys are

        explicitly sorted here so equivalent mappings produce stable prompt

        output regardless of construction order.

        Values are rendered using their existing representation only. This

        helper does not infer or expand information.

        """

        if not values:

            return ""

        items = [

            f"{key}={values[key]}"

            for key in sorted(values)

        ]

        return ", ".join(items)