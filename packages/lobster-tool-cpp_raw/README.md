# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C or C++
source code.

This tool searches for tracing tags `lobster-trace`
and extracts the name information of the function occurrence.
To be able to extract the information, the tracing tag has to be
placed in a comment line directly above the function declaration.

## Tools

* `lobster-cpp_raw`: Extract requirements from C/C++ code using a
  a simple text extracting algorithm and a regex to identify
  function declarations.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
