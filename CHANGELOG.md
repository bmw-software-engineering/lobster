# LOBSTER Release Notes

## Changelog


### 0.9.20-dev

* Enhanced Configuration Management: Transitioned from command-line arguments to YAML
  configuration files for LOBSTER-Codebeamer tools.

  **Rationale:** Managing numerous parameters via command-line arguments was cumbersome and error-prone for users.

  **Benefits:** Improved configurability, better readability, and simplified management of tool settings.

* `lobster-gtest` accepts XML nodes other than `testcase`, but ignores them.

### 0.9.19

* `lobster-trlc` requires TRLC version 2.0.0.

* Fixed bug in `lobster-python` where the tag for functions was constructed by using
  only the class name, not the function name. Now both the class name and function name
  are included in the tag.

* Add support to `lobster-codebeamer` to generate output using the following schemas:
  - requirement
  - implementation
  - activity

  The user can select the schema with a command line flag,
  or through the configuration file.

* Fixes packaging of `bmw-lobster`.

### 0.9.18

* Added a new tool `lobster-cpptest` which can extract references
  from C++ unit tests using various regex patterns.
  The references must be provided in a format similar to Doxygen comments.

* The `lobster-codebeamer` tool now uses an authentication token. 
  Token can be added either in the config file or as an argument.

* The `lobster-python` tool adds the counter logic to the function
  identifier. This improves the situations where different functions have
  the same name. Line numbers are no longer used in the identifier.

* The `lobster-codebeamer` tool now supports `refs` as an upstream reference
  
* The `lobster-online-report` tool now works with config files located in
  main- and submodules of a repository. This feature needs `git 1.7.8` or higher.

* The `lobster-codebeamer` tool now allows items without summary

* The `lobster-codebeamer` tool now uses codebeamer api v3.
  Please note that the api v3 returns the value "Unset" for a codebeamer
  item status if the status is actually empty. The api v1 did not return
  any value at all for an item with a missing status. This means that the
  resulting lobster file will now contain "Unset" as status information,
  too, instead of `Null`.

* The `lobster-html-report` tool now supports argument `--high-contrast` to use
  a color palette with a higher contrast for easier visualization.

### 0.9.17

* The `lobster-python` tool now adds the line number to the function
  identifier. This supports situations where different functions have
  the same name

* The `lobster-json` tool now adds the filename to the test identifier.
  This allows to have multiple json elements with the same name in
  different source files

* The `lobster-html-report` tool now supports argument `--dot` to specify
  the path to the graphviz dot utility instead of expecting it in PATH

* The `lobster-online-report` tool now supports argument `--out` to specify 
  the output file instead of editing the input report

* Adds `with kind` and `with prefix` functionality in lobster.conf files

### 0.9.16

* Fix infinite loop in `lobster-json` on Windows when given absolute
  paths.

* The `lobster-python` tool now also supports decorators with `.` in
  their name.

* The `lobster-python` tool now adds any tags on the test class to all
  tests in that class (in `--activity` mode only).

* The `lobster-python` tool now supports lists of tags in decorators.

### 0.9.15

* The `lobster-html-report` tool now respects line-breaks in item
  descriptions.

* The `lobster-python` tool now also includes the module name if you
  trace to a class, similar to how the module name is included if you
  trace to a function or method.

* Improve error reporting of `lobster-codebeamer`, you should get way
  fewer raw exceptions and instead more helpful messages.

* Add two new parameters to `lobster-codebeamer` if your codebeamer
  instance is painfully slow: `--timeout` to increase the timeout for
  each REST query and `--query-size` to limit how many items are
  attempted to be fetched at once.

* Add support for codebeamer items without a summary. They are now
  named something like "Unnamed item 12345". These items will show up
  as problematic in the tracing report.

### 0.9.14

* The `lobster-codebeamer` tool has a new option `--ignore-ssl-errors`
  which can be used to ignore certificate validation errors.

### 0.9.13

* The `lobster-json` tool can now deal with singleton tests (i.e. in
  places where a list of tests is expected, a single test object is
  now also allowed).

### 0.9.12

* The `lobster-trlc` tool now includes the TRLC package in the
  requirement's name.

* Rewrote the `lobster-json` tool to be more robust.
  * The `lobster-json` tool now uses a new, intended to be common,
    interface for building lobster tools. These tools can now process
    files in parallel, and also allow you to specify a file containing
    a line-separated list of files to consider (if you can't specify
    all the files you want to look at on the command-line).
  * The `lobster-json` tool can now process json files where the
    outermost item is an object.
  * Removed `--include-path-in-name` flag as it is now the default for
    `lobster-json`.
  * Removed `--item-kind` flag (we always generate activities now).

### 0.9.11

* The `lobster-online-report` now supports submodules.

* The `lobster-python` is now less fragile and continues processing
  other files in the face of encoding or python parse errors.

* Fixed a crash in `lobster-python` for comments at module level.

### 0.9.10

* Expose justification mechanism for JSON files (up only).

* Expose justification mechanism for TRLC files (up, down, and
  global).

* Improve stats display in HTML report.

* The `lobster-python` tool now has special support for PyUnit tests.

* The `lobster-python` tool now has two ways to annotate classes:
  either the entire class, or each individual method.

### 0.9.9

* In the HTML report, items are now sorted in a meaningful way.

* A Tracing_Tag can now have spaces in the name, but still not in the
  namespace. This fixes a few Simulink issues where spaces in names
  are quite common.

### 0.9.8

* There is now also a monolithic wheel available
  `bmw-lobster-monolithic` which installs the same things as
  `bmw-lobster`. It is *not recommended* to use this package, unless
  you want to integrate with bazel. The reason for this is that
  `py_wheel` does not deal well with overlapping installs, and so
  having a single wheel is preferable.

### 0.9.7

* `lobster-codebeamer` now also consults the `~/.netrc` file, if
  present, as an alternative to providing authentication in the
  environment or command-line.

* Fix missing `__init__.py` files for the packages `lobster.tools`,
  `lobster.tools.trlc`, and `lobster.tools.json`.

### 0.9.6

* `lobster-report` now has an `--out` option, to bring it in line with
  the other tools

### 0.9.5

* `lobster-codebeamer` now issues better error messages if you made a
  mistake in the query id.

* `lobster-gtest` now deals with older versions of googletest which do
  not embedd file name into the XML output. These locations are either
  guessed or simply made into `<unknown source>`. Traced tests using
  the macro provided always include a file/line number; this issue
  only affects untraced tests.

### 0.9.4

* `lobster-codebeamer` can now directly import codebeamer Queries.

### 0.9.3

* Fix copy/deepcopy bug in `lobster-trlc` where bogus error messages
  could be created for extensions of types using tuples.

### 0.9.2

* New tool [lobster-trlc](packages/lobster-tool-trlc/README.md) to
  extract [TRLC
  requirements](https://github.com/bmw-software-engineering/trlc).

* New tool [lobster-json](packages/lobster-tool-json/README.md) to
  extract data from JSON files representing verification activities.

### 0.9.1

* First PyPI release of several packages

  * bmw-lobster-core (report generation)
  * bmw-lobster-tool-cpp (C/C++ tracing)
  * bmw-lobster-tool-gtest (GoogleTest tracing)
  * bmw-lobster-tool-python (Python3 tracing)
  * bmw-lobster-tool-codebeamer (Codebeamer requirements import)
  * bmw-lobster (metapackage to install all the above)

* The TRLC and JSON tools are not quite ready for PyPI release
