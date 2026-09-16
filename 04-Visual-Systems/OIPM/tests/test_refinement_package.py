"""Package-level tests for the OIPM Iterative Refinement System."""

from __future__ import annotations

import oipm.refinement as refinement

def test_refinement_package_exports_request_types() -> None:

    assert refinement.RefinementAction is not None

    assert refinement.RefinementRequest is not None

    assert refinement.RefinementScope is not None

def test_refinement_package_exports_planning_types() -> None:

    assert refinement.RefinementEngine is not None

    assert refinement.RefinementPlan is not None

def test_refinement_package_exports_evaluator() -> None:

    assert refinement.RefinementEvaluator is not None

def test_refinement_package_exports_result_types() -> None:

    assert refinement.RefinementChange is not None

    assert refinement.RefinementResult is not None

    assert refinement.RefinementStatus is not None

def test_refinement_package_defines_expected_public_api() -> None:

    expected = {

        "RefinementAction",

        "RefinementChange",

        "RefinementEngine",

        "RefinementEvaluator",

        "RefinementPlan",

        "RefinementRequest",

        "RefinementResult",

        "RefinementScope",

        "RefinementStatus",

    }

    assert set(refinement.__all__) == expected