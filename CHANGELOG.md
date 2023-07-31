# LOBSTER Release Notes

## Changelog


### 0.9.11-dev



### 0.9.10

* Expose justification mechanism for JSON files (up only).

* Expose justification mechanism for TRLC files (up, down, and
  global).

* Improve stats display in HTML report.

* The `lobster-python` tool now has special support for PyUnit tests.

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
