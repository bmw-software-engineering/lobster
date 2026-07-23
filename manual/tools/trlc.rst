Trlc Python API
===============

Extract requirement items from TRLC models using YAML conversion rules.

API
---

::

   from lobster.tools.trlc.trlc_tool import TrlcToolConfig, lobster_trlc
   lobster_trlc(config: TrlcToolConfig)

First, prepare a configuration:

Configuration Dataclass
-----------------------

::

   from lobster.tools.trlc.trlc_tool import TrlcToolConfig, lobster_trlc

   conf = TrlcToolConfig(
      config="config.yaml",
      dir_or_files=["models/"],
      out="trlc_requirements.lobster",
   )

``TrlcToolConfig`` fields (dataclass):

- ``config: str`` - Path to the TRLC YAML config file. The file must define ``conversion-rules`` and may also include ``to-string-rules``, ``inputs``, ``inputs-from-file``, and ``exclude-patterns``.
- ``dir_or_files: Sequence[str]`` - Additional file or directory paths merged with any input paths defined in the config file.
- ``out: str`` - Destination ``.lobster`` file path. Defaults to ``lobster-trlc.lobster``.

Stable API Function
-------------------

``lobster_trlc(config: TrlcToolConfig) -> None``
  Runs end-to-end: load config, collect TRLC sources, convert matching record objects, and write a LOBSTER output file.

Example (Default Config Inputs)
-------------------------------

::

   from lobster.tools.trlc.trlc_tool import TrlcToolConfig, lobster_trlc

   conf = TrlcToolConfig(
      config="config.yaml",
      out="trlc_requirements.lobster",
   )

   lobster_trlc(conf)

Behavioral Notes
----------------
- API validates that ``config`` is non-empty before execution.
- Conversion currently supports namespace ``req``; unsupported namespaces raise ``NotImplementedError``.
- API execution propagates parser, config validation, and conversion exceptions to the caller.

Core Goals
----------
- Parse TRLC ``.rsl`` / ``.trlc`` inputs using configured conversion rules.
- Convert matching TRLC records into LOBSTER requirement items.
- Preserve trace tags, description fields, and optional version mapping in output tags.
- Produce a single LOBSTER artifact for downstream report tools.

Error Conditions
----------------
- Empty ``config`` path → ``ValueError``.
- Invalid YAML schema/content → ``yamale.YamaleError``.
- Missing file/directory inputs or invalid paths → ``ValueError`` (during input collection), or ``FileNotFoundError`` / ``PathError`` (during TRLC source registration).
- TRLC parsing/processing failures → ``trlc.errors.TRLC_Error`` / ``TrlcFailure``.
- Invalid conversion or to-string rules → ``InvalidConversionRuleError``, ``RecordObjectComponentError``, ``TupleToStringMissingError``, ``TupleToStringFailedError``.
