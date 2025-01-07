Here we give an example how to use the LOBSTER API.
The goal of this example snippet is to read a file written in scala,
and extract all function declarations as LOBSTER tags.

The scala input file is called `code.scala`, and the output file is called `scala.lobster`.

```python
from typing import Optional, Tuple

from lobster.io import lobster_write
from lobster.items import Tracing_Tag, Implementation
from lobster.location import File_Reference
from datetime import timedelta
import time


def _up_to_chr(string: str, char: str) -> str:
    """Returns the string from the beginning until the first occurrence of 'char' (excluding 'char')"""
    i = string.find(char)
    if i > 0:
        return string[:i]
    return string


def _function_declaration_to_name(declaration: str) -> str:
    """Extracts the function name from the beginning of a function declaration"""
    name = declaration.replace(" ", "")
    name = _up_to_chr(name, "(")
    name = _up_to_chr(name, ":")
    return name


def get_function(line: str) -> Optional[Tuple[str, int]]:
    """Gets the name of a scala function, assuming there is no linebreak between the 'def' keyword and the function name"""
    words = line.split()
    for i, word in enumerate(words):
        if "def" == word:
            try:
                return _function_declaration_to_name(words[i + 1]), line.find(words[i+1]) + 1
            except KeyError as ex:
                raise ValueError("Functions must be defined on the same line as the 'def' keyword!") from ex
    return None


def get_items(filename):
    items = []
    with open(filename, "r", encoding="UTF-8") as file:
        line_counter = 0
        for line in file:
            line_counter += 1
            match = get_function(line)
            if match:
                function_name, column = match
                print(f"{line_counter} Yes: {function_name}")
                implementation = Implementation(
                    language="scala",
                    kind="Function",
                    name=function_name,
                    tag=Tracing_Tag(
                        tag=function_name,
                        namespace="imp"
                    ),
                    location=File_Reference(
                        filename=filename,
                        line=line_counter,
                        column=column,
                    )
                )
                items.append(implementation)
            else:
                print(f"{line_counter} No!")
    return items


def main():
    items = get_items(filename="code.scala")
    with open("scala.lobster", "w", encoding="UTF-8") as fd:
        lobster_write(
            fd,
            kind=Implementation,
            generator="lobster_scala",
            items=items,
        )


def measure_runtime(fnc, *args, **kwargs):
    start_time = time.time()
    result = fnc(*args, **kwargs)
    runtime = int(time.time() - start_time)
    print(f"Done in {timedelta(seconds=runtime)}.")
    return result


if __name__ == '__main__':
    measure_runtime(main)
```
