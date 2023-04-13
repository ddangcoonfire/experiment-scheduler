"""
This file exists to manage sqlalchemy function
"""
import ast

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from experiment_scheduler.common.settings import USER_CONFIG

db_url = ast.literal_eval(USER_CONFIG.get("default", "db_url"))
Base = declarative_base()
engine = create_engine(db_url)
metadata = MetaData()
Session = scoped_session(sessionmaker(bind=engine))


def initialize_db():
    """
    initailize database schema
    :param request: none
    :param context: none
    :return: none
    """
    if not database_exists(db_url):
        create_database(db_url)
