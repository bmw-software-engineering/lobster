# Notes for Developers

## Type Hints

The source code of `lobster-trlc` uses type hints to increase understandability
of the source code.

The TRLC package (not to confuse with `lobster-trlc`) uses two categories of types:

- the types that a user defines,
- the Python types that are used in the implementation of TRLC

Let's look at the following examplatory RSL file written in TRLC:

```rsl
package example

tuple My_Data {
  tuple_member1 Integer
  separator @
  tuple_member2 Integer
}

type My_Requirement {
  field1 My_Data
}
```

And the corresponding TRLC file could instantiate `My_Requirement` as follows:

```trlc
package example

My_Requirement My_Instance {
    field1 = 1 @ 2
}
```

We can now use the TRLC api to iterate over all instances (called `Record_Object`
in TRLC) like this:

```python
from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager
from trlc import ast

sm = Source_Manager(Message_Handler())
sm.register_file("path/to/above.rsl")
sm.register_file("path/to/above.trlc")
symbol_table = sm.process()
result = list(symbol_table.iter_record_objects())
# since there is only one object in our example, we can fetch it by index:
my_instance = result[0]
```

Let's analyze the types:
```python
print(type(my_instance))  # trlc.ast.Record_Object
print(type(my_instance.field["field1"]))  # trlc.ast.Tuple_Aggregate
print(type(my_instance.field["field1"].typ))  # Tuple_Type<example.My_Data>
```

We immediately learn the difference between `Tuple_Aggregate` and `Tuple_Type`:

- `Tuple_Type` is a representation of the type that the user had defined,
  and which the user had given the name "My_Data".
- `Tuple_Aggregate` is the Python class type that holds the value.
  In our example the tuple is made up of two integer values `1` and `2`.

This difference is important to be able to understand the type hints given
in the implementation of `lobster-trlc`.

You can find the implementation of the mentioned types here:
- [Tuple_Aggregate](https://github.com/bmw-software-engineering/trlc/blob/trlc-2.0.2/trlc/ast.py#L934)
- [Tuple_Type](https://github.com/bmw-software-engineering/trlc/blob/trlc-2.0.2/trlc/ast.py#L2732)
- [Record_Object](https://github.com/bmw-software-engineering/trlc/blob/trlc-2.0.2/trlc/ast.py#L2926)

(Links refer to TRLC release 2.0.2)

Imagine the user defines a second tuple, like this:

```rsl
package example_extended

tuple My_Data {
    tuple_member1 Integer
    separator @
    tuple_member2 Integer
}

tuple My_Other_Data {
    tuple_member1 Integer
    separator @
    tuple_member2 Integer
    separator @
    tuple_member3 Integer
}

type My_Requirement {
    field1 My_Data
    field2 My_Other_Data
}
```

And instantiate a record object like this:

```trlc
package example_extended

My_Requirement My_Instance {
    field1 = 1 @ 2
    field2 = 3 @ 4 @ 5
}
```

Let's analyze the types again:
Let's analyze the types:
```python
print(type(my_instance.field["field1"]))  # trlc.ast.Tuple_Aggregate
print(type(my_instance.field["field1"].typ))  # Tuple_Type<example_extended.My_Data>
print(type(my_instance.field["field2"]))  # trlc.ast.Tuple_Aggregate
print(type(my_instance.field["field2"].typ))  # Tuple_Type<example_extended.My_Other_Data>
```

You can see that all user-defined tuples are stored in instances of
`trlc.ast.Tuple_Aggregate`, but only the `typ` property tells us which
user-defined type it is.
