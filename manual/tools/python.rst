Python Tool API
===============

Extract tracing tags from Python source files and generate LOBSTER activity or
implementation artifacts.

API
---

::

   from lobster.tools.python.python import PythonToolConfig, lobster_python
   lobster_python(config: PythonToolConfig)

Configuration Dataclass
-----------------------

::

   from lobster.tools.python.python import PythonToolConfig, lobster_python

   config = PythonToolConfig(
      files=["src"],
      activity=False,
      out="python.lobster",
      single=False,
      only_tagged_functions=False,
      parse_decorator=None,
      parse_versioned_decorator=None,
   )

``PythonToolConfig`` fields:

- ``files: Sequence[str]`` - List of files and/or directories. Directories are scanned recursively for ``.py`` files.
- ``activity: bool`` - When ``True``, emits activity items instead of implementation items.
- ``out: Optional[str]`` - Output ``.lobster`` path. If ``None``, output is written to stdout.
- ``single: bool`` - Disables multiprocessing and parses files sequentially.
- ``only_tagged_functions: bool`` - Keeps only extracted items that have at least one tracing target.
- ``parse_decorator: Optional[Tuple[str, str]]`` - Decorator name plus argument name for deriving trace tags.
- ``parse_versioned_decorator: Optional[Tuple[str, str, str]]`` - Decorator name, tag argument name, and version argument name.

Stable API Function
-------------------

``lobster_python(config: PythonToolConfig) -> None``
  Runs parsing and writes LOBSTER output according to the provided configuration.

Example
-------

::

   from lobster.tools.python.python import PythonToolConfig, lobster_python

   lobster_python(PythonToolConfig(
      files=["src", "tests"],
      out="python_trace.lobster",
      activity=False,
      single=True,
   ))

Behavioral Notes
----------------

- ``parse_decorator`` and ``parse_versioned_decorator`` are mutually exclusive.
- Parse failures in input files are reported to stdout and may produce partial output.
- Invalid input paths raise ``ValueError``.

Core Goals
----------
- Parse Python ``.py`` files and extract implementation or activity items.
- Convert inline ``lobster-trace`` tags and decorator-provided tags into tracing targets.
- Support folder-based scanning with optional sequential or multiprocessing execution.
- Produce a LOBSTER artifact consumable by downstream report tools.

Error Conditions
----------------
- Invalid file or directory input path → ``ValueError``.
- Invalid decorator configuration (both parse options set) → ``ValueError``.
- File decode problems while reading sources → ``UnicodeDecodeError`` is reported and file is skipped.
- Python parser syntax errors in source files → parser error is reported and output may be incomplete.
