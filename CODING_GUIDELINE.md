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
