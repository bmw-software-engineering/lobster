#!/usr/bin/env python3
#
# lobster_python - Extract Python tracing tags for LOBSTER
# Copyright (C) 2022-2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from argparse import Namespace
import sys
import os.path
import multiprocessing
import functools
import re

from libcst.metadata import PositionProvider
import libcst as cst

from lobster.items import Tracing_Tag, Implementation, Activity
from lobster.location import File_Reference
from lobster.io import lobster_write
from lobster.meta_data_tool_base import MetaDataToolBase

LOBSTER_TRACE_PREFIX = "# lobster-trace: "
LOBSTER_JUST_PREFIX = "# lobster-exclude: "
func_name = []


def count_occurrence_of_last_function_from_function_name_list(function_names):
    """
    Returns the last function and class name (if present) in a list along with
    the count of its previous occurrences.

    The function identifies the last entry in the `function_names` list, extracts
    the function and class names (if applicable), and counts prior occurrences of
    the same function.
    The result is formatted as `module.class.function-count` or `module.function-count`.

    Args:
        function_names (list):
            List of strings formatted as `module.class.function:line_number`
            or `module.function:line_number`.

    Returns:
        str: The last function (and class if applicable) with its occurrence count,
             formatted as `module.class.function-count` or `module.function-count`.

    Examples:
        function_names = ['hello.add:2', 'hello.sub:5', 'hello.add:8']
        returns: 'hello.add-2'
        class_function_names = ['Example.hello.add:2', 'Example.hello.sub:5',]
        returns: 'Example.hello.add-2'
    """
    function_and_file_name = re.split(r"[.:]", function_names[-1])
    class_name_with_module = function_names[-1].split(':', 1)[0].split(".")

    if len(class_name_with_module) == 3:
        function_and_file_name[1] = (class_name_with_module[1] + '.' +
                                     class_name_with_module[2])

    filename = function_and_file_name[0]
    last_function = function_and_file_name[1]
    count = 0
    for element in range(0, len(function_names) - 1):
        class_name_with_function = function_names[element].split(':', 1)[0].split(".")
        if len(class_name_with_function) == 3:
            if last_function == (class_name_with_function[1] + '.' +
                                 class_name_with_function[2]):
                count += 1
        if re.split(r"[.:]", function_names[element])[1] == last_function:
            count += 1
    function_name = (filename + "." + last_function +
                     ("-" + str(count) if count > 0 else ''))

    return function_name


def parse_value(val):
    if isinstance(val, cst.SimpleString):
        return val.value[1:-1]
    elif isinstance(val, cst.List):
        return [parse_value(item.value)
                for item in val.elements]
    else:
        rv = str(val.value)
        if rv == "None":
            rv = None
        return rv


class Python_Traceable_Node:
    def __init__(self, location, name, kind):
        assert isinstance(location, File_Reference)
        assert isinstance(name, str)
        assert isinstance(kind, str)
        self.location = location
        self.name     = name
        self.kind     = kind
        self.parent   = None
        self.children = []
        self.tags     = []
        self.just     = []

    def register_tag(self, tag):
        assert isinstance(tag, Tracing_Tag)
        self.tags.append(tag)

    def register_justification(self, justification):
        assert isinstance(justification, str)
        self.just.append(justification)

    def set_parent(self, node):
        assert isinstance(node, Python_Traceable_Node)
        node.children.append(self)
        self.parent = node

    def to_json(self):
        return {"kind"     : self.kind,
                "name"     : self.name,
                "tags"     : [x.to_json() for x in self.tags],
                "just"     : self.just,
                "children" : [x.to_json() for x in self.children]}

    def to_lobster(self, schema, items):
        assert schema is Implementation or schema is Activity
        assert isinstance(items, list)
        assert False

    def fqn(self):
        if self.parent:
            rv = self.parent.fqn() + "."
        else:
            rv = ""
        if self.location.line is not None and \
          isinstance(self, Python_Function):
            rv += f"{self.name}:{str(self.location.line)}"
        else:
            rv += self.name
        return rv

    def lobster_tag(self):
        return Tracing_Tag("python", self.fqn())

    def warn_ignored(self, reason):
        for tag in self.tags:
            print("%s: warning: ignored tag %s because "
                  "%s already has annotations" %
                  (self.location.to_string(),
                   tag,
                   reason))
        for just in self.just:
            print("%s: warning: ignored justification '%s' because "
                  "%s already has annotations" %
                  (self.location.to_string(),
                   just,
                   reason))


class Python_Module(Python_Traceable_Node):
    def __init__(self, location, name):
        super().__init__(location, name, "Module")

    def to_lobster(self, schema, items):
        assert schema is Implementation or schema is Activity
        assert isinstance(items, list)
        for node in self.children:
            node.to_lobster(schema, items)


class Python_Class(Python_Traceable_Node):
    def __init__(self, location, name):
        super().__init__(location, name, "Class")

    def to_lobster(self, schema, items):
        assert schema is Implementation or schema is Activity
        assert isinstance(items, list)
        # Classes are dealt with a bit differently. If you add a tag
        # or justification to a class, then children are ignored, and
        # we trace to the class.
        #
        # Alternatively, can leave out the tag and instead trace to
        # each child.

        # First get child items
        class_contents = []
        for node in self.children:
            node.to_lobster(schema, class_contents)

        # If we're extracting pyunit/unittest items, then we always ignore
        # classes, but we do add our tags to all the tests.
        if schema is Activity:
            for item in class_contents:
                for tag in self.tags:
                    item.add_tracing_target(tag)
            items += class_contents
            return

        l_item = Implementation(tag      = Tracing_Tag("python",
                                                       self.fqn()),
                                location = self.location,
                                language = "Python",
                                kind     = self.kind,
                                name     = self.fqn())

        # If we have tags or justifications on the class itself, we
        # give precedence to that.
        if self.tags or self.just:
            for tag in self.tags:
                l_item.add_tracing_target(tag)
            l_item.just_up += self.just

            for c_item in self.children:
                c_item.warn_ignored(self.name)

            items.append(l_item)
            return

        # Otherwise, we ignore the class and instead trace to each
        # child
        items += class_contents


class Python_Function(Python_Traceable_Node):
    def __init__(self, location, name):
        super().__init__(location, name, "Function")

    def set_parent(self, node):
        assert isinstance(node, Python_Traceable_Node)
        node.children.append(self)
        self.parent = node
        if isinstance(node, Python_Class):
            if self.name == "__init__":
                self.kind = "Constructor"
            else:
                self.kind = "Method"

    def to_lobster(self, schema, items):
        assert schema is Implementation or schema is Activity
        assert isinstance(items, list)

        func_name.append(self.fqn())
        tagname = count_occurrence_of_last_function_from_function_name_list(
            func_name
        )
        pattern = r"[-]"
        val = re.split(pattern, tagname)
        name_value = val[0]

        if schema is Implementation:
            l_item = Implementation(tag      = Tracing_Tag("python",
                                                           tagname),
                                    location = self.location,
                                    language = "Python",
                                    kind     = self.kind,
                                    name     = name_value)
        elif self.name.startswith("test") or self.name.startswith("_test") \
                or self.name.endswith("test"):
            l_item = Activity(tag = Tracing_Tag("pyunit",
                                                self.fqn()),
                              location  = self.location,
                              framework = "PyUnit",
                              kind      = "Test")
        else:
            return

        for tag in self.tags:
            l_item.add_tracing_target(tag)
        l_item.just_up += self.just

        # Any children of functions are not testable units. Their
        # tracing tags contribute to ours, but otherwise they don't
        # appear.
        nested_items = []
        for node in self.children:
            node.to_lobster(schema, nested_items)
        for item in nested_items:
            # TODO: Warn about useless nested justifications
            # Merge tracing tags
            for tag in item.unresolved_references:
                l_item.add_tracing_target(tag)

        items.append(l_item)


class Lobster_Visitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, file_name, options):
        super().__init__()
        assert os.path.isfile(file_name)
        self.file_name = file_name

        self.module = Python_Module(
            File_Reference(file_name),
            os.path.basename(file_name).replace(".py", ""))

        self.activity     = options["activity"]
        self.current_node = None
        self.stack        = [self.module]

        self.namespace        = options["namespace"]
        self.exclude_untagged = options["exclude_untagged"]

        self.decorator_name   = options["decorator"]
        self.dec_arg_name     = options["dec_arg_name"]
        self.dec_arg_version  = options["dec_arg_version"]

    def parse_dotted_name(self, name):
        if isinstance(name, cst.Call):
            return self.parse_dotted_name(name.func)
        elif isinstance(name, cst.Name):
            return name.value
        elif isinstance(name, cst.Attribute):
            # value -- prefix
            # attr  -- postfix
            return "%s.%s" % (self.parse_dotted_name(name.value),
                              self.parse_dotted_name(name.attr))
        else:
            return None

    def parse_decorators(self, decorators):
        for dec in decorators:
            dec_name = self.parse_dotted_name(dec.decorator)
            if dec_name is None:
                continue
            if dec_name != self.decorator_name:
                continue
            dec_args = {arg.keyword.value: parse_value(arg.value)
                        for arg in dec.decorator.args}

            # TODO: Better error messages if these assumptions are
            # violated
            assert self.dec_arg_name in dec_args
            if self.dec_arg_version:
                assert self.dec_arg_version in dec_args
                tag = Tracing_Tag(self.namespace,
                                  dec_args[self.dec_arg_name],
                                  dec_args.get(self.dec_arg_version, None))
                self.current_node.register_tag(tag)

            elif isinstance(dec_args[self.dec_arg_name], list):
                for item in dec_args[self.dec_arg_name]:
                    tag = Tracing_Tag(self.namespace, item)
                self.current_node.register_tag(tag)

            else:
                tag = Tracing_Tag(self.namespace,
                                  dec_args[self.dec_arg_name])
                self.current_node.register_tag(tag)

    def visit_ClassDef(self, node):
        line = self.get_metadata(PositionProvider, node).start.line
        loc = File_Reference(self.file_name, line)
        t_item = Python_Class(loc, node.name.value)
        t_item.set_parent(self.stack[-1])
        self.stack.append(t_item)
        self.current_node = t_item
        self.parse_decorators(node.decorators)

    def visit_FunctionDef(self, node):
        line = self.get_metadata(PositionProvider, node).start.line
        loc = File_Reference(self.file_name, line)
        t_item = Python_Function(loc, node.name.value)
        t_item.set_parent(self.stack[-1])
        self.stack.append(t_item)
        self.current_node = t_item
        self.parse_decorators(node.decorators)

    def leave_FunctionDef(self, original_node):
        self.stack.pop()
        self.current_node = self.stack[-1]

    def leave_ClassDef(self, original_node):
        self.stack.pop()
        self.current_node = self.stack[-1]

    def visit_Comment(self, node):
        line = self.get_metadata(PositionProvider, node).start.line
        # For some reason the comment in a class is associated with
        # its constructor. We can check if it preceeds it (by line),
        # and so associate it with the enclosing item.
        if self.current_node and \
           self.current_node.location.line and \
           self.current_node.location.line > line:
            actual = self.current_node.parent
        else:
            actual = self.current_node

        if node.value.startswith(LOBSTER_TRACE_PREFIX):
            tag = node.value[len(LOBSTER_TRACE_PREFIX):].strip()
            actual.register_tag(
                Tracing_Tag.from_text(self.namespace,
                                      tag))

        elif node.value.startswith(LOBSTER_JUST_PREFIX):
            reason = node.value[len(LOBSTER_JUST_PREFIX):].strip()
            actual.register_justification(reason)


def process_file(file_name, options):
    # pylint: disable=protected-access
    assert isinstance(file_name, str)
    assert isinstance(options, dict)

    items = []
    try:
        with open(file_name, "r", encoding="UTF-8") as fd:
            ast = cst.parse_module(fd.read())

        ast = cst.MetadataWrapper(ast)
        visitor = Lobster_Visitor(file_name, options)
        ast.visit(visitor)

        if options["activity"]:
            visitor.module.to_lobster(Activity, items)
        else:
            visitor.module.to_lobster(Implementation, items)

        if options["exclude_untagged"]:
            items = [item for item in items if item.unresolved_references]

        return True, items

    except cst._exceptions.ParserSyntaxError as exc:
        print(file_name, exc.message)
        return False, []

    except UnicodeDecodeError as exc:
        print(file_name, str(exc))
        return False, []

    except Exception as exc:
        print("Unspecified issue in file: %s" % file_name)
        raise


class PythonTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="python",
            description="Extract tracing tags from Python code or tests",
            official=True,
        )
        ap = self._argument_parser
        ap.add_argument("files",
                        nargs="+",
                        metavar="FILE|DIR")
        ap.add_argument("--activity",
                        action="store_true",
                        default=False,
                        help=("generate activity traces (tests) instead of"
                              " an implementation trace"))
        ap.add_argument("--out",
                        default=None)
        ap.add_argument("--single",
                        action="store_true",
                        default=False,
                        help="don't multi-thread")
        ap.add_argument("--only-tagged-functions",
                        default=False,
                        action="store_true",
                        help="only trace functions with tags")
        grp = ap.add_mutually_exclusive_group()
        grp.add_argument("--parse-decorator",
                         nargs=2,
                         metavar=("DECORATOR", "NAME_ARG"),
                         default=(None, None))
        grp.add_argument("--parse-versioned-decorator",
                         nargs=3,
                         metavar=("DECORATOR", "NAME_ARG", "VERSION_ARG"),
                         default=(None, None, None))

    def _run_impl(self, options: Namespace) -> int:
        file_list = []
        for item in options.files:
            if os.path.isfile(item):
                file_list.append(item)
            elif os.path.isdir(item):
                for path, _, files in os.walk(item):
                    for filename in files:
                        _, ext = os.path.splitext(filename)
                        if ext == ".py":
                            file_list.append(os.path.join(path, filename))
            else:
                self._argument_parser.error(f"{item} is not a file or directory")

        context = {
            "activity"         : options.activity,
            "decorator"        : None,
            "dec_arg_name"     : None,
            "dec_arg_version"  : None,
            "exclude_untagged" : options.only_tagged_functions,
            "namespace"        : "req",
        }

        if options.parse_decorator[0] is not None:
            context["decorator"]    = options.parse_decorator[0]
            context["dec_arg_name"] = options.parse_decorator[1]
        elif options.parse_versioned_decorator[0] is not None:
            context["decorator"]       = options.parse_versioned_decorator[0]
            context["dec_arg_name"]    = options.parse_versioned_decorator[1]
            context["dec_arg_version"] = options.parse_versioned_decorator[2]

        pfun = functools.partial(process_file, options=context)
        items = []
        ok    = True

        if options.single:
            for file_name in file_list:
                new_ok, new_items = pfun(file_name)
                ok    &= new_ok
                items += new_items
        else:
            with multiprocessing.Pool() as pool:
                for new_ok, new_items in pool.imap_unordered(pfun, file_list):
                    ok    &= new_ok
                    items += new_items

        if options.activity:
            schema = Activity
        else:
            schema = Implementation

        if options.out:
            with open(options.out, "w", encoding="UTF-8") as fd:
                lobster_write(fd, schema, "lobster_python", items)
            print(f"Written output for {len(items)} items to {options.out}")
        else:
            lobster_write(sys.stdout, schema, "lobster_python", items)
            print()

        if ok:
            return 0
        else:
            print("Note: Earlier parse errors make actual output unreliable")
            return 1


def main() -> int:
    return PythonTool().run()
