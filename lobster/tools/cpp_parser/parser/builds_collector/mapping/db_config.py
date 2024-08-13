from sqlalchemy import Column, DateTime, PrimaryKeyConstraint, String
from sqlalchemy.ext.declarative import declarative_base
from typing_extensions import TypeAlias

from .sql_storage import SqlStorage
from .storage import Storage

BASE: TypeAlias = declarative_base()


class BuildMetadataMapping(BASE):
    """This class is used to elaborate database 'builds' table

    Cooperate with BuildMetadata class to do various actions, e.g. get_mapping
    """

    __tablename__ = "builds"
    __table_args__ = (PrimaryKeyConstraint("uuid", "branch", "job_name"),)
    uuid = Column(String)
    job_name = Column(String)
    branch = Column(String)
    pr_url = Column(String)
    start_time = Column(DateTime)
    githash = Column(String)
    ci_result = Column(String)


def create_storage(database_url: str) -> Storage:
    """Creates database tables

    Parameters
    ----------
    database_url: str
        URL to the database server

    Returns
    -------
    Storage
        Returns storage instance
    """
    storage: Storage = SqlStorage(database_url)
    storage.create_mappings(BASE)
    return storage
