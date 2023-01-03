import sqlalchemy
import database
import channel

class Course(database.Base):
    __tablename__ = 'courses'
    name = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)
    channel = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("channels.id"), nullable=False)


def obj_to_dict(obj: Course):  # for build json format
    return {
        "name": obj.name,
        "channel": obj.channel,
    }

def add_course(name: str, channel_ID):
    session = database.Session()
    try:
        existent = channel.get_channels_by_id(channel_ID)
        if existent is not None and len(existent) == 1:
            new_course = Course(name=name, channel=channel_ID)
            session.add(new_course)
    except Exception as e:
        print(e)
        session.rollback()
    else:
        session.commit()


def remove_course(name: str, channel_ID, channel_name: str):
    session = database.Session()
    session.query(Course).filter_by(name=name, channel=channel_ID).delete(synchronize_session="evaluate")
    session.close()


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
