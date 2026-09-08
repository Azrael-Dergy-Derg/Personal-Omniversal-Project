"""Tests for the Artistic Direction and Rendering Engine package boundary."""

from oipm.artistic_direction import (

    ArtisticDirectionEngine,

    ArtisticDirectionResult,

)

def test_artistic_direction_package_exports_engine() -> None:

    """The ADRE package should expose the engine class."""

    assert ArtisticDirectionEngine is not None

def test_artistic_direction_package_exports_result() -> None:

    """The ADRE package should expose the result class."""

    assert ArtisticDirectionResult is not None

def test_artistic_direction_engine_is_instantiable() -> None:

    """The exported ADRE engine should be directly instantiable."""

    engine = ArtisticDirectionEngine()

    assert isinstance(engine, ArtisticDirectionEngine)