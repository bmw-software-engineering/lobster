# LOBSTER Configuration Files

A lobster config file (by default `lobster.yaml`) declares the tracing
policy. The syntax is fairly simple and best explained by example.
The new yaml configuration does not need an assignment to the three different 
level types requirements, implementation or activity anymore.
It just reflect a image of the internal stucture of the dictionary containing the 
different level definitions.

The new yaml configuration supports lobster files with version 5 and without schema.

## Levels

The core feature is an item level:
A typical level declaration might look like this:

``` yaml
Code: !LevelDefinition
  name: Code
  source:
  - file: cpp.lobster
  - file: matlab.lobster
  needs_tracing_up: true
  traces:
  - Requirements
```

What we have here is an implementation level called `Code` that has
two data sources (a C++ extract and a MATLAB extract). This code is
supposed to contain tracing tags that link it to items from the
`Requirements` level.

### Level attributes

#### source

The `source` attribute assigns a LOBSTER file to contribute to this
level.

#### traces and needs_tracing_up

The `traces` attribute declares the expected tracing link. This
declares that the items in this level are expected to be linked to
items from that level. It is possible to have more than one level
mentioned here (but it probably makes no sense).
`needs_tracing_up` need tobe set to true

For example, here we declare that requirements are the top-level
(since there are no links expected), and code should trace to the
requirements.

``` yaml
Requirements: !LevelDefinition
  name: Requirements
  source:
  - file: trlc.lobster
  needs_tracing_down: true
  breakdown_requirements:
  - - Code

Code: !LevelDefinition
  name: Code
  source:
  - file: python.lobster
  needs_tracing_up: true
  traces:
  - Requirements
```

#### requires

Sometimes you might want alternatives. For example we could have two
possibly ways to verify a requirement: by proof or by test. If we just
do this:

``` yaml
Requirements: !LevelDefinition
  name: Requirements
  source:
  - file: trlc.lobster
  needs_tracing_down: true
  breakdown_requirements:
  - - Code
  - - Unit Test
  - - Formal Proof

Code: !LevelDefinition
  name: Code
  source:
  - file: ada.lobster
  needs_tracing_up: true
  traces:
  - Requirements

Unit Test: !LevelDefinition
  name: Unit Test
  source:
  - file: aunit.lobster
  needs_tracing_up: true
  traces:
  - Requirements

Formal Proof: !LevelDefinition
  name: Formal Proof
  source:
  - file: gnatprove.lobster
  needs_tracing_up: true
  traces:
  - Requirements
```

Then we would get lots of errors as the tooling would require a
requirement to be broken down into all three. The `breakdown_requirements`
configuration can help here:


``` yaml
Requirements: !LevelDefinition
  name: Requirements
  source:
  - file: trlc.lobster
  needs_tracing_down: true
  breakdown_requirements:
  - - Code
  - - Unit Test
    - Formal Proof
```

Now an item is considered to be completely traced if it has both a
link to code, and either a link to a test or a link to a proof.

**Note:**
Don't forget that the `traces` configuration is always mandatory.
You cannot build links with a configuration that uses only `breakdown_requirements`.

# Examples

A simple example that just links SIMULINK models to requirements
stored in codebeamer:

``` yaml
Requirements: !LevelDefinition
  name: Requirements
  source:
  - file: cbtrace.lobster
  needs_tracing_down: true
  breakdown_requirements:
  - - Models

Models: !LevelDefinition
  name: Models
  source:
  - file: mh_imp_trace.lobster
  needs_tracing_up: true
  traces:
  - Requirements
```

A more complex example that breaks down system requirements in
codebeamer to TRLC software requirements. The C++ implementation is
traced against software requirements. Unit tests show software
requirements coverage and integration tests show system requirements
coverage. For non-functional system requirements we alternatively show
they are met with some hand-written analysis (for which we've created
our own custom LOBSTER trace tool).

``` yaml
System Requirements: !LevelDefinition
  name: System Requirements
  source:
  - file: cbtrace.lobster
  needs_tracing_down: true
  breakdown_requirements:
  - - Software Requirements
  - - Integration Tests
  - - Analysis

Software Requirements: !LevelDefinition
  name: Software Requirements
  source:
  - file: trlc.lobster
  needs_tracing_up: true
  traces:
  - System Requirements
  needs_tracing_down: true
  breakdown_requirements:
  - - Code
  - - Unit Tests

Code: !LevelDefinition
  name: Code
  source:
  - file: cpptrace.lobster
  needs_tracing_up: true
  traces:
  - Software Requirements

Unit Tests: !LevelDefinition
  name: Unit Tests
  source:
  - file: gtest_unit.lobster
  needs_tracing_up: true
  traces:
  - Software Requirements

Integration Tests: !LevelDefinition
  name: Integration Tests
  source:
  - file: gtest_int.lobster
  needs_tracing_up: true
  traces:
  - System Requirements

Analysis: !LevelDefinition
  name: Analysis
  source:
  - file: analysis.lobster
  needs_tracing_up: true
  traces:
  - System Requirements
```


# Deprecated .conf Configuration Files

The deprecated .conf lobster config file (by default `lobster.conf`) declares the tracing
policy. The syntax is fairly simple and best explained by example.

## Levels

The core feature is an item level, and there are three kinds need to be assigned:

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
   source: "cbtrace.lobster";
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
