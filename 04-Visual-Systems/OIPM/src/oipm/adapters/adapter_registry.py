"""Registry for generator-specific OIPM adapters.

The adapter registry provides controlled lookup of generator adapters

without making the processing pipeline depend on any specific generator.

The registry is intentionally small and explicit. It does not:

- interpret visual intent,

- modify VisualIntent,

- assemble prompts,

- invent generator requirements,

- or silently select an adapter.

"""

from __future__ import annotations

from oipm.adapters.generator_adapter import GeneratorAdapter

class AdapterRegistry:

    """Registry of available GeneratorAdapter implementations."""

    def __init__(self) -> None:

        self._adapters: dict[str, GeneratorAdapter] = {}

    def register(self, adapter: GeneratorAdapter) -> None:

        """Register an adapter by its stable generator name.

        Raises:

            TypeError: If the supplied object is not a GeneratorAdapter.

            ValueError: If an adapter with the same generator name is

                already registered.

        """

        if not isinstance(adapter, GeneratorAdapter):

            raise TypeError("adapter must be a GeneratorAdapter")

        name = adapter.generator_name

        if not name:

            raise ValueError("adapter generator_name must not be empty")

        if name in self._adapters:

            raise ValueError(

                f"adapter already registered for generator: {name}"

            )

        self._adapters[name] = adapter

    def get(self, generator_name: str) -> GeneratorAdapter:

        """Return the adapter registered for a generator.

        Raises:

            KeyError: If no adapter is registered for the requested

                generator.

        """

        try:

            return self._adapters[generator_name]

        except KeyError as exc:

            raise KeyError(

                f"no adapter registered for generator: {generator_name}"

            ) from exc

    def has(self, generator_name: str) -> bool:

        """Return whether an adapter is registered."""

        return generator_name in self._adapters

    def remove(self, generator_name: str) -> GeneratorAdapter:

        """Remove and return a registered adapter.

        Raises:

            KeyError: If no adapter is registered for the requested

                generator.

        """

        try:

            return self._adapters.pop(generator_name)

        except KeyError as exc:

            raise KeyError(

                f"no adapter registered for generator: {generator_name}"

            ) from exc

    def names(self) -> tuple[str, ...]:

        """Return registered generator names in deterministic order."""

        return tuple(sorted(self._adapters))

    def clear(self) -> None:

        """Remove all registered adapters."""

        self._adapters.clear()