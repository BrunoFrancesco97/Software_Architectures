import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import Enum, DateTime
import database
import crypto
import pika
import os

roles = ('user', 'staff', 'admin')
roles_enum = Enum(*roles, name="roles")


class User(database.Base):
    __tablename__ = 'user'
    email = sqlalchemy.Column(sqlalchemy.String(length=255), primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    salt = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    role = sqlalchemy.Column(roles_enum, nullable=False)
    creation = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

def obj_to_dict(obj: User):  # for build json format
    return {
        "name": obj.name,
        "surname":obj.surname,
        "email":obj.email,
        "role":obj.role,
        "creation":obj.creation
    }

def obj_to_dict2(obj: User):  # for build json format
    return {
        "name": obj.name,
        "surname":obj.surname,
        "email":obj.email,
        "role":obj.role,
        "password":obj.password,
        "salt":obj.salt,
        "event":"user"
    }


def add_user_complete(username, password, salt, name, surname, role):
    if role == 'user' or role == 'admin' or role == 'staff':
        try:
            newUser = User(email=username, password=password, salt=salt, name=name, surname=surname, role=role)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
            channel = connection.channel()
            channel.queue_declare(queue='channel_info')
            dictObj : dict = obj_to_dict2(newUser)
            dictObj["mode"] = "add"
            channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
            print("Message sent")
            connection.close()
        except Exception as e:
            print(e)

def add_user_uncomplete(username, password, salt, role):
    session = database.Session()
    if role == 'user' or role == 'admin' or role == 'staff':
        try:
            newUser = User(email=username, password=password, salt=salt, role=role)
            session.add(newUser)
        except:
            session.rollback()
        else:
            session.commit()


def remove_user(username: str):
    session = database.Session()
    user = select_user_by_email(username)
    session.delete(user[0])
    session.commit()


def select_all():
    session = database.Session()
    users = session.query(User).all()
    session.close()
    return users


def select_user_by_email(email: str):
    session = database.Session()
    user = session.query(User).filter_by(email=email).all()
    session.close()
    return user


def get_password_salt(email: str):
    session = database.Session()
    user = session.query(User).filter_by(email=email).all()
    session.close()
    if len(user) > 0:
        return user[0].password, user[0].salt
    return None


def select_user_by_email_password(email: str, password: str, salt: str):
    hash = crypto.sha256_encode_salt(password, salt)
    session = database.Session()
    user = session.query(User).filter_by(email=email,password=hash).all()
    session.close()
    return user
