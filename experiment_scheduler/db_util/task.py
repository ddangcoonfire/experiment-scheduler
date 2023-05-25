"""
Task class defined in yaml file
"""

import sqlalchemy
from sqlalchemy import Column, String, Integer, JSON
from experiment_scheduler.db_util.connection import Base, engine
from experiment_scheduler.db_util.mixin import DbCommonMixin


class Task(Base, DbCommonMixin):
    """Task
    description : define Task object
    ERD Table (link TLDR:)
    """

    __tablename__ = "task"

    id = Column(String(100), primary_key=True)
    experiment_id = Column(String(100))
    task_manager_id = Column(String(100))
    name = Column(String(100))
    command = Column(String(100))
    status = Column(Integer)
    task_env = Column(JSON)
    logfile_name = Column(String(100))
    cwd = Column(String(100))
    num_retry = Column(Integer)


if not sqlalchemy.inspect(engine).has_table(Task.get_table_name()):
    Base.metadata.create_all(engine)
