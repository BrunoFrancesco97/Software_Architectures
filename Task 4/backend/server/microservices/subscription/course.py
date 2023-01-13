import sqlalchemy
import database
import channel
import pika
import os

class Course(database.Base):
    __tablename__ = 'courses'
    name = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    channel = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("channels.id"), nullable=False)


def obj_to_dict(obj: Course):  # for build json format
    return {
        "name": obj.name,
        "channel": obj.channel,
    }

def obj_to_dict2(obj: Course):  # for build json format
    return {
        "name": obj.name,
        "channel": obj.channel,
        "event":"course"
    }

def add_course(name: str, channel_ID):
    try:
        existent = channel.get_channels_by_id(channel_ID)
        if existent is not None and len(existent) == 1:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
            channell = connection.channel()
            channell.queue_declare(queue='channel_info')
            new_course = Course(name=name, channel=channel_ID)
            dictObj : dict = obj_to_dict2(new_course)
            dictObj["mode"] = "add"
            channell.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
            )
            print("Message sent")
            connection.close()
    except Exception as e:
        print(e)

def remove_course(name: str, channel_ID, channel_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
    channell = connection.channel()
    channell.queue_declare(queue='channel_info')
    new_course = Course(name=name, channel=channel_ID)
    dictObj : dict = obj_to_dict2(new_course)
    dictObj["mode"] = "delete"
    channell.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj))
    print("Message sent")
    connection.close()


def select_all():
    session = database.Session()
    courses = session.query(Course).all()
    session.close()
    return courses


def select_course_by_channel(channel_ID):
    session = database.Session()
    course = session.query(Course).filter_by(channel=channel_ID).all()
    session.close()
    return course


def select_course_by_name(name: str):
    session = database.Session()
    course = session.query(Course).filter_by(name=name).all()
    session.close()
    return course
