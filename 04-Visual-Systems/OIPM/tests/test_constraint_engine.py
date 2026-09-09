from oipm.constraints import ConstraintEngine, ConstraintResult

from oipm.models import (

    Constraint,

    Priority,

    Source,

    VisualIntent,

)

def test_construct_returns_constraint_result():

    visual_intent = VisualIntent(user_input="A character in a dark forest")

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain fully visible",

    )

    assert isinstance(result, ConstraintResult)

def test_construct_preserves_visual_intent_identity():

    visual_intent = VisualIntent(user_input="A character in a dark forest")

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain fully visible",

    )

    assert result.visual_intent is visual_intent

def test_explicit_constraint_is_added():

    visual_intent = VisualIntent(user_input="A character in a dark forest")

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain fully visible",

    )

    assert len(result.constraints) == 1

    constraint = result.constraints[0]

    assert constraint.type == "required"

    assert constraint.target == "character"

    assert constraint.requirement == "character must remain fully visible"

def test_explicit_constraint_preserves_priority_source_and_resolution():

    visual_intent = VisualIntent(user_input="A character in a dark forest")

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain fully visible",

        priority=Priority.CRITICAL,

        source=Source.CANON,

        resolution="Preserve full-body visibility.",

    )

    constraint = result.constraints[0]

    assert constraint.priority == Priority.CRITICAL

    assert constraint.source == Source.CANON

    assert constraint.resolution == "Preserve full-body visibility."

def test_no_constraint_data_does_not_invent_constraints():

    visual_intent = VisualIntent(user_input="A character in a dark forest")

    result = ConstraintEngine().construct(visual_intent)

    assert result.visual_intent is visual_intent

    assert result.constraints == []

    assert result.warnings == []

def test_existing_constraints_are_preserved():

    visual_intent = VisualIntent(

        user_input="A character in a dark forest",

        constraints=[

            Constraint(

                type="required",

                target="character",

                requirement="character must remain fully visible",

            )

        ],

    )

    result = ConstraintEngine().construct(visual_intent)

    assert len(result.constraints) == 1

    assert result.constraints[0].requirement == (

        "character must remain fully visible"

    )

def test_duplicate_constraint_is_not_added_twice():

    visual_intent = VisualIntent(

        user_input="A character in a dark forest",

        constraints=[

            Constraint(

                type="required",

                target="character",

                requirement="character must remain fully visible",

            )

        ],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain fully visible",

    )

    assert len(result.constraints) == 1

    assert len(result.warnings) == 1

    assert "Duplicate constraint detected" in result.warnings[0]

def test_conflicting_constraint_preserves_existing_constraint():

    visual_intent = VisualIntent(

        user_input="A character in a dark forest",

        constraints=[

            Constraint(

                type="required",

                target="character",

                requirement="character must remain fully visible",

            )

        ],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must be partially obscured",

    )

    assert len(result.constraints) == 1

    assert result.constraints[0].requirement == (

        "character must remain fully visible"

    )

    assert len(result.warnings) == 1

    assert "Conflicting constraint detected" in result.warnings[0]

def test_same_type_with_different_target_can_coexist():

    visual_intent = VisualIntent(

        user_input="Two characters in a forest",

        constraints=[

            Constraint(

                type="required",

                target="character_a",

                requirement="character_a must remain visible",

            )

        ],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character_b",

        requirement="character_b must remain visible",

    )

    assert len(result.constraints) == 2

    assert result.warnings == []

def test_different_constraint_types_can_coexist_for_same_target():

    visual_intent = VisualIntent(

        user_input="A character in a forest",

        constraints=[

            Constraint(

                type="required",

                target="character",

                requirement="character must remain visible",

            )

        ],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="excluded",

        target="character",

        requirement="character must not be obscured by smoke",

    )

    assert len(result.constraints) == 2

    assert result.warnings == []

def test_missing_constraint_type_is_rejected():

    visual_intent = VisualIntent(user_input="A character in a forest")

    try:

        ConstraintEngine().construct(

            visual_intent,

            target="character",

            requirement="character must remain visible",

        )

    except ValueError as exc:

        assert "constraint_type is required" in str(exc)

    else:

        raise AssertionError("Expected ValueError")

def test_missing_requirement_is_rejected():

    visual_intent = VisualIntent(user_input="A character in a forest")

    try:

        ConstraintEngine().construct(

            visual_intent,

            constraint_type="required",

            target="character",

        )

    except ValueError as exc:

        assert "requirement is required" in str(exc)

    else:

        raise AssertionError("Expected ValueError")

def test_wrong_visual_intent_type_is_rejected():

    try:

        ConstraintEngine().construct(

            "not a visual intent",

            constraint_type="required",

            target="character",

            requirement="character must remain visible",

        )

    except TypeError as exc:

        assert "visual_intent must be a VisualIntent instance" in str(exc)

    else:

        raise AssertionError("Expected TypeError")

def test_conflict_does_not_overwrite_existing_priority_or_source():

    visual_intent = VisualIntent(

        user_input="A character in a forest",

        constraints=[

            Constraint(

                type="required",

                target="character",

                requirement="character must remain visible",

                priority=Priority.CRITICAL,

                source=Source.CANON,

                resolution="Canon requires full visibility.",

            )

        ],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain hidden",

        priority=Priority.LOW,

        source=Source.INFERENCE,

        resolution="Suggested concealment.",

    )

    constraint = result.constraints[0]

    assert constraint.requirement == "character must remain visible"

    assert constraint.priority == Priority.CRITICAL

    assert constraint.source == Source.CANON

    assert constraint.resolution == "Canon requires full visibility."

def test_multiple_distinct_constraints_are_preserved_and_added():

    visual_intent = VisualIntent(

        user_input="A character in a forest",

        constraints=[

            Constraint(

                type="required",

                target="character",

                requirement="character must remain visible",

            )

        ],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="excluded",

        target="background",

        requirement="background must not contain modern buildings",

    )

    assert len(result.constraints) == 2

    assert result.constraints[0].requirement == "character must remain visible"

    assert result.constraints[1].requirement == (

        "background must not contain modern buildings"

    )

def test_existing_constraint_object_is_not_replaced_on_duplicate():

    existing_constraint = Constraint(

        type="required",

        target="character",

        requirement="character must remain visible",

    )

    visual_intent = VisualIntent(

        user_input="A character in a forest",

        constraints=[existing_constraint],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain visible",

        priority=Priority.CRITICAL,

        source=Source.CANON,

    )

    assert result.constraints[0] is existing_constraint

def test_existing_constraint_object_is_not_replaced_on_conflict():

    existing_constraint = Constraint(

        type="required",

        target="character",

        requirement="character must remain visible",

    )

    visual_intent = VisualIntent(

        user_input="A character in a forest",

        constraints=[existing_constraint],

    )

    result = ConstraintEngine().construct(

        visual_intent,

        constraint_type="required",

        target="character",

        requirement="character must remain hidden",

    )

    assert result.constraints[0] is existing_constraint