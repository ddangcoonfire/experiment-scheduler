from sqlalchemy import Column, String, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine, metadata

table_name = "experiment"

class Experiment(Base):
    __tablename__ = table_name

    id = Column(String, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())
    tasks = relationship("Task", back_populates="experiment")

if not Table(table_name, metadata, autoload=True).exists():
    Base.metadata.create_all(engine)
