# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool to interface with the proprietary
requirements management tool
[Codebeamer](https://intland.com/codebeamer).

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
fully manages to apply. When a value is `null`, then and it'd be used
(like in the first to_string function above) then the expansion does
not apply and we move to the next, and so on. When none apply an error
is created.

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

## Tools

* `lobster-trlc`: Extrat requirements from TRLC.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).

This tool has no actual dependency on, or with, Codebeamer. It just
talks the API as described here: https://codebeamer.com/cb/wiki/117612
