"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import get_standard_tap_tests

from tap_jotform.tap import TapJotform

SAMPLE_CONFIG: dict[str, Any] = {}


def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapJotform, config=SAMPLE_CONFIG)
    for test in tests:
        test()
