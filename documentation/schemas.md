# LOBSTER JSON Schemas

## Common

Each LOBSTER JSON file shares the following common structure:

```
{
    "data"        : LIST,
    "generator"   : STRING,
    "schema"      : STRING,
    "version"     : INTEGER,
    "custom_data" : DICTIONARY object(optional)
}
```

* _data_ is the main content
* _generator_ is the name of the program that created the artefact
* _schema_ is one of the following:
  * lobster-req-trace for requirements traces
  * lobster-imp-trace for implementation traces
  * lobster-act-trace for activity traces
  * lobster-report for the tracing report
* _version_ is the version ID for this report; later version of LOBSTER
  may change data in an incompatible way and the version ID allows us
  to generate more useful error messages in this case
* _custom_data_ (optional) is an object containing high-level metadata related to the report, such as:
  * component : the component name
  * branch : the branch name
  * ci_run : a timestamp or CI run identifier

  Example:
  ```
  "custom_data": {
    "component": "LSS",
    "branch": "stable-25",
    "ci_run": "2025-05-21 01:00 UTC"
  }
  ```
  This information is used to help users identify the origin and context of the report and will be displayed in the top-right corner of the generated HTML output if provided.

Some schemas may add additional top-level items, but these four are
always present.

### Source References

A SOURCE_REF is an object with varying forms. One field is always present:

```
{
   "kind" : REF_KIND,
}
```

Based on the value of *kind* this object takes different forms.

#### File references

File references look like this:

```
{
   "kind"   : "file",
   "file"   : STRING,
   "line"   : INTEGER or null,
   "column" : INTEGER or null
}
```

#### Github references

References to github look like this:

```
{
   "kind"           : "github",
   "gh_root"        : STRING,
   "gh_repo"        : STRING,
   "filename"       : INTEGER,
   "line"           : INTEGER or null,
   "commit" : STRING
}
```

The *gh_root* is the github instance, for example
`https://github.com`. The *gh_repo* is the combination of user and
repo, for example `bmw-software-engineering/trlc`. The *commit* is
a SHA on which the user had checked out before executing the 
`lobster-online-report` tool. Finally,
*filename* and *line* has the usual meaning.

#### codebeamer references

References to the proprietary codebeamer tool look like this:

```
{
   "kind"     : "codebeamer",
   "cb_root"  : STRING,
   "tracker"  : INTEGER,
   "item"     : INTEGER,
   "version"  : INTEGER or null,
   "name"     : STRING
}
```

The *cb_root* refers to the root codebeamer URL (everything up to, but
excluding, the `/cb/`), *tracker* to the tracker that contains the
item, and *item* is the numeric id itself. The *version* if specified,
references a specific version, otherwise the reference is to the
HEAD. Finally *name* is the short human-readable name of the item.

Note: we are considering to retire this kind of reference as it is too
specific, and replace with a "online" reference that consists out of a
tool indicator (e.g. codebeamer) and a url. A design goal of LOBSTER
is after all that adding support for a new tool doesn't require a
change in LOBSTER itself.

#### Void references

A void reference can be used if an item cannot be given a proper
location or link, for whatever reason.

```
{
   "kind" : "void",
}
```

## Items

All items (requirements, implementation, and activities) share a few
basic properties.

### Version 1-2

Deprecated.

### Version 3

```
  "tag":         TRACING_TAG,
  "location":    SOURCE_REF,
  "name":        STRING,
  "refs":        LIST-OF-TRACING_TAG
  "just_up":     LIST-OF-STRING,
  "just_down":   LIST-OF-STRING,
  "just_global": LIST-OF-STRING
```

The `TRACING_TAG` is right now a string that matches this regex:

```regex
[a-z]+ .+
```

The first letter group is a namespace for the tag, e.g. `req` (for all
requirements) or e.g. `cpp` (for C++ code). The next letter group is
the actual tag name e.g. `example.requirement` or `12345`; and the
final optional group is a version. Some examples:

* `req example.requirement` TRLC requirement example.requirement
* `req 12345@42` codebeamer requirement 12345 at version 42
* `cpp kitten::foo` C++ function foo (in namespace kitten)

In the future we may make this an object.

The *name* is a more human readable name, which doesn't have to be
unique. For the names for the three examples above might be:

* `requirement` (just the trlc identifier)
* `requirement` (the actual title for item 12345 in cb)
* `foo` (just the function name)

The three justification lists *just_up*, *just_down*, and
*just_global* collect justification reasons why a link might be
missing. Generally you just use *just_up* since we link up; but in
some cases we might have to justify "from the top down". The global
justifications are both up and down, and should be used very
sparingly.

The *refs* is a list of `TRACING_TAG` referencing other items in
lobster this item should trace *up* to.

## Requirements

### Version 1-2

Deprecated.

### Version 3

Requirements are items, with the following additional fields:

```
{
   << the common item fields >>
   "framework" : STRING
   "kind"      : STRING
   "text"      : STRING or null
}
```

* *framework* is the data source, for example "codebeamer" or "TRLC".
* *kind* is a free text string describing what kind of requirement
  this is. For example "functional requirement".
* *text* is an optional copy or a summary of the requirement text.

### Version 4

As above, but adds one new field:

```
{
   << version 3 fields >>
   "status" : STRING or null
}
```

* *status* indicates the state of a requirement. This is used by some
  proprietary tools; and lobster can check that the status is one of
  the permitted ones.

## Implementation

### Version 1-2

Deprecated.

### Version 3

Implementation are items, with the following additional fields:

```
{
   << the common item fields >>
   "language" : STRING
   "kind"     : STRING
}
```

* *language* is a free text string indicating the implementation
  language. For example "Ada", "C++", or "Python".
* *kind* is a free text string describing the entity. For example
  "function", "method", "named number", "class".

## Activity

### Version 1-2

Deprecated.

### Version 3

Activity are items, with the following additional fields:

```
{
   << the common item fields >>
   "framework" : STRING
   "kind"      : STRING
   "status"    : STRING or null
}
```

* *framework* a free text string that describes where the activity
  takes place. For example "GTest", "SMTLIB Model", or "Hand-written
  analysis".
* *kind* is the type of activity. Generally, it is free text, but the
  following kinds have special meaning:

Test activities can (but are not required to) have another mapping for
"status" describing the test status. If set it can be one of the
following:

* *ok* if the test was run and no problems were found
* *fail* if the test was run and it failed
* *not run* if the test was not run for any reason

If the status is not explicitly set, then LOBSTER will assume it is
"ok". This makes sense because in a modern workflow you should have
pre-commit checks in your repo that block a commit where the tests
fail (hence we don't need to explicitly get the test status in LOBSTER
since it must always be OK).

## Report

The report schema is currently internal to LOBSTER.
