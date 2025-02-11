The goal of these test cases is to check if an error message gets printed
if one of the input files to the lobster-json tool does not exist.

There are two test setups:
- one that uses only paths to files that do not exist
- one that uses two paths, where one exists and the other does not.

Note regarding test setup:
The parameter `--out` is omitted, because the expectation is that, no lobster output is
generated.
Currently the system test framework cannot verify that **no** output file has been
created.
It can only test that the expected output files have been created.
But the framework can verify that the `STDOUT` is equal to an expected string, and by
omitting `--out` any output will be written to `STDOUT`.
This way we can verify that indeed no lobster output is generated.
The tool could create output for the valid paths, and ignore the invalid paths.
This would violate the requirements.
