"""Integration tests for C3E within the OIPM processing pipeline."""

from oipm.constraints import ConstraintEngine

from oipm.models import Priority, Source, VisualIntent

from oipm.pipeline import OIPMPipeline

def test_pipeline_executes_constraint_engine() -> None:

    """The pipeline should process explicit constraints through C3E."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon standing in a ruined castle.",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain fully visible",

    )

    assert result.constraint_processing is not None

    assert len(result.visual_intent.constraints) == 1

    constraint = result.visual_intent.constraints[0]

    assert constraint.type == "required"

    assert constraint.target == "character"

    assert constraint.requirement == "character must remain fully visible"

def test_pipeline_exposes_constraint_result() -> None:

    """PipelineResult should expose the C3E result."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A warrior standing in a forest.",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain visible",

    )

    assert result.constraint_processing is not None

    assert result.constraint_processing.visual_intent is result.visual_intent

    assert (

        result.constraint_processing.constraints

        is result.visual_intent.constraints

    )

def test_pipeline_passes_constraint_priority_source_and_resolution() -> None:

    """Explicit constraint metadata should survive pipeline processing."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A character beneath moonlight.",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain visible",

        constraint_priority=Priority.CRITICAL,

        constraint_source=Source.CANON,

        constraint_resolution="Preserve complete character visibility.",

    )

    assert result.constraint_processing is not None

    assert len(result.visual_intent.constraints) == 1

    constraint = result.visual_intent.constraints[0]

    assert constraint.priority == Priority.CRITICAL

    assert constraint.source == Source.CANON

    assert constraint.resolution == (

        "Preserve complete character visibility."

    )

def test_pipeline_does_not_invent_constraints() -> None:

    """A pipeline call without constraint input should not invent constraints."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A warrior standing in a field.",

    )

    assert result.constraint_processing is not None

    assert result.visual_intent.constraints == []

    assert result.constraint_processing.warnings == []

def test_pipeline_accepts_custom_constraint_engine() -> None:

    """The pipeline should support dependency injection for C3E."""

    class TrackingConstraintEngine(ConstraintEngine):

        def __init__(self) -> None:

            self.called = False

        def construct(

            self,

            visual_intent: VisualIntent,

            *,

            constraint_type: str | None = None,

            target: str | None = None,

            requirement: str | None = None,

            priority: Priority = Priority.HIGH,

            source: Source = Source.EXPLICIT_USER,

            resolution: str | None = None,

        ):

            self.called = True

            return super().construct(

                visual_intent,

                constraint_type=constraint_type,

                target=target,

                requirement=requirement,

                priority=priority,

                source=source,

                resolution=resolution,

            )

    constraint_engine = TrackingConstraintEngine()

    pipeline = OIPMPipeline(

        constraint_engine=constraint_engine,

    )

    result = pipeline.process(

        "A warrior standing in a forest.",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain visible",

    )

    assert constraint_engine.called is True

    assert result.constraint_processing is not None

    assert len(result.visual_intent.constraints) == 1

def test_pipeline_preserves_constraint_processing_identity() -> None:

    """C3E should operate on the same VisualIntent as earlier stages."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon beneath moonlight.",

        subject_identity="Azrael",

        location="ancient ruins",

        framing="close-up",

        light_source="moonlight",

        medium="digital painting",

        realism="semi-realistic",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain visible",

    )

    assert result.constraint_processing is not None

    assert result.constraint_processing.visual_intent is result.visual_intent

    assert result.visual_intent.subjects[0].identity == "Azrael"

    assert result.visual_intent.scene.location == "ancient ruins"

    assert result.visual_intent.composition.framing == "close-up"

    assert result.visual_intent.lighting.light_source == "moonlight"

    assert (

        result.visual_intent.artistic_direction.medium

        == "digital painting"

    )

    assert len(result.visual_intent.constraints) == 1

def test_pipeline_constraint_is_available_to_prompt_assembly() -> None:

    """Constraints processed by C3E should remain available to PAOE."""

    pipeline = OIPMPipeline()

    result = pipeline.process(

        "A dragon standing in a ruined castle.",

        subject_identity="Azrael",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain fully visible",

    )

    assert result.constraint_processing is not None

    assert len(result.visual_intent.constraints) == 1

    assert "character must remain fully visible" in result.prompt

def test_pipeline_validation_failure_skips_constraint_engine() -> None:

    """C3E should not execute when VisualIntent validation fails."""

    class TrackingConstraintEngine(ConstraintEngine):

        def __init__(self) -> None:

            self.called = False

        def construct(

            self,

            visual_intent: VisualIntent,

            *,

            constraint_type: str | None = None,

            target: str | None = None,

            requirement: str | None = None,

            priority: Priority = Priority.HIGH,

            source: Source = Source.EXPLICIT_USER,

            resolution: str | None = None,

        ):

            self.called = True

            return super().construct(

                visual_intent,

                constraint_type=constraint_type,

                target=target,

                requirement=requirement,

                priority=priority,

                source=source,

                resolution=resolution,

            )

    class InvalidatingValidator:

        def validate(self, visual_intent: VisualIntent):

            from oipm.validation import ValidationResult

            return ValidationResult(

                is_valid=False,

                issues=[],

            )

    constraint_engine = TrackingConstraintEngine()

    pipeline = OIPMPipeline(

        validator=InvalidatingValidator(),  # type: ignore[arg-type]

        constraint_engine=constraint_engine,

    )

    result = pipeline.process(

        "A dragon.",

        constraint_type="required",

        constraint_target="character",

        constraint_requirement="character must remain visible",

    )

    assert result.validation.is_valid is False

    assert constraint_engine.called is False

    assert result.constraint_processing is None

    assert result.visual_intent.constraints == []