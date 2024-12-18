The script `run_tool_tests.py` executes system tests.
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

