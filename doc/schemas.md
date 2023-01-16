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

* _kind_ is a free text string describing what kind of requirement
  this is. For example "functional requirement".
* _text_ is a copy or a summary of the requirement text.
* _framework_ is the data source, for example "codeBeamer" or "TRLC".
* _source_ is a pointer to the requirement
* _tags_ is a list of text strings pointing to other items tracked by
  LOBSTER.

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

* _kind_ is a free text string describing the entity. For example
  "function", "method", "named number", "class".
* _language_ is a free text string indicating the implementation
  language. For example "Ada", "C++", or "Python".
* _source_ is a pointer to the declaration or body of the item, as is
  most appropriate for the language. For example in C++ bodies make
  more sense as you can have multiple declarations, but in Ada
  pointing to the specification makes more sense.
* _tags_ is a list of text strings pointing to other items tracked by
  LOBSTER.

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

* _kind_ is the type of activity. Generally, it is free text, but the
  following kinds have special meaning:
  * _test_ an executable test, test activities are described below
* _framework_ a free text string that describes where the activity
  takes place. For example "GTest", "SMTLIB Model", or "Hand-written
  analysis".
* _source_ is a pointer to the artefact or test case.
* _tags_ is a list of text strings pointing to other items tracked by
  LOBSTER.

Test activities can (but are not required to) have another mapping for
"status" describing the test status. If set it can be one of the
following:

* _ok_ if the test was run and no problems were found
* _fail_ if the test was run and it failed
* _not run_ if the test was not run for any reason

## Report

The report schema is currently internal to LOBSTER.
