# LOBSTER Configuration Files

A lobster config file (by default `lobster.yaml`) declares the tracing
policy. The syntax is fairly simple and best explained by example.

**Note:** LOBSTER also still accepts the legacy configuration
format (any file extension other than `.yaml`/`.yml`, e.g. `lobster.conf`),
but that format is deprecated and will be removed in a future release; the
tool prints a warning to standard output whenever it is used.
Use the YAML
format shown below for any new configuration.

## Levels

The core feature is an item level, and there are three kinds:

* requirements (for things like trlc, codebeamer, systemweaver, doors, ...)
* implementation (for things like code or models)
* activity (for things like tests, proofs, argumentation, ...)

A typical level declaration might look like this:

```yaml
levels:
  - name: "Code"
    kind: implementation
    source:
      - "cpp.lobster"
      - "matlab.lobster"
    trace-to:
      - "Requirements"
```

What we have here is an implementation level called `Code` that has
two data sources (a C++ extract and a MATLAB extract). This code is
supposed to contain tracing tags that link it to items from the
`Requirements` level.

Declaration order does not matter: a level may be referenced by
`trace-to`/`requires` even if it is declared later in the `levels` list.

### Level attributes

#### source

The `source` attribute assigns a list of LOBSTER files to contribute to
this level.

#### trace-to

The `trace-to` attribute declares the expected tracing link. This
declares that the items in this level are expected to be linked to
items from that level. It is possible to have more than one level
mentioned here (but it probably makes no sense).

For example, here we declare that requirements are the top-level
(since there are no links expected), and code should trace to the
requirements.

```yaml
levels:
  - name: "Requirements"
    kind: requirements
    source:
      - "trlc.lobster"

  - name: "Code"
    kind: implementation
    source:
      - "python.lobster"
    trace-to:
      - "Requirements"
```

#### requires

Sometimes you might want alternatives. For example we could have two
possibly ways to verify a requirement: by proof or by test. If we just
do this:

```yaml
levels:
  - name: "Requirements"
    kind: requirements
    source:
      - "trlc.lobster"

  - name: "Code"
    kind: implementation
    source:
      - "ada.lobster"
    trace-to:
      - "Requirements"

  - name: "Unit Test"
    kind: activity
    source:
      - "aunit.lobster"
    trace-to:
      - "Requirements"

  - name: "Formal Proof"
    kind: activity
    source:
      - "gnatprove.lobster"
    trace-to:
      - "Requirements"
```

Then we would get lots of errors as the tooling would require a
requirement to be broken down into all three. The `requires`
configuration can help here:

```yaml
levels:
  - name: "Requirements"
    kind: requirements
    source:
      - "trlc.lobster"
    requires:
      - ["Code"]
      - ["Unit Test", "Formal Proof"]
```

Now an item is considered to be completely traced if it has both a
link to code, and either a link to a test or a link to a proof.

`requires` is a list of AND-groups; each group is itself a list of
OR-alternatives. In the example above, an item needs a link from `Code`
**and** a link from either `Unit Test` **or** `Formal Proof`.

**Note:**
Don't forget that the `trace-to` configuration is always mandatory.
You cannot build links with a configuration that uses only `requires`.

# Examples

A simple example that just links SIMULINK models to requirements
stored in codebeamer:

```yaml
levels:
  - name: "Requirements"
    kind: requirements
    source:
      - "cbtrace.lobster"

  - name: "Models"
    kind: implementation
    source:
      - "mh_imp_trace.lobster"
    trace-to:
      - "Requirements"
```

A more complex example that breaks down system requirements in
codebeamer to TRLC software requirements. The C++ implementation is
traced against software requirements. Unit tests show software
requirements coverage and integration tests show system requirements
coverage. For non-functional system requirements we alternatively show
they are met with some hand-written analysis (for which we've created
our own custom LOBSTER trace tool).

```yaml
levels:
  - name: "System Requirements"
    kind: requirements
    source:
      - "cbtrace.lobster"
    requires:
      - ["Integration Tests", "Analysis"]

  - name: "Software Requirements"
    kind: requirements
    source:
      - "trlc.lobster"
    trace-to:
      - "System Requirements"

  - name: "Code"
    kind: implementation
    source:
      - "cpptrace.lobster"
    trace-to:
      - "Software Requirements"

  - name: "Unit Tests"
    kind: activity
    source:
      - "gtest_unit.lobster"
    trace-to:
      - "Software Requirements"

  - name: "Integration Tests"
    kind: activity
    source:
      - "gtest_int.lobster"
    trace-to:
      - "System Requirements"

  - name: "Analysis"
    kind: activity
    source:
      - "analysis.lobster"
    trace-to:
      - "System Requirements"
```
