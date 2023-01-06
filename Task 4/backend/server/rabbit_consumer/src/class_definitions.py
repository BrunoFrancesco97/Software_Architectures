import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import Enum, DateTime
import database

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


class Channel(database.Base):
    __tablename__ = 'channels'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)


class Course(database.Base):
    __tablename__ = 'courses'
    name = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    channel = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("channels.id"), nullable=False)


class File(database.Base):
    __tablename__ = 'files'
    name = sqlalchemy.Column(sqlalchemy.String(length=255), primary_key=True)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), primary_key=True)


class Support(database.Base):
    __tablename__ = 'supports'
    sender = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    receiver = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    object = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)


class Result(database.Base):
    __tablename__ = 'results'
    assignment = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)


class Test(database.Base):
    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    exercise = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exercises.id"), nullable=False)
    given_value = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    expected = sqlalchemy.Column(sqlalchemy.String(length=255),nullable=False)   


class Solution(database.Base):
    __tablename__ = 'solution'
    exercise = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exercises.id"), primary_key=True)
    answer = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    correct = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
    hash = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    review = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=False)


class Channel_Sub(database.Base):
    __tablename__ = 'channel_subscriptions'
    channel = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("channels.id"), primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Course_Sub(database.Base):
    __tablename__ = 'course_subscriptions'
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Exercise(database.Base):
    __tablename__ = 'exercises'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    quest = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    correct = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    wrong1 = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    wrong2 = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    wrong3 = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    assignment = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    type = sqlalchemy.Column(roles_enum, nullable=False)


class Assignment(database.Base):
    __tablename__ = 'assignments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=True)
    creation = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deadline = sqlalchemy.Column(DateTime(timezone=True), nullable=False)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)