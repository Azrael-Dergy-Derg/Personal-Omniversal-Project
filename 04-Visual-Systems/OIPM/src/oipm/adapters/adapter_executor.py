"""Execution boundary for OIPM generator adapters.

The adapter executor coordinates lookup and execution of a registered

GeneratorAdapter.

It intentionally does not:

- interpret visual intent,

- modify VisualIntent,

- assemble prompts,

- invent generator requirements,

- resolve visual conflicts,

- select a generator implicitly,

- or perform generator-specific adaptation itself.

Its responsibility is limited to:

    VisualIntent + explicit generator selection

        -> registered GeneratorAdapter

        -> GeneratorAdapterResult

"""

from __future__ import annotations

from oipm.adapters.adapter_registry import AdapterRegistry

from oipm.adapters.generator_adapter import GeneratorAdapterResult

from oipm.models import VisualIntent

class AdapterExecutor:

    """Execute a registered generator adapter against VisualIntent."""

    def __init__(self, registry: AdapterRegistry) -> None:

        """Initialize the executor with an adapter registry.

        Args:

            registry: Registry containing explicitly registered

                GeneratorAdapter implementations.

        Raises:

            TypeError: If registry is not an AdapterRegistry.

        """

        if not isinstance(registry, AdapterRegistry):

            raise TypeError("registry must be an AdapterRegistry")

        self.registry = registry

    def execute(

        self,

        visual_intent: VisualIntent,

        *,

        generator_name: str,

    ) -> GeneratorAdapterResult:

        """Execute the explicitly selected generator adapter.

        Args:

            visual_intent: Validated, generator-neutral OIPM visual intent.

            generator_name: Stable identifier of the registered adapter

                to execute.

        Returns:

            GeneratorAdapterResult produced by the selected adapter.

        Raises:

            TypeError: If visual_intent is not a VisualIntent.

            KeyError: If no adapter is registered for generator_name.

            ValueError: If generator_name is empty.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError("visual_intent must be a VisualIntent")

        if not generator_name:

            raise ValueError("generator_name must not be empty")

        adapter = self.registry.get(generator_name)

        return adapter.adapt(visual_intent)