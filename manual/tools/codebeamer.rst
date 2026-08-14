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
         baseline_id=None,
         verify_ssl=True,
         page_size=100,
         schema="requirement",  # or "implementation" / "activity"
         timeout=30,
         out=None,
         num_request_retry=5,
         retry_error_codes=[500, 502, 503, 504],
         cb_auth_conf=auth,
         item_to_text=None,
   )

- ``references`` (List[str]): Names of Codebeamer fields whose referenced items should be traced (converted to ``req`` tags).
- ``import_tagged`` (str | None): Path to an existing LOBSTER artifact whose unresolved ``req`` references define item IDs to import.
- ``import_query`` (int | str | None): Report ID (int) or cbQL query string used to fetch items directly.
- ``baseline_id`` (int | None): Codebeamer baseline ID to query against. **Only allowed when** ``import_query`` **is a cbQL query string**. Raises an error if combined with ``import_tagged`` or a numeric ``import_query``.
- ``verify_ssl`` (bool): Whether to verify TLS certificates; set ``True`` in production for security.
- ``page_size`` (int): Pagination size for REST queries; a trade-off between round trips and response size (default typically 100).
- ``schema`` (str): Target schema type (``requirement``, ``implementation``, ``activity``) controlling class/namespace mapping.
- ``timeout`` (int): Per-request timeout in seconds for HTTP calls.
- ``out`` (str | None): Output ``.lobster`` filename; if ``None`` you supply one to ``lobster_codebeamer``.
- ``num_request_retry`` (int): Number of retry attempts on transient failures (must be > 0).
- ``retry_error_codes`` (List[int]): HTTP status codes that trigger retry logic (e.g. [500, 502, 503, 504]).
- ``cb_auth_conf`` (AuthenticationConfig): Authentication + root endpoint.

.. _codebeamer-item-to-text:

- ``item_to_text`` (Callable[[dict], str | None] | None): Optional
   delegate called once for each raw Codebeamer item. Its return value is
   stored in the LOBSTER ``text`` field for requirements and activities;
   returning ``None`` leaves the field empty. Exceptions propagate and abort
   the ``lobster_codebeamer`` run.
   Note that this is a pure API feature and cannot be configured through YAML.

Stable API Function
-------------------

``lobster_codebeamer(config: Config, out_file: str) -> None``
  Loads items (via query or tagged import) and writes them to a LOBSTER interchange file.

Example (Using the ``Config.item_to_text`` API Interface)
--------------------------------------------------

This example shows how to use the ``item_to_text`` interface to combine a
standard Codebeamer field and a custom field in the LOBSTER item's ``text``
property.
It assumes you have a Codebeamer instance with a custom field named
"Upstream Requirements" that contains references to other items.
The example extracts the "name" of each referenced item and appends them to the
description of the item.

::

   from lobster.tools.codebeamer.codebeamer import AuthenticationConfig, Config, lobster_codebeamer

   auth = AuthenticationConfig(
      token="my_secret_token_123",
      root="https://codebeamer.example.com"
   )

   def custom_item_to_text(item):
      derived_from_field = next(
         (field for field in item.get("customFields", [])
          if field.get("name") == "Upstream Requirements"),
         {},
      )
      derived_from = ", ".join(
         value["name"] for value in derived_from_field.get("values", [])
      )
      return f"{item.get('description', '')}\nDerived from: {derived_from}"

   conf = Config(
      references=["Depends On", "Related To"],
      import_tagged=None,
      import_query=5678,
      verify_ssl=True,
      page_size=200,
      schema="requirement",
      timeout=60,
      out=None,
      num_request_retry=3,
      retry_error_codes=[500, 502, 503, 504],
      cb_auth_conf=auth,
      item_to_text=custom_item_to_text,
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
- ``baseline_id`` is not a positive integer → ``ValueError``.
- ``baseline_id`` combined with ``import_tagged`` → ``KeyError``.
- ``baseline_id`` combined with numeric ``import_query`` → ``KeyError``.
