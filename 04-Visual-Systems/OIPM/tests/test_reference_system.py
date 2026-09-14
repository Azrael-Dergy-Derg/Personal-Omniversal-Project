"""Tests for the OIPM Reference & Consistency System orchestration layer."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.references import (

    ComparisonStatus,

    Reference,

    ReferenceRegistry,

    ReferenceRole,

    ReferenceType,

)

from oipm.references.reference_system import (

    ReferenceAnalysis,

    ReferenceConsistencySystem,

)

def make_visual_intent() -> VisualIntent:

    """Create a minimal valid VisualIntent."""

    return VisualIntent(

        user_input="Test visual intent",

    )

def make_reference(

    reference_id: str = "test-reference",

    *,

    description: str | None = None,

    tags: frozenset[str] | None = None,

    roles: frozenset[ReferenceRole] | None = None,

) -> Reference:

    """Create a test reference."""

    return Reference(

        reference_id=reference_id,

        reference_type=ReferenceType.GENERAL,

        source="test-source",

        roles=roles or frozenset(),

        description=description,

        tags=tags or frozenset(),

    )

def test_system_creates_empty_registry_by_default() -> None:

    system = ReferenceConsistencySystem()

    assert system.ids() == ()

def test_system_accepts_existing_registry() -> None:

    registry = ReferenceRegistry()

    reference = make_reference("existing-reference")

    registry.register(reference)

    system = ReferenceConsistencySystem(registry)

    assert system.get("existing-reference") is reference

def test_system_rejects_invalid_registry() -> None:

    with pytest.raises(TypeError):

        ReferenceConsistencySystem("not-a-registry")  # type: ignore[arg-type]

def test_system_registers_reference() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    system.register(reference)

    assert system.has("test-reference")

    assert system.get("test-reference") is reference

def test_system_registers_reference_through_registry() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    system.register(reference)

    assert system.registry.get("test-reference") is reference

def test_system_removes_reference() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference()

    system.register(reference)

    removed = system.remove("test-reference")

    assert removed is reference

    assert not system.has("test-reference")

def test_system_lists_reference_ids() -> None:

    system = ReferenceConsistencySystem()

    system.register(make_reference("reference-c"))

    system.register(make_reference("reference-a"))

    system.register(make_reference("reference-b"))

    assert system.ids() == (

        "reference-a",

        "reference-b",

        "reference-c",

    )

def test_system_clears_registry() -> None:

    system = ReferenceConsistencySystem()

    system.register(make_reference("reference-a"))

    system.register(make_reference("reference-b"))

    system.clear()

    assert system.ids() == ()

def test_system_analyzes_registered_reference() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference(

        "style-reference",

        description="Dark-fantasy rendering.",

        tags=frozenset({"dark-fantasy"}),

        roles=frozenset({ReferenceRole.STYLE}),

    )

    system.register(reference)

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark-fantasy rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "dark-fantasy",

    ]

    analysis = system.analyze(

        "style-reference",

        visual_intent,

    )

    assert isinstance(analysis, ReferenceAnalysis)

    assert analysis.reference_id == "style-reference"

    assert len(analysis.structural_findings) == 1

    assert len(analysis.comparison_findings) == 2

    assert analysis.conflict_report.conflict_count == 0

def test_system_reports_mismatch_without_resolving_it() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference(

        "style-reference",

        description="Dark-fantasy rendering.",

        tags=frozenset({"dark-fantasy"}),

        roles=frozenset({ReferenceRole.STYLE}),

    )

    system.register(reference)

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Photorealistic rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "science-fiction",

    ]

    analysis = system.analyze(

        "style-reference",

        visual_intent,

    )

    assert analysis.conflict_report.conflict_count == 2

    assert all(

        finding.status is ComparisonStatus.MISMATCH

        for finding in analysis.comparison_findings

    )

    assert visual_intent.metadata["reference_description"] == (

        "Photorealistic rendering."

    )

    assert visual_intent.metadata["reference_tags"] == [

        "science-fiction",

    ]

def test_system_reports_unavailable_comparison_without_conflict() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference(

        "environment-reference",

        description="Ancient stone fortress.",

        roles=frozenset({ReferenceRole.ENVIRONMENT}),

    )

    system.register(reference)

    analysis = system.analyze(

        "environment-reference",

        make_visual_intent(),

    )

    assert len(analysis.comparison_findings) == 1

    assert (

        analysis.comparison_findings[0].status

        is ComparisonStatus.UNAVAILABLE

    )

    assert analysis.conflict_report.conflict_count == 0

def test_system_rejects_missing_reference() -> None:

    system = ReferenceConsistencySystem()

    with pytest.raises(KeyError):

        system.analyze(

            "missing-reference",

            make_visual_intent(),

        )

def test_system_rejects_invalid_visual_intent() -> None:

    system = ReferenceConsistencySystem()

    system.register(make_reference())

    with pytest.raises(TypeError):

        system.analyze(

            "test-reference",

            "not-a-visual-intent",  # type: ignore[arg-type]

        )

def test_system_analysis_is_immutable() -> None:

    system = ReferenceConsistencySystem()

    system.register(make_reference())

    analysis = system.analyze(

        "test-reference",

        make_visual_intent(),

    )

    with pytest.raises(AttributeError):

        analysis.reference_id = "changed"  # type: ignore[misc]

def test_system_does_not_modify_reference_during_analysis() -> None:

    system = ReferenceConsistencySystem()

    reference = make_reference(

        description="Dark-fantasy dragon.",

        tags=frozenset({"dragon"}),

    )

    system.register(reference)

    visual_intent = make_visual_intent()

    system.analyze(

        "test-reference",

        visual_intent,

    )

    assert reference.reference_id == "test-reference"

    assert reference.description == "Dark-fantasy dragon."

    assert reference.tags == frozenset({"dragon"})

def test_system_uses_shared_registry() -> None:

    registry = ReferenceRegistry()

    system = ReferenceConsistencySystem(registry)

    reference = make_reference()

    system.register(reference)

    assert registry.get("test-reference") is reference

def test_system_can_be_reused_for_multiple_analyses() -> None:

    system = ReferenceConsistencySystem()

    reference_a = make_reference(

        "reference-a",

        description="Dark fantasy.",

    )

    reference_b = make_reference(

        "reference-b",

        description="Science fiction.",

    )

    system.register(reference_a)

    system.register(reference_b)

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = "Dark fantasy."

    analysis_a = system.analyze(

        "reference-a",

        visual_intent,

    )

    analysis_b = system.analyze(

        "reference-b",

        visual_intent,

    )

    assert (

        analysis_a.comparison_findings[0].status

        is ComparisonStatus.MATCH

    )

    assert (

        analysis_b.comparison_findings[0].status

        is ComparisonStatus.MISMATCH

    )