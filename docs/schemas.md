# LOBSTER JSON Schemas

## Common

Each LOBSTER JSON file shares the following common structure:

```
{
    "data"      : OBJECT or LIST,
    "generator" : STRING,
    "schema"    : STRING,
    "version"   : INTEGER
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

Some schemas may add additional top-level items, but these four are
always present.

### Source References

A SOURCE_REF is an object with varying forms. Two fields are always
the same:

```
{
   "ref"     : REF_KIND,
   "precise" : BOOLEAN
}
```

Based on the value of *ref* this object takes different
forms.

#### File references

File references look like this:

```
{
   "ref"     : "file",
   "precise" : BOOLEAN,
   "file"    : STRING,
   "line"    : INTEGER,
}
```

If *precise* is `true`, then a *line* number must be provided. If
*precise* is `false` then the *line* number may be `null`.

#### codebeamer references

References to the proprietary codebeamer tool look like this:

```
{
   "ref"     : "codebeamer",
   "instance" : STRING,
   "tracker"  : INTEGER,
   "item"     : INTEGER,
   "version"  : INTEGER
}
```

The *instance* refers to the root codebeamer URL, *tracker* to the
tracker that contains the item, and *item* is the numeric id
itself. References to codebeamer objects are always precise, and so
the *precise* value should be omitted or `true`.

Note: we are considering to retire this kind of reference as it is too
specific, and replace with a "online" reference that consists out of a
tool indicator (e.g. codebeamer) and a url. A design goal of LOBSTER
is after all that adding support for a new tool doesn't require a
change in LOBSTER itself.

## Requirements

### Version 1

The _data_ is an object mapping unique names to requirement
objects. Each requirement object has this structure:

```
{
   "kind"      : STRING,
   "text"      : STRING,
   "framework" : STRING,
   "source"    : SOURCE_REF,
   "tags"      : LIST OF UID STRINGS
}
```

* *kind* is a free text string describing what kind of requirement
  this is. For example "functional requirement".
* *text* is a copy or a summary of the requirement text.
* *framework* is the data source, for example "codeBeamer" or "TRLC".
* *source* is a pointer to the requirement
* *tags* is a list of text strings pointing to other items tracked by
  LOBSTER.

### Version 2

As version 1, but with an additional *name* field.

```
{
   "kind"      : STRING,
   "name"      : STRING,
   "text"      : STRING,
   "framework" : STRING,
   "source"    : SOURCE_REF,
   "tags"      : LIST OF UID STRINGS
}
```

The *name* field is a short summary of the requirement; this is
especially useful if the underlying system's unique identifiers are
something not intended for human consumption like hexdigits
(e.g. SystemWeaver) or digits (e.g. codebeamer, DOORS).

The *text* field is now optional and could be `null`.

## Implementation

### Version 1

The _data_ is an object mapping unique names to implementation
objects. Each implementation object has this structure:

```
{
   "kind"     : STRING,
   "language" : STRING,
   "source"   : SOURCE_REF,
   "tags"     : LIST OF UID STRINGS
}
```

* *kind* is a free text string describing the entity. For example
  "function", "method", "named number", "class".
* *language* is a free text string indicating the implementation
  language. For example "Ada", "C++", or "Python".
* *source* is a pointer to the declaration or body of the item, as is
  most appropriate for the language. For example in C++ bodies make
  more sense as you can have multiple declarations, but in Ada
  pointing to the specification makes more sense.
* *tags* is a list of text strings pointing to other items tracked by
  LOBSTER.

### Version 2

Same as version 1, but includes fields for justifications:

```
{
   "kind"               : STRING,
   "language"           : STRING,
   "source"             : SOURCE_REF,
   "tags"               : LIST OF UID STRINGS
   "justification"      : LIST OF STRINGS
   "justification_up"   : LIST OF STRINGS
   "justification_down" : LIST OF STRINGS
}
```

Additional fields over version 1:

* *justification* list of reasons why this item is not linked to
  anything (up or down)
* *justification_up* list of reasons why this item is not linked to
  something above it in the tracing policy
* *justification_down* list of reasons why this item is not linked to
  something below it in the tracing policy

## Activity

### Version 1

The _data_ is an object mapping unique names to activity objects. Each
activity object has this structure:

```
{
   "kind"      : STRING,
   "framework" : STRING,
   "source"    : SOURCE_REF,
   "tags"      : LIST OF UID STRINGS
}
```

* *kind* is the type of activity. Generally, it is free text, but the
  following kinds have special meaning:
  * *test* an executable test, test activities are described below
* *framework* a free text string that describes where the activity
  takes place. For example "GTest", "SMTLIB Model", or "Hand-written
  analysis".
* *source* is a pointer to the artefact or test case.
* *tags* is a list of text strings pointing to other items tracked by
  LOBSTER.

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
