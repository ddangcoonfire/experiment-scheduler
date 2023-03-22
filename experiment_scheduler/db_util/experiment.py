import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from experiment_scheduler.db_util import Base, engine
from experiment_scheduler.db_util.mixin import TableConfigurationMixin

table_name = "experiment"


class Experiment(Base, TableConfigurationMixin):
    """Experimnet
    description : define Experiment object
    ERD Table (link TLDR:)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

    name = Column(String(100))
    status = Column(String(100))
    tasks = relationship("Task", back_populates="experiment")


if not sqlalchemy.inspect(engine).has_table(table_name):
    Base.metadata.create_all(engine)
