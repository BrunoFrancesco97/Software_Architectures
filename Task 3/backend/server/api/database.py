
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost:3306/sa")

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
