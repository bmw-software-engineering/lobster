# Tool Class Inheritance

All classes representing LOBSTER tools shall inherit from `MetaDataToolBase`.

## Command Line Arguments
The class offers an instance of `ArgumentParser` via `self._argument_parser`,
which can be used to define command line arguments for the subclass.
Defining more arguments must happen in the constructor of the subclass.

The following arguments are added by the `MetaDataToolBase` class:
- "-h" and "--help"
- "-v" and "--version"

## Tool Logic
The `run()` method parses the arguments.
If the help or version messages shall not be printed,
then the private `_run_impl()` method is called afterwards.
It must be overwritten by the subclass.
The logic of the tool shall be implemented in this function.

## Error Handling
The `_run_impl()` method shall return the tool exit code.
It is recommended that the method does not raise exceptions.
It shall print user-friendly error messages to `stderr` instead,
and return an appropriate exit code.
