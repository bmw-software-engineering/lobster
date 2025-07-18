from tests_unit.lobster_trlc.trlc_hierarchy_data_test_case import \
    TrlcHierarchyDataTestCase
from lobster.tools.trlc.errors import (
    TupleComponentError, TupleError, TupleToStringFailedError, TupleToStringMissingError,
)

class ErrorTest(TrlcHierarchyDataTestCase):
    """This class tests the constructors of the error classes.
    
       This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details.
       The reason for this decision is that the TRLC AST data is challenging to mock.
    """
    def assertErrorDetails(self, error: TupleError, tuple_aggregate):
        message = str(error)
        self.assertIn(tuple_aggregate.typ.name, message)
        self.assertIn(str(tuple_aggregate.to_python_object()), message)
        self.assertIn(tuple_aggregate.location.to_string(), message)
        self.assertIn(tuple_aggregate.typ.location.to_string(), message)
        self.assertIs(error.tuple_aggregate, tuple_aggregate)

    def test_error_constructors(self):
        for record_object in self._get_level4b_record_objects():
            tuple_aggregate = record_object.field["tuple_field1"]

            error = TupleToStringFailedError(tuple_aggregate, earlier_errors=[])
            self.assertErrorDetails(error, tuple_aggregate)

            error = TupleToStringMissingError(tuple_aggregate)
            self.assertErrorDetails(error, tuple_aggregate)

            error = TupleComponentError("component_name", tuple_aggregate)
            self.assertErrorDetails(error, tuple_aggregate)
