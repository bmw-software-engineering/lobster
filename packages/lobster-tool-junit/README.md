# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool for JUnit XML test reports.

## Tools

* `lobster-junit`: Extract tracing data from JUnit XML test reports of any test
  framework, e.g. pytest, and from GoogleTest XML reports. It reads every
  report with the matching reader, so a test suite which mixes test frameworks
  is traced with one call. See the
  [documentation](../../documentation/manual-lobster_junit.md).

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
