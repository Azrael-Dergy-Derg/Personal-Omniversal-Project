"""Registry for OIPM visual references.

The Reference & Consistency System (RCS) uses this registry to maintain

controlled access to structured Reference objects.

The registry is intentionally limited to reference management. It does not:

- interpret reference meaning,

- modify references,

- promote references to canon,

- modify VisualIntent,

- resolve visual conflicts,

- compare references against VisualIntent,

- or silently determine authority.

Those responsibilities belong to later RCS components.

"""

from __future__ import annotations

from oipm.references.reference_model import Reference

class ReferenceRegistry:

    """Registry of structured OIPM visual references."""

    def __init__(self) -> None:

        """Initialize an empty reference registry."""

        self._references: dict[str, Reference] = {}

    def register(self, reference: Reference) -> None:

        """Register a reference by its stable identifier.

        Args:

            reference: Reference object to register.

        Raises:

            TypeError: If the supplied value is not a Reference.

            ValueError: If the reference identifier is empty or already

                registered.

        """

        if not isinstance(reference, Reference):

            raise TypeError("reference must be a Reference")

        reference_id = reference.reference_id

        if not reference_id:

            raise ValueError("reference_id must not be empty")

        if reference_id in self._references:

            raise ValueError(

                f"reference already registered: {reference_id}"

            )

        self._references[reference_id] = reference

    def get(self, reference_id: str) -> Reference:

        """Return the reference registered under the supplied identifier.

        Raises:

            KeyError: If no reference is registered with the identifier.

        """

        try:

            return self._references[reference_id]

        except KeyError as exc:

            raise KeyError(

                f"no reference registered: {reference_id}"

            ) from exc

    def has(self, reference_id: str) -> bool:

        """Return whether a reference is registered."""

        return reference_id in self._references

    def remove(self, reference_id: str) -> Reference:

        """Remove and return a registered reference.

        Raises:

            KeyError: If no reference is registered with the identifier.

        """

        try:

            return self._references.pop(reference_id)

        except KeyError as exc:

            raise KeyError(

                f"no reference registered: {reference_id}"

            ) from exc

    def ids(self) -> tuple[str, ...]:

        """Return registered reference identifiers in deterministic order."""

        return tuple(sorted(self._references))

    def clear(self) -> None:

        """Remove all registered references."""

        self._references.clear()