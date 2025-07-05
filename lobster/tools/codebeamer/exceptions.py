class QueryException(Exception):
    """This exception is raised when a query to the Codebeamer API fails."""


class NotFileException(Exception):
    """This exception is raised when a file is expected but the path does not point to
       a file.
    """


class MismatchException(Exception):
    """This exception is raised when there is a mismatch in the data retrieved from a
       codebeamer api call.
       For example, query page 7 has been requested, but the response data indicates
       page 8.
    """
