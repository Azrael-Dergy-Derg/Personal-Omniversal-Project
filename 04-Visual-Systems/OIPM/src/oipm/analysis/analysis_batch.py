"""Structured collections of observations for the OIPM IAFIS.

An analysis pass may produce multiple observations about a generated image,

reference image, or external feedback artifact.

This module provides an immutable container for those observations without

assigning them authority over VisualIntent or canon.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.analysis.analysis_observation import AnalysisObservation

@dataclass(frozen=True)

class AnalysisBatch:

    """Immutable collection of observations from one analysis pass.

    Attributes:

        batch_id: Unique identifier for the analysis batch.

        observations: Observations produced during the analysis.

        source_id: Optional identifier for the image or feedback artifact

            being analyzed.

        notes: Optional notes about the analysis pass.

    The batch is evidence only. It does not establish canon or mutate

    VisualIntent.

    """

    batch_id: str

    observations: tuple[AnalysisObservation, ...] = ()

    source_id: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:

        """Validate the structural requirements of the batch."""

        if not self.batch_id.strip():

            raise ValueError(

                "batch_id must not be empty"

            )

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

        if self.source_id is not None and not self.source_id.strip():

            raise ValueError(

                "source_id must be non-empty when provided"

            )

        if self.notes is not None and not self.notes.strip():

            raise ValueError(

                "notes must be non-empty when provided"

            )

    @property

    def observation_count(self) -> int:

        """Return the number of observations in the batch."""

        return len(self.observations)

    @property

    def is_empty(self) -> bool:

        """Return whether the batch contains no observations."""

        return not self.observations

    def add(

        self,

        observation: AnalysisObservation,

    ) -> AnalysisBatch:

        """Return a new batch containing an additional observation.

        The existing batch remains unchanged.

        """

        if not isinstance(

            observation,

            AnalysisObservation,

        ):

            raise TypeError(

                "observation must be an AnalysisObservation"

            )

        return AnalysisBatch(

            batch_id=self.batch_id,

            observations=self.observations + (observation,),

            source_id=self.source_id,

            notes=self.notes,

        )