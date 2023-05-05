# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**racability
**E**vidence **R**eport allows you to demonstrate software tracability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from JSON files. The
tool expects a json file with a list of objects, for which you can
specify members to extract by name. It is extremely simplistic but it
may be good enough to support some use-cases.

If you have a more complex file format you will likely need to provide
your own tool for your own files.

## Tools

* `lobster-json`: Extract activities from JSON files

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version 3](../LICENSE.md).
