import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine, metadata

table_name = "task_manager"

class TaskManager(Base):
    __tablename__ = table_name

    id = Column(String, primary_key=True)
    address = Column(String)
    default_log_file_path = Column(String)
    spec = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())

if not sqlalchemy.inspect(engine).has_table(table_name):
    Base.metadata.create_all(engine)