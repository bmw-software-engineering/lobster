# Sphinx Lobster Extension

Integrates LOBSTER traceability into Sphinx documentation builds.

## Usage

The extension registers a custom Sphinx builder named `lobster`.

The builder scans RST documents for `:requirement:upstream-ref:` roles and
produces a `_merged.lobster` file that feeds into the LOBSTER traceability chain.

## Flow

```
Sphinx build (builder=lobster)
        │
        ▼
LobsterBuilder (subclass of TextBuilder)
  - LobsterTranslator parses :requirement:upstream-ref: roles
  - Each .rst file → <outdir>/<docname>.json  (lobster-imp-trace fragment)
        │
        ▼
LobsterBuilder.finish()
  - Merges all per-doc JSON fragments into <outdir>/_merged.lobster
        │
        ▼
OutputGroupInfo(lobster = [<outdir directory>])
  (returned by the sphinx Bazel rule)
        │
        ▼
sphinx_lobster_merge rule  (tools/lobster/sphinx_lobster.bzl)
  - pure provider adapter
        │
        ▼
LobsterProvider(lobster_input = {"sphinx_docs.lobster": "<outdir>/_merged.lobster"})
```

## Architecture

The extension consists of two classes in `sphinx_lobster_builder.py`:

- **`LobsterTranslator`** (`SphinxTranslator` subclass) — visits the RST document tree,
  collects `upstream-ref` and `downstream-ref` role references, and builds a lobster
  JSON structure per document.
- **`LobsterBuilder`** (`TextBuilder` subclass) — Sphinx builder that writes one `.json`
  file per document, then merges all fragments into `_merged.lobster` in its `finish()` hook.
