"""Subject and character resolution components for OIPM.

This package contains the Subject and Character Resolution Engine (SCRE)

and supporting components responsible for resolving subject identity,

preserving subject consistency, and maintaining character-specific

visual intent.

Subject resolution does not redefine canon or invent unspecified

character information.

"""

from .subject_resolver import (

    SubjectResolutionResult,

    SubjectResolver,

)

__all__ = [

    "SubjectResolutionResult",

    "SubjectResolver",

]