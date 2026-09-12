"""Integration tests for the OIPM references package."""

from __future__ import annotations

import oipm.references as references

def test_reference_package_exports_reference_model() -> None:

    assert references.Reference is not None

    assert references.ReferenceRole is not None

    assert references.ReferenceType is not None

def test_reference_package_exports_registry() -> None:

    assert references.ReferenceRegistry is not None

def test_reference_package_exports_consistency_checker() -> None:

    assert references.ConsistencyChecker is not None

    assert references.ConsistencyFinding is not None

    assert references.ConsistencyStatus is not None

def test_reference_package_exports_consistency_comparator() -> None:

    assert references.ConsistencyComparator is not None

    assert references.ComparisonFinding is not None

    assert references.ComparisonStatus is not None

def test_reference_package_exports_conflict_reporting() -> None:

    assert references.Conflict is not None

    assert references.ConflictReport is not None

    assert references.ConflictReporter is not None

def test_reference_package_defines_expected_public_api() -> None:

    expected = {

        "ComparisonFinding",

        "ComparisonStatus",

        "ConsistencyChecker",

        "ConsistencyComparator",

        "ConsistencyFinding",

        "ConsistencyStatus",

        "Conflict",

        "ConflictReport",

        "ConflictReporter",

        "Reference",

        "ReferenceRegistry",

        "ReferenceRole",

        "ReferenceType",

    }

    assert set(references.__all__) == expected