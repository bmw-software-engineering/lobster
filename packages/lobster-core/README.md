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

* `lobster-online-report`:
  Preprocess a JSON report to contain github references instead of local file
  references.
  Repository information is retrieved by calling the `git` tool.
* `lobster-online-report-nogit`:
  This tool is similar to `lobster-online-report`, but it does not
  call the `git` tool to obtain information about the repository.
  Instead, it relies solely on information provided by the user through
  command line arguments.
  The user has to provide
  - the git hash,
  - the remote repository URL,
  - the local path to the repository.
  
  The tool then replaces local paths in a given LOBSTER report file
  with URLs to the corresponding files in the remote repository.
  
  This tool is handy when `lobster-online-report` cannot be used.
  This could be the case in a continuous integration (CI) system where
  access to `git` is restricted for security reasons.
  Imagine a CI job that runs with high credentials.
  It could be important to prevent manipulations of the git history by the CI job,
  and as a consequence access to `git` is restricted for the job runner.
* `lobster-html-report`: Generate an HTML report
* `lobster-ci-report`: Generate a compiler-message like output, useful for CI

## Requirements
`lobster-online-report` needs `git 1.7.8` or higher to support git submodules.

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
