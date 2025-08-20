from typing import Iterable
from trlc import ast


class TrlcFailure(Exception):
    """Exception if a TRLC API function indicated an error through its return value.
       In that case the TRLC message handler should have printed details to stdout, but
       these details are not provided through the API return value.
    """


class InvalidConversionRuleError(Exception):
    """Exception raised when a conversion rule is invalid, e.g., if it does not match
       any record type in the TRLC symbol table.
    """


# The errors below are usually raised when TRLC data could not be converted to a
# LOBSTER item


class RecordObjectComponentError(Exception):
    """Exception raised when a required component is missing in a RecordObject."""

    def __init__(self, component_name: str, record_object: ast.Record_Object):
        super().__init__(
            f"Component '{component_name}' not found in TRLC Record_Object "
            f"'{record_object.fully_qualified_name()}'!"
        )
        self.component_name = component_name
        self.record_object = record_object


class TupleError(Exception):
    """Exception raised for errors related to tuple aggregates."""

    def __init__(self, tuple_aggregate: ast.Tuple_Aggregate, message: str):
        super().__init__(message)
        self.tuple_aggregate = tuple_aggregate

    @staticmethod
    def tuple_details(tuple_aggregate: ast.Tuple_Aggregate) -> str:
        return f"tuple '{tuple_aggregate.typ.name}' " \
               f"with value '{tuple_aggregate.to_python_object()}', " \
               f"used at {tuple_aggregate.location.to_string()}, " \
               f"defined at {tuple_aggregate.typ.location.to_string()}"


class TupleComponentError(TupleError):
    """Exception raised when a to-string instruction cannot be applied to a tuple
       aggregate because a required component is missing.

       This can either be the case if the corresponding Tuple_Type does not have
       the required component at all, or if the component is not present (because)
       it is optional).
       """

    def __init__(self, component_name: str, tuple_aggregate: ast.Tuple_Aggregate):
        super().__init__(
            tuple_aggregate,
            f"Required tuple component "
            f"'{component_name}' is missing for "
            f"{self.tuple_details(tuple_aggregate)}!",
        )
        self.component_name = component_name


class TupleToStringMissingError(TupleError):
    """Exception raised when a to-string function is missing for a tuple aggregate."""

    def __init__(self, tuple_aggregate: ast.Tuple_Aggregate):
        super().__init__(
            tuple_aggregate,
            f"No 'to-string' function defined for "
            f"{self.tuple_details(tuple_aggregate)}!"
        )


class TupleToStringFailedError(TupleError):
    """Exception raised when all to-string conversion instructions failed to be
       applied to a tuple."""

    def __init__(
        self,
        tuple_aggregate: ast.Tuple_Aggregate,
        earlier_errors: Iterable[Exception],
    ):
        earlier_errors_text = '\n'.join(str(e) for e in earlier_errors)
        super().__init__(
            tuple_aggregate,
            f"All 'to_string' conversion functions failed for "
            f"{self.tuple_details(tuple_aggregate)}!\n"
            f"The following errors occurred when applying the given functions:\n"
            f"{earlier_errors_text}"
        )
        self.earlier_errors = earlier_errors
