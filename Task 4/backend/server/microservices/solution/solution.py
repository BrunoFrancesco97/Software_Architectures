import sqlalchemy
import database
import crypto
import pika 
import utils
import os

class Solution(database.Base):
    __tablename__ = 'solution'
    exercise = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exercises.id"), primary_key=True)
    answer = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    correct = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
    hash = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    review = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=False)


def obj_to_dict(obj: Solution):  # for build json format
    return {
        "exercise": obj.exercise,
        "answer": obj.answer,
        "user": obj.user,
        "correct": obj.correct,
        "hash": obj.hash,
        "review": obj.review,
    }

def obj_to_dict2(obj: Solution):  # for build json format
    return {
        "exercise": obj.exercise,
        "answer": obj.answer,
        "user": obj.user,
        "correct": obj.correct,
        "hash": obj.hash,
        "review": obj.review,
        "event":"solution"
    }

def obj_to_dict_quest(obj: Solution, quest):  # for build json format
    return {
        "exercise": obj.exercise,
        "answer": obj.answer,
        "user": obj.user,
        "correct": obj.correct,
        "hash": obj.hash,
        "review": obj.review,
        "quest": quest,
    }


def compute_hash(answer: str):
    answer = answer.strip()
    while '  ' in answer:
        answer = answer.replace('  ', ' ')
    answer = crypto.sha256_basic(answer)
    return answer


def add_solution(exercise: int, answer: str, user: str, correct, review):
    try:
        answer_b64 = utils.encode(answer)
        new_solution = Solution(exercise=exercise, answer=answer_b64, user=user, correct=correct, hash=compute_hash(answer),review=review)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_solution)
        dictObj["mode"] = "add"
        dictObj["type"] = "1"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)

def add_solution_open(exercise: int, answer: str, user: str, review):
    try:
        answer_b64 = utils.encode(answer)
        new_solution = Solution(exercise=exercise, answer=answer_b64, user=user, hash=compute_hash(answer),review=review)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_solution)
        dictObj["mode"] = "add"
        dictObj["type"] = "2"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)


def get_solutions_by_name(user: str):
    session = database.Session()
    solutions = session.query(Solution).filter_by(user=user).all()
    session.close()
    return solutions


def get_solutions_by_exercise(exercise: str):
    session = database.Session()
    solutions = session.query(Solution).filter_by(exercise=exercise).all()
    session.close()
    return solutions


def get_solutions_by_name_and_exercise(user: str, exercise, review):
    session = database.Session()
    solutions = session.query(Solution).filter_by(exercise=exercise, user=user, review=review).all()
    session.close()
    return solutions


def get_solutions_by_hash(hash: str, exercise: int):
    session = database.Session()
    solutions = session.query(Solution).filter_by(hash=hash, exercise=exercise).all()
    session.close()
    return solutions


def get_unreviewed_solution(exercise):
    session = database.Session()
    solutions = session.query(Solution).filter_by(exercise=exercise, review=False).all()
    session.close()
    return solutions


def check_solution(exercise, user, correct):
    new_solution = Solution(exercise=exercise, user=user, correct=correct)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
    channel = connection.channel()
    channel.queue_declare(queue='channel_info')
    dictObj : dict = obj_to_dict2(new_solution)
    dictObj["mode"] = "update"
    channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
    connection.close()
