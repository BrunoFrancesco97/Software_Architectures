import sqlalchemy
import database
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import pika
import os

class Result(database.Base):
    __tablename__ = 'results'
    assignment = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("assignments.id"), nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

def obj_to_dict(obj: Result):  # for build json format
    return {
        "assignment": obj.assignment,
        "user": obj.user,
        "subscription":obj.subscription,
        "result":obj.result,
        "comment":obj.comment,
        "id":obj.id
    }

def obj_to_dict2(obj: Result):  # for build json format
    return {
        "assignment": obj.assignment,
        "user": obj.user,
        "subscription":obj.subscription,
        "result":obj.result,
        "comment":obj.comment,
        "id":obj.id,
        "event":"result"
    }

def add_result_without_comment(assignment_el: int, user_el: str, result_el: int):
    try:
        new_result = Result(assignment=assignment_el, user=user_el, result=result_el)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_result)
        dictObj["mode"] = "add"
        dictObj["type"] = "1"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)


def add_result_with_comment(assignment_el: int, user_el: str, result_el: int, comment_el: str):
    try:
        new_result = Result(assignment=assignment_el, user=user_el, result=result_el, comment=comment_el)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_result)
        dictObj["mode"] = "add"
        dictObj["type"] = "2"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)

def add_result_without_vote(assignment_el: int, user_el: str, comment_el: str):
    try:
        new_result = Result(assignment=assignment_el, user=user_el, comment=comment_el)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_result)
        dictObj["mode"] = "add"
        dictObj["type"] = "3"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)


def remove_result(id_el):
    new_result = Result(id=id_el)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
    channel = connection.channel()
    channel.queue_declare(queue='channel_info')
    dictObj : dict = obj_to_dict2(new_result)
    dictObj["mode"] = "delete"
    channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
    print("Message sent")
    connection.close()



def selectAll():
    session = database.Session()
    results = session.query(Result).all()
    session.close()
    return results


def get_result_by_id(id_el):
    session = database.Session()
    results = session.query(Result).filter_by(id=id_el).all()
    session.close()
    return results


def get_results_by_user(user : str):
    session = database.Session()
    results = session.query(Result).filter_by(user=user).all()
    session.close()
    return results


def get_results_by_assignment(assignment: int):
    session = database.Session()
    results = session.query(Result).filter_by(assignment=assignment).all()
    session.close()
    return results

def get_results_by_assignment_user(assignment: int, user : str):
    session = database.Session()
    results = session.query(Result).filter_by(assignment=assignment,user=user).all()
    session.close()
    return results
