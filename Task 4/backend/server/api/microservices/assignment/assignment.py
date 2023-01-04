import datetime

import sqlalchemy
import database
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import result
import pika 

class Assignment(database.Base):
    __tablename__ = 'assignments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=True)
    creation = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deadline = sqlalchemy.Column(DateTime(timezone=True), nullable=False)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), nullable=False)


def add_assignment(name: str, year : int, month : int, day : int, hour : int, minutes : int, course_el: str):
    session = database.Session()
    try:
        x = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), 00)
        new_assignments = Assignment(name=name, deadline=x, course=course_el)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channell = connection.channel()
        channell.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_assignments)
        dictObj["mode"] = "add"
        channell.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
        print("Message sent")
        connection.close()
    except Exception as e:
        return (False,None)
    else:
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

def obj_to_dict2(obj: Assignment):  # for build json format
    return {
        "id" : obj.id,
        "name": obj.name,
        "creation": obj.creation,
        "deadline" : obj.deadline,
        "course" : obj.course,
        "event" : "assignment"
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
