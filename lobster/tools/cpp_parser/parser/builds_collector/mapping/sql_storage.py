import contextlib
import json
from typing import Any, List, Optional

import pandas as pd
import requests
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.test_status import (
    TestStatus,
)

from .storage import BaseClass, Storage, TableClass


class SqlStorage(Storage):
    """This class is used to manipulate database storage actions"""

    def __init__(self, config: str) -> None:
        super().__init__(config)
        self.engine = create_engine(config)
        self.dbsession = sessionmaker(bind=self.engine, expire_on_commit=False)

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
        if inspect(self.engine).has_table(table_name):
            df_narrow_cached = pd.read_sql(table_name, self.engine, index_col="index")
            df_narrow_cached["test_status"] = df_narrow_cached["test_status"].apply(lambda x: TestStatus[x])
            df_narrow_cached["error_log"] = df_narrow_cached["error_log"].apply(json.loads)
            return df_narrow_cached
        return None

    def write_dataframe(self, table_name: str, df_to_write: pd.DataFrame) -> None:
        """Writes dataframe to the storage

        Parameters
        ----------
        table_name: str
            Name of the table in database
        df_to_write: pd.DataFrame
            Dataframe to be written
        """
        df_sql = df_to_write.copy()
        df_sql["test_status"] = df_sql["test_status"].apply(lambda x: x.name)
        df_sql["error_log"] = df_sql["error_log"].apply(json.dumps)
        df_sql.to_sql(table_name, self.engine, if_exists="replace")

    def get_mappings(self, table_cls: TableClass, criteria: Optional[List[TableClass]] = None) -> List[TableClass]:
        """Returns all mappings according to a criteria

        Function expects the same type of criteria as the table_cls, e.g. when table_cls is VerdictMapping
        the criteria is expected to be the list of VerdictMapping.

        Parameters
        ----------
        table_cls: TableClass
            Mapping class
        criteria: Optional[List[TableClass]]
            Criteria for this operation.

        Returns
        -------
        result: List[TableClass]
            The cached mappings in the database according to the criteria.
        """
        if not criteria:
            criteria = []
        with self.create_session() as session:
            query = session.query(table_cls).filter(*criteria)
            result = query.all()
        return result

    def update_mappings(self, table_cls: TableClass, updated_values: List[TableClass]) -> None:
        """Updates mappings with provided values

        Parameters
        ----------
        table_cls: TableClass
            Mapping class
        updated_values: List[TableClass]
            Values to be replaced
        """
        with self.create_session() as session:
            session.query(table_cls)
            for value in updated_values:
                session.merge(value)

    def delete_mappings(self, table_cls: TableClass, criteria: Optional[List[TableClass]] = None) -> None:
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
        if not criteria:
            criteria = []
        with self.create_session() as session:
            session.query(table_cls).filter(*criteria).delete()

    def create_mappings(self, base: BaseClass) -> None:
        """Creates mappings

        Parameters
        ----------
        base: BaseClass
            Mapping class
        """
        base.metadata.create_all(self.engine)

    @contextlib.contextmanager
    def create_session(self) -> Optional[requests.Session]:
        """Creates mappings

        Raises
        ------
        Exception
            If session couldn't commit, i.e. commit is invalid.
            The session is guaranteed to be in a valid state, i.e., the commit completed fully, or the session is rolled back.

        Returns
        -------
        result: Optional[TableClass]
            Database session instance
        """
        session = self.dbsession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
