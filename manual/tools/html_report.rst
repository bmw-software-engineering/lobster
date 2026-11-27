HTML Report Python API
======================

Generate standalone HTML traceability evidence reports from LOBSTER report files.

API
---

::

  from lobster.tools.core.html_report import lobster_html_report

  lobster_html_report(
     lobster_report_path: str,
     output_html_path: str,
     high_contrast: bool = False,         # optional high contrast colors
     render_md: bool = False,             # optional Markdown rendering
      source_root: str = "",              # optional source link prefix
  )

Parameters
----------
- ``lobster_report_path`` (str): Path to the input LOBSTER report file (e.g., ``report.lobster``). This file must already exist and be produced by your reporting pipeline.
- ``output_html_path`` (str): Path for the output HTML file (e.g., ``lobster_report.html``).
- ``high_contrast`` (bool, optional): If ``True``, uses higher-contrast colors to improve readability.
- ``render_md`` (bool, optional): If ``True``, requirement text is rendered as Markdown (tables supported); if ``False``, text is escaped and shown as plain text.
- ``source_root`` (str, optional): Prefix prepended to source links in the report.

Stable API Function
-------------------

``lobster_html_report(lobster_report_path: str, output_html_path: str, high_contrast: bool = False, render_md: bool = False, source_root: str = "") -> None``
  Loads a LOBSTER report file and generates a standalone HTML report with a tracing policy diagram.

Example (With Markdown and High Contrast)
------------------------------------------

::

  from lobster.tools.core.html_report import lobster_html_report

  lobster_html_report(
     lobster_report_path="artifact/report.lobster",
     output_html_path="docs/tracing.html",
     high_contrast=True,
     render_md=True,
  )

Behavioral Notes
----------------
- Returns ``None``; writes HTML content to ``output_html_path`` as a side effect.
- The tracing policy diagram is always rendered without an external rendering utility.
- The tracing policy visualization is not qualified for safety-related use.
- Supports Markdown tables in requirement descriptions when ``render_md=True``.
- The HTML output is self-contained and suitable for CI/CD pipelines.

Core Goals
----------
- Generate a single HTML report for traceability evidence.
- Include coverage summaries, detailed item listings, and source links.
- Support visual customization with high contrast and Markdown rendering.

Error Conditions
----------------
- Missing input report file → ``FileNotFoundError``.
