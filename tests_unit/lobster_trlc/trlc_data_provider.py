from pathlib import Path
from typing import Callable, Iterable, List, Optional, Set
from unittest import TestCase
from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager
from trlc import ast


__unittest = True


class TrlcDataProvider:
    """This class provides infrastructure to run tests with real TRLC
       data as input, no mocks.
       The TRLC data is stored in the 'data' subdirectory of this test module.
    """

    def __init__(
            self,
            callback_test_case: TestCase,
            trlc_input_files: List[Path],
            expected_record_object_names: Optional[Set[str]] = None,
            expected_tuple_type_names: Optional[Set[str]] = None,
            expected_record_type_names: Optional[Set[str]] = None,
        ) -> None:
        """Processes the TRLC files and populates the symbol table with the
           expected record objects and tuple types.

           :param callback_test_case: The test case that will be used to call assert
               functions to verify the correctness of the test setup.
           :param trlc_input_files: A list of TRLC input files to be processed.
           :param expected_record_object_names: A set of expected record object names
               that should be present in the symbol table after processing the TRLC files.
           :param expected_tuple_type_names: A set of expected tuple type names that
               should be present in the symbol table after processing the TRLC files.
        """
        # pylint: disable=too-many-arguments
        def init_set(value: Optional[Set[str]]) -> Set[str]:
            return value if value is not None else set()

        # initialization
        self._sm = Source_Manager(Message_Handler())
        self._callback_test_case = callback_test_case
        self._expected_record_object_names = init_set(expected_record_object_names)
        self._expected_record_type_names = init_set(expected_record_type_names)
        self._expected_tuple_type_names = init_set(expected_tuple_type_names)
        # register and process the TRLC input files
        for file in trlc_input_files:
            self._sm.register_file(str(file))
        self._symbol_table = self._sm.process()
        self._callback_test_case.assertIsNotNone(
            self._symbol_table,
            "Invalid test setup: Failed to process TRLC data!",
        )

    @property
    def symbol_table(self) -> ast.Symbol_Table:
        """Returns the symbol table containing the processed TRLC data."""
        return self._symbol_table

    def get_tuple_types(self) -> List[ast.Tuple_Type]:
        """Returns all tuple types in the symbol table and ensures they match exactly
           the expected types."""
        result = []
        for n_pkg in self._symbol_table.values(ast.Package):
            for tuple_type in n_pkg.symbols.values(ast.Tuple_Type):
                result.append(tuple_type)
        names = set(n_obj.name for n_obj in result)
        self._callback_test_case.assertSetEqual(
            names,
            self._expected_tuple_type_names,
            "Invalid test setup: TRLC input files do not contain the expected "
            "tuple types!",
        )
        return result

    def get_record_objects(self) -> Iterable[ast.Record_Object]:
        """This function returns a list of all record objects in the symbol table,
           and at the same time ensures that the symbol table is correctly populated
           with the expected record objects.
           Always use this function in unit tests to iterate over the record objects.
        """
        result = list(self._symbol_table.iter_record_objects())
        names = set(n_obj.name for n_obj in result)
        self._callback_test_case.assertSetEqual(
            names,
            self._expected_record_object_names,
            "Invalid test setup: TRLC input files do not contain the expected "
            "record objects!",
        )
        return result

    def get_filtered_record_objects(
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
        result = [n_obj for n_obj in self.get_record_objects()
                  if op(n_obj.n_typ.name, record_type_name)]
        self._callback_test_case.assertGreater(
            len(result),
            0,
            f"Invalid filter: No record objects of type '{record_type_name}' found!",
        )
        return result

    def get_record_types(self) -> Iterable[ast.Record_Type]:
        """Returns all record types in the symbol table."""
        record_types = []
        for n_pkg in self._symbol_table.values(ast.Package):
            for n_typ in n_pkg.symbols.values(ast.Record_Type):
                record_types.append(n_typ)
        names = set(record_type.name for record_type in record_types)
        self._callback_test_case.assertSetEqual(
            names,
            self._expected_record_type_names,
            "Invalid test setup: TRLC input files do not contain the expected "
            "record types!",
        )
        return record_types
