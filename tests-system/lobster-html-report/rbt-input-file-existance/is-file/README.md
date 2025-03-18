This test uses a little workaround:
The file extension of the HTML output file is set to `.lobster`,
because the system test infrastructure is currently only able to compare the actual
value to the expected value for files ending on `*.lobster` (and only these files
will be cleaned up after test execution).
