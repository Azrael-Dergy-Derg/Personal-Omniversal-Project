"""Contract tests for the OIPM Generator Adaptation Layer."""

from __future__ import annotations

import pytest

from oipm.adapters import GeneratorAdapter, GeneratorAdapterResult

from oipm.models import VisualIntent

class StubGeneratorAdapter(GeneratorAdapter):

    """Minimal adapter used to verify the GAL contract."""

    @property

    def generator_name(self) -> str:

        return "stub-generator"

    def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

        self._validate_input(visual_intent)

        return GeneratorAdapterResult(

            generator=self.generator_name,

            prompt=visual_intent.metadata.user_input,

            parameters={},

            warnings=[],

        )

def test_concrete_adapter_implements_required_contract() -> None:

    adapter = StubGeneratorAdapter()

    assert adapter.generator_name == "stub-generator"

def test_concrete_adapter_accepts_visual_intent() -> None:

    intent = VisualIntent()

    intent.metadata.user_input = "A dragon standing in a ruined castle."

    adapter = StubGeneratorAdapter()

    result = adapter.adapt(intent)

    assert isinstance(result, GeneratorAdapterResult)

    assert result.generator == "stub-generator"

    assert result.prompt == "A dragon standing in a ruined castle."

def test_adapter_rejects_non_visual_intent() -> None:

    adapter = StubGeneratorAdapter()

    with pytest.raises(TypeError, match="visual_intent must be a VisualIntent"):

        adapter.adapt("not a visual intent")  # type: ignore[arg-type]

def test_adapter_does_not_modify_visual_intent() -> None:

    intent = VisualIntent()

    intent.metadata.user_input = "A dragon standing in a ruined castle."

    before = intent.model_dump()

    adapter = StubGeneratorAdapter()

    adapter.adapt(intent)

    after = intent.model_dump()

    assert after == before

def test_adapter_result_supports_generator_parameters() -> None:

    class ParameterAdapter(GeneratorAdapter):

        @property

        def generator_name(self) -> str:

            return "parameter-generator"

        def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

            self._validate_input(visual_intent)

            return GeneratorAdapterResult(

                generator=self.generator_name,

                prompt="adapted prompt",

                parameters={

                    "width": 1024,

                    "height": 1024,

                    "steps": 30,

                },

                warnings=[],

            )

    result = ParameterAdapter().adapt(VisualIntent())

    assert result.parameters == {

        "width": 1024,

        "height": 1024,

        "steps": 30,

    }

def test_adapter_result_supports_warnings() -> None:

    class WarningAdapter(GeneratorAdapter):

        @property

        def generator_name(self) -> str:

            return "warning-generator"

        def adapt(self, visual_intent: VisualIntent) -> GeneratorAdapterResult:

            self._validate_input(visual_intent)

            return GeneratorAdapterResult(

                generator=self.generator_name,

                prompt="adapted prompt",

                parameters={},

                warnings=["Generator does not support one requested feature."],

            )

    result = WarningAdapter().adapt(VisualIntent())

    assert result.warnings == [

        "Generator does not support one requested feature."

    ]

def test_adapter_result_is_independent_of_visual_intent() -> None:

    intent = VisualIntent()

    intent.metadata.user_input = "Original input."

    adapter = StubGeneratorAdapter()

    result = adapter.adapt(intent)

    intent.metadata.user_input = "Changed input."

    assert result.prompt == "Original input."

def test_generator_adapter_remains_abstract() -> None:

    with pytest.raises(TypeError):

        GeneratorAdapter()  # type: ignore[abstract]