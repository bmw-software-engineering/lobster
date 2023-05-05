# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**racability
**E**vidence **R**eport allows you to demonstrate software tracability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains the core LOBSTER tools: the basic API and tools
for generating reports.

## Tools

You can generate a report linking everything together with `lobster-report`.
The report is in JSON, but you can generate more readable versions of it
with additional tools:

* `lobster-online-report`: Preprocess a JSON report to contain github
  references instead of local file references
* `lobster-html-report`: Generate a HTML report
* `lobster-ci-report`: Generate a compiler-message like output, useful for CI

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version 3](../LICENSE.md).

Several LOBSTER tools rely on other tools to process data and extract
tracing tags. These tools are run-time (but not link or program)
dependencies. Their copyright and license is as follows:

The LOBSTER HTML report generator `lobster-html-report` includes some
of the [Feather Icons](https://feathericons.com) in the report it
generates. The Feather Icons are licensed under the [MIT
License](https://github.com/feathericons/feather/blob/master/LICENSE).

The LOBSTER HTML report generator `lobster-html-report` uses `dot`
from the [graphviz project](https://graphviz.org/) to produce some of
the pictures it includes in the report it generates. Graphviz is
licensed under the [Common Public License, Version
1.0](https://graphviz.org/license).
