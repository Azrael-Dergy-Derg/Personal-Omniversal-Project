"""Prompt assembly components for the Omniversal Image Prompt Maker (OIPM).

This package contains components responsible for converting structured

VisualIntent data into image-generation prompt representations.

Prompt assembly does not redefine visual intent. It translates the

structured source-of-truth into prompt text while preserving the

information supplied by upstream OIPM systems.

"""

from .prompt_assembler import PromptAssembler

__all__ = [

    "PromptAssembler",

]