from pathlib import Path
from unittest import TestCase

from tests_unit.lobster_trlc.trlc_data_provider import TrlcDataProvider


__unittest = True


class TrlcOptionalFieldTestCase(TestCase):

    PACKAGE_NAME = "optional_field_test"

    def setUp(self) -> None:
        self._trlc_data_provider = TrlcDataProvider(
            callback_test_case=self,
            trlc_input_files=[
                Path(__file__).parent / "data" / "optional_field_test.rsl",
                Path(__file__).parent / "data" / "optional_field_test.trlc",
            ],
            expected_record_object_names={
                "A",
                "B",
                "C",
            },
        )
        super().setUp()
