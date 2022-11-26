import sqlalchemy
import database
from sqlalchemy import Enum

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



def add_exercise_uncomplete(quest: str, correct: str, assignment, type: str):
    session = database.Session()
    try:
        new_exercise = Exercise(quest=quest, correct=correct, assignment=assignment, type=type)
        session.add(new_exercise)
    except:
        session.rollback()
    else:
        session.commit()


def add_exercise_complete(quest: str, correct: str, wrong1: str, wrong2: str, wrong3: str, assignment, type: str):
    session = database.Session()
    try:
        new_exercise = Exercise(quest=quest, correct=correct, wrong1=wrong1, wrong2=wrong2, wrong3=wrong3,
                                assignment=assignment, type=type)
        session.add(new_exercise)
    except:
        session.rollback()
    else:
        session.commit()


def remove_exercise(id_el):
    session = database.Session()
    session.query(Exercise).filter_by(id=id_el).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    channels = session.query(Exercise).all()
    session.flush()
    return channels


def get_exercise_by_id(id_el):
    session = database.Session()
    exercise = session.query(Exercise).filter_by(id=id_el).all()
    session.flush()
    return exercise


def get_exercises_by_assignment(assignment):
    session = database.Session()
    channels = session.query(Exercise).filter_by(assignment=assignment).all()
    session.flush()
    return channels
