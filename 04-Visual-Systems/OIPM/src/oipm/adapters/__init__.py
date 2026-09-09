"""Generator Adaptation Layer package for OIPM.

The Generator Adaptation Layer (GAL) translates generator-neutral OIPM

visual specifications into generator-specific representations.

GAL must not:

- redefine visual intent,

- invent missing visual information,

- alter canon,

- resolve upstream conflicts,

- replace VisualIntent as the source of truth,

- or perform prompt assembly that belongs to PAOE.

Generator-specific adapters should be implemented as separate modules

within this package.

"""

from __future__ import annotations

from .generator_adapter import (

    GeneratorAdapter,

    GeneratorAdapterResult,

)

__all__ = [

    "GeneratorAdapter",

    "GeneratorAdapterResult",

]