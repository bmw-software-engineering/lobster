import unittest
from logging import CRITICAL, ERROR, INFO, WARNING
from unittest import TestCase

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import Event, logging


class TestEventLogger(TestCase):
    def setUp(self) -> None:
        self.levels = logging.levels
        list(logging.flush())

    def tearDown(self) -> None:
        list(logging.flush())
        logging.levels = self.levels
        logging.initlialized = False  # we cannot call basicConfig twice but we can fake it

    def _log_all_once(self) -> None:
        logging.critical("Critical")
        logging.error("Error")
        logging.warning("Warning")
        logging.info("Info")
        logging.debug("Debug")

    def test_basicConfig(self) -> None:
        self.assertFalse(logging.initialized)
        logging.basicConfig("error.log")
        self.assertTrue(logging.initialized)
        self.assertEqual(len(logging.events), 0)
        logging.basicConfig(filename=None)
        self.assertTrue(logging.initialized)
        self.assertEqual(len(logging.events), 1)
        self.assertEqual(logging.events[0].severity, ERROR)

    def test_log_error(self) -> None:
        logging.initlialized = True  # we cannot call basicConfig twice but we can fake it
        logging.error("Error")
        self.assertEqual(len(logging.events), 1)
        self.assertEqual(logging.events[0].severity, ERROR)
        self.assertEqual(logging.events[0].message, "Error")
        logging.debug("Debug")
        logging.info("Info")
        self.assertEqual(len(logging.events), 1)
        self.assertEqual(logging.events[0].severity, ERROR)
        self.assertEqual(logging.events[0].message, "Error")
        logging.critical("Critical")
        self.assertEqual(len(logging.events), 2)
        self.assertEqual(logging.events[1].severity, CRITICAL)
        self.assertEqual(logging.events[1].message, "Critical")
        logging.warning("Warning")
        self.assertEqual(len(logging.events), 3)
        self.assertEqual(logging.events[2].severity, WARNING)
        self.assertEqual(logging.events[2].message, "Warning")

    def test_flush_error(self) -> None:
        logging.initlialized = True  # we cannot call basicConfig twice but we can fake it
        logging.levels = [CRITICAL, ERROR]
        self._log_all_once()
        self.assertEqual(len(logging.events), 2)
        actual_log = logging.flush(ERROR)
        self.assertEqual(len(logging.events), 2)
        expected_log = [Event(CRITICAL, "Critical"), Event(ERROR, "Error")]
        for (actual, expected) in zip(actual_log, expected_log):
            self.assertEqual(actual, expected)
        self.assertEqual(len(logging.events), 0)

    def test_flush_warning(self) -> None:
        logging.initlialized = True  # we cannot call basicConfig twice but we can fake it
        logging.levels = [ERROR, INFO]
        self._log_all_once()
        self.assertEqual(len(logging.events), 2)
        actual_log = logging.flush(WARNING)
        self.assertEqual(len(logging.events), 2)
        expected_log = [Event(ERROR, "Error")]
        for (actual, expected) in zip(actual_log, expected_log):
            self.assertEqual(actual, expected)
        self.assertEqual(len(logging.events), 0)

    def test_getLevelName(self) -> None:
        self.assertEqual(logging.getLevelName(WARNING), "WARNING")


if __name__ == "__main__":
    unittest.main()
