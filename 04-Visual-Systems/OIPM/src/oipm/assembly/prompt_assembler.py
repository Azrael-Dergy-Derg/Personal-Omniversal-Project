"""Prompt assembly for the Omniversal Image Prompt Maker (OIPM).

The PromptAssembler converts structured VisualIntent data into a

deterministic natural-language image-generation prompt.

This initial implementation is intentionally conservative. It does not:

- invent unspecified visual information

- resolve ambiguity

- alter canon

- make independent artistic decisions

- apply generator-specific syntax

- optimize prompts for a specific image model

Those responsibilities belong to later OIPM systems.

"""

from __future__ import annotations

from oipm.models import Attribute, VisualIntent

class PromptAssembler:

    """Assemble a prompt from an OIPM VisualIntent."""

    name = "PromptAssembler"

    version = "0.1.0"

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

            if parts:

                subject_descriptions.append(

                    " ".join(parts)

                )

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

        if composition.perspective:

            parts.append(composition.perspective)

        if composition.depth_of_field:

            parts.append(composition.depth_of_field)

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

        if lighting.direction:

            parts.append(lighting.direction)

        if lighting.intensity:

            parts.append(lighting.intensity)

        if lighting.quality:

            parts.append(lighting.quality)

        if lighting.color_temperature:

            parts.append(lighting.color_temperature)

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

        requirements: list[str] = []

        for constraint in visual_intent.constraints:

            requirements.append(constraint.requirement)

        if not requirements:

            return ""

        return "Constraints: " + "; ".join(requirements) + "."

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