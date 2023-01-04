import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import os 

Base = declarative_base()
#engine = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost:3306/4_course")
engine = sqlalchemy.create_engine("mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['DB_URL']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME'])

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
