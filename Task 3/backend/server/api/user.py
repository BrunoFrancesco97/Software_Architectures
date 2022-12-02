import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import Enum, DateTime
import database
import crypto

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



def add_user_complete(username, password, salt, name, surname, role):
    session = database.Session()
    if role == 'user' or role == 'admin' or role == 'staff':
        try:
            newUser = User(email=username, password=password, salt=salt, name=name, surname=surname, role=role)
            session.add(newUser)
        except:
            session.rollback()
        else:
            session.commit()


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
    session.flush()
    return users


def select_user_by_email(email: str):
    session = database.Session()
    user = session.query(User).filter_by(email=email).all()
    session.flush()
    return user


def get_password_salt(email: str):
    session = database.Session()
    user = session.query(User).filter_by(email=email).all()
    session.flush()
    if len(user) > 0:
        return user[0].password, user[0].salt
    return None


def select_user_by_email_password(email: str, password: str, salt: str):
    hash = crypto.sha256_encode_salt(password, salt)
    session = database.Session()
    user = session.query(User).filter_by(email=email).all()
    session.flush()
    return user
