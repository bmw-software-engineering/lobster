from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager
import sys
from lobster.items import Tracing_Tag, Requirement
from lobster.location import File_Reference
from lobster.io import lobster_write

trlc_file_path = "path of trlc files"
target_tool = "lobster_codebeamer"

mh = Message_Handler()
sm = Source_Manager(mh)

sm.register_directory(trlc_file_path)

symbols = sm.process()
if symbols is None:
    sys.exit(1)

items = []
for obj in symbols.iter_record_objects():
    data = obj.to_python_dict()

    if "UseCase" == obj.n_typ.name:
        for temp in obj.field["affected_tools"].value:
            if temp.value.name == target_tool:
                print("suraj",  temp.value.name)
                item_loc = File_Reference(filename = obj.location.file_name,
                                  line     = obj.location.line_no,
                                  column   = obj.location.col_no)
                item_tag = Tracing_Tag(namespace = "req",
                               tag       = obj.fully_qualified_name(),
                               version   = None)
                
                rv = Requirement(tag       = item_tag,
                                location  = item_loc,
                                framework = "TRLC",
                                kind      = obj.n_typ.name,
                                name      = obj.fully_qualified_name(),
                                text      = obj.field["description"].value)
                items.append(rv)

            
print(items)
with open("usecase.lobster", "w", encoding="UTF-8") as fd:
    lobster_write(fd=fd,
                    kind=Requirement,
                    generator="lobster-trlc",
                    items=items)
print("lobster-trlc: successfully wrote %u items to %s" %
        (len(items), "usecase.lobster"))
