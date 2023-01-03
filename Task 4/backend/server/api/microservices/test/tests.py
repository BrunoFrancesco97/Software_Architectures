import sqlalchemy
import database
from sqlalchemy import Enum



class Test(database.Base):
    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    exercise = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    given_value = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    expected = sqlalchemy.Column(sqlalchemy.String(length=255),nullable=False)

def obj_to_dict(obj: Test):  # for build json format
    return {
        "id":obj.id,
        "name": obj.name,
        "comment":obj.comment,
        "exercise":obj.exercise,
        "parameter":obj.given_value,
        "expected":obj.expected
    }



def add_test_uncomplete(name: str, exercise: int, given_value : str, expected : str):
    session = database.Session()
    try:
        new_test = Test(name=name, exercise=exercise, given_value=given_value, expected= expected)
        session.add(new_test)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True 

def add_test_complete(name: str, comment: str, exercise: int, given_value : str, expected : str):
    session = database.Session()
    try:
        new_test = Test(name=name, exercise=exercise, comment=comment, given_value=given_value, expected=expected)
        session.add(new_test)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True 


def remove_test(id_el):
    session = database.Session()
    session.query(Test).filter_by(id=id_el).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    exercise = session.query(Test).all()
    session.close()
    return exercise


def get_test_by_id(id_el):
    session = database.Session()
    exercise = session.query(Test).filter_by(id=id_el).all()
    session.close()
    return exercise

def get_tests_by_exercise(exercise):
    session = database.Session()
    exercise = session.query(Test).filter_by(exercise=exercise).all()
    session.close()
    return exercise