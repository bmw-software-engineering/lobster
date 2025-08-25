from collections import defaultdict
import os.path


class FileTagGenerator:
    def __init__(self):
        self._basenames_to_lookup = defaultdict(dict)

    def get_tag(self, file_name: str) -> str:
        """Generates a unique tag for the given file based on its basename.
           The tag is in the format 'basename:index', where index is the
           number of times the basename has been encountered so far.
        """
        basename = os.path.basename(file_name)
        lookup = self._basenames_to_lookup[basename]
        return lookup.setdefault(file_name, f"{basename}:{len(lookup) + 1}")
