"""Structured interpretation results for the OIPM IAFIS.

IAFIS separates evidence from interpretation.

Observations describe evidence identified by an analysis process.

Feedback describes reports, preferences, corrections, or concerns.

Interpretations connect that evidence to a possible visual meaning without

automatically modifying VisualIntent, canon, or user intent.

Downstream reasoning systems remain responsible for deciding what action,

if any, should follow an interpretation.

"""

from __future__ import annotations

from dataclasses import dataclass

from enum import Enum

from oipm.analysis.analysis_observation import AnalysisObservation

from oipm.analysis.feedback_item import FeedbackItem

class InterpretationType(str, Enum):

    """Type of interpretation produced from analysis evidence."""

    MATCH = "match"

    MISMATCH = "mismatch"

    MISSING = "missing"

    EXTRA = "extra"

    AMBIGUOUS = "ambiguous"

    POTENTIAL_CONFLICT = "potential_conflict"

    CONSISTENT = "consistent"

    UNKNOWN = "unknown"

@dataclass(frozen=True)

class FeedbackInterpretation:

    """Immutable interpretation of image-analysis evidence.

    Attributes:

        interpretation_id: Unique identifier for the interpretation.

        interpretation_type: Structured classification of the finding.

        target: Subject, attribute, or domain affected.

        summary: Human-readable explanation of the interpretation.

        observation_ids: Identifiers of observations supporting it.

        feedback_ids: Identifiers of feedback items supporting it.

        confidence: Confidence in the interpretation itself.

        requires_reasoning: Whether downstream reasoning is required before

            any action can be taken.

    An interpretation is not an instruction to modify VisualIntent.

    """

    interpretation_id: str

    interpretation_type: InterpretationType

    target: str

    summary: str

    observation_ids: tuple[str, ...] = ()

    feedback_ids: tuple[str, ...] = ()

    confidence: str | None = None

    requires_reasoning: bool = True

    def __post_init__(self) -> None:

        """Validate the structural requirements of an interpretation."""

        if not self.interpretation_id.strip():

            raise ValueError(

                "interpretation_id must not be empty"

            )

        if not self.target.strip():

            raise ValueError(

                "target must not be empty"

            )

        if not self.summary.strip():

            raise ValueError(

                "summary must not be empty"

            )

        if any(

            not observation_id.strip()

            for observation_id in self.observation_ids

        ):

            raise ValueError(

                "observation_ids must not contain empty values"

            )

        if any(

            not feedback_id.strip()

            for feedback_id in self.feedback_ids

        ):

            raise ValueError(

                "feedback_ids must not contain empty values"

            )

        if self.confidence is not None and not self.confidence.strip():

            raise ValueError(

                "confidence must be non-empty when provided"

            )

@dataclass(frozen=True)

class InterpretationInput:

    """Immutable evidence package supplied to an interpretation process.

    The input deliberately keeps observations and feedback separate so that

    downstream logic can distinguish direct visual evidence from reported

    evaluation or user feedback.

    """

    observations: tuple[AnalysisObservation, ...] = ()

    feedback: tuple[FeedbackItem, ...] = ()

    def __post_init__(self) -> None:

        """Validate the evidence collections."""

        if any(

            not isinstance(

                observation,

                AnalysisObservation,

            )

            for observation in self.observations

        ):

            raise TypeError(

                "observations must contain only AnalysisObservation instances"

            )

        if any(

            not isinstance(

                item,

                FeedbackItem,

            )

            for item in self.feedback

        ):

            raise TypeError(

                "feedback must contain only FeedbackItem instances"

            )