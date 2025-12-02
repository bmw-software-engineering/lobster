Report Python API
=================

Generate the canonical ``report.lobster`` artefact used by downstream HTML / Online report tools.

Programmatic API
----------------

::

   from lobster.tools.core.report.report import lobster_report
   lobster_report(lobster_config_file: str, output_file: str)

Stable API Function
-------------------
``lobster_report(lobster_config_file: str, output_file: str) -> None``
  Parses the configuration file and writes a LOBSTER report artefact.

Configuration File (lobster.conf)
---------------------------------
The file passed as ``lobster_config_file`` defines trace levels, their relationships, and input item sources. Typical content includes:

- Levels: requirement / implementation / activity sections with names and trace directions.
- Source artefacts: paths to existing ``.lobster`` files to merge.
- Custom data: optional metadata injected into the final report.

You supply only the path; validation & parsing are handled internally by ``Report.parse_config``.

Behavioral Notes
----------------
- The function has no return value (annotation may overstate ``dict``); it writes to ``output_file`` and exits.
- Errors in the configuration (missing file, malformed structure) raise exceptions or are surfaced via tool error handlers.
- Downstream tools (HTML / Online) rely on the fully populated ``report.lobster`` produced here.

Core Goals
----------
- Aggregate and normalize items from multiple sources.
- Compute coverage & tracing status for each level.
- Provide a single artefact for visualization/export tools.

Error Conditions
----------------
- Missing ``lobster.conf`` → ``FileNotFoundError``.
- Structural problems (invalid sections) → may raise ``LOBSTER_Error`` or ``LOBSTER_Exception``.

Performance Tips
----------------
- Keep ``lobster.conf`` focused; remove unused levels to reduce processing.
- Split very large inputs into multiple artefacts and merge incrementally if memory is constrained.

Security Tips
-------------
- Avoid embedding secrets in comments or custom data; the report may be published downstream.
- Ensure referenced paths point to trusted artefacts only.

Module Reference
----------------

Import path: ``lobster.tools.core.report.report``.
