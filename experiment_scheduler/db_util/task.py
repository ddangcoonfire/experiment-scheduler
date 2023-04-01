import sqlalchemy
from sqlalchemy import Column, String
from experiment_scheduler.db_util.connection import Base, engine
from experiment_scheduler.db_util.mixin import DbCommonMixin


class Task(Base, DbCommonMixin):
    """Task
    description : define Task object
    ERD Table (link TLDR:)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

    id = Column(String(100), primary_key=True)
    experiment_id = Column(String(100))
    task_manager_id = Column(String(100))
    name = Column(String(100))
    command = Column(String(100))
    status = Column(String(100))
    logfile_name = Column(String(100))


if not sqlalchemy.inspect(engine).has_table(Task.get_table_name()):
    Base.metadata.create_all(engine)
