from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar

import pandas as pd

TableClass = TypeVar("TableClass")
BaseClass = TypeVar("BaseClass")


class Storage(ABC):
    """Interface which describes various functions to work with storage"""

    def __init__(self, config: str) -> None:
        self.config = config

    @abstractmethod
    def read_dataframe(self, table_name: str) -> Optional[pd.DataFrame]:
        """Gets the cached dataframe from storage if a table with the provided table name exists.

        Parameters
        ----------
        table_name: str
            Name of the table in database

        Returns
        -------
        Optional[pd.DataFrame]
            Returns cached dataframe if the table exists
        """

    @abstractmethod
    def write_dataframe(self, table_name: str, df_to_write: pd.DataFrame) -> None:
        """Writes dataframe to the storage

        Parameters
        ----------
        table_name: str
            Name of the table in database
        df_to_write: pd.DataFrame
            Dataframe to be written
        """

    @abstractmethod
    def get_mappings(
        self, table_cls: TableClass, criteria: Optional[List[TableClass]] = None, distinct: bool = False
    ) -> List[TableClass]:
        """Returns all mappings according to a criteria

        Function expects the same type of criteria as the table_cls, e.g. when table_cls is VerdictMapping
        the criteria is expected to be the list of VerdictMapping.

        Parameters
        ----------
        table_cls: TableClass
            Mapping class
        criteria: Optional[List[TableClass]]
            Criteria for this operation.
        distinct: bool
            Filters same data

        Returns
        -------
        result: List[TableClass]
            The cached mappings in the database according to the criteria.
        """

    @abstractmethod
    def update_mappings(self, table_cls: TableClass, updated_values: List[TableClass]) -> None:
        """Updates mappings with provided values

        Parameters
        ----------
        table_cls: TableClass
            Mapping class
        updated_values: List[TableClass]
            Values to be replaced
        """

    @abstractmethod
    def delete_mappings(self, table_cls: TableClass, criteria: Optional[List[Any]] = None) -> None:
        """Deletes mappings according to the criteria

        Function expects the same type of criteria as the table_cls, e.g. when table_cls is VerdictMapping
        the criteria is expected to be the list of VerdictMapping.

        Parameters
        ----------
        table_cls: TableClass
            Mapping class
        criteria: Optional[List[TableClass]]
            Criteria for this operation.
        """

    @abstractmethod
    def create_mappings(self, base: BaseClass) -> None:
        """Creates mappings

        Parameters
        ----------
        base: BaseClass
            Mapping class
        """
