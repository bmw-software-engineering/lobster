from os.path import abspath
from typing import Dict, Match
from lobster.file_tag_generator import FileTagGenerator
from lobster.items import Implementation, Tracing_Tag
from lobster.location import File_Reference


class ImplementationBuilder:
    """
    A specialized file tag generator for C/C++ files.
    It generates Tracing_Tag and File_Reference objects based on the file name and line
    number.
    """

    MIN_NUM_GROUPS = 4
    REASON_GROUP_NUM = MIN_NUM_GROUPS + 1
    REFERENCE_GROUP_NUM = MIN_NUM_GROUPS + 1

    def __init__(self) -> None:
        self._generator = FileTagGenerator()

    def from_match_if_new(
            self,
            db: Dict[str, Implementation],
            match: Match,
    ) -> Implementation:
        """
        Builds and insert a new Implementation object into the database if it does not
        already exist.
        Otherwise, it returns the existing Implementation object.
        """
        impl = self.from_match(match)
        return db.setdefault(impl.tag.key(), impl)

    def from_match(self, match: Match) -> Implementation:
        """
        Generate an Implementation object from a regex match object.
        """
        filename, line_nr, kind, function_name, *_ = match.groups()
        try:
            line_nr = int(line_nr)
        except ValueError as exc:
            raise ValueError(f"Invalid line number '{line_nr}' "
                             f"in regex group '{match.group(2)}'!") from exc

        return Implementation(
            tag = self._get_tag(filename, function_name, line_nr),
            location = self._get_location(filename, line_nr),
            language = "C/C++",
            kind = kind,
            name = function_name,
        )

    def _get_tag(self, file: str, function_name: str, line_nr: int) -> Tracing_Tag:
        """
        Generate a unique tag for the given file.
        """
        file_tag = self._generator.get_tag(file)
        function_uid = f"{file_tag}:{function_name}:{line_nr}"
        return Tracing_Tag("cpp", function_uid)

    @staticmethod
    def _get_location(file: str, line_nr: int) -> File_Reference:
        """
        Generate a location object for the file using its absolute path.
        """
        return File_Reference(abspath(file), line_nr)
