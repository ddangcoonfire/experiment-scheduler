from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database

SCHEMA_NAME = "test2"

db_url = f"mysql+pymysql://root:@localhost:3306/{SCHEMA_NAME}?charset=utf8" # db_url = f"sqlite:///{SCHEMA_NAME}.db"

if not database_exists(db_url):
    create_database(db_url)

engine = create_engine(db_url, echo=True)

Base = declarative_base()
metadata = MetaData()
Session = sessionmaker(bind=engine)
