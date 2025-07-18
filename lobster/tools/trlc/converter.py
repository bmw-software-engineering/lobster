from pathlib import Path
from typing import Iterable, List, Optional
from trlc import ast

from lobster.items import Item, Requirement, Tracing_Tag
from lobster.location import File_Reference
from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.conversion_rule_lookup import (
    build_record_type_to_conversion_rule_lookup,
)
from lobster.tools.trlc.errors import (
    TupleComponentError, TupleToStringFailedError, TupleToStringMissingError,
)
from lobster.tools.trlc.hierarchy_tree import build_children_lookup
from lobster.tools.trlc.item_wrapper import ItemWrapper
from lobster.tools.trlc.text_generation import build_text_from_instructions
from lobster.tools.trlc.to_string_rules import (
    ToStringRules, build_tuple_type_to_ruleset_map,
)


class Converter:
    def __init__(
            self,
            conversion_rules: Iterable[ConversionRule],
            to_string_rules: Iterable[ToStringRules],
            symbol_table: ast.Symbol_Table,
    ) -> None:
        self._conversion_rule_lookup = build_record_type_to_conversion_rule_lookup(
            conversion_rules=conversion_rules,
            children_lookup=build_children_lookup(symbol_table),
            symbol_table=symbol_table,
        )
        self._to_string_rules = build_tuple_type_to_ruleset_map(
            symbol_table=symbol_table,
            to_string_rule_sets=to_string_rules,
        )

    def lobster_norm_path(self, path: str) -> str:
        p = Path(path).resolve()
        p = p.relative_to(Path.cwd())
        return str(p)

    def generate_lobster_object(self, n_obj: ast.Record_Object) -> Optional[Item]:
        rule = self._conversion_rule_lookup.get(n_obj.n_typ)
        if not rule:
            return None

        item_tag = Tracing_Tag(
            namespace=rule.lobster_namespace,
            tag=n_obj.fully_qualified_name(),
            version=None,
        )

        item_loc = File_Reference(
            filename=self.lobster_norm_path(n_obj.location.file_name),
            line=n_obj.location.line_no,
            column=n_obj.location.col_no
        )

        item_wrapper = ItemWrapper(n_obj)
        item_text = self._get_description(item_wrapper, rule.description_fields)

        if rule.lobster_namespace != "req":
            raise NotImplementedError(
                f"Conversion for namespace '{rule.lobster_namespace}' not implemented."
            )
        rv = Requirement(
            tag=item_tag,
            location=item_loc,
            framework="TRLC",
            kind=n_obj.n_typ.name,
            name=n_obj.fully_qualified_name(),
            text=item_text
        )

        for tag_entry in rule.tags:
            field_value = item_wrapper.get_field(tag_entry.field)
            if field_value is None:
                continue
            raw_field = item_wrapper.get_field_raw(tag_entry.field)
            if isinstance(raw_field.typ, ast.Array_Type):
                for element in field_value:
                    text = str(element)
                    tag = Tracing_Tag.from_text(tag_entry.namespace, text)
                    rv.add_tracing_target(tag)
            elif isinstance(raw_field, ast.Tuple_Aggregate):
                text = self._tuple_value_as_string(raw_field)
                tag = Tracing_Tag.from_text(tag_entry.namespace, text)
                rv.add_tracing_target(tag)
            else:
                text = str(field_value)
                tag = Tracing_Tag.from_text(tag_entry.namespace, text)
                rv.add_tracing_target(tag)
        return rv

    def _tuple_value_as_string(self, tuple_aggregate: ast.Tuple_Aggregate):
        to_string_rules = self._to_string_rules.get(tuple_aggregate.typ)
        if not to_string_rules:
            raise TupleToStringMissingError(tuple_aggregate)

        # We have functions, so we attempt to apply until we get
        # one that works, in order.
        earlier_errors = []
        for instruction_list in to_string_rules.rules:
            try:
                return build_text_from_instructions(instruction_list, tuple_aggregate)
            except TupleComponentError as e:
                # If the instruction set is invalid, we skip to the next one.
                earlier_errors.append(e)
                continue
        # If we reach here, it means no instruction worked.
        # We raise an error to indicate that no valid instruction set was found.
        raise TupleToStringFailedError(tuple_aggregate, earlier_errors)

    @staticmethod
    def _get_description(
        item_data: ItemWrapper,
        description_fields: List[str],
    ) -> Optional[str]:
        if len(description_fields) == 1:
            return item_data.get_field(description_fields[0])
        elif len(description_fields) > 1:
            return "\n\n".join(
                f"{field}: {item_data.get_field(field)}"
                for field in description_fields if item_data.get_field(field)
            )
        return None
