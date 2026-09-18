"""Structured feedback items for the OIPM Image Analysis & Feedback

Interpretation System.

Feedback is not automatically truth.

IAFIS must preserve the distinction between what is directly observed,

what is reported by a user or evaluator, and what is later inferred by

downstream reasoning.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

class FeedbackSource(str, Enum):

    """Origin of a feedback item."""

    USER = "user"

    EXTERNAL_EVALUATOR = "external_evaluator"

    ANALYSIS_PROCESS = "analysis_process"

class FeedbackType(str, Enum):

    """Kind of feedback being reported."""

    CORRECTION = "correction"

    PREFERENCE = "preference"

    PROBLEM = "problem"

    PRESERVATION = "preservation"

    QUESTION = "question"

    OBSERVATION = "observation"

@dataclass(frozen=True)

class FeedbackItem:

    """Immutable structured feedback item.

    Attributes:

        feedback_id: Unique identifier for the feedback item.

        source: Origin of the feedback.

        feedback_type: Type of feedback being expressed.

        target: Optional subject, attribute, or domain being discussed.

        message: Human-readable feedback content.

        evidence: Optional supporting evidence supplied with the feedback.

        confidence: Optional confidence expressed by the source.

    Feedback items do not directly modify VisualIntent.

    """

    feedback_id: str

    source: FeedbackSource

    feedback_type: FeedbackType

    target: str | None

    message: str

    evidence: str | None = None

    confidence: str | None = None

    def __post_init__(self) -> None:

        """Validate the structural requirements of feedback."""

        if not self.feedback_id.strip():

            raise ValueError(

                "feedback_id must not be empty"

            )

        if not self.message.strip():

            raise ValueError(

                "message must not be empty"

            )

        if self.target is not None and not self.target.strip():

            raise ValueError(

                "target must be non-empty when provided"

            )

        if self.evidence is not None and not self.evidence.strip():

            raise ValueError(

                "evidence must be non-empty when provided"

            )

        if self.confidence is not None and not self.confidence.strip():

            raise ValueError(

                "confidence must be non-empty when provided"

            )