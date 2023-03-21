import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine, metadata

table_name = "task"

class Task(Base, Mixin):
    __tablename__ = table_name

    id = Column(String, primary_key=True)
    experiment_id = Column(String, ForeignKey('experiment.id'))
    name = Column(String)
    command = Column(String)
    status = Column(String)
    task_logfile_name = Column(String)  # task_manager의 default_log_file_path에 branches
    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())
    experiment = relationship("Experiment", back_populates="tasks")
    # task_manager_address = Column(String) -> task_manager_id 로 1:N mapping

# if not sqlalchemy.inspect(engine).has_table(table_name):
#     Base.metadata.create_all(engine)
