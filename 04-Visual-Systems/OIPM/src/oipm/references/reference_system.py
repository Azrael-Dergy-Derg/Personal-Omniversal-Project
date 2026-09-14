"""High-level orchestration boundary for the OIPM Reference & Consistency System.

This module provides the public orchestration layer for RCS.

RCS coordinates reference registration, structural consistency checking,

attribute comparison, and conflict reporting.

It does not:

- modify VisualIntent,

- modify references,

- promote references to canon,

- invent visual information,

- resolve conflicts,

- select an authoritative source,

- or silently alter user intent.

RCS reports consistency information so that downstream OIPM decision and

reasoning systems can make explicit, controlled decisions.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.models import VisualIntent

from oipm.references.consistency_checker import (

    ConsistencyChecker,

    ConsistencyFinding,

)

from oipm.references.consistency_comparator import (

    ComparisonFinding,

    ConsistencyComparator,

)

from oipm.references.conflict_report import (

    ConflictReport,

    ConflictReporter,

)

from oipm.references.reference_model import Reference

from oipm.references.reference_registry import ReferenceRegistry

@dataclass(frozen=True)

class ReferenceAnalysis:

    """Complete RCS analysis result for one registered reference.

    Attributes:

        reference_id: Identifier of the analyzed reference.

        structural_findings: Results from structural consistency checking.

        comparison_findings: Results from attribute-level comparison.

        conflict_report: Report containing detected mismatches.

    The analysis is informational and contains no resolution decision.

    """

    reference_id: str

    structural_findings: tuple[ConsistencyFinding, ...]

    comparison_findings: tuple[ComparisonFinding, ...]

    conflict_report: ConflictReport

class ReferenceConsistencySystem:

    """Coordinate the OIPM Reference & Consistency System."""

    def __init__(

        self,

        registry: ReferenceRegistry | None = None,

    ) -> None:

        """Initialize the RCS orchestration boundary.

        Args:

            registry: Optional existing reference registry. If omitted,

                a new empty registry is created.

        Raises:

            TypeError: If registry is not a ReferenceRegistry.

        """

        if registry is not None and not isinstance(

            registry,

            ReferenceRegistry,

        ):

            raise TypeError(

                "registry must be a ReferenceRegistry"

            )

        self.registry = registry or ReferenceRegistry()

        self._checker = ConsistencyChecker()

        self._comparator = ConsistencyComparator()

        self._reporter = ConflictReporter()

    def register(self, reference: Reference) -> None:

        """Register a reference with the RCS registry."""

        self.registry.register(reference)

    def get(self, reference_id: str) -> Reference:

        """Return a registered reference."""

        return self.registry.get(reference_id)

    def has(self, reference_id: str) -> bool:

        """Return whether a reference is registered."""

        return self.registry.has(reference_id)

    def remove(self, reference_id: str) -> Reference:

        """Remove and return a registered reference."""

        return self.registry.remove(reference_id)

    def ids(self) -> tuple[str, ...]:

        """Return registered reference identifiers."""

        return self.registry.ids()

    def clear(self) -> None:

        """Remove all registered references."""

        self.registry.clear()

    def analyze(

        self,

        reference_id: str,

        visual_intent: VisualIntent,

    ) -> ReferenceAnalysis:

        """Analyze one registered reference against VisualIntent.

        The analysis performs structural checking first, followed by

        attribute-level comparison and conflict reporting.

        Args:

            reference_id: Identifier of the registered reference.

            visual_intent: VisualIntent to compare against.

        Returns:

            Complete immutable ReferenceAnalysis.

        Raises:

            TypeError: If visual_intent is not a VisualIntent.

            KeyError: If the reference is not registered.

        """

        if not isinstance(visual_intent, VisualIntent):

            raise TypeError(

                "visual_intent must be a VisualIntent"

            )

        reference = self.registry.get(reference_id)

        structural_findings = self._checker.check(

            reference,

            visual_intent,

        )

        comparison_findings = self._comparator.compare(

            reference,

            visual_intent,

        )

        conflict_report = self._reporter.build_report(

            comparison_findings,

        )

        return ReferenceAnalysis(

            reference_id=reference.reference_id,

            structural_findings=structural_findings,

            comparison_findings=comparison_findings,

            conflict_report=conflict_report,

        )