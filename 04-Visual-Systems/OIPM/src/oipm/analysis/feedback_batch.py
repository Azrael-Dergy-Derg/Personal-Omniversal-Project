"""Structured collections of feedback for the OIPM IAFIS.

A feedback pass may contain multiple user reports, evaluator comments,

analysis-process findings, or preservation requests.

This module provides an immutable container for those feedback items

without assigning them authority over VisualIntent or canon.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.analysis.feedback_item import FeedbackItem

@dataclass(frozen=True)

class FeedbackBatch:

    """Immutable collection of feedback items from one feedback pass.

    Attributes:

        batch_id: Unique identifier for the feedback batch.

        feedback: Feedback items contained in the batch.

        source_id: Optional identifier for the image, generation, or

            evaluation associated with the feedback.

        notes: Optional notes about the feedback pass.

    The batch is evidence only. It does not establish canon or mutate

    VisualIntent.

    """

    batch_id: str

    feedback: tuple[FeedbackItem, ...] = ()

    source_id: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:

        """Validate the structural requirements of the batch."""

        if not self.batch_id.strip():

            raise ValueError(

                "batch_id must not be empty"

            )

        if any(

            not isinstance(item, FeedbackItem)

            for item in self.feedback

        ):

            raise TypeError(

                "feedback must contain only FeedbackItem instances"

            )

        if self.source_id is not None and not self.source_id.strip():

            raise ValueError(

                "source_id must be non-empty when provided"

            )

        if self.notes is not None and not self.notes.strip():

            raise ValueError(

                "notes must be non-empty when provided"

            )

    @property

    def feedback_count(self) -> int:

        """Return the number of feedback items in the batch."""

        return len(self.feedback)

    @property

    def is_empty(self) -> bool:

        """Return whether the batch contains no feedback items."""

        return not self.feedback

    def add(

        self,

        feedback: FeedbackItem,

    ) -> FeedbackBatch:

        """Return a new batch containing an additional feedback item.

        The existing batch remains unchanged.

        """

        if not isinstance(

            feedback,

            FeedbackItem,

        ):

            raise TypeError(

                "feedback must be a FeedbackItem"

            )

        return FeedbackBatch(

            batch_id=self.batch_id,

            feedback=self.feedback + (feedback,),

            source_id=self.source_id,

            notes=self.notes,

        )