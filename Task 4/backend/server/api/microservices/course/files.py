import sqlalchemy
import database
import json 
import requests 
from url_sec import *

class File(database.Base):
    __tablename__ = 'files'
    name = sqlalchemy.Column(sqlalchemy.String(length=255), primary_key=True)
    course = sqlalchemy.Column(sqlalchemy.String(length=40), primary_key=True)


def add_file(name: str, course: str, channel_name: str, file):
    session = database.Session()
    try:
            response = requests.put(URL_FILE+'/'+channel_name+"/"+course+"/"+name)
            js = json.loads(response.content)
            if js['added'] == True:
                new_file = File(name=name, course=course)
                session.add(new_file)
            else:
                session.rollback()
                return False
    except:
        session.rollback()
    else:
        session.commit()
        return True 


def obj_to_dict(obj: File):  # for build json format
    return {
        "name": obj.name,
        "course" : obj.course,
    }

def remove_file(name: str, course: str, channel_name: str):
    session = database.Session()
    try:
        response = requests.put(URL_FILE+'/'+channel_name+"/"+course+"/"+name)
        js = json.loads(response.content)
        if js['removed'] == True:
            session = database.Session()
            session.query(File).filter_by(name=name, course=course).delete(synchronize_session="evaluate")
        else:
                session.rollback()
                return False
    except:
        session.rollback()
    else:
        session.commit()
        return True


def select_all():
    session = database.Session()
    courses = session.query(File).all()
    session.close()
    return courses


def select_files_by_course(course: str):
    session = database.Session()
    files = session.query(File).filter_by(course=course).all()
    session.close()
    return files


def select_file(name: str, course: str):
    session = database.Session()
    files = session.query(File).filter_by(name=name, course=course).all()
    session.close()
    return files
