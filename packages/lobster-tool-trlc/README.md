# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

## Configuration

This tool requires a few parameters in a configuration file.
They describe how to convert a TRLC record type to a LOBSTER item.

For example, your TRLC input files may contain a `Requirement` type,
which has a `summary` field, and you want to use this field as text
in the LOBSTER item.
Such a mapping can be defined in the configuration file.

Example:

```yaml
inputs:
  - carrot.rsl
  - carrot1.trlc
  - carrot2.trlc
  - potato.rsl
  - potato.trlc

conversion-rules:
  - package: vegtables
    record-type: Requirement
    namespace: req
    description-fields:
      - summary
      - other_summary
    justification-up-fields:
      - justification1
      - justification2
    justification-down-fields:
      - justification3
    justification-global-fields:
      - justification4
    tags:
      - derived_from
    applies-to-derived-types: true
  - package: vegtables
    record-type: Security_Requirement
    namespace: req
    description-fields:
      - summary
      - extra_text
    tags:
      - field: trace
        namespace: act

to-string-rules:
  - package: vegtables
    tuple_type: External_Id
    namespace: req
    to_string:
      - "$(item)@$(version)"
      - "$(item)"
```

By default none of the objects are traced, but adding a declaration
like this marks this type (and all its extensions) as things to trace.

The `description-fields` specify which fields carry the description text that
can be optionally included in LOBSTER.

The `tags` field identifies the field carrying tags.
In LOBSTER all tags are namespaced, and by default the namespace is "req" as that
is generally what you want to do with TRLC.
But you can change this by including the namespace, see the example above.

Three namespaces are supported:

- `req` for "requirement"
- `act` for "activity"
- `imp` for "implementation"

For tuple types like this one:

```yaml
trlc_config: |
  tuple Codebeamer_Id {
    item Integer
    separator @
    version optional Integer
  }
```

You need to provide a series of text expansions so that the
`lobster-trlc` tool can build lobster tags from it.
You can do this via the `to-string-rules` configuration entry.

These `to-string` functions are applied in order, and the tool picks the first one that
fully manages to apply. If a value is `null` and required for the
the expansion (as in the first `to-string` function above), the current
function is skipped, and the next one is attempted. If none of the functions
can be applied, an error is raised.

If you need to justify requirements not being linked or implemented,
then you can also define up to three extra fields (using `justification_up`,
`justification_down`, and `justification_global`) that should carry this
information.
See the example above.

The meaning of "up" is along the usual direction of tracing tags. For
example putting this in a software requirement means it is not linked
to a system requirement. The meaning of "down" is against the usual
direction of tracing tags. For example putting this in a software
requirement means it is either not implemented or not tested.

As you can see the down justification is much more imprecise than an
up justification. You should only use them if there is no other way to
attach this justification on the actual offending object.

Finally the "global" justification is a catch all: it just means no
tracing policy will be validated at all when considering this object.

## Executing lobster-trlc tool

`lobster-trlc` takes two command line arguments as follows:
* `--config` - Yaml based config file path in which the following parameters can be 
  mentioned.
  * `inputs`: A list of input file paths (can include directories).
  * `inputs_from_file`: A file containing paths to input files or directories.  
* `out`: The name of the output file where results will be stored.

### Command

```
> lobster-trlc --config "path/to/the/config/file.yaml" --out "output/path.lobster"
```

## Tools

`lobster-trlc`: Extract requirements from TRLC.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
