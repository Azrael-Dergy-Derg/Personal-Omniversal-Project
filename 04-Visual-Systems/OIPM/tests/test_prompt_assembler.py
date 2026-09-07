"""Tests for the OIPM PromptAssembler."""

from __future__ import annotations

import pytest

from oipm.assembly.prompt_assembler import PromptAssembler

from oipm.models import (

    ArtisticDirection,

    Attribute,

    Constraint,

    Lighting,

    Priority,

    Scene,

    Source,

    Subject,

    VisualIntent,

)

def test_assembler_creates_prompt_from_subject() -> None:

    """A defined subject should appear in the assembled prompt."""

    subject = Subject(

        identity="Azrael",

        type="character",

        species="dragon",

    )

    intent = VisualIntent(subjects=[subject])

    prompt = PromptAssembler().assemble(intent)

    assert "Azrael character dragon" in prompt

def test_assembler_includes_subject_attributes() -> None:

    """Explicit subject attributes should be preserved."""

    subject = Subject(

        identity="Azrael",

        type="character",

        species="dragon",

        physical_attributes={

            "scale_color": Attribute(

                value="matte black",

                source=Source.CANON,

                priority=Priority.CRITICAL,

            )

        },

    )

    intent = VisualIntent(subjects=[subject])

    prompt = PromptAssembler().assemble(intent)

    assert "matte black" in prompt

def test_assembler_includes_scene_information() -> None:

    """Explicit scene information should appear in the prompt."""

    intent = VisualIntent(

        scene=Scene(

            location="ancient ruined fortress",

            time="night",

            weather="rain",

            environmental_conditions=["wet stone"],

        )

    )

    prompt = PromptAssembler().assemble(intent)

    assert "ancient ruined fortress" in prompt

    assert "night" in prompt

    assert "rain" in prompt

    assert "wet stone" in prompt

def test_assembler_includes_composition_information() -> None:

    """Explicit composition information should be preserved."""

    intent = VisualIntent()

    intent.composition.shot_type = "full-body shot"

    intent.composition.perspective = "low-angle perspective"

    intent.composition.depth_of_field = "shallow depth of field"

    prompt = PromptAssembler().assemble(intent)

    assert "full-body shot" in prompt

    assert "low-angle perspective" in prompt

    assert "shallow depth of field" in prompt

def test_assembler_includes_lighting_information() -> None:

    """Explicit lighting information should be preserved."""

    intent = VisualIntent(

        lighting=Lighting(

            intent="dramatic moonlight",

            direction="side lighting",

            intensity="low intensity",

            quality="soft light",

            atmosphere=["misty atmosphere"],

        )

    )

    prompt = PromptAssembler().assemble(intent)

    assert "dramatic moonlight" in prompt

    assert "side lighting" in prompt

    assert "low intensity" in prompt

    assert "soft light" in prompt

    assert "misty atmosphere" in prompt

def test_assembler_includes_artistic_direction() -> None:

    """Explicit artistic direction should be preserved."""

    intent = VisualIntent(

        artistic_direction=ArtisticDirection(

            medium="digital painting",

            realism="semi-realistic",

            linework="bold inked contours",

            shading="controlled cel-shading",

            texture="rich textured brushwork",

        )

    )

    prompt = PromptAssembler().assemble(intent)

    assert "digital painting" in prompt

    assert "semi-realistic" in prompt

    assert "bold inked contours" in prompt

    assert "controlled cel-shading" in prompt

    assert "rich textured brushwork" in prompt

def test_assembler_includes_constraints() -> None:

    """Explicit constraints should be preserved."""

    intent = VisualIntent(

        constraints=[

            Constraint(

                type="exclusion",

                requirement="no modern technology",

            ),

            Constraint(

                type="requirement",

                requirement="preserve canonical appearance",

            ),

        ]

    )

    prompt = PromptAssembler().assemble(intent)

    assert "no modern technology" in prompt

    assert "preserve canonical appearance" in prompt

def test_assembler_combines_sections_deterministically() -> None:

    """Prompt sections should be assembled in a stable order."""

    subject = Subject(

        identity="Azrael",

        type="character",

        species="dragon",

    )

    intent = VisualIntent(

        subjects=[subject],

        scene=Scene(location="ruined fortress"),

        lighting=Lighting(intent="moonlight"),

    )

    prompt = PromptAssembler().assemble(intent)

    assert prompt.index("Subjects:") < prompt.index("Scene:")

    assert prompt.index("Scene:") < prompt.index("Lighting:")

def test_assembler_returns_empty_prompt_for_empty_intent() -> None:

    """An empty VisualIntent should produce an empty prompt."""

    intent = VisualIntent()

    prompt = PromptAssembler().assemble(intent)

    assert prompt == ""

def test_assembler_rejects_non_visual_intent_input() -> None:

    """The assembler should reject objects of the wrong type."""

    assembler = PromptAssembler()

    with pytest.raises(TypeError):

        assembler.assemble("not a visual intent")  # type: ignore[arg-type]

def test_assembler_does_not_invent_unspecified_information() -> None:

    """The assembler should only emit information present in VisualIntent."""

    subject = Subject(

        identity="Azrael",

        species="dragon",

    )

    intent = VisualIntent(subjects=[subject])

    prompt = PromptAssembler().assemble(intent)

    assert "Azrael" in prompt

    assert "dragon" in prompt

    assert "moonlight" not in prompt

    assert "armor" not in prompt

    assert "castle" not in prompt

    assert "cinematic" not in prompt

def test_assembler_preserves_multiple_subjects() -> None:

    """Multiple explicitly defined subjects should remain distinguishable."""

    first = Subject(

        identity="Azrael",

        species="dragon",

    )

    second = Subject(

        identity="Vilona",

        species="kobold",

    )

    intent = VisualIntent(

        subjects=[first, second],

    )

    prompt = PromptAssembler().assemble(intent)

    assert "Azrael" in prompt

    assert "dragon" in prompt

    assert "Vilona" in prompt

    assert "kobold" in prompt