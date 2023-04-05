"""
Experiment class is ORM class of Experiment defined in user's yaml file
"""

import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from experiment_scheduler.db_util.connection import Base, engine
from experiment_scheduler.db_util.mixin import DbCommonMixin


class Experiment(Base, DbCommonMixin):
    """Experimnet
    description : define Experiment object
    ERD Table (link TLDR:)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

    __tablename__ = "experiment"

    id = Column(String(100), primary_key=True)
    name = Column(String(100))
    status = Column(String(100))
    tasks = relationship(
        "Task",
        primaryjoin="Experiment.id==Task.experiment_id",
        foreign_keys="Task.experiment_id",
        uselist=True,
    )


if not sqlalchemy.inspect(engine).has_table(Experiment.get_table_name()):
    Base.metadata.create_all(engine)
