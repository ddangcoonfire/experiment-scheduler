from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import declarative_mixin, declared_attr
from experiment_scheduler.db_util import Session

import logging

logger = logging.getLogger()


def io_logger(func):
    def wrapper(self, *args, **kwargs):
        self.logger.debug(f"task_id from request : {args[1].task_id}")  # request
        result = func(self, *args, **kwargs)
        self.logger.debug(f"response.status : {result.status}")
        return result

    return wrapper


@declarative_mixin
class TableConfigurationMixin:
    """TableConfigurationMixin
    desc : common table information
    Returns:
        _type_: _description_
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(
        DateTime(timezone=True), onupdate=now(), server_default=now()
    )

    @classmethod
    def get_table_name(cls):
        return cls.__tablename__

    # def __init__(self):
    #     self._query = None
    #
    # def get_query(self, *args, **kwargs) -> Query:
    #     query = self._query or Session.query(self)
    #     return query
    #
    # def get(self, order_by: str = None, *args, **kwargs):
    #     query: Query = self.get_query(*args, **kwargs)
    #     query = query.filter(args)
    #     query = query.filter_by(kwargs)
    #
    #     if order_by:
    #         query = query.order_by(order_by)
    #     query.first()

    @classmethod
    def insert(cls, obj):
        with Session() as session:
            try:
                session.add(obj)
            except:
                session.rollback()
                raise
            else:
                session.commit()
