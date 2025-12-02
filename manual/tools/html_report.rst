HTML Report Python API
======================

This section describes the end-user facing HTML Report API for LOBSTER.

Generate rich HTML reports from LOBSTER data and test results.

Programmatic API
----------------
::

  from lobster.tools.core.html_report import lobster_html_report

  lobster_html_report(
     lobster_report_path="report.lobster",
     output_html_path="lobster_report.html",
     dot_path=None,               # optional Graphviz 'dot' path
     high_contrast=False,         # optional high contrast colors
     render_md=False,             # optional Markdown rendering
  )

Alternatively, use the CLI entrypoint:

::

  python -m lobster.tools.core.html_report --lobster_report_path path/to/report.lobster --out report.html

.. toctree::
   :maxdepth: 2
   :caption: html report API Docs

Stable API functions
--------------------

- ``lobster_html_report(lobster_report_path: str, output_html_path: str, dot_path: Optional[str] = None, high_contrast: bool = False, render_md: bool = False) -> None`` — programmatic API; renders a consolidated HTML report from a LOBSTER report file.
- ``HtmlReportTool.run(args: Optional[Sequence[str]]) -> int`` — CLI entrypoint via tool class.
- ``main(args: Optional[Sequence[str]]) -> int`` — module entrypoint.

Detailed API call breakdown
----------------------------

What it does
------------
- Loads a previously generated LOBSTER report file (``.lobster``) and produces a standalone HTML report.
- Optionally renders a tracing policy SVG diagram if Graphviz ``dot`` is available.
- Supports visual options for high contrast colors and Markdown rendering in requirement descriptions.

Parameters
------------
- ``lobster_report_path`` (str): Path to the input LOBSTER report file (e.g., ``report.lobster``). This file must already exist and be produced by your reporting pipeline.
- ``output_html_path`` (str): Path for the output HTML file (e.g., ``lobster_report.html``).
- ``dot_path`` (str, optional): Path to the Graphviz ``dot`` executable. If ``None``, the tool tries ``dot`` from PATH. If ``dot`` isn’t found, the HTML report is still generated, but the tracing policy diagram is omitted; a warning is printed.
- ``high_contrast`` (bool, optional): If ``True``, uses higher-contrast colors to improve readability.
- ``render_md`` (bool, optional): If ``True``, requirement text is rendered as Markdown (tables supported); if ``False``, text is escaped and shown as plain text.

Returns
-------
- ``None`` — writes the HTML content to ``output_html_path``.

Goals and how to achieve them
-----------------------------

- Generate a single CI-friendly HTML report: call ``lobster_html_report(lobster_report_path, output_html_path)``.
- Control output path and filename: set ``output_html_path`` or ``--out``.
- Include summaries, detailed listings, and links: the content comes from the input LOBSTER report; use your report generation step to control sections.

Module reference
----------------

Import path: ``lobster.tools.core.html_report``.
