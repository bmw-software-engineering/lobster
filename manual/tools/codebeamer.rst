Codebeamer Python API
=====================

This section describes the end-user facing Codebeamer API for LOBSTER.

First, prepare a configuration programmatically and authenticate:

Programmatic API
----------------
::

   from lobster.tools.codebeamer.codebeamer import AuthenticationConfig, Config

   auth = AuthenticationConfig(token="<TOKEN>", root="https://codebeamer.example")
   conf = Config(
         references=[],
         import_tagged=None,
         import_query=1234,  # report ID or cbQL query string
         verify_ssl=True,
         page_size=100,
         schema="requirement",  # or "implementation" / "activity"
         timeout=30,
         out=None,
         num_request_retry=5,
         retry_error_codes=[500, 502, 503, 504],
         cb_auth_conf=auth,
   )

Then call the API function to fetch items from codebeamer and write LOBSTER output:

::

   from lobster.tools.codebeamer.codebeamer import lobster_codebeamer
   lobster_codebeamer(conf, "cb_requirements.lobster")

Stable API Functions
--------------------

``lobster_codebeamer(config: Config, out_file: str) -> None``
   Loads items (via query or tagged import) and writes them to a LOBSTER interchange file.

``Config`` / ``AuthenticationConfig``
   Data containers; instantiate directly (no builder pattern) for explicitness.

Core Goals
----------

- Import by query/report ID → set ``import_query`` (int or cbQL string).
- Import by referenced IDs → set ``import_tagged`` to a prior LOBSTER artefact.
- Control item kind → set ``schema`` (``requirement`` / ``implementation`` / ``activity``).
- Harden network calls → tune ``num_request_retry`` & ``retry_error_codes``; enable ``verify_ssl``.
- Tune performance → adjust ``page_size`` & ``timeout``.
- Trace extra relationships → list custom field names in ``references``.

Configuration Parameters (Programmatic API)
------------------------------------------
Attributes accepted by ``AuthenticationConfig`` and ``Config`` when used in Python.

AuthenticationConfig
--------------------
- ``token`` (str | None): Bearer token for Codebeamer. Preferred over user/password.
- ``user`` (str | None): Username (used only if ``token`` is not provided).
- ``password`` (str | None): Password (paired with ``user``); may be auto-populated via ``~/.netrc``.
- ``root`` (str): Base HTTPS URL of the Codebeamer instance (must start with ``https://``).

Config
------
- ``references`` (List[str]): Names of Codebeamer fields whose referenced items should be traced (converted to ``req`` tags).
- ``import_tagged`` (str | None): Path to an existing LOBSTER artefact whose unresolved ``req`` references define item IDs to import.
- ``import_query`` (int | str | None): Report ID (int) or cbQL query string used to fetch items directly.
- ``verify_ssl`` (bool): Whether to verify TLS certificates; set ``True`` in production for security.
- ``page_size`` (int): Pagination size for REST queries; a trade-off between round trips and response size (default typically 100).
- ``schema`` (str): Target schema type (``requirement``, ``implementation``, ``activity``) controlling class/namespace mapping.
- ``timeout`` (int): Per-request timeout in seconds for HTTP calls.
- ``out`` (str | None): Output ``.lobster`` filename; if ``None`` you supply one to ``lobster_codebeamer``.
- ``num_request_retry`` (int): Number of retry attempts on transient failures (must be > 0).
- ``retry_error_codes`` (List[int]): HTTP status codes that trigger retry logic (e.g. [500, 502, 503, 504]).
- ``cb_auth_conf`` (AuthenticationConfig): Authentication + root endpoint.

Minimum Required
----------------
- ``cb_auth_conf.root`` (HTTPS) AND one of ``import_query`` / ``import_tagged``.

Behavioral Notes
----------------
- ``import_tagged`` overrides ``import_query`` if both provided.
- ``schema`` maps to namespace class: requirement→``req`` / implementation→``imp`` / activity→``act``.
- Exponential backoff is implicit (1s, 2s, 4s...) based on ``num_request_retry``.
- Missing ``token`` triggers user/password or ``~/.netrc`` resolution.

Error Conditions
----------------
- Missing/invalid ``root`` (non-HTTPS) → ``KeyError``.
- Absent both ``import_query`` & ``import_tagged`` → ``KeyError``.
- ``num_request_retry <= 0`` → ``ValueError``.
- Unrecognised ``schema`` → ``KeyError``.

Performance Tips
----------------
- Lower ``page_size`` for slow links; raise moderately for fewer requests.
- Increase ``timeout`` for large reports.
- Use only transient server codes in ``retry_error_codes`` (e.g. 500/502/503/504).

Security Tips
-------------
- Always prefer a ``token`` over password auth.
- Set ``verify_ssl=True`` outside controlled test environments.
- Rotate tokens periodically.

Module Reference
----------------

Import path: ``lobster.tools.codebeamer.codebeamer``.

