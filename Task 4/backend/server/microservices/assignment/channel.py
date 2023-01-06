import os
import sqlalchemy
import database
import pika

class Channel(database.Base):
    __tablename__ = 'channels'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)



def obj_to_dict(obj: Channel):  
    return {
        "id": obj.id,
        "name": obj.name
    }

def obj_to_dict2(obj: Channel):  
    return {
        "id": obj.id,
        "name": obj.name,
        "event":"channel"
    }


def add_channel(name: str):
    new_channel = Channel(name=name)
    channel_got = get_channels_by_name(name)
    if channel_got is not None and len(channel_got) == 0:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_channel)
        dictObj["mode"] = "add"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
            )
        print("Message sent")
        connection.close()



def remove_channel(name: str):
    session = database.Session()
    session.query(Channel).filter_by(name=name).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    channels = session.query(Channel).all()
    session.close()
    return channels


def get_channels_by_id(id):
    session = database.Session()
    channels = session.query(Channel).filter_by(id=id).all()
    session.close()
    return channels


def get_channels_by_name(name: str):
    session = database.Session()
    channels = session.query(Channel).filter_by(name=name).all()
    session.close()
    return channels

