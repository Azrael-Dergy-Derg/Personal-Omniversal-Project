“”“Tests for the OIPM VisualIntentValidator.”””

from future import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from oipm.models import Relationship, Subject, VisualIntent
from oipm.validation.visual_intent_validator import (
ValidationIssue,
VisualIntentValidator,
)

def test_valid_visual_intent_passes_validation() -> None:
“”“A structurally valid VisualIntent should pass validation.”””
intent = VisualIntent()
intent.metadata.user_input = “A dark fantasy dragon beneath a moonlit sky.”