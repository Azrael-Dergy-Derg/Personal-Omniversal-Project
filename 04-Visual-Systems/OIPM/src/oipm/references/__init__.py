"""Reference & Consistency System package for OIPM.

The RCS manages structured visual references and supports controlled

consistency checking against OIPM visual intent.

References provide evidence or guidance. They do not automatically

become canon or replace VisualIntent as the source of truth.

"""

from __future__ import annotations

from .consistency_checker import (

    ConsistencyChecker,

    ConsistencyFinding,

    ConsistencyStatus,

)

from .consistency_comparator import (

    ComparisonFinding,

    ComparisonStatus,

    ConsistencyComparator,

)

from .conflict_report import (

    Conflict,

    ConflictReport,

    ConflictReporter,

)

from .reference_model import (

    Reference,

    ReferenceRole,

    ReferenceType,

)

from .reference_registry import ReferenceRegistry

__all__ = [

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

]