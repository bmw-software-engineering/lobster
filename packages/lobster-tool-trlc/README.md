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
  - package: vegetables
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
  - package: vegetables
    record-type: Security_Requirement
    namespace: req
    description-fields:
      - summary
      - extra_text
    tags:
      - field: trace
        namespace: act

to-string-rules:
  - package: vegetables
    tuple-type: External_Id
    to-string:
      - "$(item)@$(version)"
      - "$(item)"
```

Only record types covered by a `conversion-rules` entry are emitted as LOBSTER items.
Set `applies-to-derived-types: true` to apply a rule to derived record types as well;
the default is `false`.

The `description-fields` specify which fields carry the description text that
can be optionally included in LOBSTER.

### Version parameter (`version-field`)

Use `version-field` inside a `conversion-rules` entry to select which TRLC
record field is written as the generated LOBSTER item version.

Some teams call this a "version flag" in prose, but the exact configuration
key is `version-field`.

Example:

```yaml
conversion-rules:
  - package: vegetables
    record-type: Requirement
    namespace: req
    version-field: p_version
```

Behavior:

- **Configured and field exists:** If `version-field` is configured and the record object
  contains a field with that name, the tool sets the tag version to that field's value.
- **Configured but field missing:** If `version-field` is configured but the record object
  does not contain a field with that name, the tool sets the tag version to `None`.
- **Not configured:** If no `version-field` entry is present in the conversion rule,
  the tool sets the tag version to `None` regardless of the record object.

`version-field` sets the version on the generated LOBSTER item tag. Separately,
expressions such as `$(item)@$(version)` in `to-string-rules` read the `version`
component from the TRLC tuple being formatted. If that tuple component is unset, that
rule is skipped and the next rule is attempted.

Example configuring both the item version and tuple formatting:

```yaml
to-string-rules:
  - package: vegetables
    tuple-type: External_Id
    to-string:
      - "$(item)@$(version)"
      - "$(item)"

conversion-rules:
  - package: vegetables
    record-type: Requirement
    namespace: req
    version-field: p_version
    tags:
      - external_id
```

Here, `p_version` sets the generated Requirement item's tag version. The
`to-string-rules` independently format each `external_id` tuple, preferring the
`item@version` form and falling back to `item` when the tuple's `version` component
is unset.

Generated output example:

```json
{
  "data": [
    {
      "tag": "req test_reqs.req_with_version@1234",
      "location": {
        "kind": "file",
        "file": "reqs.trlc",
        "line": 3,
        "column": 9
      },
      "name": "test_reqs.req_with_version",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "TRLC",
      "kind": "featReq",
      "text": "Feature requirement with an explicit version",
      "status": null
    }
  ],
  "generator": "lobster-trlc",
  "schema": "lobster-req-trace",
  "version": 4
}
```

If `p_version` is unset, the generated item tag has no version suffix:
`req test_reqs.req_with_version`.

The `tags` field identifies fields carrying tracing targets. Their namespace defaults
to `req`; specify a `namespace` for an individual tag entry to override it, as in the
example above. The generated LOBSTER item tag itself uses the `req` namespace.

LOBSTER trace tags support these namespaces:

- `req` for "requirement"
- `act` for "activity"
- `imp` for "implementation"

Define tuple types in a TRLC schema (`.rsl` file):

```trlc
package example

tuple Codebeamer_Id {
  item Integer
  separator @
  version optional Integer
}
```

In the YAML configuration, provide text expansions for each tuple type so
`lobster-trlc` can build LOBSTER tags from its values:

```yaml
to-string-rules:
  - package: example
    tuple-type: Codebeamer_Id
    to-string:
      - "$(item)@$(version)"
      - "$(item)"
```

These `to-string` rules are tried in order, and the tool picks the first one that
fully manages to apply. If a value is `null` and required for the
expansion (as in the first `to-string` rule above), the current
function is skipped, and the next one is attempted. If none of the functions
can be applied, an error is raised.

To provide justification text for requirements that are not linked or implemented,
configure `justification-up-fields`, `justification-down-fields`, and/or
`justification-global-fields` in a `conversion-rules` entry. Each key accepts either
a single TRLC field name or a list of field names. See the example above.

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

`lobster-trlc` takes the following command line arguments:
* `--config` - YAML based config file path in which the following parameters can be
  mentioned.
  * `inputs`: A list of input file paths (can include directories).
  * `inputs-from-file`: A file containing paths to input files or directories.
* `DIR|FILE` (optional positional arguments): Additional input directories or files.
* `--out`: The name of the output file where results will be stored.

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
