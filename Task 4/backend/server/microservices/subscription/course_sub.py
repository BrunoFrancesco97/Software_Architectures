import sqlalchemy
import database
from sqlalchemy import DateTime
from sqlalchemy.sql import func
import pika
import os

class Course_Sub(database.Base):
    __tablename__ = 'course_subscriptions'
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


def obj_to_dict(obj: Course_Sub):  # for build json format
    return {
        "user": obj.user,
        "course": obj.course,
        "subscription": obj.subscription,
    }

def obj_to_dict2(obj: Course_Sub):  # for build json format
    return {
        "user": obj.user,
        "course": obj.course,
        "event":"course_sub"
    }



def add_subscription(course: str, user: str):
    try:
        sub = select_course_subs(user, course)
        if sub is not None and len(sub) == 0:
            new_course_sub = Course_Sub(course=course, user=user)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
            channel = connection.channel()
            channel.queue_declare(queue='channel_info')
            dictObj : dict = obj_to_dict2(new_course_sub)
            dictObj["mode"] = "add"
            channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
                )
            print("Message sent")
            connection.close()
    except Exception as e:
        print(e)

def remove_subscription(name: str, course: str):
    session = database.Session()
    session.query(Course_Sub).filter_by(user=name, course=course).delete(synchronize_session="evaluate")
    session.close()
    session.commit()


def select_all():
    session = database.Session()
    courses = session.query(Course_Sub).all()
    session.close()
    return courses


def select_course_subs_by_courses(course: str):
    session = database.Session()
    sub = session.query(Course_Sub).filter_by(course=course).all()
    session.close()
    return sub


def select_course_subs_by_user(name: str):
    session = database.Session()
    sub = session.query(Course_Sub).filter_by(user=name).all()
    session.close()
    return sub


def select_course_subs(name: str, course: str):
    session = database.Session()
    sub = session.query(Course_Sub).filter_by(user=name, course=course).all()
    session.close()
    return sub
