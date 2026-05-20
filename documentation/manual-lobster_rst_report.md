# lobster-rst-report

Generate reStructuredText (RST) traceability reports from LOBSTER
report files, for inclusion in a Sphinx documentation project.

## Overview

`lobster-rst-report` converts a `.lobster` report file into RST that
can be built by Sphinx.  The output uses
[sphinx-design](https://sphinx-design.readthedocs.io/) directives
(dropdowns, grids, cards) for a rich presentation and
[sphinx.ext.graphviz](https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html)
for the tracing policy diagram.

Two output modes are available:

* **Single-page** (`--out FILE`) — one RST file containing the entire
  report.
* **Multi-page** (`--out-dir DIR`) — an `index.rst` plus one RST file
  per tracing level, linked via `toctree` directives.

## Installation

`lobster-rst-report` is included in the `bmw-lobster-core` and
`bmw-lobster-monolithic` packages.

Your Sphinx project additionally requires:

```
pip install sphinx-design
```

## Usage

```
lobster-rst-report [LOBSTER_REPORT] [--out FILE | --out-dir DIR] [--source-root PREFIX]
```

| Argument | Description |
|---|---|
| `LOBSTER_REPORT` | Path to the `.lobster` report file (default: `report.lobster`). |
| `--out FILE` | Write a single-page RST report to `FILE` (default: `lobster_report.rst`). |
| `--out-dir DIR` | Write a multi-page RST report to `DIR` (index.rst + one page per level). |
| `--source-root PREFIX` | Prefix prepended to file reference URLs.  Use this when the RST output directory differs from the workspace root. |

`--out` and `--out-dir` are mutually exclusive.

### Example

```bash
# Generate a multi-page RST report
lobster-rst-report report.lobster --out-dir docs/traceability

# Generate a single-page RST report
lobster-rst-report report.lobster --out docs/traceability.rst
```

## Sphinx project setup

Your Sphinx `conf.py` must load the required extensions:

```python
extensions = ["sphinx_design", "sphinx.ext.graphviz"]
```

For multi-page mode, include the generated `index.rst` via a `toctree`
in your main documentation:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Traceability

   traceability/index
```

### Optional: custom CSS

The generated RST uses the CSS class `lobster-issue-card` for issue
message cards.  You can style them in a custom stylesheet:

```css
.lobster-issue-card .sd-card-body {
    background-color: #f8d7da;
}
.lobster-issue-card {
    border: 2px solid #dc3545;
}
```

## Bazel integration

The tool is available as a Bazel subrule for use in custom rules:

```starlark
load("//:lobster.bzl", "subrule_lobster_rst_report")
```

The subrule accepts a `.lobster` report file and produces a single-page
`.rst` file.  It automatically computes `--source-root` based on the
package depth so that file reference links resolve correctly.
