"""Tests for the Generator Adaptation Layer contract."""

from __future__ import annotations

from typing import Any

import pytest

from oipm.adapters.generator_adapter import (

    GeneratorAdapter,

    GeneratorAdapterResult,

)

from oipm.models import VisualIntent

class TestGeneratorAdapterResult:

    """Tests for the adapter result container."""

    def test_result_is_constructible(self) -> None:

        result = GeneratorAdapterResult(

            generator="test-generator",

            prompt="test prompt",

            parameters={"steps": 20},

            warnings=[],

        )

        assert result.generator == "test-generator"

        assert result.prompt == "test prompt"

        assert result.parameters == {"steps": 20}

        assert result.warnings == []

    def test_result_is_immutable(self) -> None:

        result = GeneratorAdapterResult(

            generator="test-generator",

            prompt="test prompt",

            parameters={},

            warnings=[],

        )

        with pytest.raises(AttributeError):

            result.prompt = "changed"  # type: ignore[misc]

class TestGeneratorAdapter:

    """Tests for the abstract adapter contract."""

    def test_adapter_is_abstract(self) -> None:

        with pytest.raises(TypeError):

            GeneratorAdapter()  # type: ignore[abstract]

    def test_concrete_adapter_can_be_implemented(self) -> None:

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="test prompt",

                    parameters={},

                    warnings=[],

                )

        adapter = TestAdapter()

        assert adapter.generator_name == "test-generator"

    def test_adapter_accepts_visual_intent(self) -> None:

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="test prompt",

                    parameters={},

                    warnings=[],

                )

        visual_intent = VisualIntent(user_input="A dragon")

        adapter = TestAdapter()

        result = adapter.adapt(visual_intent)

        assert result.generator == "test-generator"

    def test_adapter_rejects_wrong_input_type(self) -> None:

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="test prompt",

                    parameters={},

                    warnings=[],

                )

        adapter = TestAdapter()

        with pytest.raises(TypeError, match="visual_intent must be a VisualIntent"):

            adapter.adapt("not a visual intent")  # type: ignore[arg-type]

    def test_validation_does_not_modify_visual_intent(self) -> None:

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="test prompt",

                    parameters={},

                    warnings=[],

                )

        visual_intent = VisualIntent(user_input="A dragon")

        original_input = visual_intent.user_input

        TestAdapter().adapt(visual_intent)

        assert visual_intent.user_input == original_input

    def test_adapter_result_can_contain_generator_parameters(self) -> None:

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                parameters: dict[str, Any] = {

                    "width": 1024,

                    "height": 1024,

                    "steps": 30,

                }

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="test prompt",

                    parameters=parameters,

                    warnings=[],

                )

        result = TestAdapter().adapt(

            VisualIntent(user_input="A dragon")

        )

        assert result.parameters["width"] == 1024

        assert result.parameters["height"] == 1024

        assert result.parameters["steps"] == 30

    def test_adapter_can_return_warnings(self) -> None:

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="test prompt",

                    parameters={},

                    warnings=["Generator does not support a requested feature."],

                )

        result = TestAdapter().adapt(

            VisualIntent(user_input="A dragon")

        )

        assert result.warnings == [

            "Generator does not support a requested feature."

        ]

    def test_adapter_does_not_require_generator_specific_behavior_in_core(self) -> None:

        visual_intent = VisualIntent(user_input="A dragon")

        class TestAdapter(GeneratorAdapter):

            @property

            def generator_name(self) -> str:

                return "neutral-test-generator"

            def adapt(

                self,

                visual_intent: VisualIntent,

            ) -> GeneratorAdapterResult:

                self._validate_input(visual_intent)

                return GeneratorAdapterResult(

                    generator=self.generator_name,

                    prompt="generator-neutral test output",

                    parameters={},

                    warnings=[],

                )

        result = TestAdapter().adapt(visual_intent)

        assert result.generator == "neutral-test-generator"

        assert result.prompt == "generator-neutral test output"