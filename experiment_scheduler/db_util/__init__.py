from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base

# db_url = "sqlite:///test.db"
db_url = "mysql+pymysql://root:jungsu123@@127.0.0.1?port=3306/new_schema"
Base = declarative_base()
engine = create_engine(db_url, echo=True)
connection = engine.connect()
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

