"""
TaskManager class is ORM class of TaskManager
TaskManager class is to manage task_manager's metadata
"""

import sqlalchemy
from sqlalchemy import Column, String, JSON, Integer
from experiment_scheduler.db_util.connection import Base, engine
from experiment_scheduler.db_util.mixin import DbCommonMixin


class TaskManager(Base, DbCommonMixin):
    """TaskManger
    description : define TaskManger object
    ERD Table (link TLDR;)
    """

    __tablename__ = "task_manager"

    id = Column(String(100), primary_key=True)
    address = Column(String(100))
    log_file_path = Column(String(100), server_default="./log/")
    status = Column(Integer)
    spec = Column(JSON)


if not sqlalchemy.inspect(engine).has_table(TaskManager.get_table_name()):
    Base.metadata.create_all(engine)
