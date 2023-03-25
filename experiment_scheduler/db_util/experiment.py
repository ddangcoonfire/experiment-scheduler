import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from experiment_scheduler.db_util import Base, engine
from experiment_scheduler.db_util.mixin import TableConfigurationMixin


class Experiment(Base, TableConfigurationMixin):
    """Experimnet
    description : define Experiment object
    ERD Table (link TLDR:)
    Args:
        Base (_type_): _description_
        TableConfigurationMixin (_type_): mixin
    """

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
