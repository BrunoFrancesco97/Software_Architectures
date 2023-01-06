import sqlalchemy
import database
from sqlalchemy import Enum
import pika
import os

roles = ('multiple', 'open', 'develop', 'quiz')
roles_enum = Enum(*roles, name="roles")


class Exercise(database.Base):
    __tablename__ = 'exercises'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    quest = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    correct = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    wrong1 = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    wrong2 = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    wrong3 = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    assignment = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("assignments.id"), nullable=False)
    type = sqlalchemy.Column(roles_enum, nullable=False)

def obj_to_dict(obj: Exercise):  # for build json format
    return {
        "id":obj.id,
        "quest": obj.quest,
        "assignment":obj.assignment,
        "type":obj.type
    }
def obj_to_dict2(obj: Exercise):  # for build json format
    return {
        "id":obj.id,
        "quest": obj.quest,
        "correct":obj.correct,
        "assignment":obj.assignment,
        "type":obj.type,
        "event":"exercise"
    }

def obj_to_dict3(obj: Exercise):  # for build json format
    return {
        "id":obj.id,
        "quest": obj.quest,
        "correct":obj.correct,
        "wrong1":obj.wrong1,
        "wrong2":obj.wrong2,
        "wrong3":obj.wrong3,
        "assignment":obj.assignment,
        "type":obj.type,
        "event":"exercise"
    }


def add_exercise_uncomplete(quest: str, correct: str, assignment, type: str):
    session = database.Session()
    try:
        new_exercise = Exercise(quest=quest, correct=correct, assignment=assignment, type=type)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channell = connection.channel()
        channell.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_exercise)
        dictObj["mode"] = "add"
        dictObj["type"] = "1"
        channell.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
        print("Message sent")
        connection.close()
    except:
        return (False,None)
    else:
        exercise = session.query(Exercise).filter_by(quest=quest, assignment=assignment).all()
        session.close()
        return (True,exercise[0])


def add_exercise_complete(quest: str, correct: str, wrong1: str, wrong2: str, wrong3: str, assignment, type: str):
    try:
        new_exercise = Exercise(quest=quest, correct=correct, wrong1=wrong1, wrong2=wrong2, wrong3=wrong3,
                                assignment=assignment, type=type)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channell = connection.channel()
        channell.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict3(new_exercise)
        dictObj["mode"] = "add"
        dictObj["type"] = "2"
        channell.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)



def remove_exercise(id_el):
    session = database.Session()
    session.query(Exercise).filter_by(id=id_el).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    exercise = session.query(Exercise).all()
    session.close()
    return exercise


def get_exercise_by_id(id_el):
    session = database.Session()
    exercise = session.query(Exercise).filter_by(id=id_el).all()
    session.close()
    return exercise


def get_exercises_by_assignment(assignment):
    session = database.Session()
    exercise = session.query(Exercise).filter_by(assignment=assignment).all()
    session.close()
    return exercise


def get_exercise_by_type_and_assignment(type, assignment):
    session = database.Session()
    exercise = session.query(Exercise).filter_by(type=type, assignment=assignment).all()
    session.close()
    return exercise

