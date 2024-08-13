from __future__ import annotations

import enum


class TestStatus(enum.Enum):
    """Enum class that is used to define test result status

    Those results are defined by Zuul, except for RERUN which is an additional classification that (potentially) overrides the Zuul build result."""

    NO_STATUS = enum.auto()  # Defined in GTest
    CACHED_PASSED = enum.auto()  # Defined in GTest
    PASSED = enum.auto()  # Defined in GTest
    FAILED = enum.auto()  # Defined in GTest
    TIMEOUT = enum.auto()  # Defined in GTest
    GLOBAL_PROBLEM = enum.auto()
    FLAKY = enum.auto()
    RERUN = enum.auto()

    @classmethod
    def from_string_label(cls, label: str) -> TestStatus:
        """Creates TestStatus entity from label string.

        Parameters
        ----------
        label: str
            The input label.

        Returns
        -------
        TestStatus
            The corresponding TestStatus.
        """
        if label in ["NO STATUS", "NO_STATUS", cls.NO_STATUS]:
            test_status = cls.NO_STATUS
        elif label in ["(cached) PASSED", "CACHED_PASSED", cls.CACHED_PASSED]:
            test_status = cls.CACHED_PASSED
        elif label in ["PASSED", cls.PASSED]:
            test_status = cls.PASSED
        elif label in ["FAILED", cls.FAILED]:
            test_status = cls.FAILED
        elif label in ["FLAKY", cls.FLAKY]:
            test_status = cls.FLAKY
        elif label in ["TIMEOUT", cls.TIMEOUT]:
            test_status = cls.TIMEOUT
        else:
            assert label in ["GLOBAL_PROBLEM", cls.GLOBAL_PROBLEM], label
            return cls.GLOBAL_PROBLEM
        return test_status
