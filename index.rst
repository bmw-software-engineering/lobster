LOBSTER Python APIs
===================

Welcome to the LOBSTER documentation. This site provides:

- Tool APIs: Python interfaces for extracting and generating traceability from code, tests, JSON vectors, reports, and external systems (e.g., Codebeamer).
- Common APIs: Shared infrastructure used by all tools (data models, locations, IO helpers, error handling, and base classes).

What you can do with LOBSTER
----------------------------

- Extract implementation traces from Python/C++ code.
- Convert unit test outputs (CppTest/Json) into activity traces.
- Import requirements and artifacts from Codebeamer via REST API.
- Turn JSON test vectors into activity traces.
- Generate CI and HTML traceability reports.

How tools share common setup
----------------------------

All tools use shared modules under ``lobster.common`` for:

- Data models (items: Requirement, Implementation, Activity, and Tracing_Tag)
- References and locations (e.g., Codebeamer_Reference, File_Reference)
- Error handling (Message_Handler, LOBSTER_Error)
- Input/Output helpers (lobster_read, lobster_write)
- Tool base classes (MetaDataToolBase, LOBSTER_Per_File_Tool)

Browse the sections below to find the APIs and examples you need.

.. toctree::
  :maxdepth: 2
  :caption: Tools API Docs

  manual/tools/index
