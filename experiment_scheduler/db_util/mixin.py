from sqlalchemy import Column, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import declarative_mixin, declared_attr, Query
from experiment_scheduler.db_util.connection import Session


@declarative_mixin
class DbCommonMixin:
    """TableConfigurationMixin
    desc : common table information
    Returns:
        _type_: _description_
    """

    @declared_attr
    def __tablename__(cls):
        """
        set Table Name for saving metadata
        :param request: none
        :param context: none
        :return: table name
        """
        return cls.__name__.lower()

    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(
        DateTime(timezone=True), onupdate=now(), server_default=now()
    )

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
    def list(cls, order_by: str = None, *args, **kwargs):
        """
        select all data conditionally in certain table
        :param request: condition, order
        :return: data(s)
        """
        query: Query = Session().query(cls)
        query = query.filter(*args)
        query = query.filter_by(**kwargs)

        if order_by:
            query = query.order_by(order_by)
        return query.all()

    @classmethod
    def get(cls, order_by: str = None, *args, **kwargs):
        """
        select a data conditionally in certain table
        :param request: condition, order
        :return: data
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
        """
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
        """
        update data having request id in certain table
        this method is temporal for testing
        :param request: id, instance of pre-defined class
        :return: none
        """
        with Session() as session:
            try:
                session.query(cls).filter_by(id=id).update(update)
            except:
                session.rollback()
                raise
            else:
                session.commit()

    def commit(self):
        """
        for using orm update, need to commit at update
        :param request: id, instance of pre-defined class
        :return: none
        """
        Session.object_session(self).commit()
