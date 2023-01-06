#dbms orm manager
from flask_sqlalchemy import *
from sqlalchemy import *

#password hashing
import hashlib
from passlib.hash import pbkdf2_sha512

engine=create_engine('postgresql://hiilboamnwouaa:9f01a615b7f07a47da7c28f4157bcfd52589fc980b25239198216734444c8508@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/d56jh23cv8aqpc',echo=True,isolation_level="READ COMMITTED")

metadata=MetaData()
providers=Table('providers',metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('password',String(128), nullable=False),
    Column('region', String(25), nullable=False),
    Column('province',String(25), nullable=False)
)

metadata.create_all(engine)
