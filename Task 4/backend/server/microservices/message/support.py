import sqlalchemy
import database
import pika
import os

class Support(database.Base):
    __tablename__ = 'supports'
    sender = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    receiver = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    object = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)


def obj_to_dict(obj: Support):  # for build json format
    return {
        "sender": obj.sender,
        "receiver": obj.receiver,
        "object": obj.object,
        "message": obj.message,
    }

def obj_to_dict2(obj: Support):  # for build json format
    return {
        "sender": obj.sender,
        "receiver": obj.receiver,
        "object": obj.object,
        "message": obj.message,
        "event": "message"
    }



def send_message(sender: str, receiver: str, object_message: str, message: str):
    try:
        new_message = Support(sender=sender, receiver=receiver, object=object_message, message=message)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT']))
        channel = connection.channel()
        channel.queue_declare(queue='channel_info')
        dictObj : dict = obj_to_dict2(new_message)
        dictObj["mode"] = "add"
        channel.basic_publish(exchange='', routing_key='channel_info', body=str(dictObj)
        )
        print("Message sent")
        connection.close()
    except Exception as e:
        print(e)

def select_messages_by_receiver(receiver: str):
    session = database.Session()
    messages = session.query(Support).filter_by(receiver=receiver).all()
    session.close()
    return messages
