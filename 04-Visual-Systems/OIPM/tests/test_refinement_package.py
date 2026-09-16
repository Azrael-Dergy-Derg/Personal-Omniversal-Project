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

def test_refinement_package_exports_application_types() -> None:

    assert refinement.RefinementApplier is not None

    assert refinement.RefinementApplication is not None

def test_refinement_package_exports_orchestration_types() -> None:

    assert refinement.RefinementExecution is not None

    assert refinement.RefinementSystem is not None

def test_refinement_package_exports_result_types() -> None:

    assert refinement.RefinementChange is not None

    assert refinement.RefinementResult is not None

    assert refinement.RefinementStatus is not None

def test_refinement_package_defines_expected_public_api() -> None:

    expected = {

        "RefinementAction",

        "RefinementApplier",

        "RefinementApplication",

        "RefinementChange",

        "RefinementEngine",

        "RefinementEvaluator",

        "RefinementExecution",

        "RefinementPlan",

        "RefinementRequest",

        "RefinementResult",

        "RefinementScope",

        "RefinementStatus",

        "RefinementSystem",

    }

    assert set(refinement.__all__) == expected