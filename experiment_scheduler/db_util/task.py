import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine
from experiment_scheduler.db_util.mixin import TableConfigurationMixin

table_name = "task"

class Task(Base, TableConfigurationMixin):
    """Task
    description : define Task object
    ERD Table (link TLDR:)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

    experiment_id = Column(String(100), ForeignKey('experiment.id'))
    task_manager_id = Column(String(100), ForeignKey('taskmanager.id'))
    name = Column(String(100))
    command = Column(String(100))
    status = Column(String(100))
    logfile_name = Column(String(100))  # task_manager의 default_log_file_path에 branches
    experiment = relationship("Experiment", back_populates="tasks")
    task_manager = relationship("TaskManager", back_populates="tasks")

if not sqlalchemy.inspect(engine).has_table(table_name):
    Base.metadata.create_all(engine)
