import unittest
from unittest import TestCase

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.test_status import (
    TestStatus,
)


class TestTestStatus(TestCase):
    def test_from_string_label(self) -> None:
        labels = [
            "NO STATUS",
            "NO_STATUS",
            "(cached) PASSED",
            "CACHED_PASSED",
            "PASSED",
            "FAILED",
            "FLAKY",
            "TIMEOUT",
            "GLOBAL_PROBLEM",
        ]

        targets = [
            TestStatus.NO_STATUS,
            TestStatus.NO_STATUS,
            TestStatus.CACHED_PASSED,
            TestStatus.CACHED_PASSED,
            TestStatus.PASSED,
            TestStatus.FAILED,
            TestStatus.FLAKY,
            TestStatus.TIMEOUT,
            TestStatus.GLOBAL_PROBLEM,
        ]

        for label, target in zip(labels, targets):
            self.assertEqual(TestStatus.from_string_label(label), target)


if __name__ == "__main__":
    unittest.main()
