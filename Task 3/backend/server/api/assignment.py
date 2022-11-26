import datetime

import sqlalchemy
import database
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class Assignment(database.Base):
    __tablename__ = 'assignments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=True)
    creation = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deadline = sqlalchemy.Column(DateTime(timezone=True), nullable=False)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), nullable=False)


def add_assignment(name: str, year : int, month : int, day : int, hour : int, seconds : int, course_el: str):
    session = database.Session()
    try:
        x = datetime.datetime(int(year), int(month), int(day), int(hour), int(seconds), 00)
        new_assignments = Assignment(name=name, deadline=x, course=course_el)
        session.add(new_assignments)
    except Exception as e:
        print(e)
        session.rollback()
    else:
        session.commit()


def remove_assignment(id_el):
    session = database.Session()
    session.query(Assignment).filter_by(id=id_el).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    channels = session.query(Assignment).all()
    session.flush()
    return channels


def get_assignments_by_id(id_el):
    session = database.Session()
    channels = session.query(Assignment).filter_by(id=id_el).all()
    session.flush()
    return channels


def get_assignments_by_name(name):
    session = database.Session()
    channels = session.query(Assignment).filter_by(name=name).all()
    session.flush()
    return channels


def get_assignments_by_course(course: str):
    session = database.Session()
    channels = session.query(Assignment).filter_by(course=course).all()
    session.flush()
    return channels
