from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine, metadata

table_name = "task"

class Task(Base):
    __tablename__ = table_name

    id = Column(String, primary_key=True)
    experiment_id = Column(String, ForeignKey('experiment.id'))
    name = Column(String)
    command = Column(String)
    status = Column(String)
    task_manager_address = Column(String)
    task_logfile_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())
    experiment = relationship("Experiment", back_populates="tasks")

if not Table(table_name, metadata, autoload=True).exists():
    Base.metadata.create_all(engine)
