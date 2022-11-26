import sqlalchemy
import database
import os
import app


class File(database.Base):
    __tablename__ = 'files'
    name = sqlalchemy.Column(sqlalchemy.String(length=255), primary_key=True)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), primary_key=True)


def add_file(name: str, course: str, channel_name: str, file):
    session = database.Session()
    try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + channel_name + '/' + course + '/', name))
        new_file = File(name=name, course=course)
        session.add(new_file)
    except:
        session.rollback()
    else:
        session.commit()


def remove_file(name: str, course: str, channel_name: str):
    session = database.Session()
    try:
        os.remove(app.config['UPLOAD_FOLDER'] + channel_name + '/' + course + '/' + name)
        course = select_file(name, course)
        session.delete(course)
    except:
        session.rollback()
    else:
        session.commit()


def select_all():
    session = database.Session()
    courses = session.query(File).all()
    session.flush()
    return courses


def select_files_by_course(course: str):
    session = database.Session()
    files = session.query(File).filter_by(course=course).all()
    session.flush()
    return files


def select_file(name: str, course: str):
    session = database.Session()
    files = session.query(File).filter_by(name=name, course=course).all()
    session.flush()
    return files
