"""Integration tests for the OIPM Reference & Consistency System."""

from __future__ import annotations

from oipm.models import VisualIntent

from oipm.references import (

    ComparisonStatus,

    ConflictReporter,

    ConsistencyChecker,

    ConsistencyComparator,

    Reference,

    ReferenceRegistry,

    ReferenceRole,

    ReferenceType,

)

def make_visual_intent() -> VisualIntent:

    """Create a minimal VisualIntent for integration testing."""

    return VisualIntent(

        user_input="Test visual intent",

    )

def test_reference_can_flow_through_registry_and_comparison() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="azrael-reference",

        reference_type=ReferenceType.CHARACTER,

        source="approved character reference",

        roles=frozenset(

            {

                ReferenceRole.APPEARANCE,

                ReferenceRole.ANATOMY,

            }

        ),

        description="Adult anthropomorphic dragon.",

        tags=frozenset(

            {

                "dragon",

                "anthropomorphic",

            }

        ),

        authoritative=True,

    )

    registry.register(reference)

    stored_reference = registry.get("azrael-reference")

    assert stored_reference is reference

    visual_intent = make_visual_intent()

    checker = ConsistencyChecker()

    structural_findings = checker.check(

        stored_reference,

        visual_intent,

    )

    assert isinstance(structural_findings, tuple)

def test_reference_can_flow_through_full_comparison_pipeline() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="style-reference",

        reference_type=ReferenceType.STYLE,

        source="approved style reference",

        roles=frozenset({ReferenceRole.STYLE}),

        description="Dark-fantasy graphic-novel rendering.",

        tags=frozenset(

            {

                "dark-fantasy",

                "graphic-novel",

            }

        ),

    )

    registry.register(reference)

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark-fantasy graphic-novel rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "dark-fantasy",

        "graphic-novel",

    ]

    stored_reference = registry.get("style-reference")

    comparator = ConsistencyComparator()

    findings = comparator.compare(

        stored_reference,

        visual_intent,

    )

    assert len(findings) == 2

    assert all(

        finding.status is ComparisonStatus.MATCH

        for finding in findings

    )

    reporter = ConflictReporter()

    report = reporter.build_report(findings)

    assert report.finding_count == 2

    assert report.conflict_count == 0

    assert report.conflicts == ()

def test_full_pipeline_reports_mismatch_without_resolving_it() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="style-reference",

        reference_type=ReferenceType.STYLE,

        source="approved style reference",

        description="Dark-fantasy graphic-novel rendering.",

        tags=frozenset({"dark-fantasy"}),

    )

    registry.register(reference)

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Photorealistic rendering."

    )

    visual_intent.metadata["reference_tags"] = [

        "science-fiction",

    ]

    stored_reference = registry.get("style-reference")

    comparator = ConsistencyComparator()

    findings = comparator.compare(

        stored_reference,

        visual_intent,

    )

    assert len(findings) == 2

    assert all(

        finding.status is ComparisonStatus.MISMATCH

        for finding in findings

    )

    reporter = ConflictReporter()

    report = reporter.build_report(findings)

    assert report.finding_count == 2

    assert report.conflict_count == 2

    assert report.conflicts[0].reference_value == (

        "Dark-fantasy graphic-novel rendering."

    )

    assert report.conflicts[0].visual_intent_value == (

        "Photorealistic rendering."

    )

    assert report.conflicts[1].reference_value == frozenset(

        {"dark-fantasy"}

    )

    assert report.conflicts[1].visual_intent_value == [

        "science-fiction",

    ]

    # The conflict is reported, not resolved.

    assert visual_intent.metadata["reference_description"] == (

        "Photorealistic rendering."

    )

    assert visual_intent.metadata["reference_tags"] == [

        "science-fiction",

    ]

def test_unavailable_comparison_is_not_reported_as_conflict() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="environment-reference",

        reference_type=ReferenceType.ENVIRONMENT,

        source="environment reference",

        description="Ancient stone fortress.",

    )

    registry.register(reference)

    visual_intent = make_visual_intent()

    stored_reference = registry.get("environment-reference")

    comparator = ConsistencyComparator()

    findings = comparator.compare(

        stored_reference,

        visual_intent,

    )

    assert len(findings) == 1

    assert findings[0].status is ComparisonStatus.UNAVAILABLE

    reporter = ConflictReporter()

    report = reporter.build_report(findings)

    assert report.finding_count == 1

    assert report.conflict_count == 0

    assert report.conflicts == ()

def test_registry_reference_remains_unchanged_after_processing() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="continuity-reference",

        reference_type=ReferenceType.CHARACTER,

        source="continuity reference",

        roles=frozenset({ReferenceRole.CONTINUITY}),

        description="Approved continuity reference.",

        tags=frozenset({"continuity"}),

        authoritative=True,

    )

    registry.register(reference)

    visual_intent = make_visual_intent()

    checker = ConsistencyChecker()

    checker.check(

        registry.get("continuity-reference"),

        visual_intent,

    )

    comparator = ConsistencyComparator()

    comparator.compare(

        registry.get("continuity-reference"),

        visual_intent,

    )

    assert registry.get("continuity-reference") is reference

    assert reference.reference_id == "continuity-reference"

    assert reference.authoritative is True

    assert reference.description == "Approved continuity reference."

    assert reference.tags == frozenset({"continuity"})

def test_multiple_references_can_be_processed_independently() -> None:

    registry = ReferenceRegistry()

    appearance_reference = Reference(

        reference_id="appearance",

        reference_type=ReferenceType.CHARACTER,

        source="appearance reference",

        description="Black scales and purple underbelly.",

    )

    style_reference = Reference(

        reference_id="style",

        reference_type=ReferenceType.STYLE,

        source="style reference",

        description="Painterly dark-fantasy rendering.",

    )

    registry.register(appearance_reference)

    registry.register(style_reference)

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Painterly dark-fantasy rendering."

    )

    comparator = ConsistencyComparator()

    appearance_findings = comparator.compare(

        registry.get("appearance"),

        visual_intent,

    )

    style_findings = comparator.compare(

        registry.get("style"),

        visual_intent,

    )

    assert len(appearance_findings) == 1

    assert appearance_findings[0].status is ComparisonStatus.MISMATCH

    assert len(style_findings) == 1

    assert style_findings[0].status is ComparisonStatus.MATCH

def test_processing_does_not_promote_reference_to_visual_intent() -> None:

    registry = ReferenceRegistry()

    reference = Reference(

        reference_id="reference-a",

        reference_type=ReferenceType.CHARACTER,

        source="approved reference",

        authoritative=True,

    )

    registry.register(reference)

    visual_intent = make_visual_intent()

    comparator = ConsistencyComparator()

    findings = comparator.compare(

        registry.get("reference-a"),

        visual_intent,

    )

    reporter = ConflictReporter()

    report = reporter.build_report(findings)

    assert reference.authoritative is True

    assert not hasattr(reference, "visual_intent")

    assert report.conflict_count == 0