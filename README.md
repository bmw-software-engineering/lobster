# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**racability
**E**vidence **R**eport allows you to demonstrate software tracability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This repository contains the prototype for LOBSTER, which is a key
ingredient to make TRCL more useful.

It has tools to extract tracing tags from a variety of sources,
combine them and produce a tracing report.

## Supported inputs

The following inputs are supported:

* `lobster_gtest`: GoogleTest tests (via the XML test output)
* `lobster_matlab`: MATLAB code and tests (via the MISS_HIT tool mh_trace)
  * requires PyPI package `miss_hit` (and `miss_hit_core`)
* `lobster_trlc`: Requirements written in TRLC
  * requires Python TRLC package
* `lobster_python`: Requirements written in TRLC
  * requires PyPI package `libcst`

## Yet unreleased inputs

These inputs are working but have not yet been open sourced:

* `lobster_cpp`: C and C++ code (via a custom clang-tidy check)

We plan to do this before 2023-01-31.

## Planned inputs

The following inputs are planned but not implemeted yet:

* `lobster_codebeamer`: Requirements from codeBeamer
* `lobster_java`: Java code
* `lobster_kotlin`: Kotlin code
* `lobster_ada`: Ada and SPARK code (via libadalang)
* `lobster_latex`: Requirements written in LaTeX
* `lobster_markdown`: Requirements written in Markdown

## Reports

You can generate a report linking everything together with `lobster_report`.
The report is in JSON, but you can generate more readable versions of it
with additional tools:

* `lobster_html_report`: Generate a HTML report
* `lobster_ci_report`: Generate a compiler-message like output, useful for CI

There are futher formats planned:

* `lobster_pdf_report`: Generate a PDF report
* `lobster_markdown_report`: Generate a Markdown report

## Data interchange

It is easy to expand the languages and activities supported by LOBSTER
by adding new tracing tools, as long as they create data in the
[common interchange](doc/schemas.md) format for LOBSTER.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version 3](LICENSE.md).

Several LOBSTER tools rely on other tools to process data and extract
tracing tags. These tools are run-time (but not link or program)
dependencies. Their copyright and license is as follows:

* `lobster_matlab` uses `mh_trace` to extract tracing
  information. `mh_trace` is part of the [MISS_HIT
  project](https://misshit.org) and is licensed under the [GNU Affero
  General Public License, Version 3](https://misshit.org/license.html).

The LOBSTER HTML report generator `lobster_html_report` includes some
of the [Feather Icons](https://feathericons.com) in the report it
generates. The Feather Icons are licensed under the [MIT
License](https://github.com/feathericons/feather/blob/master/LICENSE).

The LOBSTER HTML report generator `lobster_html_report` uses `dot`
from the [graphviz project](https://graphviz.org/) to produce some of
the pictures it includes in the report it generates. Graphviz is
licensed under the [Common Public License, Version
1.0](https://graphviz.org/license).
