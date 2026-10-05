# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package `bmw-lobster-monolithic` is an alternative package that
installs the same things as the metapackage
[bmw-lobster](https://pypi.org/project/bmw-lobster) and additionally installs lobster-pkg. This package may
be interesting for people who wish to integrate into bazel, as
`py_wheel` cannot deal with overlapping installs. In this repository,
build the distributable artifact with `bazel build //packages/lobster-monolithic:wheel.dist`.
The release packaging flow then stages the resulting wheel into
`packages/lobster-monolithic/meta_dist/` for publishing.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
