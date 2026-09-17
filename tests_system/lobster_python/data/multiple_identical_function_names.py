# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

flag = False
requirements_global = None

if flag:
    def get_requirements(requirements):
        return requirements
else:
    def set_requirements(requirements):
        requirements_global = requirements
        return requirements_global


def get_requirements(requirements):
    return requirements


def display_requirements():
    print(get_requirements())


def set_requirements(requirements):
    requirements_global = requirements
    return requirements_global


def get_requirements(requirements):
    return requirements
