"""Tests for the OIPM generator adapter configuration model."""

from __future__ import annotations

import pytest

from oipm.adapters.adapter_config import AdapterConfig

def test_adapter_config_requires_generator() -> None:

    with pytest.raises(ValueError):

        AdapterConfig(

            generator="",

            display_name="Test Generator",

        )

def test_adapter_config_requires_display_name() -> None:

    with pytest.raises(ValueError):

        AdapterConfig(

            generator="test-generator",

            display_name="",

        )

def test_adapter_config_stores_required_metadata() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

    )

    assert config.generator == "test-generator"

    assert config.display_name == "Test Generator"

def test_adapter_config_defaults_are_empty() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

    )

    assert config.supported_parameters == frozenset()

    assert config.supported_features == frozenset()

    assert config.notes is None

def test_adapter_config_stores_supported_parameters() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

        supported_parameters=frozenset(

            {

                "width",

                "height",

            }

        ),

    )

    assert config.supported_parameters == frozenset(

        {

            "width",

            "height",

        }

    )

    assert config.supports_parameter("width")

    assert config.supports_parameter("height")

    assert not config.supports_parameter("steps")

def test_adapter_config_stores_supported_features() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

        supported_features=frozenset(

            {

                "negative_prompt",

                "reference_image",

            }

        ),

    )

    assert config.supported_features == frozenset(

        {

            "negative_prompt",

            "reference_image",

        }

    )

    assert config.supports_feature("negative_prompt")

    assert config.supports_feature("reference_image")

    assert not config.supports_feature("unsupported_feature")

def test_adapter_config_stores_optional_notes() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

        notes="Development configuration.",

    )

    assert config.notes == "Development configuration."

def test_adapter_config_is_immutable() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

    )

    with pytest.raises(AttributeError):

        config.generator = "changed"  # type: ignore[misc]

def test_adapter_config_does_not_contain_visual_intent() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

    )

    assert not hasattr(config, "visual_intent")

    assert not hasattr(config, "prompt")

def test_adapter_config_is_generator_neutral() -> None:

    config = AdapterConfig(

        generator="test-generator",

        display_name="Test Generator",

    )

    assert config.generator == "test-generator"

    assert "prompt" not in config.__dataclass_fields__

    assert "visual_intent" not in config.__dataclass_fields__