"""Structured observations produced by the OIPM image-analysis boundary.

IAFIS begins with observations rather than conclusions.

An observation records what an analysis process identifies in an image or

feedback artifact. Observations are evidence for downstream reasoning; they

are not automatically treated as truth, canon, or user intent.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

class ObservationSource(str, Enum):

    """Origin of an image-analysis observation."""

    IMAGE = "image"

    EXTERNAL_FEEDBACK = "external_feedback"

    USER_REPORT = "user_report"

    ANALYSIS_PROCESS = "analysis_process"

class ObservationConfidence(str, Enum):

    """Confidence associated with an observation."""

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"

    UNKNOWN = "unknown"

@dataclass(frozen=True)

class AnalysisObservation:

    """Immutable observation produced during image analysis.

    Attributes:

        observation_id: Unique identifier for the observation.

        source: Origin of the observation.

        subject: Optional target or entity associated with the observation.

        attribute: Visual attribute being observed.

        value: Observed value or description.

        confidence: Confidence associated with the observation.

        evidence: Optional description of the evidence supporting the

            observation.

        notes: Optional additional analysis notes.

    Observations do not modify VisualIntent and do not establish canon.

    """

    observation_id: str

    source: ObservationSource

    subject: str | None

    attribute: str

    value: str

    confidence: ObservationConfidence = ObservationConfidence.UNKNOWN

    evidence: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:

        """Validate the structural requirements of an observation."""

        if not self.observation_id.strip():

            raise ValueError(

                "observation_id must not be empty"

            )

        if not self.attribute.strip():

            raise ValueError(

                "attribute must not be empty"

            )

        if not self.value.strip():

            raise ValueError(

                "value must not be empty"

            )

        if self.subject is not None and not self.subject.strip():

            raise ValueError(

                "subject must be non-empty when provided"

            )

        if self.evidence is not None and not self.evidence.strip():

            raise ValueError(

                "evidence must be non-empty when provided"

            )

        if self.notes is not None and not self.notes.strip():

            raise ValueError(

                "notes must be non-empty when provided"

            )