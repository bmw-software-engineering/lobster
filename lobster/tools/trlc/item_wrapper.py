# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from typing import Any
from trlc import ast
from lobster.tools.trlc.errors import RecordObjectComponentError


class ItemWrapper:
    def __init__(self, n_obj: ast.Record_Object):
        self._n_obj = n_obj
        self._item_data = n_obj.to_python_dict()

    def get_field(self, field_name: str) -> Any:
        try:
            return self._item_data[field_name]
        except KeyError as ex:
            raise RecordObjectComponentError(field_name, self._n_obj) from ex

    def get_field_raw(self, field_name: str) -> Any:
        """Returns the raw TRLC representation of the field."""
        try:
            return self._n_obj.field[field_name]
        except KeyError as ex:
            raise RecordObjectComponentError(field_name, self._n_obj) from ex

    def get_field_value_or_none(self, field_name: str) -> Any:
        if field := self._n_obj.field.get(field_name, None):
            return field.to_python_object()
        return None
