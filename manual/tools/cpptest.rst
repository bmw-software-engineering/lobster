CppTest Python API
==================

Extract activity traces from C++ test source comments.

API
---

::

   from lobster.tools.cpptest.cpptest import lobster_cpptest
   lobster_cpptest(config: Config)

First, prepare a configuration:

Configuration Dataclass
-----------------------

::

   from lobster.tools.cpptest.cpptest import Config, lobster_cpptest

   conf = Config(
         codebeamer_url="https://codebeamer.example",
         kind="req",            # or "act" / "imp"
         files=["tests"],            # dirs/files (.cpp/.cc/.c/.h)
         output_file="cpptest_activities.lobster",
   )

``Config`` fields (dataclass):

- ``codebeamer_url: str`` - Base URL used to build requirement links (forms item references in output).
- ``kind: KindTypes`` - Namespace for tracing targets (``req`` / ``act`` / ``imp``); influences tag semantics.
- ``files: List[str]`` - File and/or directory roots scanned for extensions ``.cpp .cc .c .h``.
- ``output_file: str`` - Destination ``.lobster`` file (includes orphan tests merged in).

Stable API Function
-------------------

``lobster_cpptest(config: Config) -> None``
  Runs end-to-end: parse test files, extract markers, write LOBSTER output.

Example (Scanning Test Directory)
----------------------------------

::

   from lobster.tools.cpptest.cpptest import Config, lobster_cpptest

   conf = Config(
      codebeamer_url="https://codebeamer.example",
      kind="req",
      files=["tests/unit", "tests/integration"],
      output_file="test_activities.lobster",
   )

   lobster_cpptest(conf)

Behavioral Notes
----------------
- Extracts tracing markers with prefix ``CB-#`` from code comments; these become requirement references.
- Tests without tracing markers are still included in the output.
- Each test gets a unique identifier based on filename, function name, and line number.
- Tracing relies only on comment markers (no custom field mapping like the codebeamer tool).

Core Goals
----------
- Extract C++ test cases and convert them to LOBSTER activities.
- Include all tests (both traced and untraced) in a single output file.
- Control the namespace using the ``kind`` parameter.
- Track exact file locations and line numbers for each test.

Error Conditions
----------------
- Missing required marker file/dirs → ``FileNotFoundError``.
- No matching test files after scan → ``ValueError``.
- Unsupported ``kind`` value → ``ValueError`` (must be one of ``req, act, imp``).
- Invalid config file structure (when using parser) → ``KeyError`` / ``ValueError``.
