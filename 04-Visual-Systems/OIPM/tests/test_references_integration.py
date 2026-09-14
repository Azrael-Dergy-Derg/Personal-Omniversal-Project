"""Integration tests for the OIPM Reference & Consistency System."""

from __future__ import annotations

from oipm.models import VisualIntent

from oipm.references import (

    ComparisonStatus,

    Reference,

    ReferenceConsistencySystem,

    ReferenceRole,

    ReferenceType,

)

def make_visual_intent() -> VisualIntent:

    """Create a minimal valid VisualIntent."""

    return VisualIntent(

        user_input="Create a dark-fantasy character portrait.",

    )

def make_reference() -> Reference:

    """Create a representative style reference."""

    return Reference(

        reference_id="dark-fantasy-reference",

        reference_type=ReferenceType.STYLE,

        source="test-reference-source",

        roles=frozenset(

            {

                ReferenceRole.STYLE,

                ReferenceRole.CONTINUITY,

            }

        ),

        description="Dark-fantasy graphic-novel rendering.",

        tags=frozenset(

            {

                "dark-fantasy",

                "graphic-novel",

            }

        ),

    )

def test_complete_rcs_match_flow() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark-fantasy graphic-novel rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "dark-fantasy",

        "graphic-novel",

    ]

    system.register(reference)

    analysis = system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert analysis.reference_id == "dark-fantasy-reference"

    assert len(analysis.structural_findings) == 2

    assert all(

        finding.matchable

        for finding in analysis.structural_findings

    )

    assert len(analysis.comparison_findings) == 2

    assert all(

        finding.status is ComparisonStatus.MATCH

        for finding in analysis.comparison_findings

    )

    assert analysis.conflict_report.conflict_count == 0

def test_complete_rcs_mismatch_flow() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Photorealistic cinematic rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "photorealistic",

        "cinematic",

    ]

    system.register(reference)

    analysis = system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert len(analysis.comparison_findings) == 2

    assert all(

        finding.status is ComparisonStatus.MISMATCH

        for finding in analysis.comparison_findings

    )

    assert analysis.conflict_report.conflict_count == 2

def test_complete_rcs_unavailable_flow() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    system.register(reference)

    analysis = system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert len(analysis.comparison_findings) == 2

    assert all(

        finding.status is ComparisonStatus.UNAVAILABLE

        for finding in analysis.comparison_findings

    )

    assert analysis.conflict_report.conflict_count == 0

def test_rcs_does_not_modify_visual_intent() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Existing description."

    )

    visual_intent.metadata["reference_tags"] = [

        "existing-tag",

    ]

    original_description = visual_intent.metadata[

        "reference_description"

    ]

    original_tags = list(

        visual_intent.metadata["reference_tags"]

    )

    system.register(reference)

    system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert visual_intent.metadata["reference_description"] == (

        original_description

    )

    assert visual_intent.metadata["reference_tags"] == original_tags

def test_rcs_does_not_modify_reference() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    original_description = reference.description

    original_tags = reference.tags

    original_roles = reference.roles

    system.register(reference)

    system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert reference.description == original_description

    assert reference.tags == original_tags

    assert reference.roles == original_roles

def test_rcs_does_not_resolve_conflicts() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Completely different rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "unrelated-style",

    ]

    original_description = visual_intent.metadata[

        "reference_description"

    ]

    original_tags = list(

        visual_intent.metadata["reference_tags"]

    )

    system.register(reference)

    analysis = system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert analysis.conflict_report.conflict_count == 2

    assert visual_intent.metadata["reference_description"] == (

        original_description

    )

    assert visual_intent.metadata["reference_tags"] == original_tags

def test_rcs_supports_multiple_references() -> None:

    system = ReferenceConsistencySystem()

    style_reference = make_reference()

    environment_reference = Reference(

        reference_id="environment-reference",

        reference_type=ReferenceType.ENVIRONMENT,

        source="environment-source",

        roles=frozenset(

            {

                ReferenceRole.ENVIRONMENT,

            }

        ),

        description="Ancient fortress environment.",

        tags=frozenset(

            {

                "fortress",

            }

        ),

    )

    system.register(style_reference)

    system.register(environment_reference)

    assert system.ids() == (

        "dark-fantasy-reference",

        "environment-reference",

    )

    visual_intent = make_visual_intent()

    style_analysis = system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    environment_analysis = system.analyze(

        "environment-reference",

        visual_intent,

    )

    assert (

        style_analysis.reference_id

        == "dark-fantasy-reference"

    )

    assert (

        environment_analysis.reference_id

        == "environment-reference"

    )

def test_rcs_preserves_reference_and_visual_intent_separation() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    visual_intent = make_visual_intent()

    system.register(reference)

    analysis = system.analyze(

        "dark-fantasy-reference",

        visual_intent,

    )

    assert analysis.reference_id == reference.reference_id

    assert reference is system.get("dark-fantasy-reference")

    assert visual_intent.user_input == (

        "Create a dark-fantasy character portrait."

    )