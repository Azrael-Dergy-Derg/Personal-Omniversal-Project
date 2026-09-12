"""Tests for the OIPM reference consistency comparator."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.references.consistency_comparator import (

    ComparisonStatus,

    ConsistencyComparator,

)

from oipm.references.reference_model import Reference, ReferenceType

def make_reference(

    reference_id: str = "test-reference",

    *,

    description: str | None = None,

    tags: frozenset[str] | None = None,

) -> Reference:

    """Create a test reference."""

    return Reference(

        reference_id=reference_id,

        reference_type=ReferenceType.GENERAL,

        source="test-source",

        description=description,

        tags=tags or frozenset(),

    )

def make_visual_intent() -> VisualIntent:

    """Create a minimal valid VisualIntent."""

    return VisualIntent(

        user_input="Test visual intent",

    )

def test_comparator_accepts_valid_inputs() -> None:

    comparator = ConsistencyComparator()

    findings = comparator.compare(

        make_reference(),

        make_visual_intent(),

    )

    assert isinstance(findings, tuple)

def test_comparator_rejects_non_reference() -> None:

    comparator = ConsistencyComparator()

    with pytest.raises(TypeError):

        comparator.compare(

            "not-a-reference",  # type: ignore[arg-type]

            make_visual_intent(),

        )

def test_comparator_rejects_non_visual_intent() -> None:

    comparator = ConsistencyComparator()

    with pytest.raises(TypeError):

        comparator.compare(

            make_reference(),

            "not-visual-intent",  # type: ignore[arg-type]

        )

def test_comparator_ignores_reference_without_comparable_metadata() -> None:

    comparator = ConsistencyComparator()

    findings = comparator.compare(

        make_reference(),

        make_visual_intent(),

    )

    assert findings == ()

def test_description_without_visual_intent_value_is_unavailable() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

    )

    findings = comparator.compare(

        reference,

        make_visual_intent(),

    )

    assert len(findings) == 1

    assert findings[0].attribute == "description"

    assert findings[0].status == ComparisonStatus.UNAVAILABLE

    assert findings[0].reference_value == "Dark fantasy dragon"

    assert findings[0].visual_intent_value is None

def test_matching_description_is_match() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark fantasy dragon"

    )

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert len(findings) == 1

    assert findings[0].attribute == "description"

    assert findings[0].status == ComparisonStatus.MATCH

    assert findings[0].reference_value == "Dark fantasy dragon"

    assert findings[0].visual_intent_value == "Dark fantasy dragon"

def test_different_description_is_mismatch() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Bright science-fiction dragon"

    )

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert len(findings) == 1

    assert findings[0].attribute == "description"

    assert findings[0].status == ComparisonStatus.MISMATCH

def test_tags_without_visual_intent_value_are_unavailable() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        tags=frozenset({"dark-fantasy", "dragon"}),

    )

    findings = comparator.compare(

        reference,

        make_visual_intent(),

    )

    assert len(findings) == 1

    assert findings[0].attribute == "tags"

    assert findings[0].status == ComparisonStatus.UNAVAILABLE

    assert findings[0].reference_value == frozenset(

        {"dark-fantasy", "dragon"}

    )

    assert findings[0].visual_intent_value is None

def test_matching_tags_are_match() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        tags=frozenset({"dark-fantasy", "dragon"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_tags"] = [

        "dragon",

        "dark-fantasy",

    ]

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert len(findings) == 1

    assert findings[0].attribute == "tags"

    assert findings[0].status == ComparisonStatus.MATCH

def test_different_tags_are_mismatch() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        tags=frozenset({"dark-fantasy", "dragon"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_tags"] = [

        "science-fiction",

        "dragon",

    ]

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert len(findings) == 1

    assert findings[0].attribute == "tags"

    assert findings[0].status == ComparisonStatus.MISMATCH

def test_tag_order_does_not_affect_match() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        tags=frozenset({"dragon", "dark-fantasy", "comic"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_tags"] = [

        "comic",

        "dragon",

        "dark-fantasy",

    ]

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert findings[0].status == ComparisonStatus.MATCH

def test_string_tag_value_can_be_compared() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        tags=frozenset({"dark-fantasy"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_tags"] = "dark-fantasy"

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert findings[0].status == ComparisonStatus.MATCH

def test_invalid_tag_container_does_not_create_match() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        tags=frozenset({"dark-fantasy"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_tags"] = 12345

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert findings[0].status == ComparisonStatus.MISMATCH

def test_description_and_tags_are_both_compared() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

        tags=frozenset({"dragon", "dark-fantasy"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark fantasy dragon"

    )

    visual_intent.metadata["reference_tags"] = [

        "dragon",

        "dark-fantasy",

    ]

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert len(findings) == 2

    assert {

        finding.attribute

        for finding in findings

    } == {"description", "tags"}

    assert all(

        finding.status == ComparisonStatus.MATCH

        for finding in findings

    )

def test_findings_are_deterministically_ordered() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

        tags=frozenset({"dragon"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark fantasy dragon"

    )

    visual_intent.metadata["reference_tags"] = ["dragon"]

    findings_a = comparator.compare(

        reference,

        visual_intent,

    )

    findings_b = comparator.compare(

        reference,

        visual_intent,

    )

    assert findings_a == findings_b

def test_comparator_does_not_modify_reference() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

        tags=frozenset({"dragon"}),

    )

    original_description = reference.description

    original_tags = reference.tags

    original_source = reference.source

    comparator.compare(

        reference,

        make_visual_intent(),

    )

    assert reference.description == original_description

    assert reference.tags == original_tags

    assert reference.source == original_source

def test_comparator_does_not_modify_visual_intent() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

        tags=frozenset({"dragon"}),

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark fantasy dragon"

    )

    visual_intent.metadata["reference_tags"] = ["dragon"]

    original_metadata = dict(visual_intent.metadata)

    comparator.compare(

        reference,

        visual_intent,

    )

    assert visual_intent.metadata == original_metadata

def test_comparator_does_not_resolve_mismatch() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Science-fiction dragon"

    )

    original_value = visual_intent.metadata["reference_description"]

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    assert findings[0].status == ComparisonStatus.MISMATCH

    assert (

        visual_intent.metadata["reference_description"]

        == original_value

    )

def test_comparison_finding_is_immutable() -> None:

    comparator = ConsistencyComparator()

    reference = make_reference(

        description="Dark fantasy dragon",

    )

    visual_intent = make_visual_intent()

    visual_intent.metadata["reference_description"] = (

        "Dark fantasy dragon"

    )

    findings = comparator.compare(

        reference,

        visual_intent,

    )

    with pytest.raises(AttributeError):

        findings[0].status = ComparisonStatus.MISMATCH  # type: ignore[misc]