"""Iterative Refinement System package for OIPM.

IRS manages controlled refinement of structured visual intent.

The system separates:

- refinement requests,

- refinement planning,

- refinement evaluation,

- refinement application,

- refinement results,

- and eventual state mutation.

Refinement does not silently alter canon, references, or VisualIntent.

"""

from __future__ import annotations

from .refinement_applier import (

    RefinementApplier,

    RefinementApplication,

)

from .refinement_engine import (

    RefinementEngine,

    RefinementPlan,

)

from .refinement_evaluator import RefinementEvaluator

from .refinement_request import (

    RefinementAction,

    RefinementRequest,

    RefinementScope,

)

from .refinement_result import (

    RefinementChange,

    RefinementResult,

    RefinementStatus,

)

__all__ = [

    "RefinementAction",

    "RefinementApplier",

    "RefinementApplication",

    "RefinementChange",

    "RefinementEngine",

    "RefinementEvaluator",

    "RefinementPlan",

    "RefinementRequest",

    "RefinementResult",

    "RefinementScope",

    "RefinementStatus",

]