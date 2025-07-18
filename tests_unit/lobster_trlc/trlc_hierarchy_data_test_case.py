import operator
from pathlib import Path
from typing import Iterable
from unittest import TestCase
from trlc import ast

from tests_unit.lobster_trlc.trlc_data_provider import TrlcDataProvider


__unittest = True


class TrlcHierarchyDataTestCase(TestCase):

    PACKAGE_NAME = "hierarchy_tree_test"

    # Instances of Level4B have a tuple field
    LEVEL4B_TYPE_NAME = "Level4B"

    def setUp(self) -> None:
        self._trlc_data_provider = TrlcDataProvider(
            callback_test_case=self,
            trlc_input_files=[
                Path(__file__).parent / "data" / "hierarchy_tree.rsl",
                Path(__file__).parent / "data" / "hierarchy_tree.trlc",
            ],
            expected_record_object_names={
                "Level1_Item",
                "Level2A_Item",
                "Level2B_Item",
                "Level3A_Item",
                "Level3B_Item",
                "Level4A_Item",
                "Level4B_Item",
            },
            expected_tuple_type_names={
                "TwoValues",
                "ThreeValues",
                "FourValues",
            },
        )
        super().setUp()

    def _get_level4b_record_objects(self) -> Iterable[ast.Record_Object]:
        """This function returns all record objects of type Level4B.
        """
        return self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.eq,
        )
