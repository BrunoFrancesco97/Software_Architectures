import datetime

import sqlalchemy
import database
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import result

class Assignment(database.Base):
    __tablename__ = 'assignments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=True)
    creation = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deadline = sqlalchemy.Column(DateTime(timezone=True), nullable=False)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)


def add_assignment(name: str, year : int, month : int, day : int, hour : int, minutes : int, course_el: str):
    session = database.Session()
    try:
        x = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), 00)
        new_assignments = Assignment(name=name, deadline=x, course=course_el)
        session.add(new_assignments)
    except Exception as e:
        session.rollback()
        return (False,None)
    else:
        session.commit()
        channels = session.query(Assignment).filter_by(name=name, course=course_el).all()
        session.close()
        return (True,channels[0])


def obj_to_dict(obj: Assignment):  # for build json format
    return {
        "id" : obj.id,
        "name": obj.name,
        "creation": obj.creation,
        "deadline" : obj.deadline,
        "course" : obj.course,
    }

def remove_assignment(id_el):
    session = database.Session()
    session.query(Assignment).filter_by(id=id_el).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    assignments = session.query(Assignment).all()
    session.close()
    return assignments


def get_assignments_by_id(id_el):
    session = database.Session()
    assignments = session.query(Assignment).filter_by(id=id_el).all()
    session.close()
    return assignments


def get_assignments_by_name(name):
    session = database.Session()
    assignments = session.query(Assignment).filter_by(name=name).all()
    session.close()
    return assignments


def get_assignments_by_course(course: str):
    session = database.Session()
    assignments = session.query(Assignment).filter_by(course=course).all()
    session.close()
    return assignments

def get_assignments_by_course_done(course: str, name : str):
    session = database.Session()
    assignments = session.query(Assignment).join(result.Result).filter(result.Result.user == name and Assignment.course == course).all()
    session.close()
    return assignments

def get_assignments_by_name_course(name : str, course: str):
    session = database.Session()
    assignments = session.query(Assignment).filter_by(name=name, course=course).all()
    session.close()
    return assignments
