# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package `bmw-lobster` is a metapackage that installs all other
LOBSTER packages as a convenience:

* [bmw-lobster-core](https://pypi.org/project/bmw-lobster-core)
* [bmw-lobster-tool-codebeamer](https://pypi.org/project/bmw-lobster-tool-codebeamer)
* [bmw-lobster-tool-cpp](https://pypi.org/project/bmw-lobster-tool-cpp)
* [bmw-lobster-tool-gtest](https://pypi.org/project/bmw-lobster-tool-gtest)
* [bmw-lobster-tool-json](https://pypi.org/project/bmw-lobster-tool-json)
* [bmw-lobster-tool-python](https://pypi.org/project/bmw-lobster-tool-python)
* [bmw-lobster-tool-trlc](https://pypi.org/project/bmw-lobster-tool-trlc)
* [miss_hit](https://pypi.org/project/miss_hit)

Note there is also a monolithic wheel
[bmw-lobster-monolithic](https://pypi.org/project/bmw-lobster-monolithic),
which may be interesting for people who wish to integrate into bazel,
as `py_wheel` cannot deal with overlapping installs.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
