# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This repository contains the prototype for LOBSTER, which is a key
ingredient to make [TRLC](https://github.com/bmw-software-engineering/trlc/)
and other supported tools more useful.

It has tools to extract tracing tags from a variety of sources to
combine them and produce a tracing report. The [TRLC tracing
report](https://bmw-software-engineering.github.io/trlc/tracing.html)
from the [TRLC
Project](https://github.com/bmw-software-engineering/trlc/) is a
reasonable example of what is possible when lobster is used in combination
with TRLC or any of the other supported tools.

## Installing

All tools can be installed separately from PyPI, but there is a
convenient meta-package `bmw-lobster` which installs everything.

```
$ pip3 install bmw-lobster
```
Note that some distributions require to run the installation command in a
virtual environment.
Under Linux:
```
python3 -m venv my-virtual-environment
source my-virtual-environment/bin/activate
pip3 install bmw-lobster
```

Alternatively, use `pipx`:
```
$ pipx install bmw-lobster --include-deps
```

For the HTML Report `graphviz` is also used to generate the tracing policy diagram. More on that in the user [manual](https://github.com/bmw-software-engineering/lobster/blob/main/documentation/user-manual.md).

```
$ sudo apt-get install -y graphviz
```

The `lobster-cpp` converter tool needs a specific version of `clang-tidy`. Please see [here](https://github.com/bmw-software-engineering/lobster/blob/main/documentation/user-manual.md#clang-tidy-file-generation) to create it.

## Supported inputs

The following requirements frameworks are supported:

* [TRLC](https://github.com/bmw-software-engineering/trlc/)
* [Codebeamer](packages/lobster-tool-codebeamer/README.md)

The following programming languages are supported:

* C++
  * [lobster-cpp](packages/lobster-tool-cpp/README.md) (to extract tags from target code)
  * [lobster-cpptest](packages/lobster-tool-cpptest/README.md) (to extract tags from test code)
* [Python3](packages/lobster-tool-python/README.md)
* [SIMULINK and MATLAB](https://misshit.org) using the 3rd-party tool
  MISS_HIT; supports both code and tests
* [Rust](https://github.com/NewTec-GmbH/lobster-rust) using the 3rd-party tool lobster-rust; currently only supports code

The following verification and miscellaneous frameworks are supported:

* Bazel, see [Python3](packages/lobster-tool-python/README.md)
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

The individual PyPI packages that `bmw-lobster` depends on are:

* `bmw-lobster-core` the core API and various report generators.
  All other tools depend on this.
  The package also contains core tools.
  See the package description for more details.
  [Link](https://pypi.org/project/bmw-lobster-core)
* `bmw-lobster-tool-codebeamer` (for requirements in Codebeamer) [Link](https://pypi.org/project/bmw-lobster-tool-codebeamer)
* `bmw-lobster-tool-cpp` (for C/C++ code) [Link](https://pypi.org/project/bmw-lobster-tool-cpp)
* `bmw-lobster-tool-cpptest` (for C/C++ code) [Link](https://pypi.org/project/bmw-lobster-tool-cpp)
* `bmw-lobster-tool-gtest` (for GoogleTest tests) [Link](https://pypi.org/project/bmw-lobster-tool-gtest)
* `bmw-lobster-tool-json` (for activities in JSON) [Link](https://pypi.org/project/bmw-lobster-tool-json)
* `bmw-lobster-tool-python` (for Python3 code) [Link](https://pypi.org/project/bmw-lobster-tool-python)
* `bmw-lobster-tool-trlc` (for TRLC code) [Link](https://pypi.org/project/bmw-lobster-tool-trlc)
* `miss_hit` (for MATLAB/Octave code or Simulink models) [Link](https://pypi.org/project/miss_hit)

### For LOBSTER developers

* [System Test Coverage Report](https://bmw-software-engineering.github.io/lobster/htmlcov-system/index.html)
* [Unit Test Coverage Report](https://bmw-software-engineering.github.io/lobster/htmlcov-unit/index.html)
* [Coding Guideline](CODING_GUIDELINE.md)
* [Requirements Guideline](lobster/tools/REQUIREMENTS.md)
* [System Test Framework](tests-system/README.md)

#### Requirements Coverage 

The requirement-to-test coverage is measured using LOBSTER itself.
Each LOBSTER tool has got a report on its own.
Here are the links to the individual requirement coverage reports:

* [Requirement Coverage Report TRLC](https://bmw-software-engineering.github.io/lobster/tracing-trlc.html)
* [Requirement Coverage Report Python](https://bmw-software-engineering.github.io/lobster/tracing-python.html)
* [Requirement Coverage Report Json](https://bmw-software-engineering.github.io/lobster/tracing-json.html)
* [Requirement Coverage Report Gtest](https://bmw-software-engineering.github.io/lobster/tracing-gtest.html)
* [Requirement Coverage Report Cpptest](https://bmw-software-engineering.github.io/lobster/tracing-cpptest.html)
* [Requirement Coverage Report Cpp](https://bmw-software-engineering.github.io/lobster/tracing-cpp.html)
* [Requirement Coverage Report Core CI Report](https://bmw-software-engineering.github.io/lobster/tracing-core_ci_report.html)
* [Requirement Coverage Report Core HTML Report](https://bmw-software-engineering.github.io/lobster/tracing-core_html_report.html)
* [Requirement Coverage Report Core Online Report](https://bmw-software-engineering.github.io/lobster/tracing-core_online_report.html)
* Requirement Coverge Report Core Online Report Nogit: not yet available
* [Requirement Coverage Report Core Report](https://bmw-software-engineering.github.io/lobster/tracing-core_report.html)
* [Requirement Coverage Report Codebeamer](https://bmw-software-engineering.github.io/lobster/tracing-codebeamer.html)

### Simple lobster-demo

A simple example can be found in the repository: [lobster-demo](https://github.com/bmw-software-engineering/lobster-demo).
It is still work in progress.

## Workflow of LOBSTER

The lobster tool uses several steps to accomplish a fully modular software traceability
and requirements coverage report.
You can consider lobster as a set of
1. conversion tools,
2. a common interchange format,
3. the report creation tool and
4. a renderer for the tracing report.

For a more detailed description please read our [user guide](https://github.com/bmw-software-engineering/lobster/blob/main/documentation/config_files.md).

These steps are in the following diagram and go from left to right side:

```mermaid
graph LR
    subgraph "Converter-Tools"
        direction TB
        A1[Lobster-python]
        A2[Lobster-trlc]
        A3[Lobster-json]
        A4[Lobster-cpp]
        A5[Lobster-codebeamer]
        A6[Lobster-gtest]
    end
 
    subgraph "Common inter. format"
        direction TB
        B1[Python.lobster]
        B2[Trlc.lobster]
        B3[Json.lobster]
        B4[Cpp.lobster]
        B5[Codebeamer.lobster]
        B6[Gtest.lobster]
    end
 
    subgraph "Generate lobster report"
        direction TB
        D1[Lobster-online-report]
        D1 ---> D2
        D2[Lobster-report -> report.lobster]
        D3[Tracing policy -> lobster.conf]
        D3 ---> D2
    end
 
    subgraph "Renderer"
        direction TB
        C1[html]
        C2[CI]
        C3["..."]
    end
 
    %% Main connections
    A1 ---> B1
    A2 ---> B2
    A3 ---> B3
    A4 ---> B4
    A5 ---> B5
    A6 ---> B6

 
    %% Connect all schema elements to Lobster-report -> report.lobster
    B1 ----> D2
    B2 ----> D2
    B3 ----> D2
    B4 ----> D2
    B5 ----> D2
    B6 ----> D2
 
    %% Connect Lobster-report -> report.lobster to renderers
    D2 ---> C1
    D2 ---> C2
    D2 ---> C3
 ```

## Planned inputs

The following inputs are planned but not implemented yet:

* `lobster-java`: Java code
* `lobster-kotlin`: Kotlin code

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version 3](LICENSE.md).
