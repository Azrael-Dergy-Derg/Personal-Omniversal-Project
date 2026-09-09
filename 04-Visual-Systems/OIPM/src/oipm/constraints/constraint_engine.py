"""Constraint, Conflict, and Consistency Engine for OIPM.

The Constraint, Conflict, and Consistency Engine (C3E) is responsible for

organizing explicitly supplied constraints and identifying basic conflicts

within a VisualIntent.

The initial implementation is intentionally conservative. It does not

invent constraints, silently overwrite existing information, resolve

ambiguous conflicts through guesswork, or alter canon.

VisualIntent remains the source of truth.

More advanced conflict resolution, priority reasoning, provenance analysis,

and cross-domain consistency reasoning belong to later OIPM reasoning

components.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import Constraint, Priority, Source, VisualIntent

@dataclass(frozen=True)

class ConstraintResult:

    """Result produced by the Constraint, Conflict, and Consistency Engine."""

    visual_intent: VisualIntent

    constraints: tuple[Constraint, ...]

    warnings: tuple[str, ...] = ()

class ConstraintEngine:

    """Conservatively construct and validate image constraints."""

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

    ) -> ConstraintResult:

        """Apply an explicitly supplied constraint.

        A constraint is added only when its required fields are supplied.

        Existing constraints are preserved. If the supplied constraint

        conflicts with an existing constraint targeting the same subject

        or domain, the existing constraint remains authoritative and a

        warning is produced.

        No unspecified constraint is invented.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent instance")

        constraints = visual_intent.constraints

        warnings: list[str] = []

        if constraint_type is None and target is None and requirement is None:

            return ConstraintResult(

                visual_intent=visual_intent,

                constraints=tuple(constraints),

                warnings=tuple(warnings),

            )

        if constraint_type is None:

            raise ValueError(

                "constraint_type is required when supplying a constraint"

            )

        if requirement is None:

            raise ValueError(

                "requirement is required when supplying a constraint"

            )

        supplied_constraint = Constraint(

            type=constraint_type,

            target=target,

            requirement=requirement,

            priority=priority,

            source=source,

            resolution=resolution,

        )

        for existing_constraint in constraints:

            same_type = existing_constraint.type == supplied_constraint.type

            same_target = existing_constraint.target == supplied_constraint.target

            if not (same_type and same_target):

                continue

            if existing_constraint.requirement == supplied_constraint.requirement:

                warnings.append(

                    "Duplicate constraint detected; existing constraint "

                    "was preserved."

                )

                return ConstraintResult(

                    visual_intent=visual_intent,

                    constraints=tuple(constraints),

                    warnings=tuple(warnings),

                )

            warnings.append(

                f"Conflicting constraint detected for type "

                f"'{constraint_type}' and target '{target}'; "

                "existing constraint was preserved."

            )

            return ConstraintResult(

                visual_intent=visual_intent,

                constraints=tuple(constraints),

                warnings=tuple(warnings),

            )

        constraints.append(supplied_constraint)

        return ConstraintResult(

            visual_intent=visual_intent,

            constraints=tuple(constraints),

            warnings=tuple(warnings),

        )