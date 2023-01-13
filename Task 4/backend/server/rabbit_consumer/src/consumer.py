import pika
import database 
import json 
import url_db 
import class_definitions
import base64
import os, sys

URL_USERS = [url_db.URL_LOGIN, url_db.URL_USER] #OK
URL_ASSIGNMENTS = [url_db.URL_ASSIGNMENT, url_db.URL_COURSE, url_db.URL_EXERCISE] #?
URL_CHANNELS = [url_db.URL_ASSIGNMENT, url_db.URL_CHANNEL, url_db.URL_COURSE, url_db.URL_FILE, url_db.URL_CHANNEL_SUB] #OK
URL_COURSES = [url_db.URL_ASSIGNMENT, url_db.URL_CHANNEL, url_db.URL_COURSE,  url_db.URL_FILE, url_db.URL_CHANNEL_SUB] #OK
URL_EXERCISES = [url_db.URL_EXERCISE, url_db.URL_SOLUTION]  #OK
URL_FILES = [url_db.URL_COURSE, url_db.URL_FILE] #OK
URL_MESSAGES = [url_db.URL_MESSAGE] #OK
URL_RESULTS = [url_db.URL_ASSIGNMENT, url_db.URL_COURSE, url_db.URL_EXERCISE, url_db.URL_RESULT, url_db.URL_SOLUTION] #OK
URL_SOLUTIONS = [url_db.URL_EXERCISE, url_db.URL_SOLUTION] #UPDATE
URL_CHANNEL_SUBS = [url_db.URL_CHANNEL, url_db.URL_FILE, url_db.URL_CHANNEL_SUB] #OK
URL_COURSE_SUBS = [url_db.URL_COURSE, url_db.URL_EXERCISE, url_db.URL_FILE, url_db.URL_COURSE_SUB] #OK
URL_TESTS = [url_db.URL_EXERCISE, url_db.URL_TEST] #OK

def write_db(ch, method, properties, body):
    try:
        x : dict = json.loads(body.decode(encoding="UTF-8").replace("'",'\"').replace("False","\"False\"").replace("True","\"True\"").replace("None","\"None\""))
        if x.get('event') == "user":
            if x.get('mode') == 'add':
                for link in URL_USERS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.User(email=x.get('email'), password=x.get('password'), salt=x.get('salt'), name=x.get('name'), surname=x.get('surname'), role=x.get('role'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'channel':
            if x.get('mode') == 'add':
                for link in URL_CHANNELS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.Channel(name=x.get('name'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit() 
        elif x.get('event') == 'course':
            if x.get('mode') == 'add':
                for link in URL_COURSES:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.Course(name=x.get('name'), channel=x.get('channel'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'file':
            if x.get('mode') == 'add':
                    for link in URL_FILES:
                        database.set(link)
                        session = database.Session()
                        try:
                            session.add(class_definitions.File(name=x.get('name'), course=x.get('course'))) 
                        except:
                            session.rollback()
                        else:
                            session.commit() 
        elif x.get('event') == 'message':
            if x.get('mode') == 'add':
                for link in URL_MESSAGES:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.Support(sender=x.get('sender'), receiver=x.get('receiver'), object=x.get('object'), message=x.get('message'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'result':
            if x.get('mode') == 'add':
                for link in URL_RESULTS:
                    database.set(link)
                    session = database.Session()
                    try:
                        if x.get('type') == '1':
                            session.add(class_definitions.Result(assignment=x.get('assignment'), user=x.get('user'), result=x.get('result'))) 
                        elif x.get('type') == '2':
                            session.add(class_definitions.Result(assignment=x.get('assignment'), user=x.get('user'), result=x.get('result'), comment=x.get('comment')))  
                        elif x.get('type') == '3':
                            session.add(class_definitions.Result(assignment=x.get('assignment'), user=x.get('user'), comment=x.get('comment')))  
                        else:
                            session.rollback()
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'test':
            if x.get('mode') == 'add':
                for link in URL_TESTS:
                    database.set(link)
                    session = database.Session()
                    try:
                        if x.get('type') == '1':
                            session.add(class_definitions.Test(name=x.get('name'), exercise=x.get('exercise'), given_value=x.get('parameter'), expected= x.get('expected'))) 
                        elif x.get('type') == '2':
                            session.add(class_definitions.Test(name=x.get('name'), exercise=x.get('exercise'), comment=x.get('comment'), given_value=x.get('parameter'), expected=x.get('expected')))  
                        else:
                            session.rollback()
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'solution':
            if x.get('mode') == 'add':
                for link in URL_SOLUTIONS:
                    database.set(link)
                    session = database.Session()
                    try:
                        if x.get('type') == '1':
                            session.add(class_definitions.Solution(exercise=x.get('exercise'), answer=x.get('answer'), user=x.get('user'), correct=eval(x.get('correct')), hash=x.get('hash'),review=eval(x.get('review')))) 
                        elif x.get('type') == '2':
                            session.add(class_definitions.Solution(exercise=x.get('exercise'), answer=x.get('answer'), user=x.get('user'), hash=x.get('hash'),review=eval(x.get('review'))))
                        else:
                            session.rollback()
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'channel_sub':
            if x.get('mode') == 'add':
                for link in URL_CHANNEL_SUBS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.Channel_Sub(channel=x.get('channel'), user=x.get('user'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit()
            if x.get('mode') == 'delete':
                for link in URL_CHANNEL_SUBS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.query(class_definitions.Channel_Sub).filter_by(user=x.get('user'), channel=x.get('channel')).delete(synchronize_session="evaluate")
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'course_sub':
            if x.get('mode') == 'add':
                for link in URL_COURSE_SUBS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.Course_Sub(course=x.get('course'), user=x.get('user'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit()
            if x.get('mode') == 'delete':
                for link in URL_COURSE_SUBS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.query(class_definitions.Course_Sub).filter_by(user=x.get('user'), course=x.get('course')).delete(synchronize_session="evaluate")
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'assignment':
            if x.get('mode') == 'add':
                for link in URL_ASSIGNMENTS:
                    database.set(link)
                    session = database.Session()
                    try:
                        session.add(class_definitions.Assignment(name=x.get('name'), deadline=x.get('deadline'), course=x.get('course'))) 
                    except:
                        session.rollback()
                    else:
                        session.commit()
        elif x.get('event') == 'exercise':
            if x.get('mode') == 'add':
                for link in URL_EXERCISES:
                    database.set(link)
                    session = database.Session()
                    try:
                        if x.get('type') == '1':
                            session.add(class_definitions.Exercise(quest=x.get('quest'), correct=x.get('correct'), assignment=x.get('assignment'), type=x.get('type'))) 
                        elif x.get('type') == '2':
                            session.add(class_definitions.Exercise(quest=x.get('quest'), correct=x.get('correct'), wrong1=x.get('wrong1'), wrong2=x.get('wrong2'), wrong3=x.get('wrong3'),
                                    assignment=x.get('assignment'), type=x.get('type')))  
                        else:
                            session.rollback()
                    except:
                        session.rollback()
                    else:
                        session.commit()
        else:
            print("Error")
    except Exception as e:
        print(e) 
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['URL_RABBIT'], socket_timeout=5, connection_attempts=10))
    channel = connection.channel()
    channel.queue_declare(queue='channel_info')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='channel_info', on_message_callback=write_db)
    print("Starting consuming")
    channel.start_consuming()