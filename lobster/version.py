#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import argparse
import sys
from argparse import ArgumentParser

VERSION_TUPLE = (0, 9, 19)
VERSION_SUFFIX = "dev"

LOBSTER_VERSION = ("%u.%u.%u" % VERSION_TUPLE) + (
    "-%s" % VERSION_SUFFIX if VERSION_SUFFIX else ""
)

FULL_NAME = "LOBSTER %s" % LOBSTER_VERSION


# def get_version(func):
#     # all_objects = ap.get_class_objects()
#     # for obj in all_objects:
#     #     obj.print_value()
#     # ap.g_common.add_argument("-v, --version", action="store_true",
#     #                 default=None,
#     #                 help="Get version for the tool")
#     def version():
#         print("Hello")
#         if sys.argv[1] == "--version" or sys.argv[1] == "-v":
#             print(FULL_NAME)
#             return sys.exit(0)
#         else:
#             func()
#         # def execution(func):
#         #     print("YELO")
#         #     print(sys.argv[1])
#         #     if sys.argv[1] == "--version" or sys.argv[1] == "-v":
#         #         print(FULL_NAME)
#         #         return sys.exit(0)
#         #     else:
#         #         func()
#     return version


def get_version(ap):
    # all_objects = ap.get_class_objects()
    # for obj in all_objects:
    #     obj.print_value()
    # print(ap)
    # print(ap.__dict__)
    print("TYPE OF AP ", type(ap))
    if type(ap) == ArgumentParser:
        ap.add_argument("-v, --version", action="store_true",
                        default=None,
                        help="Get version for the tool")
        print(type(ap))
        def version(func):
            def execution():
                print("YELO")
                print(sys.argv[1])
                if sys.argv[1] == "--version" or sys.argv[1] == "-v":
                    print(FULL_NAME)
                    return sys.exit(0)
                else:
                    return func()
            return execution
        return version
    else:
        print("AP TYPE " , type(ap))
        def version(func):
            print("Function TYPE ", type(func))
            print(func)
            if type(ap) != ArgumentParser:
                func.ap.add_argument("-v, --version", action="store_true",
                            default=None,
                            help="Get version for the tool")
                if sys.argv[1] == "--version" or sys.argv[1] == "-v":
                    return sys.exit(0)
            return ap(func)
        return version