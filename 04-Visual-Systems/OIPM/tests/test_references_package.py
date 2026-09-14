"""Package-level tests for the OIPM Reference & Consistency System."""

from __future__ import annotations

import oipm.references as references

def test_reference_package_exports_core_types() -> None:

    assert references.Reference is not None

    assert references.ReferenceRole is not None

    assert references.ReferenceType is not None

    assert references.ReferenceRegistry is not None

def test_reference_package_exports_consistency_types() -> None:

    assert references.ConsistencyChecker is not None

    assert references.ConsistencyFinding is not None

    assert references.ConsistencyStatus is not None

    assert references.ConsistencyComparator is not None

    assert references.ComparisonFinding is not None

    assert references.ComparisonStatus is not None

def test_reference_package_exports_conflict_types() -> None:

    assert references.Conflict is not None

    assert references.ConflictReport is not None

    assert references.ConflictReporter is not None

def test_reference_package_exports_orchestration_types() -> None:

    assert references.ReferenceAnalysis is not None

    assert references.ReferenceConsistencySystem is not None

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

        "ReferenceAnalysis",

        "ReferenceConsistencySystem",

        "ReferenceRegistry",

        "ReferenceRole",

        "ReferenceType",

    }

    assert set(references.__all__) == expected