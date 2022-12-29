import sqlalchemy
import database


class Support(database.Base):
    __tablename__ = 'supports'
    sender = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("user.email"), nullable=False)
    receiver = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("user.email"), nullable=False)
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




def send_message(sender: str, receiver: str, object_message: str, message: str):
    session = database.Session()
    try:
        new_message = Support(sender=sender, receiver=receiver, object=object_message, message=message)
        session.add(new_message)
    except:
        session.rollback()
    else:
        session.commit()


def select_messages_by_receiver(receiver: str):
    session = database.Session()
    messages = session.query(Support).filter_by(receiver=receiver).all()
    session.close()
    return messages
