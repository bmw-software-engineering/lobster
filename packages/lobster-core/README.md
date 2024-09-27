# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains the core LOBSTER tools: the basic API and tools
for generating reports.

## Tools

You can generate a report linking everything together with `lobster-report`.
The report is in JSON, but you can generate more readable versions of it
with additional tools:

* `lobster-report`: Creation of JSON format report from provided config file
* `lobster-online-report`: Preprocess a JSON report to contain github
  references instead of local file references
* `lobster-html-report`: Generate a HTML report
* `lobster-ci-report`: Generate a compiler-message like output, useful for CI

## Configuration
The `lobster-report` tool works with a config file. In it you can declare the 
upstream, downstream and source of tracing policies. 

The configuration file follows the following rules:

* This file is able to get multiple `trace to` and `trace from` keys.
* `trace to` specifies all the outgoing targets.
* `trace from` specifies all the incoming targets.
* Multiple lines of the same rule are treated as if they had an `and` between them.
* `or` is supported in each line, to specify that only one target is needed, not 
  all of them.
* Self-references are also allowed.


```
requirements "Requirements" {
   source: "file1.lobster";
}

requirements "System Requirements" {
   source: "file2.lobster";
   trace to: "Models" or "Software Requirements";
   trace to: "Requirements";
   trace from: "System Requirements" or "Integration Tests";
   trace from: "Unit Tests";
}
```

## Requirements
* `lobster-online-report`: This tool needs `git 1.7.8` or higher to support 
  git submodules

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).

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
