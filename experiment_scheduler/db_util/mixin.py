from sqlalchemy import Column, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import declarative_mixin, declared_attr, Query
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

    @classmethod
    def list(cls, order_by: str = None, *args, **kwargs):
        query: Query = Session().query(cls)
        query = query.filter(*args)
        query = query.filter_by(**kwargs)

        if order_by:
            query = query.order_by(order_by)
        return query.all()

    @classmethod
    def get(cls, order_by: str = None, *args, **kwargs):
        query: Query = Session().query(cls)
        query = query.filter(*args)
        query = query.filter_by(**kwargs)

        if order_by:
            query = query.order_by(order_by)
        return query.first()

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

    @classmethod
    def update(cls, id, update):
        with Session() as session:
            try:
                session.query(cls).filter_by(id=id).update(update)
            except:
                session.rollback()
                raise
            else:
                session.commit()

    def commit(self):
        Session.object_session(self).commit()
