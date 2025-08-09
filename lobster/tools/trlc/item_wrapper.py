from typing import Any
from trlc import ast
from lobster.tools.trlc.errors import RecordObjectComponentError


class ItemWrapper:
    def __init__(self, n_obj: ast.Record_Object):
        self._n_obj = n_obj
        self._item_data = n_obj.to_python_dict()

    @property
    def n_obj(self) -> ast.Record_Object:
        return self._n_obj

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
