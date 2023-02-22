from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base

db_url = "sqlite:///test.db"
Base = declarative_base()
engine = create_engine(db_url, echo=True)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)

