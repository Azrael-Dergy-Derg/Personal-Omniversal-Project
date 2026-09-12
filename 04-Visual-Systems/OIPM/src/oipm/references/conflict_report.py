"""Conflict reporting for the OIPM Reference & Consistency System.

This module organizes consistency comparison findings into an explicit

conflict report.

The report is informational. It does not:

- resolve conflicts,

- choose an authoritative source,

- modify VisualIntent,

- modify references,

- promote references to canon,

- invent missing information,

- or silently discard mismatches.

Conflict resolution belongs to a separate decision/rules layer.

"""

from __future__ import annotations

from dataclasses import dataclass

from oipm.references.consistency_comparator import (

    ComparisonFinding,

    ComparisonStatus,

)

@dataclass(frozen=True)

class Conflict:

    """Structured representation of a detected reference conflict.

    Attributes:

        reference_id: Identifier of the reference involved.

        attribute: Attribute that differs between the reference and

            VisualIntent.

        reference_value: Value supplied by the reference.

        visual_intent_value: Corresponding VisualIntent value.

        message: Human-readable description of the conflict.

    A Conflict records disagreement only. It does not determine which

    value should be retained.

    """

    reference_id: str

    attribute: str

    reference_value: object

    visual_intent_value: object

    message: str

@dataclass(frozen=True)

class ConflictReport:

    """Immutable report containing detected reference conflicts.

    Attributes:

        conflicts: Deterministically ordered detected conflicts.

        finding_count: Number of comparison findings examined.

        conflict_count: Number of mismatches represented by the report.

    The report contains no resolution decision.

    """

    conflicts: tuple[Conflict, ...]

    finding_count: int

    conflict_count: int

class ConflictReporter:

    """Convert comparison findings into explicit conflict reports."""

    def build_report(

        self,

        findings: tuple[ComparisonFinding, ...],

    ) -> ConflictReport:

        """Build a conflict report from comparison findings.

        Only findings with a status of MISMATCH become conflicts.

        MATCH and UNAVAILABLE findings remain outside the conflict list.

        UNAVAILABLE does not mean that a conflict exists; it means there

        is insufficient comparable information.

        Args:

            findings: Comparison findings produced by

                ConsistencyComparator.

        Returns:

            Immutable ConflictReport.

        Raises:

            TypeError: If findings is not a tuple or contains an invalid

                finding.

        """

        if not isinstance(findings, tuple):

            raise TypeError("findings must be a tuple")

        for finding in findings:

            if not isinstance(finding, ComparisonFinding):

                raise TypeError(

                    "findings must contain ComparisonFinding objects"

                )

        conflicts = tuple(

            self._to_conflict(finding)

            for finding in findings

            if finding.status is ComparisonStatus.MISMATCH

        )

        return ConflictReport(

            conflicts=conflicts,

            finding_count=len(findings),

            conflict_count=len(conflicts),

        )

    @staticmethod

    def _to_conflict(

        finding: ComparisonFinding,

    ) -> Conflict:

        """Convert a mismatch finding into a Conflict."""

        return Conflict(

            reference_id=finding.reference_id,

            attribute=finding.attribute,

            reference_value=finding.reference_value,

            visual_intent_value=finding.visual_intent_value,

            message=finding.message,

        )