import sqlalchemy
import database
import pika 
import os

class Test(database.Base):
    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    exercise = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exercises.id"), nullable=False)
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

def obj_to_dict2(obj: Test):  # for build json format
    return {
        "id":obj.id,
        "name": obj.name,
        "comment":obj.comment,
        "exercise":obj.exercise,
        "parameter":obj.given_value,
        "expected":obj.expected,
        "event":"test"
    }


def add_test_uncomplete(name: str, exercise: int, given_value : str, expected : str):
    try:
        new_test = Test(name=name, exercise=exercise, given_value=given_value, expected= expected)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_test)
        dictObj["mode"] = "add"
        dictObj["type"] = "1"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        return False
    else:
        return True 

def add_test_complete(name: str, comment: str, exercise: int, given_value : str, expected : str):
    try:
        new_test = Test(name=name, exercise=exercise, comment=comment, given_value=given_value, expected=expected)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_test)
        dictObj["mode"] = "add"
        dictObj["type"] = "2"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except:
        return False
    else:
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