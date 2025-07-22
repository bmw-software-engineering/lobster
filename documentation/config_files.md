# LOBSTER Configuration Files

A lobster config file (by default `lobster.conf`) declares the tracing
policy. The syntax is fairly simple and best explained by example.

## Levels

The core feature is an item level, and there are three kinds:

* requirements (for things like trlc, codebeamer, systemweaver, doors, ...)
* implementation (for things like code or models)
* activity (for things like tests, proofs, argumentation, ...)

A typical level declaration might look like this:

```
implementation "Code" {
  source: "cpp.lobster";
  source: "matlab.lobster";
  trace to: "Requirements";
}
```

What we have here is an implementation level called `Code` that has
two data sources (a C++ extract and a MATLAB extract). This code is
supposed to contain tracing tags that link it to items from the
`Requirements` level.

### Level attributes

#### source

The `source` attribute assigns a LOBSTER file to contribute to this
level.

#### trace to

The `trace to` attribute declares the expected tracing link. This
declares that the items in this level are expected to be linked to
items from that level. It is possible to have more than one level
mentioned here (but it probably makes no sense).

For example, here we declare that requirements are the top-level
(since there are no links expected), and code should trace to the
requirements.

```
requirements "Requirements" {
   source: "trlc.lobster";
}

implementation "Code" {
   source: "python.lobster";
   trace to: "Requirements";
}
```

#### requires

Sometimes you might want alternatives. For example we could have two
possibly ways to verify a requirement: by proof or by test. If we just
do this:

```
requirements "Requirements" {
   source: "trlc.lobster";
}

implementation "Code" {
   source: "ada.lobster";
   trace to: "Requirements";
}

activity "Unit Test" {
   source: "aunit.lobster";
   trace to: "Requirements";
}

activity "Formal Proof" {
   source: "gnatprove.lobster";
   trace to: "Requirements";
}
```

Then we would get lots of errors as the tooling would require a
requirement to be broken down into all three. The `requires`
configuration can help here:


```
requirements "Requirements" {
   source: "trlc.lobster";
   requires: "Code";
   requires: "Unit Test" or "Formal Proof";
}
```

Now an item is considered to be completely traced if it has both a
link to code, and either a link to a test or a link to a proof.

**Note:**
Don't forget that the `trace to` configuration is always mandatory.
You cannot build links with a configuration that uses only `requires`.

# Examples

A simple example that just links SIMULINK models to requirements
stored in codebeamer:

```
requirements "Requirements" {
   source: "cbtrace.lobster";
}

implementation "Models" {
   source: "mh_imp_trace.lobster";
   trace to: "Requirements";
}
```

A more complex example that breaks down system requirements in
codebeamer to TRLC software requirements. The C++ implementation is
traced against software requirements. Unit tests show software
requirements coverage and integration tests show system requirements
coverage. For non-functional system requirements we alternatively show
they are met with some hand-written analysis (for which we've created
our own custom LOBSTER trace tool).

```
requirements "System Requirements" {
   source: "cbtrace.lobster"
   requires: "Integration Tests" or "Analysis";
}

requirements "Software Requirements" {
   source: "trlc.lobster";
   trace to: "System Requirements";
}

implementation "Code" {
   source: "cpptrace.lobster";
   trace to: "Software Requirements";
}

activity "Unit Tests" {
   source: "gtest_unit.lobster";
   trace to: "Software Requirements";
}

activity "Integration Tests" {
   source: "gtest_int.lobster";
   trace to: "System Requirements";
}

activity "Analysis" {
   source: "analysis.lobster";
   trace to: "System Requirements";
}
```
