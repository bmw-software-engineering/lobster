System tests run a tool and verify their output.
They are different from unit tests, which test single Python functions within a tool.

It runs on Windows and Linux.

# Features
This section describes the features of the LOBSTER system test framework.

It consists of these main classes: `Asserter`, `SystemTestCase` and `TestRunner`.

The `SystemTestCase` class inherits from `unittest` and takes care to provide
a temporary directory for the tool under test.

The `TestRunner`
- provides logic to prepare the temporary directory such that it
contains necessary input files,
- provides ways to set command line arguments,
- and can execute the tool under test.

The `Asserter` is a convenience class which implements assertions that are commonly
needed to verify the test result.

## Test Setup
During test setup, features of `TestRunner` are:
- enrich `*.lobster` files with current git hashes
  (not yet implemented, needed to test  `lobster-online-report`),
- copy input files to a temporary directory,
- and use the temporary directory as the current working directory.

Notes:
- For some tests it is mandatory to copy the input files into the current working
  directory, for others it is not.
  The current implementation of the system test framework *always* copies the input
  files into the temporary directory.
  This should be optimized in the future.
  For example, a test might verify that the tool under test scans the current working
  directory for input files.
  In this case it is necessary to prepare the directory properly.
  On the other hand, a test that verifies the output based on a certain input
  can have that input located anywhere in the file system.
  Here it is not necessary to copy the files. 
- The tool `lobster-html-report` should be executed in a virtual environment
  where one can control whether `graphviz` is available.
  The tool behaves differently whether the package is or is not available.
  Hence the system test framework should control the creation of the virtual
  environment.
  This is currently not supported.

## Test Execution
After test execution the `Asserter` class can compare actual values of the following data against their expectation values:
- `STDOUT`
- `STDERR`
- the tool exit code
- and all `*.lobster` and `*.html` files generated by the tool under test.

The class replaces the placeholder string `TEST_CASE_PATH` in `*.lobster` files with
actual paths of the current environment to ease the comparison of paths.
It also replaces all pairs of `\` with `/` for the same reason
(so `\\` becomes `/`).

The `TestRunner` measures the branch coverage.

## Teardown
During teardown the `SystemTestCase` class deletes every temporary folder.
Any files that the tool under test has created outside of this folder will not be
deleted and must be cleaned up separately.

# Traceability
The traces from system test cases to requirements can be collected by running `lobster-python`.
The target `system-tests.lobster-%` in the [Makefile](../Makefile) executes
`lobster-python` for a particular tool.
For example
```bash
> make system-tests.lobster-json
```
will create a file called `system-tests.lobster` which contains LOBSTER items that
- represent the system test cases of `lobster-json`,
- and contain information about the linked requirements.

# Deprecated Framework
The deprecated script `run_tool_tests.py` also executes system tests.
It can execute system tests for all lobster tools.

The one and only command line argument to the script must be the name of the tool under
test.
For example, to run system tests for `lobster-trlc`, the tool must be started like this:
```
> python3 run_tool_tests.py lobster-trlc
```

System test cases always consist of the following folder structure:
```
test-case/
├─ input/
│  ├─ args.txt
expected-output/
├─ exit-code.txt
├─ stderr.txt
├─ stdout.txt
├─ *.lobster

```

The target `make system-tests` in the root `Makefile` sets the current working
directory of the tool under test to the `input` folder.

The files must contain the following piece of information:
- `args.txt`:
  This file shall contain the command line arguments that must be used to start the tool
  under test. Each line represents a separate argument.
- `exit-code.txt`: This file shall contain the expected exit code of the tool under test.
- `stderr.txt`: This file shall contain the expected standard error stream of the tool
  under test.
- `stdout.txt`: This file shall contain the expected standard output stream of the tool
  under test.
- `*.lobster`: There can be zero to infinite many `*.lobster` files given. The tool
  under test is expected to generate all these files inside the current working directory
  during the execution of the test case.

Any additional files needed by the tool under test must be located in the `input`
folder.

The expected values will all be compared against their actual values, and test cases
only count as "passed" if the values match.

Each test case using this deprecated approach shall be migrated to the above approach using `unittest`.
