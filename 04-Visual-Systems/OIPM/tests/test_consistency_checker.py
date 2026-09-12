"""Tests for the OIPM Reference & Consistency System checker."""

from __future__ import annotations

import pytest

from oipm.models import VisualIntent

from oipm.references.consistency_checker import (

    ConsistencyChecker,

    ConsistencyStatus,

)

from oipm.references.reference_model import (

    Reference,

    ReferenceRole,

    ReferenceType,

)

def make_reference(

    reference_id: str = "test-reference",

    roles: frozenset[ReferenceRole] | None = None,

) -> Reference:

    """Create a minimal test reference."""

    return Reference(

        reference_id=reference_id,

        reference_type=ReferenceType.GENERAL,

        source="test-source",

        roles=roles or frozenset(),

    )

def make_visual_intent() -> VisualIntent:

    """Create a minimal valid VisualIntent."""

    return VisualIntent(

        user_input="Test visual intent",

    )

def test_checker_accepts_valid_inputs() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    assert isinstance(findings, tuple)

def test_checker_rejects_non_reference() -> None:

    checker = ConsistencyChecker()

    visual_intent = make_visual_intent()

    with pytest.raises(TypeError):

        checker.check("not-a-reference", visual_intent)  # type: ignore[arg-type]

def test_checker_rejects_non_visual_intent() -> None:

    checker = ConsistencyChecker()

    reference = make_reference()

    with pytest.raises(TypeError):

        checker.check(reference, "not-visual-intent")  # type: ignore[arg-type]

def test_checker_returns_no_findings_when_reference_has_no_roles() -> None:

    checker = ConsistencyChecker()

    reference = make_reference()

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    assert findings == ()

def test_checker_marks_existing_scene_as_matchable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.ENVIRONMENT})

    )

    visual_intent = make_visual_intent()

    visual_intent.scene = object()  # type: ignore[assignment]

    findings = checker.check(reference, visual_intent)

    assert len(findings) == 1

    assert findings[0].reference_id == "test-reference"

    assert findings[0].role == ReferenceRole.ENVIRONMENT

    assert findings[0].status == ConsistencyStatus.MATCHABLE

def test_checker_marks_missing_scene_as_unmatchable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.ENVIRONMENT})

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    assert len(findings) == 1

    assert findings[0].role == ReferenceRole.ENVIRONMENT

    assert findings[0].status == ConsistencyStatus.UNMATCHABLE

def test_checker_marks_existing_lighting_as_matchable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    visual_intent = make_visual_intent()

    visual_intent.lighting = object()  # type: ignore[assignment]

    findings = checker.check(reference, visual_intent)

    assert findings[0].status == ConsistencyStatus.MATCHABLE

def test_checker_marks_missing_lighting_as_unmatchable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    assert findings[0].status == ConsistencyStatus.UNMATCHABLE

def test_checker_marks_existing_composition_as_matchable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.COMPOSITION})

    )

    visual_intent = make_visual_intent()

    visual_intent.composition = object()  # type: ignore[assignment]

    findings = checker.check(reference, visual_intent)

    assert findings[0].status == ConsistencyStatus.MATCHABLE

def test_checker_marks_missing_composition_as_unmatchable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.COMPOSITION})

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    assert findings[0].status == ConsistencyStatus.UNMATCHABLE

def test_checker_orders_findings_deterministically() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset(

            {

                ReferenceRole.STYLE,

                ReferenceRole.LIGHTING,

                ReferenceRole.COMPOSITION,

                ReferenceRole.ENVIRONMENT,

            }

        )

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    roles = tuple(finding.role for finding in findings)

    assert roles == tuple(

        sorted(roles, key=lambda role: role.value)

    )

def test_checker_does_not_modify_reference() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    original_roles = reference.roles

    original_source = reference.source

    original_id = reference.reference_id

    checker.check(reference, make_visual_intent())

    assert reference.roles == original_roles

    assert reference.source == original_source

    assert reference.reference_id == original_id

def test_checker_does_not_modify_visual_intent_metadata() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    visual_intent = make_visual_intent()

    original_metadata = dict(visual_intent.metadata)

    checker.check(reference, visual_intent)

    assert visual_intent.metadata == original_metadata

def test_checker_does_not_promote_reference_to_canon() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.APPEARANCE})

    )

    visual_intent = make_visual_intent()

    checker.check(reference, visual_intent)

    assert reference.authoritative is False

    assert not hasattr(reference, "canon")

def test_finding_contains_human_readable_message() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    assert findings[0].message

    assert isinstance(findings[0].message, str)

def test_finding_is_immutable() -> None:

    checker = ConsistencyChecker()

    reference = make_reference(

        roles=frozenset({ReferenceRole.LIGHTING})

    )

    visual_intent = make_visual_intent()

    findings = checker.check(reference, visual_intent)

    with pytest.raises(AttributeError):

        findings[0].status = ConsistencyStatus.MATCHABLE  # type: ignore[misc]