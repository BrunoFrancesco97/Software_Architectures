import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = None 
Base = declarative_base()
Session = sqlalchemy.orm.sessionmaker()

def set(url):
    engine = sqlalchemy.create_engine(url) 
    Base.metadata.create_all(engine)    
    Session.configure(bind=engine)



