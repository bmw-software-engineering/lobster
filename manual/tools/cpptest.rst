CppTest Python API
==================

Extract requirement/activity/implementation traces from C++ test source comments and emit LOBSTER activities.

First, prepare a configuration:

Programmatic API
----------------

::

   from lobster.tools.cpptest.cpptest import Config, lobster_cpptest

   conf = Config(
         codebeamer_url="https://codebeamer.example",
         kind="req",            # or "act" / "imp"
         files=["tests"],            # dirs/files (.cpp/.cc/.c/.h)
         output_file="cpptest_activities.lobster",
   )

Then call the API function to fetch items and write LOBSTER output:

::

   from lobster.tools.cpptest.cpptest import lobster_cpptest
   lobster_cpptest(conf)

Stable API Functions
--------------------

``lobster_cpptest(config: Config) -> None``
  Runs end-to-end: parse test files, extract markers, write LOBSTER output.

Configuration Dataclass
-----------------------
``Config`` fields (dataclass):

- ``codebeamer_url: str`` - Base URL used to build requirement links (forms item references in output).
- ``kind: KindTypes`` - Namespace for tracing targets (``req`` / ``act`` / ``imp``); influences tag semantics.
- ``files: List[str]`` - File and/or directory roots scanned for extensions ``.cpp .cc .c .h``.
- ``output_file: str`` - Destination ``.lobster`` file (includes orphan tests merged in).

Behavioral Notes
----------------
- Requirement markers parsed via prefix ``CB-#``; value becomes tracing target tag (namespace = ``kind``).
- Orphan tests (no tracing targets) are still included, grouped and merged into output.
- Each function/activity gets a unique tag composed from file + function name + line number.
- Custom field mapping is not used here (unlike codebeamer tool); trace links rely solely on markers in comments.

Core Goals
----------
- Map C++ test cases → LOBSTER Activities.
- Aggregate orphan and traced tests into a single artefact.
- Allow switching semantic namespace via ``kind``.
- Preserve precise file and line locations.

Error Conditions
----------------
- Missing required marker file/dirs → ``FileNotFoundError``.
- No matching test files after scan → ``ValueError``.
- Unsupported ``kind`` value → ``ValueError`` (must be one of ``req, act, imp``).
- Invalid config file structure (when using parser) → ``KeyError`` / ``ValueError``.

Performance Tips
----------------
- Limit directory breadth to avoid scanning large trees unnecessarily.
- Use targeted file lists for incremental runs.
- Keep ``files`` list short; split large repositories into batches if needed.

Security Tips
-------------
- Ensure ``codebeamer_url`` is HTTPS to avoid mixed-content references.
- Do not embed secrets in comments—markers are parsed verbatim.

Module Reference
----------------

Import path: ``lobster.tools.cpptest.cpptest``.
