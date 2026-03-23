Codebeamer Python API
=====================

This section describes the end-user facing Codebeamer API for LOBSTER.

API
---

::

   from lobster.tools.codebeamer.codebeamer import lobster_codebeamer
   lobster_codebeamer(config: Config, out_file: str)

First, prepare a configuration:

Configuration Parameters
------------------------

Attributes accepted by ``AuthenticationConfig`` and ``Config`` when used in Python.

AuthenticationConfig
~~~~~~~~~~~~~~~~~~~~

::

   from lobster.tools.codebeamer.codebeamer import AuthenticationConfig

   auth = AuthenticationConfig(token="<TOKEN>", root="https://codebeamer.example")

- ``token`` (str | None): Bearer token for Codebeamer. Preferred over user/password.
- ``user`` (str | None): Username (used only if ``token`` is not provided).
- ``password`` (str | None): Password (paired with ``user``); may be auto-populated via ``~/.netrc``.
- ``root`` (str): Base HTTPS URL of the Codebeamer instance (must start with ``https://``).

Config
~~~~~~

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

- ``references`` (List[str]): Names of Codebeamer fields whose referenced items should be traced (converted to ``req`` tags).
- ``import_tagged`` (str | None): Path to an existing LOBSTER artifact whose unresolved ``req`` references define item IDs to import.
- ``import_query`` (int | str | None): Report ID (int) or cbQL query string used to fetch items directly.
- ``verify_ssl`` (bool): Whether to verify TLS certificates; set ``True`` in production for security.
- ``page_size`` (int): Pagination size for REST queries; a trade-off between round trips and response size (default typically 100).
- ``schema`` (str): Target schema type (``requirement``, ``implementation``, ``activity``) controlling class/namespace mapping.
- ``timeout`` (int): Per-request timeout in seconds for HTTP calls.
- ``out`` (str | None): Output ``.lobster`` filename; if ``None`` you supply one to ``lobster_codebeamer``.
- ``num_request_retry`` (int): Number of retry attempts on transient failures (must be > 0).
- ``retry_error_codes`` (List[int]): HTTP status codes that trigger retry logic (e.g. [500, 502, 503, 504]).
- ``cb_auth_conf`` (AuthenticationConfig): Authentication + root endpoint.

Stable API Function
-------------------

``lobster_codebeamer(config: Config, out_file: str) -> None``
  Loads items (via query or tagged import) and writes them to a LOBSTER interchange file.

Example (Using Query with Custom Settings)
-------------------------------------------

::

   from lobster.tools.codebeamer.codebeamer import AuthenticationConfig, Config, lobster_codebeamer

   auth = AuthenticationConfig(
      token="my_secret_token_123",
      root="https://codebeamer.example.com"
   )

   conf = Config(
      references=["Depends On", "Related To"],
      import_tagged=None,
      import_query=5678,
      verify_ssl=True,
      page_size=200,
      schema="implementation",
      timeout=60,
      out=None,
      num_request_retry=3,
      retry_error_codes=[500, 502, 503, 504],
      cb_auth_conf=auth,
   )

   lobster_codebeamer(conf, "codebeamer_items.lobster")

Core Goals
----------
- Fetch items using a query or report ID by setting ``import_query``.
- Fetch items referenced in an existing LOBSTER file by setting ``import_tagged``.
- Choose the item type (requirement, implementation, or activity) using ``schema``.
- Make network calls more reliable by configuring ``num_request_retry`` and ``verify_ssl``.
- Improve performance by adjusting ``page_size`` and ``timeout``.
- Trace additional relationships by listing custom field names in ``references``.

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
