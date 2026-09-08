"""Scene Construction Engine for OIPM.

The Scene Construction Engine (SCE) is responsible for establishing and

maintaining environmental intent within a VisualIntent.

The initial implementation is intentionally conservative. It preserves

explicit scene information without inventing environmental details,

silently resolving conflicts, or making independent artistic decisions.

Future SCE capabilities will include:

- location and environment resolution

- structural environment construction

- weather and atmospheric condition handling

- time-of-day resolution

- environmental interaction

- narrative-to-visual scene translation

- supporting-element placement

- scene consistency validation

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import Scene, VisualIntent

@dataclass(frozen=True)

class SceneConstructionResult:

    """Result produced by the Scene Construction Engine."""

    visual_intent: VisualIntent

    scene: Scene

    warnings: tuple[str, ...] = ()

class SceneConstructor:

    """Construct and maintain scene information within VisualIntent.

    The constructor preserves supplied information and does not invent

    unspecified environmental details.

    """

    name = "SceneConstructor"

    version = "0.1.0"

    def construct(

        self,

        visual_intent: VisualIntent,

        *,

        location: str | None = None,

        time: str | None = None,

        weather: str | None = None,

        narrative_context: str | None = None,

    ) -> SceneConstructionResult:

        """Construct or update scene information.

        Args:

            visual_intent: The structured source-of-truth representation.

            location: Optional explicit scene location.

            time: Optional explicit time or time-of-day.

            weather: Optional explicit weather condition.

            narrative_context: Optional narrative context for the scene.

        Returns:

            A SceneConstructionResult containing the updated VisualIntent

            and scene representation.

        Raises:

            TypeError: If visual_intent is not a VisualIntent instance.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent instance."

            )

        scene = visual_intent.scene

        warnings: list[str] = []

        self._apply_scalar_field(

            scene,

            "location",

            location,

            warnings,

        )

        self._apply_scalar_field(

            scene,

            "time",

            time,

            warnings,

        )

        self._apply_scalar_field(

            scene,

            "weather",

            weather,

            warnings,

        )

        self._apply_scalar_field(

            scene,

            "narrative_context",

            narrative_context,

            warnings,

        )

        return SceneConstructionResult(

            visual_intent=visual_intent,

            scene=scene,

            warnings=tuple(warnings),

        )

    @staticmethod

    def _apply_scalar_field(

        scene: Scene,

        field_name: str,

        supplied_value: str | None,

        warnings: list[str],

    ) -> None:

        """Apply explicit scalar scene data without silent overwrites."""

        if supplied_value is None:

            return

        existing_value = getattr(scene, field_name)

        if existing_value is None:

            setattr(scene, field_name, supplied_value)

            return

        if existing_value != supplied_value:

            warnings.append(

                f"Existing scene {field_name} conflicts with supplied "

                f"{field_name}; existing value was preserved."

            )