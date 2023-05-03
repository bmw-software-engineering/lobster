# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**racability
**E**vidence **R**eport allows you to demonstrate software tracability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C or C++
source code. This tool is making use of a clang-tidy hack, and for
this to work you need to build [our clang-tidy
fork](https://github.com/bmw-software-engineering/llvm-project) and
place the `clang-tidy` binary somewhere on your PATH.

This tool works using a custom clang-tidy checker `lobster-trace`
which emits tracing information as clang checks.

We plan to rework this tool to be a stand-alone clang tool in the
future.

## Tools

* `lobster-cpp`: Extract requirements from C/C++ code using a
  clang-tidy hack

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version 3](../LICENSE.md).
