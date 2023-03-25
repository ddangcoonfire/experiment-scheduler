import sqlalchemy
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine
from experiment_scheduler.db_util.mixin import TableConfigurationMixin

table_name = "task_manager"


class TaskManager(Base, TableConfigurationMixin):
    """TaskManger
    description : define TaskManger object
    ERD Table (link TLDR;)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

    address = Column(String(100))
    default_log_file_path = Column(String(100))
    spec = Column(JSON)


if not sqlalchemy.inspect(engine).has_table(table_name):
    Base.metadata.create_all(engine)
