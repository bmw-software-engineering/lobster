from pathlib import Path
from unittest import TestCase

from tests_unit.lobster_trlc.trlc_data_provider import TrlcDataProvider


__unittest = True


class TrlcToStringDataTestCase(TestCase):

    PACKAGE_NAME = "to_string_test"

    def setUp(self) -> None:
        self._trlc_data_provider = TrlcDataProvider(
            callback_test_case=self,
            trlc_input_files=[
                Path(__file__).parent / "data" / "to_string_test.rsl",
                Path(__file__).parent / "data" / "to_string_test.trlc",
            ],
            expected_tuple_type_names={
                "ship",
            },
            expected_record_object_names={
                "BOBBY",
                "TONY",
                "ELLEN",
            },
        )
        super().setUp()
