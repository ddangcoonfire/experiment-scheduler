import sqlalchemy
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine
from experiment_scheduler.db_util.mixin import TableConfigurationMixin

table_name = "task_manager"

class TaskManager(Base, TableConfigurationMixin):
    # __tablename__ = table_name

    # id = Column(String(100), primary_key=True)
    # created_at = Column(DateTime(timezone=True), server_default=now())
    # last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())

    address = Column(String(100))
    default_log_file_path = Column(String(100))
    spec = Column(JSON)
    tasks = relationship("Task", back_populates="task_manager")

if not sqlalchemy.inspect(engine).has_table(table_name):
    Base.metadata.create_all(engine)