from typing import Iterable, List, Optional
from trlc import ast

from lobster.common.items import Item, Requirement, Tracing_Tag
from lobster.common.location import File_Reference
from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.conversion_rule_lookup import (
    build_record_type_to_conversion_rule_lookup,
    get_record_types,
)
from lobster.tools.trlc.errors import (
    InvalidConversionRuleError,
    TupleComponentError,
    TupleToStringFailedError,
    TupleToStringMissingError,
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
        # check if any rule is left-over and could not be allocated to a record type
        orphan_rules = set(conversion_rules) - \
            set(self._conversion_rule_lookup.values())

        if orphan_rules:
            raise self._build_orphan_rules_exception(symbol_table, orphan_rules)
        self._to_string_rules = build_tuple_type_to_ruleset_map(
            symbol_table=symbol_table,
            to_string_rule_sets=to_string_rules,
        )

    def _build_orphan_rules_exception(
        self,
        symbol_table: ast.Symbol_Table,
        orphan_rules: Iterable[ConversionRule],
    ) -> InvalidConversionRuleError:
        orphan_rule_names = ", ".join(
            f"{rule.package_name}.{rule.type_name}" for rule in orphan_rules
        )
        available_type_names = ', '.join(
            record_type.fully_qualified_name()
            for record_type in get_record_types(symbol_table)
        )
        if available_type_names:
            available_types_message = (
                f"Detected record types are '{available_type_names}'."
            )
        else:
            available_types_message = (
                "The TRLC symbol table contains no record types at all."
            )
        if self._conversion_rule_lookup:
            successfully_mapped_types = ', '.join(
                f"{rule.package_name}.{rule.type_name}"
                for rule in set(self._conversion_rule_lookup.values())
            )
        else:
            successfully_mapped_types = "none"

        return InvalidConversionRuleError(
            f"The following conversion rules do not match any record type in "
            f"the TRLC symbol table: {orphan_rule_names}. {available_types_message} "
            f"The following conversion rules were successfully mapped to TRLC types: "
            f"{successfully_mapped_types}."
        )

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
            filename=n_obj.location.file_name,
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
            for field_str_value in self._generate_text(item_wrapper, tag_entry.field):
                tag = Tracing_Tag.from_text(tag_entry.namespace, field_str_value)
                rv.add_tracing_target(tag)
        for value_list, fields in (
            (rv.just_up, rule.justification_up_fields),
            (rv.just_down, rule.justification_down_fields),
            (rv.just_global, rule.justification_global_fields),
        ):
            for just_field in fields:
                value_list.extend(self._generate_text(item_wrapper, just_field))
        return rv

    def _generate_text(self, item_wrapper: ItemWrapper, field_name: str) -> List[str]:
        """Generates a list of texts for the values in the given field

           The function always returns a list of strings, even if the field is a
           single-value field.
        """
        field_value = item_wrapper.get_field(field_name)
        if field_value is None:
            return []
        raw_field = item_wrapper.get_field_raw(field_name)
        if isinstance(raw_field.typ, ast.Array_Type):
            texts = []
            for element in raw_field.value:
                if isinstance(element, ast.Tuple_Aggregate):
                    texts.append(self._tuple_value_as_string(element))
                elif isinstance(element, ast.Record_Reference):
                    texts.append(element.target.fully_qualified_name())
                else:
                    texts.append(str(element.to_python_object()))
            return texts
        elif isinstance(raw_field, ast.Tuple_Aggregate):
            return [self._tuple_value_as_string(raw_field)]
        return [str(field_value)]

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

    def _get_description(
        self,
        item_wrapper: ItemWrapper,
        description_fields: List[str],
    ) -> str:
        """Generates a description text for the LOBSTER item.

           The text of a LOBSTER item is always a single string, not a list of strings,
           even if there are multiple description fields to consider.

           This string uses a different format depending on the number of description
           fields:
           - If there is only one description field, it returns the text of that field.
           - If there are multiple description fields, it formats them as "field: text"
             pairs and joins them with two newlines.

           If a field is a Array_Type, then all individual values are joined
           with a comma.

           If a field is a Tuple_Aggregate, it is converted to a string using the
           `self._tuple_value_as_string` method.
        """
        def join_field_str_values(texts: Iterable[str]) -> str:
            return ', '.join(texts)

        # if there is only one description field, then return it directly
        if len(description_fields) == 1:
            return join_field_str_values(
                self._generate_text(item_wrapper, description_fields[0]),
            )

        # if there are multiple description fields (or zero), then format them
        field_text_map = {}
        for field in description_fields:
            text = join_field_str_values(self._generate_text(item_wrapper, field))
            if text:
                field_text_map[field] = text

        return "\n\n".join(
            f"{field}: {text}"
            for field, text in field_text_map.items()
        )
