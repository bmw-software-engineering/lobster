Online Report Python API
========================

Transform local file references in a LOBSTER report into immutable GitHub URLs (commit-pinned) for web publication.

Programmatic API
----------------
::

  from lobster.tools.core.online_report.online_report import Config, lobster_online_report

  cfg = Config(
     repo_root=".",
     base_url="https://github.com/org/repo",
     commit_id="<GIT_COMMIT_SHA>",
     report="report.lobster",   # optional; defaults to "report.lobster"
  )

Then call the API function to fetch items and write LOBSTER output:

::
  from lobster.tools.core.online_report.online_report import lobster_online_report
  lobster_online_report(cfg, "online_report.lobster")

Stable API Function
-------------------
``lobster_online_report(config: Config, out_file: str) -> None``
  Loads the existing report, rewrites ``File_Reference`` locations as ``Github_Reference`` objects, then writes an updated artefact.

Configuration Dataclass
-----------------------
``Config`` fields:
- ``repo_root: str`` - Absolute or relative path to the Git repository root; used to compute in‑repo relative paths.
- ``base_url: str`` - Base GitHub (or forge) URL without trailing slash (e.g. ``https://github.com/org/repo``).
- ``commit_id: str`` - Commit hash ensuring links resolve to a stable snapshot.
- ``report: str`` - Path to the input LOBSTER report (default ``report.lobster``).

Behavioral Notes
----------------
- Only items whose location is a ``File_Reference`` are converted; existing ``Github_Reference`` entries remain untouched.
- Paths outside ``repo_root`` are skipped with a warning (not inside repository).
- Output preserves all non-location metadata (tags, tracing status, messages).
- The tool does not perform a git rev-parse; it trusts the provided ``commit_id``.

Core Goals
----------
- Produce a shareable report with stable, clickable source links.
- Decouple downstream viewers from local filesystem paths.
- Facilitate publishing in portals or static hosting.

Error Conditions
----------------
- Missing input report file → ``FileNotFoundError``.
- Invalid config structure (when parsed from YAML) → ``KeyError`` / ``ValueError``.
- Non-string fields for ``base_url`` / ``repo_root`` / ``commit_id`` → ``ValueError``.

Performance Tips
----------------
- Use a shallow report (filter unnecessary items) to minimize link conversion time.
- Ensure ``repo_root`` is the smallest directory containing all referenced files.

Security Tips
-------------
- Use a full commit SHA (not a branch) to avoid mutable content drifting.
- Avoid embedding sensitive paths; everything under ``repo_root`` may surface in published URLs.

Example (Custom Root & Commit)
------------------------------
::

  cfg = Config(
     repo_root="/workspace/project",
     base_url="https://github.com/org/project",
     commit_id="d34db33f7e8c9a...",
     report="artifact/report.lobster",
  )
  lobster_online_report(cfg, "artifact/online_report.lobster")

Module Reference
----------------

Import path: ``lobster.tools.core.online_report.online_report``.
