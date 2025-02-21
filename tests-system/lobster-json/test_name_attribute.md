If the `--name-attribute` option is not specified,
then the tag name must be constructed based on the following two values:
- path of the json file
- item counter

# Test case "flat-input-structure"
- No files or directories are specified.
  The tool is expected to search for input files in the current working directory.
- `--name-attribute` is not given.
  The tool is expected to construct LOBSTER item tags by taking the file name and
  appending an integer counter, starting at 1.
  This is implemented inside function `syn_test_name`, and it must handle all file
  paths as relative paths, because no input files were given explicitly.
- `--out` is specified.
  The tool is expected to use that path name for the output file.
- `--single` is specified to make the tool output predictable.

# Test case "nested-input-structure"
This is the same as the above test, except that its input file is nested in a
sub-sub-directory.
The tool is expected to take the names of the sub-directories into account when
generating te tag name.
