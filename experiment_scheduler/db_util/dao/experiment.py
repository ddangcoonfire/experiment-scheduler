import sqlalchemy
from sqlalchemy import Column, String, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine, metadata

table_name = "experiment"

class Experiment(Base):
    __tablename__ = table_name

    id = Column(String, primary_key=True)
    name = Column(String)
    status = Column(String) # task의 상태에 대해 방어적으로 status define
    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())
    tasks = relationship("Task", back_populates="experiment")

# if not sqlalchemy.inspect(engine).has_table(table_name):
#     Base.metadata.create_all(engine)
