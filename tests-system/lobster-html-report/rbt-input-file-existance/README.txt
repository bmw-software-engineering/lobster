There are two tests:
- input file exists
- input file does not exist

The content of the `*.lobster` input files do not matter for the above test cases.

The tests only verify:
- that the error message is printed if the file is missing, and vice versa,
- that the tool return code is 1 (or not 0)

These tests assume that the `dot` utility is not available.
This will generate a warning message, which is of no interest here.
