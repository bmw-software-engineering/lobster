import argparse
from typing import List
import sys
from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager
from lobster.items import Tracing_Tag, Requirement
from lobster.location import File_Reference
from lobster.io import lobster_write

TRLC_TYPE = "UseCase"
USECASE_FIELD_AFFECTED_TOOLS = "affected_tools"
USECASE_FIELD_DESCRIPTION = "description"


def parse_args():
    ap = argparse.ArgumentParser(conflict_handler='resolve')

    ap.add_argument("--target",
                    help="Tool name to filter use cases",
                    type=str,
                    required=True)

    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--out",
                    help="Output file name",
                    type=str)

    return ap.parse_args()

def register_files(options: argparse.Namespace, sm: Source_Manager):
    for file in options.files:
        if not sm.register_file(file):
            print("Error: %s" % sm.mh.get_error_message())
            sys.exit(1)


def generate_items(symbols, target: str) -> List[Requirement]:
    items = []
    for obj in symbols.iter_record_objects():
        if TRLC_TYPE == obj.n_typ.name:
            for temp in obj.field[USECASE_FIELD_AFFECTED_TOOLS].value:
                if temp.value.name == target:
                    item_loc = File_Reference(filename = obj.location.file_name,
                                    line     = obj.location.line_no,
                                    column   = obj.location.col_no)
                    item_tag = Tracing_Tag(namespace = "req",
                                tag       = obj.fully_qualified_name(),
                                version   = None)

                    rv = Requirement(
                        tag=item_tag,
                        location=item_loc,
                        framework="TRLC",
                        kind=obj.n_typ.name,
                        name=obj.fully_qualified_name(),
                        text=obj.field[USECASE_FIELD_DESCRIPTION].value
                    )
                    items.append(rv)
    return items

def generate_lobster_file(items: List[Requirement], out: str):
    with open(out, "w", encoding="UTF-8") as fd:
        lobster_write(fd=fd,
                        kind=Requirement,
                        generator="usecase-extractor",
                        items=items)
    print(f"usecase-extractor: successfully wrote {len(items)} usecases to {out}")

def main():
    options = parse_args()
    print(f"Running usecases extraction tool for target: {options.target}")
    mh = Message_Handler()
    sm = Source_Manager(mh)
    register_files(options, sm)
    symbols = sm.process()
    if symbols is None:
        sys.exit(1)
    items = generate_items(symbols, options.target)
    generate_lobster_file(items, options.out)

if __name__ == "__main__":
    main()
