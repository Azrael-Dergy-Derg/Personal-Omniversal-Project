"""Reference & Consistency System package for OIPM.

The RCS manages structured visual references and supports controlled

consistency checking against OIPM visual intent.

References provide evidence or guidance. They do not automatically

become canon or replace VisualIntent as the source of truth.

"""

from __future__ import annotations

from .reference_model import (

    Reference,

    ReferenceRole,

    ReferenceType,

)

__all__ = [

    "Reference",

    "ReferenceRole",

    "ReferenceType",

]