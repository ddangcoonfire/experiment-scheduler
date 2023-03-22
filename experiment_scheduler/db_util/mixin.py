from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import declarative_mixin, declared_attr


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

    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=now(), server_default=now())

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
