import sqlalchemy
import os
import shutil
import database
import app


class Channel(database.Base):
    __tablename__ = 'channels'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)



def obj_to_dict(obj: Channel):  # for build json format
    return {
        "id": obj.id,
        "name": obj.name,
    }

def add_channel(name: str):
    session = database.Session()
    try:
        new_channel = Channel(name=name)
        channel_got = get_channels_by_name(name)
        if channel_got is not None and len(channel_got) == 0:
            session.add(new_channel)
            os.mkdir(app.UPLOAD_FOLDER + name)
    except:
        session.rollback()
    else:
        session.commit()



def remove_channel(name: str):
    session = database.Session()
    session.query(Channel).filter_by(name=name).delete(synchronize_session="evaluate")
    session.commit()
    shutil.rmtree(app.UPLOAD_FOLDER + name)


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

