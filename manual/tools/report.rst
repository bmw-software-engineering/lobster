Report Python API
=================

Generate the canonical ``report.lobster`` artifact used by downstream HTML / Online report tools.

API
---

::

   from lobster.tools.core.report.report import lobster_report
   lobster_report(lobster_config_file: str, output_file: str)

Parameters
----------
- ``lobster_config_file`` (str): Path to the LOBSTER configuration file (typically ``lobster.conf``) defining trace levels, relationships, and input sources. See `Configuration File (lobster.conf)`_.
- ``output_file`` (str): Path where the generated ``report.lobster`` artifact will be written.

Stable API Function
-------------------
``lobster_report(lobster_config_file: str, output_file: str) -> dict``
  Parses the configuration file and writes a LOBSTER report artifact.

Example
-------

::

  from lobster.tools.core.report.report import lobster_report

   lobster_report(
       lobster_config_file="lobster/tools/lobster.conf",
       output_file="report.lobster"
   )

Configuration File (lobster.conf)
---------------------------------
The file passed as ``lobster_config_file`` defines trace levels, their relationships, and input item sources. Typical content includes:

- Levels: requirement / implementation / activity sections with names and trace directions.
- Source artifacts: paths to existing ``.lobster`` files to merge.
- Custom data: optional metadata injected into the final report.

You supply only the path; validation & parsing are handled internally by ``Report.parse_config``.

Behavioral Notes
----------------
- Errors in the configuration (missing file, malformed structure) raise exceptions or are surfaced via tool error handlers.
- Downstream tools (HTML / Online) rely on the fully populated ``report.lobster`` produced here.

Core Goals
----------
- Aggregate and normalize items from multiple sources.
- Compute coverage & tracing status for each level.
- Provide a single artifact for visualization/export tools.

Error Conditions
----------------
- Missing ``lobster.conf`` → ``FileNotFoundError``.
- Structural problems (invalid sections) → may raise ``LOBSTER_Error`` or ``LOBSTER_Exception``.
