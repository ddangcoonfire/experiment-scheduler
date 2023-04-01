import sqlalchemy
from sqlalchemy import Column, String, JSON
from experiment_scheduler.db_util.connection import Base, engine
from experiment_scheduler.db_util.mixin import DbCommonMixin


class TaskManager(Base, DbCommonMixin):
    """TaskManger
    description : define TaskManger object
    ERD Table (link TLDR;)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

    id = Column(String(100), primary_key=True)
    address = Column(String(100))
    default_log_file_path = Column(String(100))
    spec = Column(JSON)


if not sqlalchemy.inspect(engine).has_table(TaskManager.get_table_name()):
    Base.metadata.create_all(engine)
