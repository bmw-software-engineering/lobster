# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C or C++
source code. This tool is making use of a clang-tidy hack, and for
this to work you need to build [our clang-tidy
fork](https://github.com/bmw-software-engineering/llvm-project) and
place the `clang-tidy` binary somewhere on your PATH.

Instructions for clang-tidy [here](https://github.com/bmw-software-engineering/lobster/blob/main/documentation/user-manual.md#clang-tidy-file-generation).

This tool works using a custom clang-tidy checker `lobster-trace`
which emits tracing information as clang checks.

We plan to rework this tool to be a stand-alone clang tool in the
future.

## Tools

* `lobster-cpp`: Extract requirements from C/C++ code using a
  clang-tidy hack

## Usage

This tool supports C/C++ code.

For this you can embedd tracing tags like this:

```cpp
#include <string>
class Potato {
public:
    std::string potato() {
        // lobster-trace: something.example
        return "potato";
    }
};
```

You can add justifications as well:

```cpp
#include <string>
class Potato {
public:
    std::string potato() {
        // lobster-exclude: Reason to justify the exlude
        return "potato";
    }
};
```

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
