"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import get_tap_test_class

from tap_jotform.tap import TapJotform

SAMPLE_CONFIG: dict[str, Any] = {}

TestTapJotform = get_tap_test_class(TapJotform, config=SAMPLE_CONFIG)
