import operator
from pathlib import Path
from typing import Callable, Iterable
from unittest import TestCase
from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager
from trlc import ast


class IntegrationTestCaseBase(TestCase):
    """This unit test base class provides infrastructure to run tests with real TRLC
       data as input, no mocks.
       The TRLC data is stored in the 'data' subdirectory of this test module.
       An inheriting test class can hence be considered as an integration test of
       classes and functions, and less as pure unit tests.
    """

    # Instances of Level4B have a tuple field
    LEVEL4B_TYPE_NAME = "Level4B"

    # The record objects that are expected to be present in the symbol table
    _EXPECTED_RECORD_OBJECTS = (
        "Level1_Item",
        "Level2A_Item",
        "Level2B_Item",
        "Level3A_Item",
        "Level3B_Item",
        "Level4A_Item",
        "Level4B_Item",
    )

    def setUp(self) -> None:
        self._sm = Source_Manager(Message_Handler())
        rsl_file = Path(__file__).parent / "data" / "hierarchy_tree.rsl"
        trlc_file = Path(__file__).parent / "data" / "hierarchy_tree.trlc"
        self._sm.register_file(str(rsl_file))
        self._sm.register_file(str(trlc_file))
        self._symbol_table = self._sm.process()
        self.assertIsNotNone(
            self._symbol_table,
            "Invalid test setup: Failed to process TRLC data!",
        )

    def _get_record_objects(self) -> Iterable[ast.Record_Object]:
        """This function returns a list of all record objects in the symbol table,
           and at the same time ensures that the symbol table is correctly populated
           with the expected record objects.
           Always use this function in unit tests to iterate over the record objects.
        """
        result = list(self._symbol_table.iter_record_objects())
        names = tuple(n_obj.name for n_obj in result)
        self.assertTupleEqual(names, self._EXPECTED_RECORD_OBJECTS)
        return result

    def _get_filtered_record_objects(
            self,
            record_type_name: str,
            op: Callable[[str, str], bool],
    ) -> Iterable[ast.Record_Object]:
        """This function filters the record objects by their type name using the
           provided operator. The operator can be '==', '!=', or any custom Callable
           that takes two string arguments and returns a boolean.
           The function returns a list of record objects that match the filter criteria.

           The function guarantees that at least one such object exists in the symbol
           table. Otherwise, it fails the test. This is a safety measure to ensure
           that the test setup is correct and that the test iterates over at least
           one record object.
        """
        result = [n_obj for n_obj in self._get_record_objects()
                  if op(n_obj.n_typ.name, record_type_name)]
        self.assertGreater(
            len(result),
            0,
            f"Invalid filter: No record objects of type '{record_type_name}' found!",
        )
        return result

    def _get_level4b_record_objects(self) -> Iterable[ast.Record_Object]:
        """This function returns all record objects of type Level4B.
        """
        return self._get_filtered_record_objects(self.LEVEL4B_TYPE_NAME, operator.eq)
