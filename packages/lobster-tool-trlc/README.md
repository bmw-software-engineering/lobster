# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

## Configuration

This tool is a bit more complex and you need to supply a config file,
named (by default) `lobster-trlc.conf`. In it you can declare how
you'd like tracing tags to be extracted.

For record types you can write:

```
package.typename {
   description = field_name
   tags = field_name
}
```

By default none of the objects are traced, but adding a declaration
like this marks this type (and all its extensions) as things to trace.

The `description` marks which field carries the description text that
can be optionally included in LOBSTER.

The tags field identifies the field carrying a tags field. In LOBSTER
all tags are namespaced, and by default the namespace is "req" as that
is generally what you want to do. But you can change this by including
the namespace like so:

```
   tags "franka" = field_name
```

For tuple types like this one:

```
tuple Codebeamer_Id {
  item Integer
  separator @
  version optional Integer
}
```

You need to provide a series of text expansions so that the
`lobster-trlc` tool can build lobster tags from it. You can do this
like so:

```
example.Codebeamer_Id {
  to_string = "$(item)@$(version)"
  to_string = "$(item)"
}
```

These functions are applied in order, and we pick the first one that
fully manages to apply. If a value is `null` and required for the
the expansion (as in the first `to_string` function above), the current
function is skipped, and the next one is attempted. If none of the functions
can be applied, an error is raised.

If you need to justify requirements not being linked or implemented,
then you can also defined up to three extra fields (using `just_up`,
`just_down`, and `just_global`) that should carry this
information. For example:

```trlc
type Requirement {
   text String
   unimplemented_justification optional String
}
```

With this config file:

```plain
example.Requirement {
   description = text
   just_down   = unimplemented_justification
}
```

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
  * `trlc_config_file`: trlc configuration file as mentioned in the configuration 
    section and also in the example mentioned below see (trlc_config.conf)
  * `inputs`: A list of input file paths (can include directories).
  * `inputs_from_file`: A file containing paths to input files or directories.
  * `traverse_bazel_dirs`:  Enter bazel-* directories, which are excluded by default.
   
* `out`: The name of the output file where results will be stored.

### Command

lobster-trlc --config "path to the yaml config file" --out "output file path"

### Example

#### trlc_config.conf
```yaml
req.Requirement {
  description = description
}
```

#### trlc_config_file.yaml
```yaml
inputs: [list of paths to *.trlc and *. rsl files separated by commas]
trlc_config_file: "path to the above mentioned trlc_config.conf file"
```
#### In this case the command will be
`lobster-trlc --config=trlc_config_file.yaml --out=trlc.lobster`

## Tools

* `lobster-trlc`: Extrat requirements from TRLC.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).

This tool has no actual dependency on, or with, Codebeamer. It just
talks the API as described here: https://codebeamer.com/cb/wiki/117612
