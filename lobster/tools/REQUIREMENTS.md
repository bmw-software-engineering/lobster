This document describes how requirements shall be written and interpreted for all `lobster` tools.
It is a mandatoy guideline and is also a style guide.

# Requirement Levels

There are the following levels:

1. use cases (not yet written)
2. system requirements
3. software requirements

Use cases and requirements are written in the TRLC language.
Requirements are written individually for each lobster tool,
but use cases are written for the whole lobster eco-system.
For example, the requirements for `lobster-json` are not dependent on the requirements for `lobster-report`.
But a use case may describe the need to parse `c++` and `trlc` input files, and generate a traceability report for these.

The system requirements of one tool describe the behavior of that tool, considering possible inputs and describing the outputs.
System requirements are derived from use cases.

The software requirements of that tool are derived from the system requirements of that tool.

Each system requirement must be broken down into software requirements.
Each software requirement must be derived from system requirements.

LOBSTER itself is used to generate traceability reports to measure the above constraints.

# Requirement Aspects
## Introduction
Requirements may have several input conditions.
For example, `lobster-json` has got a configuration parameter called `FILE_OR_DIR`, where the user can specify a list of files combined with a list of directories.

- If a given path is an existing file (determined by the OS)
- and if such a file contains well-formatted JSON
- and the configuration parameter `out` points to a file that can be written (i.e write permissions exist)

then the tool will start parsing that input file and generate output for it.

For each above condition there is also an "error path".
So there must be requirements that describe what the tool shall do if any of the conditions is not met.
And each condition may have a different consequence on failure.
For example, the tool shall print a certain error message if the path does not exist,
and shall print a completely different error message if the content is not valid JSON.

All the above conditions and all their error paths must be tested.
This leads to a large number of tests for one single requirement.
It is a common problem in the domain of requirements engineering.
The challenge is to keep track whether all aspects of a requirement are tested.

Therefore,
to reduce the complexity of mapping tests to requirements,
requirements for all LOBSTER tools shall be split into single aspects in TRLC.

## Semantics
The order of TRLC objects is given through their order in the `*.trlc` file.
TRLC objects from different `*.trlc` files have no ordering relative to each other.

The `requirements.rsl` defines the types `System_Requirement` and `System_Requirement_Aspect`.
These shall be used to split a requirement sentence or paragraph into separate TRLC objects.
System tests shall be mapped to `System_Requirement` and `System_Requirement_Aspect`, depending on the aspect that the system test verifies.

A requirement may consist of zero or one `System_Requirement` object,
and arbitrary many `System_Requirement_Aspect` objects.

Any `System_Requirement` object is always the start of a requirement.
The first `System_Requirement_Aspect` object without any preceding `System_Requirement`
object is also always the start of a requirement.
Other `System_Requirement_Aspect` objects belong to the previously started system
requirement.

The word `OTHERWISE` shall always refer to the immediate preceding condition.
That condition may be found in the same TRLC object or in a preceding TRLC object
(limited to `System_Requirement` and `System_Requirement_Aspect`, ignoring any other
types in between).

The following words shall be written in capital letters for visual enhancement:
- AND
- OR
- IF
- OTHERWISE
- THEN
- SHALL

## Example
Please have a look at [json/input_files.trlc](json/input_files.trlc)
to find an example `*.trlc` file that is using the `System_Requirement_Aspect` type.
