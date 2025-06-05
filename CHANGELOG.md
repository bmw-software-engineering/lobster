# LOBSTER Release Notes

## Changelog


### 0.12.3-dev

* `lobster-report`
  - If there are zero items in one level of the tracing policy, then this level now
    shows a coverage of 0%.
    Previously its coverage was 100%.
    Note that the coverage ratio cannot be computed in a mathematical way if there
    are zero items, because the formula requires to divide by the total number of items.
    If this denominator is zero, obviously the division cannot be performed.
    So neither 100% nor 0% makes sense, but choosing 0% is the safe decision
    when the tool is used in a safety-critical context.
    Having zero input items is probably not what the user intended to do,
    and shall be notified about this empty input.
    The user has a greater chance to detect this empty input if the report shows 0% coverage
    compared to 100%, which indicates that everything is okay.

* `lobster-cpp`
  * The file basename is used to construct the function UID.
    A counter is then appended to the basename to handle situations where files in
    different folders have the same basename.
    Now `lobster-cpp` and `lobster-cpptest` use the same logic to generate function UIDs.
  * The `*.lobster` output file uses the absolute path for location entries instead of a
    relative path.
    This simplifies the usage of the LOBSTER tools, for instance in a CI system, where
    different tools are called from different working directories.

* `lobster-codebeamer`
  - Fix for handling `references` as a list of field names instead of a dictionary.

* `lobster-html-report`
  - The SVG's in the HTML report were rendered on every use. Now the SVGs
    are rendered once and reused for at all the remaining occurences.
    This will reduce the overall HTML file size.
  - Displays custom data (if provided) in the top-right corner of the HTML report.

* `Separate Coverage Reports`
  - Separate coverage reports for unit tests (`.coverage.unit`) and system tests (`.coverage.system`).

### 0.12.2

* `lobster-online-report`
  - Fix for git hash generation for submodules when the tool is executed from 
    outside a git repository where the submodule is specified as a relative path.

* `lobster-cpptest`
  - Add support for identical test case files in different folders:
    If test cases exist in different files with the same file names, same test case names
    and same line numbers, then previously these were treated as duplicate definitions
    by `lobster-report`.
    Now `lobster-cpptest` generates a unique ID by appending a counter to the file base
    name, which is used as tag in the final report.
    An alternative had been to use the absolute or relative path of the file instead of
    just the file base name, but that would have decreased the readability of the report.

* `lobster-html-report`:
  - Fix bug where `/cb` appeared twice in codebeamer URLs, leading to an incorrect URL.
  - Fix bug where codebeamer URLs always pointed to the HEAD version of the codebeamer item,
    even if a specific version was given.
  - Add encoding tag to HTML header.
    This fixes rendering issues of symbols in the generated HTML file.

### 0.12.1

* `lobster-html-report`
  - Fix for timestamp generation of git hashes for git submodules. 
 
* `lobster-codebeamer`
  - Added configurable retry logic for HTTPS requests. Introduced support for two new YAML configuration parameters:
    - `retry_error_codes`: A list of HTTP status codes (e.g., `[429, 503, 504]`) that should trigger a retry.
    - `num_request_retry`: An integer specifying the maximum number of retry attempts if a request fails with a status code from `retry_error_codes`.
  - Fix for `.netrc`-based authentication handling in the `lobster-codebeamer` tool when
  fetching the machine name (domain name).

* `lobster-cpptest` 
  - The tool now writes orphan tests into all output files.
  - It now displays a test-name instead of a fixture-name
  in the lobster-report and lobster-html-report.

* `lobster-online-report`
  - Fix for git hash generation when the tool is executed from 
  outside a git repository where the .git folder is not available.
  - Reformulate the summary message so that it becomes clear whether the input file has been modified, or whether a new output file has been created.

* `lobster-cpp` 
  - The uses the relative file path of a c++ file to generate 
  the unique identifier of a function in that file. This way files with identical
  names (but in different folders) are supported, and they can even have
  C++ functions with identical names without running into a
  "duplicate definition" problem.
  Previously only the file's base name was used.
  - Add command line argument `--skip-clang-errors` to `lobster-cpp`.
  This argument allows the user to specify a list of `clang-tidy`
  errors which shall be skipped.

### 0.12.0

* `lobster-trlc` and `lobster-json`
  - All command-line arguments except  `--config` and `--out` are 
  moved to Yaml based config file. `--config` and `--out` command-line arguments are still supported.

* `lobster-python` 
  - Add a note to [lobster-python](packages/lobster-tool-python/README.md)
  that it can be used for [Bazel](https://bazel.build/) files, too.
  - When running `lobster-python --activity` the tool assumes that Python methods with the following name pattern are tests:
    - name starting with `_test` or `test`
    - or name ending with `test`

    Previously only `test` was considered.

* `General updates`
  - Update installation instructions with `pip3` and `pipx`.

### 0.11.0

* `lobster-codebeamer`
  - Change the behavior of `lobster-codebeamer` such that an output file is always created, even if the codebeamer server has returned zero items.
  - The tool used to append `/cb` to the `root` parameter in config file 
  and now the user explicitly needs to add it while specifying the `root`.

* `lobster-trlc`
  - now requires at least version 2.0.1 of TRLC,
  as TRLC 2.0.1 contains the important bug fix
  [Detecting duplicated components](https://github.com/bmw-software-engineering/trlc/pull/121),
  including an essential improvement in the
  [Language Reference Manual](https://bmw-software-engineering.github.io/trlc/lrm.html).
  
    Without the TRLC bug fix `lobster-trlc` will not detect all traces if TRLC authors exploit the bug.
    
    Imagine the following TRLC snippet:
    ```
    Requirement Windscreen_Wiper {
      derived_from = [Safety_Critical_Requirement]
      derived_from = [Boring_Requirement]
    }
    ```
    Here the trace from `Windscreen_Wiper` to `Safety_Critical_Requirement` will not 
    be detected by `lobster-trlc` if the version of `trlc` is less than 2.0.1.

* `lobster-online-report`
  - The `--commit` command line argument in the tool is now 
  removed and no longer available. It was redundant and is already replaced by the 
  automated git hash feature that doesn't require user intervention and is handled 
  by the code. See changelog `0.10.0` for more information.

* `lobster-cpptest`
  - Removed limitation from `lobster-cpptest` which skipped output files that had less than two LOBSTER items.

* `lobster-json` 
  - Minor fix of handling multithreading.
  - Introduced YAML-based configuration for `lobster-json`, replacing individual command-line arguments.
  - Added a `--config` argument to specify a YAML configuration file.
    - Eliminated the command-line arguments `--single`, `--inputs`, and `--inputs-from-file`,
    unifying user interaction across all lobster tools. Values can now be specified 
    using the YAML configuration file.
    - The argument `--out` is still supported as command line argument, and takes precedence over any value given in the YAML configuration file.

* `lobster-html-report`
  - The title and placeholder for search box is renamed to `Filter` in 
  tool.
  - The tool gives consistent error message if the input file does not exist, even if the user specified no value. In that case the tool tries to open the file called `lobster.report` in the current working directory as input, and it gives the same error message if that file does not exist.

* `lobster-report`
  - If the constraint `valid_status` is omitted in the configuration file, then no status check is performed.

* `General updates`
  - Include dependency to `PyYAML` in [requirements.txt](requirements.txt).

### 0.10.0

* `lobster-html-report` adds actual git commit hashes to the source in the HTML report.

* `lobster-online-report` now contains the actual git commit hashes when the user executes the tool.

* The configuration management for the following tools has been migrated from 
  command-line arguments to YAML configuration files.
  * `lobster-cpptest`
  * `lobster-codebeamer`

### 0.9.21

* `lobster-codebeamer` now supports query string along with query ID, query string (cbQL) can be passed 
  as a command line argument to `--import-query` for the tool `lobster-codebeamer`.

* `lobster-html-report` has the following updates.
  * Filter items by status (Ok, Missing, Partial, Warning, Justified)
  * Hide/Unhide Issues.
  * Search in issues and detailed report.

* Add support to view version for lobster tools for following tools:
  - `lobster-ci-report`
  - `lobster-codebeamer`
  - `lobster-cpp`
  - `lobster-cpptest`
  - `lobster-gtest`
  - `lobster-html-report`
  - `lobster-json`
  - `lobster-online-report`
  - `lobster-python`
  - `lobster-report`
  - `lobster-trlc`

### 0.9.20

* Add `--compile-commands` flag to `lobster-cpp`. This allows to specify a path to the
  compile command database and is effectively a wrapper around the `-p` argument of
  `clang tidy`. See the official documentation of `clang tidy` for more details on this
  parameter.

* `lobster-cpptest` writes absolute paths into its `*.lobster` output files instead of
  paths relative to the current working directory.

* If a `*.lobster` file contains a tag more than once, then an error message
  ("duplicated definition") is printed for each consecutive entry with the same tag,
  instead of printing it just for the first entry.
  The following tools are affected:
  * `lobster-codebeamer`
  * `lobster-report`

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
