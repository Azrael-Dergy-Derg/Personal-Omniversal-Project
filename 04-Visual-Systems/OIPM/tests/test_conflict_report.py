"""Tests for OIPM RCS conflict reporting."""

from __future__ import annotations

import pytest

from oipm.references.consistency_comparator import (

    ComparisonFinding,

    ComparisonStatus,

)

from oipm.references.conflict_report import (

    ConflictReport,

    ConflictReporter,

)

def make_finding(

    *,

    reference_id: str = "reference-a",

    attribute: str = "description",

    status: ComparisonStatus = ComparisonStatus.MISMATCH,

    reference_value: object = "reference value",

    visual_intent_value: object = "VisualIntent value",

) -> ComparisonFinding:

    """Create a test comparison finding."""

    return ComparisonFinding(

        reference_id=reference_id,

        attribute=attribute,

        status=status,

        reference_value=reference_value,

        visual_intent_value=visual_intent_value,

        message=f"comparison result for {attribute}",

    )

def test_reporter_builds_empty_report_from_no_findings() -> None:

    reporter = ConflictReporter()

    report = reporter.build_report(())

    assert isinstance(report, ConflictReport)

    assert report.conflicts == ()

    assert report.finding_count == 0

    assert report.conflict_count == 0

def test_mismatch_becomes_conflict() -> None:

    reporter = ConflictReporter()

    finding = make_finding(

        status=ComparisonStatus.MISMATCH,

    )

    report = reporter.build_report((finding,))

    assert report.finding_count == 1

    assert report.conflict_count == 1

    assert len(report.conflicts) == 1

    conflict = report.conflicts[0]

    assert conflict.reference_id == "reference-a"

    assert conflict.attribute == "description"

    assert conflict.reference_value == "reference value"

    assert conflict.visual_intent_value == "VisualIntent value"

def test_match_does_not_become_conflict() -> None:

    reporter = ConflictReporter()

    finding = make_finding(

        status=ComparisonStatus.MATCH,

    )

    report = reporter.build_report((finding,))

    assert report.finding_count == 1

    assert report.conflict_count == 0

    assert report.conflicts == ()

def test_unavailable_does_not_become_conflict() -> None:

    reporter = ConflictReporter()

    finding = make_finding(

        status=ComparisonStatus.UNAVAILABLE,

    )

    report = reporter.build_report((finding,))

    assert report.finding_count == 1

    assert report.conflict_count == 0

    assert report.conflicts == ()

def test_mixed_findings_only_report_mismatches() -> None:

    reporter = ConflictReporter()

    findings = (

        make_finding(

            attribute="description",

            status=ComparisonStatus.MATCH,

        ),

        make_finding(

            attribute="tags",

            status=ComparisonStatus.MISMATCH,

        ),

        make_finding(

            attribute="lighting",

            status=ComparisonStatus.UNAVAILABLE,

        ),

        make_finding(

            attribute="composition",

            status=ComparisonStatus.MISMATCH,

        ),

    )

    report = reporter.build_report(findings)

    assert report.finding_count == 4

    assert report.conflict_count == 2

    assert tuple(

        conflict.attribute

        for conflict in report.conflicts

    ) == ("tags", "composition")

def test_report_preserves_conflict_order() -> None:

    reporter = ConflictReporter()

    findings = (

        make_finding(

            reference_id="reference-a",

            attribute="first",

        ),

        make_finding(

            reference_id="reference-b",

            attribute="second",

        ),

        make_finding(

            reference_id="reference-c",

            attribute="third",

        ),

    )

    report = reporter.build_report(findings)

    assert tuple(

        conflict.reference_id

        for conflict in report.conflicts

    ) == (

        "reference-a",

        "reference-b",

        "reference-c",

    )

def test_report_counts_all_findings() -> None:

    reporter = ConflictReporter()

    findings = (

        make_finding(status=ComparisonStatus.MATCH),

        make_finding(status=ComparisonStatus.MISMATCH),

        make_finding(status=ComparisonStatus.UNAVAILABLE),

        make_finding(status=ComparisonStatus.MISMATCH),

    )

    report = reporter.build_report(findings)

    assert report.finding_count == 4

    assert report.conflict_count == 2

def test_report_requires_tuple() -> None:

    reporter = ConflictReporter()

    with pytest.raises(TypeError):

        reporter.build_report([])  # type: ignore[arg-type]

def test_report_rejects_invalid_finding_type() -> None:

    reporter = ConflictReporter()

    with pytest.raises(TypeError):

        reporter.build_report(

            ("not-a-finding",)  # type: ignore[arg-type]

        )

def test_conflict_preserves_original_message() -> None:

    reporter = ConflictReporter()

    finding = ComparisonFinding(

        reference_id="reference-a",

        attribute="description",

        status=ComparisonStatus.MISMATCH,

        reference_value="A",

        visual_intent_value="B",

        message="Reference description differs from VisualIntent.",

    )

    report = reporter.build_report((finding,))

    assert (

        report.conflicts[0].message

        == "Reference description differs from VisualIntent."

    )

def test_report_does_not_resolve_conflict() -> None:

    reporter = ConflictReporter()

    finding = make_finding(

        reference_value="reference value",

        visual_intent_value="VisualIntent value",

    )

    report = reporter.build_report((finding,))

    conflict = report.conflicts[0]

    assert conflict.reference_value == "reference value"

    assert conflict.visual_intent_value == "VisualIntent value"

def test_report_is_deterministic() -> None:

    reporter = ConflictReporter()

    findings = (

        make_finding(

            reference_id="reference-a",

            attribute="description",

        ),

        make_finding(

            reference_id="reference-b",

            attribute="tags",

        ),

    )

    report_a = reporter.build_report(findings)

    report_b = reporter.build_report(findings)

    assert report_a == report_b

def test_report_is_immutable() -> None:

    reporter = ConflictReporter()

    report = reporter.build_report(

        (make_finding(),)

    )

    with pytest.raises(AttributeError):

        report.conflict_count = 99  # type: ignore[misc]

def test_conflict_is_immutable() -> None:

    reporter = ConflictReporter()

    report = reporter.build_report(

        (make_finding(),)

    )

    with pytest.raises(AttributeError):

        report.conflicts[0].attribute = "changed"  # type: ignore[misc]