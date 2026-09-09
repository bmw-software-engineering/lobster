# LOBSTER Coding Guidelines

LOBSTER (Lightweight Open BMW Software Traceability Evidence Report) extracts tracing tags
from requirements/tests/code sources and combines them into requirements-coverage reports.
See [README.md](../README.md) for the tool overview and [CODING_GUIDELINE.md](../CODING_GUIDELINE.md)
for Python style rules (Black style, CamelCase classes, `test_*.py` mirrors module name, 88 char
lines, prefer dataclasses over dicts, single-line comments over inline/multi-line).

## Repository layout

- Each extractor/reporter tool lives under `lobster/tools/<tool>/` (or `lobster/tools/core/<tool>/`
  for the "core" tools that consume other tools' output: `report`, `html_report`, `online_report`,
  `ci_report`).
- Shared base classes (config handling, directory traversal, `inputs_from_file`, etc.) live in
  `lobster/common/tool.py` (`LOBSTER_Tool` / `LOBSTER_Per_File_Tool`).
- Tests are per-tool and self-contained under `tests_unit/lobster_<tool>/` and
  `tests_system/lobster_<tool>/`, each with its own `BUILD.bazel` and fixture data — even for
  behavior backed by shared base-class code, don't try to dedupe tests across tools
  (see [lobster/tools/REQUIREMENTS.md](../lobster/tools/REQUIREMENTS.md)).
- Only `tests_unit/lobster_<tool>/` is scanned by the tracing pipeline; a stray top-level
  `tests_unit/test_<tool>.py` file is invisible to it.

## Requirements & traceability (TRLC)

This repo's own requirements/tests are tracked in TRLC and traced with LOBSTER itself
(dogfooding). Schema is [lobster/requirements.rsl](../lobster/requirements.rsl).

- New features and behavior changes must be requirements-driven: add or update the relevant
  `.trlc` requirement(s) *before or alongside* implementation, then write tests that verify
  the requirement — never add a requirement retroactively just to justify code/tests that
  were written by observing what the implementation happens to do.
- Hierarchy: `UseCase` → `System_Requirement` (`derived_from` a UseCase) →
  `Software_Requirement` (`derived_from` a System_Requirement).
- Each tool has its own RSL package `<tool>_req`, importing `req` and `UseCases`, with content
  under `lobster/tools/<tool>/requirements/` (or `lobster/tools/core/<tool>/requirements/`).
- Tests reference requirements via `# lobster-trace: <package>.<RequirementName>` comments.
  **System tests trace only to `System_Requirement`; unit/software tests trace only to
  `Software_Requirement`** — never mix these.
- TRLC does not resolve forward references: a `type` in a `.rsl` file must be declared before
  any other `type` that references it.
- Model one requirement per distinct observable behavior; consolidate near-duplicate cases
  (e.g. the same failure reached via different input paths) into a single requirement rather
  than one-per-test-case.
- A `System_Requirement` is expected to show "PARTIAL" coverage (not fully OK) until it has
  incoming refs from both a `Software_Requirement` and a system test — this is by design, not
  a bug; check `ref_up`/`ref_down` on the individual item instead of only the top-level %.
- Don't add `# lobster-trace:` comments to production `.py` files — code-level tracing is out
  of scope; only requirement-to-test coverage is tracked.
- To cross-check that every requirement has a test and vice versa, don't hand-roll regex; use
  the TRLC Python API (`trlc.trlc.Source_Manager`, `iter_record_objects()`) or
  `trlc <path> --debug-api-dump`.

## Build, test, and tracing commands

- Use the repo's `.venv/` (`source .venv/bin/activate`). If missing:
  `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements_dev.txt -r requirements.txt`
- `bazel test //lobster:trlc` validates `requirements.rsl` + all `.trlc` files (warnings as errors) —
  run this after any TRLC change.
- Prefer scoped Bazel targets for a single tool over the full suite:
  `bazel test //tests_unit/lobster_<tool>/... //tests_system/lobster_<tool>/...`
  (exercises real BUILD.bazel deps/data). Reserve `make test-unit` / `make test-system` for
  full-suite runs with coverage thresholds.
- `./tracing/tracing.sh` regenerates the tracing evidence for all tools; it deletes and
  recreates `tracing_out/` itself, so no manual cleanup is needed first. Run it via
  `export PYTHONPATH="$PWD"` if not already exported.
- Inspect a tool's coverage with:
  `bazel run //:lobster-ci-report -- tracing_out/<tool>/tracing.lobster --show-coverage`
- `tracing_out/`, `docs/*.html`, and `docs/*.lobster` are generated review evidence and are
  gitignored — do not commit them. Root-level `*.lobster` files (e.g. `report.lobster`,
  `code.lobster`) are also untracked local artifacts, not committed files.

## Conventions

- Tests must assert against requirement-derived expected behavior, never against whatever the
  implementation currently happens to do. The one exception is pure fixture plumbing (see below).
- When a tool's implementation needs refactoring to make its logic unit-testable, prefer
  extracting small, directly-callable functions from an orchestration method over writing a
  test that just re-runs the whole CLI path and asserts on stdout — verify no behavior change
  by re-running existing system tests before/after the refactor.
- The one exception to the rule above is pure fixture plumbing: if you hand-write a
  `*.lobster` JSON file as test *input data* (instead of generating it by running a real
  LOBSTER tool), check it against [documentation/schemas.md](../documentation/schemas.md) first.
  That doc covers the common envelope and the req-trace/imp-trace/act-trace schemas, but
  explicitly calls the `lobster-report` schema "internal" (undocumented) — for report fixtures
  specifically, also run the real tool against the file once and confirm it's accepted without
  errors. Either way, this only guards against a malformed fixture causing a false pass/fail;
  it must not be used to decide what the test should assert.
