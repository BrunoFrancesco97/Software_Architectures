import sqlalchemy
import database
from sqlalchemy import DateTime
from sqlalchemy.sql import func
import channel
import pika 

class Channel_Sub(database.Base):
    __tablename__ = 'channel_subscriptions'
    channel = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("channels.id"), primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


def obj_to_dict(obj: Channel_Sub):  # for build json format
    return {
        "user": obj.user,
        "channel": obj.channel,
        "subscription": obj.subscription,
    }

def obj_to_dict2(obj: Channel_Sub):  # for build json format
    return {
        "user": obj.user,
        "channel": obj.channel,
        "event":"channel_sub"
    }

def obj_to_dict_complete(obj):  # for build json format
    return {
        "channel": obj.name,
    }


def add_subscription(channel, user: str):
    try:
        sub = select_channel_subs(user, channel)
        if sub is not None and len(sub) == 0:
            new_channel_sub = Channel_Sub(channel=channel, user=user)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channell = connection.channel()
            channell.queue_declare(queue='channel_info')
            dictObj : dict = obj_to_dict2(new_channel_sub)
            dictObj["mode"] = "add"
            channell.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
            )
            print("Message sent")
            connection.close()
    except Exception as e:
        print(e)


def remove_subscription(name: str, channel: id):
    session = database.Session()
    session.query(Channel_Sub).filter_by(user=name, channel=channel).delete(synchronize_session="evaluate")
    session.commit()


def select_all():
    session = database.Session()
    courses = session.query(Channel_Sub).all()
    session.close()
    return courses


def select_channel_subs_by_channels(channel):
    session = database.Session()
    sub = session.query(Channel_Sub).filter_by(channel=channel).all()
    session.close()
    return sub


def select_channel_subs_by_user(name: str):
    session = database.Session()
    # sub = session.query(Channel_Sub).filter_by(user=name).all()
    sub = session.query(channel.Channel).join(Channel_Sub).filter(Channel_Sub.user==name).all()
    session.close()
    return sub


def select_channel_subs(name: str, channel):
    session = database.Session()
    sub = session.query(Channel_Sub).filter_by(user=name, channel=channel).all()
    session.close()
    return sub
