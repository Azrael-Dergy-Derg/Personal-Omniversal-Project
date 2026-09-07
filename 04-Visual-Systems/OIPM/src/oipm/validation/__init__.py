"""Validation components for the Omniversal Image Prompt Maker (OIPM).

This package contains validation logic used to verify the structural

and semantic integrity of OIPM's internal representations.

"""

from .visual_intent_validator import (

    ValidationIssue,

    ValidationResult,

    VisualIntentValidator,

)

__all__ = [

    "ValidationIssue",

    "ValidationResult",

    "VisualIntentValidator",

]