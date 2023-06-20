# LOBSTER Release Notes

## Changelog


### 0.9.7-dev



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
