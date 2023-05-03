# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**racability
**E**vidence **R**eport allows you to demonstrate software tracability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This repository contains the prototype for LOBSTER, which is a key
ingredient to make TRCL more useful.

It has tools to extract tracing tags from a variety of sources,
combine them and produce a tracing report. You can look at a [canned
example](https://bmw-software-engineering.github.io/lobster/example_report.html)
from [the
testsuite](integration-tests/projects/basic),
which combines a variety of languages and tools into a single report.

## Installing

All tools can be installed separately from PyPI, but there is a
convenient meta-package `bmw-lobster` which installs everything.

```
$ pip3 install bmw-lobster
```

## Supported inputs

The following requirements frameworks are supported:

* [TRLC](work-in-progress) (only some use cases supported right now)
* [Codebeamer](lobster-tool-codebeamer) (only some use cases supported
  right now)

The following programming languages are supported:

* [C/C++](lobster-tool-cpp)
* [Python3](lobster-tool-python)
* [SIMULINK and MATLAB](https://misshit.org) using the 3rd-party tool
  MISS_HIT; supports both code and tests

The following verification and miscellaneous frameworks are supported:

* [GoogleTest](lobster-tool-gtest)
* [JSON](work-in-progress) useful if your test framework is encoded in
  JSON

## Documentation

* Writing [configuration files](docs/config_files.md) for LOBSTER.
* It is easy to expand the languages and activities supported by
  LOBSTER by adding new tracing tools, as long as they create data in
  the [common interchange format](docs/schemas.md) for LOBSTER.

(More to come...)

## Installing individual packages

The individual packages that `bmw-lobster` depends on are:

* `bmw-lobster-core` the core API and various report generators. All
  other tools depend on this.
* `bmw-lobster-tool-cpp` (for C/C++ code)
* `bmw-lobster-tool-gtest` (for GoogleTest tests)
* `bmw-lobster-tool-python` (for Python3 code)
* `bmw-lobster-tool-beamer` (for requirements in Codebeamer)
* `miss_hit` (for MATLAB/Octave code or Simulink models)

## Planned inputs

The following inputs are planned but not implemeted yet:

* `lobster-java`: Java code
* `lobster-kotlin`: Kotlin code
* `lobster-ada`: Ada and SPARK code (via libadalang)
* `lobster-latex`: Requirements written in LaTeX
* `lobster-markdown`: Requirements written in Markdown

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version 3](LICENSE.md).
