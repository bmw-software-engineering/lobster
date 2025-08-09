
from abc import abstractmethod
import argparse
from functools import partial
import multiprocessing
import sys
from typing import Sequence, Tuple, Union
from yaml import YAMLError
from lobster.items import Activity, Implementation, Requirement
from lobster.tool2 import LOBSTER_Tool2
from lobster.tool2_config import Config


class LOBSTER_Per_File_Tool2(LOBSTER_Tool2):
    def __init__(self, name, description, extensions, official=False):
        super().__init__(name, description, extensions, official)

    @classmethod
    @abstractmethod
    def _process(
            cls,
            options: Config,
            file_name,
    ) -> Tuple[bool, Sequence[Union[Activity, Implementation, Requirement]]]:
        pass

    @abstractmethod
    def _load_config(self, config_file: str) -> Config:
        """Load the configuration from a YAML file."""

    def _run_impl(self, options: argparse.Namespace) -> int:
        try:
            return self._execute(options)
        except (FileNotFoundError, PermissionError) as e:
            print(f"File access error: {e}", file=sys.stderr)
            return 1
        except YAMLError as e:
            print(f"Configuration error: {e}", file=sys.stderr)
            return 1
        except (UnicodeDecodeError, SyntaxError) as e:
            print(f"File parsing error: {e}", file=sys.stderr)
            return 1
        except (OSError, RuntimeError) as e:
            print(f"System error: {e}", file=sys.stderr)
            return 1

        return 1

    def _execute(self, options: argparse.Namespace) -> int:
        config = self._load_config(options.config)
        work_list = self._create_worklist(config)

        ok = True
        items = []
        pfun = partial(self._process, config)

        if options.single:
            for file_name in work_list:
                new_ok, new_items = pfun(file_name)
                ok &= new_ok
                items += new_items
        else:
            with multiprocessing.Pool() as pool:
                for new_ok, new_items in pool.imap(pfun, work_list, 4):
                    ok &= new_ok
                    items += new_items
                pool.close()
                pool.join()

        if ok:
            self._write_output(config.schema, options.out, items)
        else:
            print(f"{self.name}: aborting due to earlier errors")

        return int(not ok)
