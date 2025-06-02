from os.path import abspath
from lobster.file_tag_generator import FileTagGenerator
from lobster.items import Tracing_Tag
from lobster.location import File_Reference


class TagLocationGenerator:
    """
    A specialized file tag generator for C/C++ files.
    It generates Tracing_Tag and File_Reference objects based on the file name and line
    number.
    """
    def __init__(self) -> None:
        self._generator = FileTagGenerator()

    def get_tag(self, file: str, function_name: str, line_nr: int) -> Tracing_Tag:
        """
        Generate a unique tag for the given file.
        """
        file_tag = self._generator.get_tag(file)
        function_uid = f"{file_tag}:{function_name}:{line_nr}"
        return Tracing_Tag("cpp", function_uid)

    @staticmethod
    def get_location(file: str, line_nr: int) -> File_Reference:
        """
        Generate a location object for the file using its absolute path.
        """
        return File_Reference(abspath(file), line_nr)
