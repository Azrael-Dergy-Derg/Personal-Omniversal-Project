"""Interpretation boundary for the OIPM Image Analysis & Feedback

Interpretation System.

This module converts structured observations and feedback into structured

interpretations.

The interpreter does not:

- modify VisualIntent,

- modify canon,

- resolve conflicts,

- decide which source is authoritative,

- invent missing visual information,

- or apply refinements.

Its responsibility is limited to identifying relationships between evidence

and reported intent.

"""

from __future__ import annotations

from oipm.analysis.analysis_observation import AnalysisObservation

from oipm.analysis.feedback_interpretation import (

    FeedbackInterpretation,

    InterpretationInput,

    InterpretationType,

)

from oipm.analysis.feedback_item import FeedbackItem

class AnalysisInterpreter:

    """Interpret structured IAFIS evidence without changing project state."""

    def interpret(

        self,

        evidence: InterpretationInput,

    ) -> tuple[FeedbackInterpretation, ...]:

        """Produce structured interpretations from supplied evidence.

        The current implementation uses explicit evidence relationships only.

        It does not perform speculative visual inference.

        Args:

            evidence: Observations and feedback to interpret.

        Returns:

            Immutable tuple of structured interpretations.

        Raises:

            TypeError: If evidence is not an InterpretationInput.

        """

        if not isinstance(evidence, InterpretationInput):

            raise TypeError(

                "evidence must be an InterpretationInput"

            )

        interpretations: list[FeedbackInterpretation] = []

        for feedback in evidence.feedback:

            matching_observations = self._matching_observations(

                feedback,

                evidence.observations,

            )

            if matching_observations:

                interpretations.append(

                    self._interpret_with_observations(

                        feedback,

                        matching_observations,

                    )

                )

            else:

                interpretations.append(

                    self._interpret_without_observations(

                        feedback,

                    )

                )

        return tuple(interpretations)

    def _matching_observations(

        self,

        feedback: FeedbackItem,

        observations: tuple[AnalysisObservation, ...],

    ) -> tuple[AnalysisObservation, ...]:

        """Return observations explicitly matching the feedback target."""

        if feedback.target is None:

            return ()

        matches = tuple(

            observation

            for observation in observations

            if (

                observation.attribute == feedback.target

                or observation.subject == feedback.target

            )

        )

        return matches

    def _interpret_with_observations(

        self,

        feedback: FeedbackItem,

        observations: tuple[AnalysisObservation, ...],

    ) -> FeedbackInterpretation:

        """Interpret feedback supported by related observations."""

        observation_ids = tuple(

            observation.observation_id

            for observation in observations

        )

        interpretation_type = self._classify_supported_feedback(

            feedback

        )

        return FeedbackInterpretation(

            interpretation_id=(

                f"interpretation:{feedback.feedback_id}"

            ),

            interpretation_type=interpretation_type,

            target=feedback.target or "global",

            summary=(

                f"Feedback '{feedback.feedback_id}' has "

                f"{len(observations)} related observation(s)."

            ),

            observation_ids=observation_ids,

            feedback_ids=(feedback.feedback_id,),

            confidence=feedback.confidence,

            requires_reasoning=True,

        )

    def _interpret_without_observations(

        self,

        feedback: FeedbackItem,

    ) -> FeedbackInterpretation:

        """Interpret feedback for which no direct observation was found."""

        return FeedbackInterpretation(

            interpretation_id=(

                f"interpretation:{feedback.feedback_id}"

            ),

            interpretation_type=InterpretationType.UNKNOWN,

            target=feedback.target or "global",

            summary=(

                f"No direct observation was matched to "

                f"feedback '{feedback.feedback_id}'."

            ),

            observation_ids=(),

            feedback_ids=(feedback.feedback_id,),

            confidence=feedback.confidence,

            requires_reasoning=True,

        )

    def _classify_supported_feedback(

        self,

        feedback: FeedbackItem,

    ) -> InterpretationType:

        """Classify supported feedback without deciding an action."""

        if feedback.feedback_type.value == "preservation":

            return InterpretationType.CONSISTENT

        if feedback.feedback_type.value == "correction":

            return InterpretationType.POTENTIAL_CONFLICT

        if feedback.feedback_type.value == "problem":

            return InterpretationType.MISMATCH

        if feedback.feedback_type.value == "question":

            return InterpretationType.AMBIGUOUS

        if feedback.feedback_type.value == "preference":

            return InterpretationType.UNKNOWN

        return InterpretationType.UNKNOWN