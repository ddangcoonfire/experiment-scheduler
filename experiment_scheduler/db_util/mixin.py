"""
DBCommonMixin class contains common column and method
"""
from sqlalchemy import Column, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import declarative_mixin, Query
from sqlalchemy.exc import SQLAlchemyError
from experiment_scheduler.db_util.connection import Session


@declarative_mixin
class DbCommonMixin:
    """TableConfigurationMixin
    desc : common table information
    """

    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now(), server_default=now())

    @classmethod
    def get_table_name(cls):
        """
        get Table Name
        :param request: none
        :param context: none
        :return: table name
        """
        return cls.__tablename__

    @classmethod
    def list(cls, *args, order_by: str = None, **kwargs):
        """
        select all data conditionally in certain table
        :param request: condition, order
        :return: data(s)

        ex)
            Task.list(status=1, order_by=Task.created_at)
        """
        query: Query = Session().query(cls)
        query = query.filter(*args)
        query = query.filter_by(**kwargs)

        if order_by:
            query = query.order_by(order_by)
        return query.all()

    @classmethod
    def get(cls, *args, order_by: str = None, **kwargs):
        """
        select a data conditionally in certain table
        :param request: condition, order
        :return: data

        ex)
            Task.get(id=1)
        """
        query: Query = Session().query(cls)
        query = query.filter(*args)
        query = query.filter_by(**kwargs)

        if order_by:
            query = query.order_by(order_by)
        return query.first()

    @classmethod
    def insert(cls, obj):
        """
        insert data in certain table
        :param request: instance of pre-defined class
        :return: none

        ex)
            Task.insert(Task(id='task_id', experiment_id='exp_id', name='name' ...))
        """
        with Session() as session:
            try:
                session.add(obj)
                session.commit()
            except SQLAlchemyError:
                session.rollback()

    def commit(self):
        """
        for using orm update, need to commit at update
        :return: none

        ex)
            obj = Task.get(id=1)
            obj.status = 2
            obj.commit()
        """
        with Session.object_session(self) as session:
            try:
                session.commit()
            except SQLAlchemyError:
                session.rollback()
