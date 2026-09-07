"""Processing pipeline components for the Omniversal Image Prompt Maker (OIPM).

This package contains the orchestration layer responsible for connecting

OIPM processing stages into a coherent image-generation workflow.

"""

from .pipeline import OIPMPipeline, PipelineResult

__all__ = [

    "OIPMPipeline",

    "PipelineResult",

]