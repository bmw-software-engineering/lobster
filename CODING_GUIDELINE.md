# Coding Guideline

Since the introduction of the coding guideline,
we mostly follow the [_Black_ Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

Note that there is still older code around,
where the coding guideline has not yet been applied.

## Classes

The nomenclature of classes shall adhere to the following guideline:

- Classes shall use the CamelCase pattern.
- File names shall be equal to the class names, but all lower case letters.
- Private members shall have at least one leading underscore.
  Refer to [Private variables and name mangling](https://docs.python.org/3/tutorial/classes.html#private-variables)
  to read more about it.

Example:
```python
class CamelCase:
    pass
```
Here the file shall be named `camelcase.py`.

In general, files should not be too lengthy.
We don't want to give a specific limit on the number of lines.
Consider to keep classes in separate files,
instead of having one large file for multiple classes.

## Tests
We are using the `unittest` test framework for unit tests.
Test class names shall consist of the name of the class under test, 
with a `Test` postfix.

Example:
```python
from unittest import TestCase

class CamelCaseTest(TestCase):
    def test_function1(self):
        instance_under_test = CamelCase()
        result = instance_under_test.function1()
        self.assertEqual(True, result)
```

The file name shall be `test_camelcase.py`

## Line Length
The line length is 88 characters.

## Architecture
Consider to create classes with dedicated properties over using dictionaries with keys.

Example of the preferred approach:
```python
from dataclasses import dataclass


@dataclass
class Car:
    color: str

car = Car(color="red")
```

Counter-example of the disfavoured approach:
```python
car = {"color": "red"}
```
The latter examples with a dictionary is easier to get started with,
but it is harder to maintain and refactor.
Also pylint will not be able to give warnings when accessing a key that does not exist.



## Comments

It's good to avoid inline comments and single line comments should be preferred.

```python
def generate_lobster_report():
  
  # Please prefer to use this single line commenting style for better readability.
  lobster_report = ""
  
  return lobster_report  # Avoid commenting style like this comment.
```


## Documentation Strings a.k.a. Docstring

### One line docstring

One line docstrings as the name suggests, should fit in one line

Example:
```python
def sum_of_two_numbers(number1, number2):
  """Return the sum of two numbers."""
  return number1 + number2
```


### Multi-line docstring

Multi-line docstring consists of a single line summary with a blank line followed by it and then followed by more
detailed description. To know more about it please visit official documentation [Python Multi-line docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings).

```python
def generate_lobster_report(data, metadata):
  """
  Function to generate a lobster report.

  Keyword arguments:
  data -- data contains the actual data used to generate the report
  metadata -- metadata about the report
  """
  
  # some operations
  lobster_report = ""
  return lobster_report
```


## Blank lines

- Top-level functions and classes should be separated by 2 blank lines.
- A single blank line should be added between two methods of a class.
- Used blank lines inside a function/method based on logical sections and refrain from adding too much blank lines.


## Imports

Imports should always be added on top of the file and there order should be as in the below mentioned sequence.
- Standard library imports
- Third-party imports
- Application imports

Add a blank line between each type of imports.


- ### **Direct package/Module imports**
  - ```python
    # This is Correct
    import sys
    import os
    
    # Don't do this
    import sys, os
    
    # This one is fine
    from os import path
    ```
- ### **Absolute vs relative imports**
  - As per the PEP 8 guidelines absolute imports are recommended over relative imports.
  - ```python
    import lobster.items
    from lobster import items
    from lobster.items import Implementation, TracingTag
    
    # Although in case of complex package layouts relative imports are acceptable
    
    from .items import Implementation
    ```

- ### **Long import statements**
  For long import statements i.e. line length more than 88 characters, use the below format for import statements
  ```python
  from lobster.items import Tracing_Tag, Requirement, Implementation, Activity, Tracing_Status
  # The above import line is above 88 characters so surround the import statements using 
  # round brackets.
  
  from lobster.items import (
  Tracing_Tag, Requirement, Implementation, Activity, Tracing_Status
  )
  ```

- ### Important points
  - #### **Use relative imports only when the package structure is complex like one given in the example below**
  - #### **Do not use wildcard imports as it makes unclear exactly what is used from the imported package/module**
    - Example of wildcard imports
    ```python
    # Don't use wildcard imports
    from lobster import *
    ```


## String Quotes

Python supports single quoted as well as double-quoted strings. The PEP8 guideline doesn't have any guideline to use these.
But using one style would help the reader on focusing on the code and avoid any distraction.
The *Black coding style recommends to used double-quoted string as it match with the 
docstring standard as per PEP8*


## Function Lengths

There is no standard as such defined for the length of the functions.
However, if a functions is too long i.e lot of screen scrolling required to read as a whole then it is advisable to identify 
and club related code and move them to new functions. Breaking the code into smaller functions would also help in code reusability.


## Constants

Constants are generally defined at module level and in capital letters. For separation underscores are used.

Example : `SCHEMA`, `ERROR_SEVERITY`
