# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This repository contains the prototype for LOBSTER, which is a key
ingredient to make TRCL more useful.

It has tools to extract tracing tags from a variety of sources combine
them and produce a tracing report. The [TRLC tracing
report](https://bmw-software-engineering.github.io/trlc/tracing.html)
from the [TRLC
Project](https://github.com/bmw-software-engineering/trlc/) is a
reasonable example of what is possible.

## Installing

All tools can be installed separately from PyPI, but there is a
convenient meta-package `bmw-lobster` which installs everything.

```
$ pip3 install bmw-lobster
```

## Supported inputs

The following requirements frameworks are supported:

* [TRLC](work-in-progress) (only some use cases supported right now)
* [Codebeamer](packages/lobster-tool-codebeamer/README.md) (only some
  use cases supported right now)

The following programming languages are supported:

* [C/C++](packages/lobster-tool-cpp/README.md)
* [Python3](packages/lobster-tool-python/README.md)
* [SIMULINK and MATLAB](https://misshit.org) using the 3rd-party tool
  MISS_HIT; supports both code and tests

The following verification and miscellaneous frameworks are supported:

* [GoogleTest](packages/lobster-tool-gtest/README.md)
* [JSON](packages/lobster-tool-json/README.md) useful if your test
  framework is encoded in JSON

## Documentation

* Writing [configuration files](documentation/config_files.md) for LOBSTER.
* It is easy to expand the languages and activities supported by
  LOBSTER by adding new tracing tools, as long as they create data in
  the [common interchange format](documentation/schemas.md) for LOBSTER.

(More to come...)

## Installing individual packages

The individual packages that `bmw-lobster` depends on are:

* `bmw-lobster-core` the core API and various report generators. All
  other tools depend on this.
* `bmw-lobster-tool-cpp` (for C/C++ code)
* `bmw-lobster-tool-gtest` (for GoogleTest tests)
* `bmw-lobster-tool-python` (for Python3 code)
* `bmw-lobster-tool-beamer` (for requirements in Codebeamer)
* `bmw-lobster-tool-json` (for activities in JSON)
* `miss_hit` (for MATLAB/Octave code or Simulink models)

### For LOBSTER developers

* [Code Coverage Report](https://bmw-software-engineering.github.io/lobster/htmlcov/index.html)

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
