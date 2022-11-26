import json
import base64
import os

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, set_access_cookies, \
    unset_jwt_cookies
from werkzeug.utils import secure_filename
from datetime import timedelta
import channel
import channel_sub
import course
import course_sub
import crypto
import user
import utils
import result
import files
import support
import subprocess
import exercise
import shutil
import assignment
import solution
import re

# https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/


# TODO: IMPLEMENTARE SISTEMA BASATO SU UNA CODA FIFO DI ASSIGNMENTS, PRENDO QUINDI L'ASSIGNMENT, CONTROLLO CHE TIPO SIA
# TODO: A SECONDA DEL TIPO MI CREO UN THREAD CHE SI CREA UN DOCKERFILE, MI SALVA IL FILE NEL SERVER
# TODO: E LO COPIA NEL CONTAINER, ESEGUE IL CONTAINER, SI PESCA L'OUTPUT E LO RESTITUISCE

# TODO: BISOGNA CAPIRE COME RICEVERE L'OUTPUT DA CONTAINER DOCKER


app = Flask(__name__)
UPLOAD_FOLDER = 'userdata/'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config[
    'JWT_SECRET_KEY'] = 'vnjfueofkskf'  # TODO: IN APP SERIE QUESTA ANDREBBE PORTATA FUORI DA QUI, MAGARI IN UN FILE
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

jwt = JWTManager(app)

"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO SHOW ALL POSSIBLE ENDPOINTS A CLIENT CAN INTERROGATE
"""


@app.get('/')
def show_endpoints():
    data = ['login', 'logout', 'channel','course','channel_subscription','course_subscription','file','message','assignment','exercise']
    return jsonify({'endpoints': data}), 200


"""
TYPE: GET
BODY: NONE
HEADER: AUTHORIZATION: Basic base64(email:password)
ENDPOINT USED IN ORDER TO DO A LOGIN GIVEN A MAIL AND A PASSWORD
"""


# LOGIN
@app.get('/login')
def login():
    try:
        token = base64.b64decode(request.headers.get('Authorization').split(' ')[1]).decode('UTF-8')
        email = token.split(":")[0]  # TODO: Dovrei sanitizzare
        password = token.split(':')[1]  # TODO: Dovrei sanitizzare
        if email is not None and password is not None:
            username: str = utils.whitespaces_remover(email)
            password: str = utils.whitespaces_remover(password)
            if len(username) > 0 and len(password) > 0:
                user_DB = user.select_user_by_email(username)
                if user_DB is not None and len(user_DB) == 1:
                    (passwordHashedDB, salt) = user.get_password_salt(username)
                    if (passwordHashedDB, salt) is not None:
                        password_hash = crypto.sha256_encode_salt(password, salt)
                        if password_hash == passwordHashedDB:
                            access_token = create_access_token(identity={'user': username, 'role': user_DB[0].role})
                            resp = jsonify({'login': True})
                            set_access_cookies(resp, access_token)
                            return resp, 200
    except Exception as e:
        print(e)
        return utils.forbidden_response()
    else:
        return utils.forbidden_response()


"""
TYPE: POST
BODY: EMAIL,PASSWORD, NAME, SURNAME, ROLE
ENDPOINT USED IN ORDER TO REGISTRATE A USER INTO THE PLATFORM
"""


@app.post('/login')
def registration():
    try:
        data = json.loads(request.data.decode(encoding='UTF-8'))
        email = data['email']  # TODO: DOVREI SANITIZZARE NAME
        password = data['password']  # TODO: DOVREI SANITIZZARE NAME
        name = data['name']  # TODO: DOVREI SANITIZZARE NAME
        surname = data['surname']  # TODO: DOVREI SANITIZZARE NAME
        role = data['role']  # TODO: DOVREI SANITIZZARE NAME
        if email is not None and password is not None and role is not None:
            username: str = utils.whitespaces_remover(email)
            password: str = utils.whitespaces_remover(password)
            if len(username) > 0 and len(password) > 0:
                check = user.select_user_by_email(username)
                if len(check) == 0:
                    (passwordHash, salt) = crypto.sha256_encode(password)
                    user.add_user_complete(username, passwordHash, salt, name, surname, role)
                    return utils.registration_response()
    except Exception as e:
        print(e)
        return utils.forbidden_response()
    else:
        return utils.forbidden_response()


"""
TYPE: GET
BODY: NONE
ENDPOINT USED BY USERS TO PERFORM A LOGOUT
"""


@app.get('/logout')
@jwt_required()
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


"""
TYPE: GET
BODY: NONE
URL: NAME OF THE CHANNEL
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
"""


@app.get('/channel/<name>')
@jwt_required()
def get_channel_courses(name):
    channel_got = channel.get_channels_by_name(name)  # TODO: DOVREI SANITIZZARE NAME
    if channel_got is not None and len(channel_got) == 1:
        courses_got = course.select_course_by_channel(channel_got[0].id)
        courses_new = [course.obj_to_dict(item) for item in courses_got]
        return jsonify(courses_new), 200
    return jsonify({'courses': []}), 403


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED IN ORDER TO ADD A NEW CHANNEL, ONLY ADMINS AND STAFF MEMBERS CAN PERFORM THIS ACTION
"""


@app.post('/channel')
@jwt_required()
def add_channel():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        name = data['channel']  # TODO: DOVREI SANITIZZARE NAME
        if name is not None:
            channel.add_channel(name)
            resp = jsonify({'response': 'ok'})
            return resp, 200
    return jsonify({'Add': 'no'}), 401


"""
TYPE: DELETE
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS IN ORDER TO REMOVE A CHANNEL
"""


@app.delete('/channel')
@jwt_required()
def remove_channel():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        name = data['channel']  # TODO: DOVREI SANITIZZARE NAME
        if name is not None:
            channel.remove_channel(name)
            resp = jsonify({'response': 'ok'})
            return resp, 200
    return jsonify({'Remove': 'no'}), 401


"""
TYPE: GET
BODY: 
URL: NAME OF THE COURSE
ENDPOINT USED IN ORDER TO GET ALL FILES AND ASSIGNMENTS OF A SPECIFIC COURSE WHICH NAME IS SPECIFIED INSIDE THE ENDOPOINT URL
"""


@app.get('/course/<name>')
@jwt_required()
def get_course_stuff(name):
    pass


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME), COURSE (COURSE NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO ADD A NEW COURSE RELATED TO A CHANNEL
"""


@app.post('/course')
@jwt_required()
def add_course():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        channel_name = data['channel']  # TODO: DOVREI SANITIZZARE NAME
        course_name = data['course']  # TODO: DOVREI SANITIZZARE NAME
        if channel_name is not None and course_name is not None:
            channel_got = channel.get_channels_by_name(channel_name)
            if channel_got is not None and len(channel_got) == 1:
                course.add_course(course_name, channel_got[0].id)
                resp = jsonify({'response': 'ok'})
                return resp, 200
    return jsonify({'Add': 'no'}), 401


"""
TYPE: DELETE
BODY: CHANNEL (CHANNEL NAME), COURSE (COURSE NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO REMOVE A NEW COURSE RELATED TO A CHANNEL
"""


@app.delete('/course')
@jwt_required()
def remove_course():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        channel_name = data['channel']  # TODO: DOVREI SANITIZZARE NAME
        course_name = data['course']  # TODO: DOVREI SANITIZZARE NAME
        if channel_name is not None and course_name is not None:
            course_got = course.select_course_by_name(course_name)
            if course_got is not None and len(course_got) == 1:
                course.remove_course(course_name, course_got[0].channel, channel_name)
                resp = jsonify({'response': 'ok'})
                return resp, 200
    return jsonify({'Add': 'no'}), 401


"""
TYPE: GET
BODY: NONE
ENDPOINT THAT RETURNS ALL CHANNEL SUBSCRIPTIONS OF THE USER WHO COMMIT THE REQUEST
"""


@app.get('/channel_subscription')
@jwt_required()
def get_channel_sub():
    username = get_jwt_identity()
    channel_sub_list = channel_sub.select_channel_subs_by_user(username['user'])
    channel_new = [channel_sub.obj_to_dict_complete(item) for item in channel_sub_list]
    resp = jsonify({'channels': channel_new})
    return resp, 200


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED BY A USER TO ADD A NEW CHANNEL SUBSCRIPTION
"""


@app.post('/channel_subscription')
@jwt_required()
def add_channel_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data['channel']  # TODO: DOVREI SANITIZZARE NAME
    if name is not None:
        channel_got = channel.get_channels_by_name(name)
        if channel_got is not None and len(channel_got) == 1:
            channel_sub.add_subscription(channel_got[0].id, username['user'])
            resp = jsonify({'response': 'ok'})
            return resp, 200
    return jsonify({'response': 'no'}), 403


"""
TYPE: DELETE
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED BY A USER TO DELETE A NEW CHANNEL SUBSCRIPTION
"""


@app.delete('/channel_subscription')
@jwt_required()
def delete_channel_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data['channel']  # TODO: DOVREI SANITIZZARE NAME
    if name is not None:
        channel_got = channel.get_channels_by_name(name)
        if channel_got is not None and len(channel_got) == 1:
            channel_sub.remove_subscription(username['user'], channel_got[0].id)
            resp = jsonify({'response': 'ok'})
            return resp, 200
    return jsonify({'response': 'no'}), 403


"""
TYPE: GET
BODY: NONE
ENDPOINT USED BY A USER TO GET ALL ITS COURSE SUBSCRIPTIONS
"""


@app.get('/course_subscription')
@jwt_required()
def get_course_sub():
    username = get_jwt_identity()
    course_sub_list = course_sub.select_course_subs_by_user(username['user'])
    course_sub_list_new = [course_sub.obj_to_dict(item) for item in course_sub_list]
    resp = jsonify({'courses': course_sub_list_new})
    return resp, 200


"""
TYPE: POST
BODY: COURSE (COURSE NAME)
ENDPOINT USED BY A USER TO ADD A NEW COURSE SUBSCRIPTION
"""


@app.post('/course_subscription')
@jwt_required()
def add_course_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data['course']
    if name is not None:
        course_got = course.select_course_by_name(name)
        if course_got is not None and len(course_got) == 1:
            course_sub.add_subscription(name, username['user'])
            resp = jsonify({'response': 'ok'})
            return resp, 200
    return jsonify({'response': 'no'}), 403


"""
TYPE: DELETE
BODY: COURSE (COURSE NAME)
ENDPOINT USED BY A USER TO REMOVE A NEW COURSE SUBSCRIPTION
"""


@app.delete('/course_subscription')
@jwt_required()
def delete_course_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    course_name = data['course']  # TODO: DOVREI SANITIZZARE course_name
    if course_name is not None:
        course_sub.remove_subscription(username['user'], course_name)
        resp = jsonify({'response': 'ok'})
        return resp, 200
    return jsonify({'response': 'no'}), 403


"""
TYPE: PUT
BODY: COURSE (COURSE NAME), CHANNEL (CHANNEL NAME)
ENDPOINT USED BY A USER TO UPLOAD A FILES RELATED TO A COURSE AND CHANNEL
"""


@app.put('/file')
@jwt_required()
def upload_file():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        course_name = data['course']
        channel_name = data['channel']
        if course_name is not None and channel_name is not None:
            course_subscription = course_sub.select_course_subs_by_user(
                username['user'])  # Check if I'm subscripted to the course I want to update the file
            channel_got = channel.get_channels_by_name(channel_name)
            course_got = course.select_course_by_name(
                course_name)  # Check if the course is linked to the channel (consistency of information)
            if channel_got is not None and len(channel_got) == 1:
                channel_subscription = channel_sub.select_channel_subs(username['user'], channel_got[
                    0].id)  # Check if I'm subscribed to the channel the course is linked
                if course_subscription is not None and channel_subscription is not None and len(
                        course_subscription) == 1 and \
                        len(channel_subscription) == 1 and course_got is not None and len(
                    course_got) == 1:  # If true then I've got the right permissions to upload it
                    files_got = request.files.getlist("file")
                    for file in files_got:
                        if file and utils.allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            files.add_file(filename, course_name, channel_name, file)
                            return jsonify({'uploaded': 'ok'}), 200
    else:
        return jsonify({'uploaded': 'no'}), 401
    return jsonify({'uploaded': 'no'}), 403


"""
TYPE: DELETE
BODY: COURSE (COURSE NAME), CHANNEL (CHANNEL NAME). FILE (FILENAME)
ENDPOINT USED BY A USER TO DELETE AN ALREADY UPLOADED FILE RELATED TO A COURSE AND CHANNEL
"""


@app.delete('/file')
@jwt_required()
def delete_file():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        course_name = data['course']
        channel_name = data['channel']
        file_name = data['file']
        if course_name is not None and channel_name is not None:
            course_subscription = course_sub.select_course_subs_by_user(
                username.user)  # Check if I'm subscripted to the course I want to update the file
            channel_got = channel.get_channels_by_name(channel_name)
            course_got = course.select_course_by_name(
                course_name)  # Check if the course is linked to the channel (consistency of information)
            if channel_got is not None and len(channel_got) == 1:
                channel_subscription = channel_sub.select_channel_subs(username.user, channel_got[
                    0].id)  # Check if I'm subscripted to the channel the course is linked
                if course_subscription is not None and channel_subscription is not None and len(
                        course_subscription) == 1 and \
                        len(channel_subscription) == 1 and course_got is not None and len(
                    course_got) == 1:  # If true then I've got the right permissions to upload it
                    file_got = files.select_file(file_name, course_name)
                    if file_got is not None and len(file_got) == 1:
                        files.remove_file(file_got[0], course_name, channel_name)
                        return jsonify({'deleted': 'ok'}), 200
    else:
        return jsonify({'deleted': 'no'}), 401
    return jsonify({'deleted': 'no'}), 403


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
"""


@app.get('/message')
@jwt_required()
def get_received_messages():
    username = get_jwt_identity()
    messages = support.select_messages_by_receiver(username['user'])
    messages_new = [support.obj_to_dict(item) for item in messages]
    return jsonify({'messages': messages_new}), 200


"""
TYPE: POST
BODY: RECEIVER (RECEIVER EMAIL), OBJECT (OBJECT MESSAGE), MESSAGE (MESSAGE CONTENT)
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
"""


@app.post('/message')
@jwt_required()
def send_message():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    receiver = data['receiver']  # TODO: DOVREI SANITIZZARE NAME
    object_message = data['object']  # TODO: DOVREI SANITIZZARE NAME
    message = data['message']  # TODO: DOVREI SANITIZZARE NAME
    if receiver is not None and object is not None and message is not None:
        support.send_message(username['user'], receiver, object_message, message)
        return jsonify({'send': 'ok'}), 200
    return jsonify({'send': 'no'}), 403


"""
TYPE: POST
BODY: NAME (ASSIGNMENT_NAME), DEADLINE (TIMESTAMP OF DEADLINE), COURSE (COURSE ASSOCIATED TO THE ASSIGNMENT)
ENDPOINT USED IN ORDER TO CREATE A NEW ASSIGNMENT
"""


@app.post('/assignment')
@jwt_required()
def add_assignment():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        name = data['name']
        year = data['year']
        month = data['month']
        day = data['day']
        hour = data['hour']
        seconds = data['seconds']
        course_got = data['course']
        if len(course.select_course_by_name(course_got)) == 1:
            assignment.add_assignment(name, year, month, day, hour, seconds, course_got)
            return jsonify({'added': 'true'}), 200
        else:
            return jsonify({'added': 'false'}), 400
    return jsonify({'added': 'false'}), 401


"""
TYPE: DELETE
BODY: 
ENDPOINT USED IN ORDER TO DELETE A NEW ASSIGNMENT
"""


@app.delete('/assignment')
@jwt_required()
def remove_assignment():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        pass



"""
TYPE: GET
BODY: ASSIGNMENT (ASSIGNMENT ID)
ENDPOINT USED IN ORDER TO GET ALL EXERCISES RELATED TO AN ASSIGNMENT
"""


@app.get('/exercise')
@jwt_required()
def get_exercises():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    assignment_id = data['assignment']
    assignment_got = assignment.get_assignments_by_id(assignment_id)
    if len(assignment_got) == 1:
        sub = course_sub.select_course_subs(username['user'],assignment_got[0].course)
        if len(sub) == 1: #I'm subscribed to that course thus I must be able to see the exercises of an assignment
            exercises = exercise.get_exercises_by_assignment(assignment_id)
            exercises_new = [exercise.obj_to_dict(item) for item in exercises]
            return jsonify({'exercises': exercises_new}),200
        else:
            return jsonify({'exercises': []}),401
    return jsonify({'exercises': []}),400



"""
TYPE: POST
BODY: 
ENDPOINT USED IN ORDER TO DELETE A NEW ASSIGNMENT
"""


@app.post('/exercise')
@jwt_required()
def create_exercise():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        quest = data['quest']
        correct = data['correct']
        assignment_el = data['assignment']
        type_el = data['type']
        if type_el == 'multiple' or type_el == 'open' or type_el == 'develop' or type_el == 'quiz':
            if 'wrong1' in data.keys() and 'wrong2' in data.keys() and 'wrong3' in data.keys():
                exercise.add_exercise_complete(quest, correct, data['wrong1'], data['wrong2'], data['wrong3'], assignment_el, type_el)
            else:
                exercise.add_exercise_uncomplete(quest, correct, assignment_el, type_el)
            return jsonify({'added': 'true'}), 200
        else:
            return jsonify({'added': 'false'}), 400
    return jsonify({'added': 'false'}), 401


"""
TYPE: PUT
BODY: FORM DATA(FILE OR TEXT, LANGUAGE, EXERCISE ID)
ENDPOINT USED IN ORDER TO UPLOAD AS USER AN ASSIGNMENT GIVEN
"""


@app.put('/exercise')
@jwt_required()
def send_exercise_develop():
    username = get_jwt_identity()
    response = jsonify({'ok': 'no'}), 400
    SIMILARITY_CONSTRAINT = 0.82
    if username['role'] == 'user':  
        language = request.form['language']
        file = request.files
        if len(file) > 0:
            program = request.files['file'].read().decode('UTF-8')
        else:
            program: str = request.form['text']
        if language is not None:
            exercise_id = request.form['exercise']
            correct = exercise.get_exercise_by_id(exercise_id)
            if len(correct) == 1:
                if language == 'Python':
                    path: str = 'dockerdata/dockerfiles/python/' + username['user']
                    res = ""
                    try:
                        if not os.path.exists(path):
                            os.mkdir(path)
                            f = open(path + "/app.py", "w")
                            f.write(program)
                            f.close()
                            res = subprocess.check_output("python3 " + path + "/app.py", stderr=subprocess.STDOUT, 
                                                        shell=True).decode('UTF-8') 
                    except subprocess.CalledProcessError as e:
                        res = e.output.decode('UTF-8')[e.output.decode('UTF-8').find('app.py'):]
                        ' '.join(res.split())
                    finally:
                        shutil.rmtree(path)
                        if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                            solution.add_solution(exercise_id, program, username['user'],True)    
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, True)
                        else:
                            solution.add_solution(exercise_id, program, username['user'],False)
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, False)
                        my_solutions = solution.get_solutions_by_name_and_exercise(username['user'], exercise_id)
                        total_number_exercises = exercise.get_exercises_by_assignment(correct[0].assignment)
                        if len(my_solutions) == len(total_number_exercises):
                            right = 0
                            for el in my_solutions:
                                if el.correct == True:
                                    right = right + 1
                            if right == 0:
                                result.add_result_without_comment(correct[0].assignment, username['user'],0)
                            else: 
                                result.add_result_without_comment(correct[0].assignment, username['user'],(right/len(total_number_exercises))*100)
                elif language == 'C':
                    path: str = 'dockerdata/dockerfiles/c/' + username['user']
                    try:
                        if not os.path.exists(path):
                            os.mkdir(path)
                            f = open(path + "/app.c", "w")
                            f.write(program.replace('>', '>\n'))
                            f.close()
                            subprocess.check_output("gcc -lstdc++ " + path + "/app.c -o " + path + "/app",
                                                    stderr=subprocess.STDOUT, shell=True)
                            res = subprocess.check_output("./" + path + "/app", stderr=subprocess.STDOUT,
                                                        shell=True).decode('UTF-8')
                    except subprocess.CalledProcessError as e:
                        response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
                    finally:
                        shutil.rmtree(path)
                        if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                            solution.add_solution(exercise_id, program, username['user'],True)    
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, True)
                        else:
                            solution.add_solution(exercise_id, program, username['user'],False)
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, False)
                        my_solutions = solution.get_solutions_by_name_and_exercise(username['user'], exercise_id)
                        total_number_exercises = exercise.get_exercises_by_assignment(correct[0].assignment)
                        if len(my_solutions) == len(total_number_exercises):
                            right = 0
                            for el in my_solutions:
                                if el.correct == True:
                                    right = right + 1
                            if right == 0:
                                result.add_result_without_comment(correct[0].assignment, username['user'],0)
                            else: 
                                result.add_result_without_comment(correct[0].assignment, username['user'],(right/len(total_number_exercises))*100) 
                elif language == 'Java':
                    path: str = 'dockerdata/dockerfiles/java/' + username['user']
                    try:
                        if not os.path.exists(path):
                            os.mkdir(path)
                            f = open(path + "/app.java", "w")
                            f.write(program.replace('\"', '"'))
                            f.close()
                            res = subprocess.check_output("java " + path + "/app.java", stderr=subprocess.STDOUT,
                                                        shell=True).decode('UTF-8')
                    except subprocess.CalledProcessError as e:
                        response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
                    finally:
                        shutil.rmtree(path)
                        if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                            solution.add_solution(exercise_id, program, username['user'],True)    
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, True)
                        else:
                            solution.add_solution(exercise_id, program, username['user'],False)
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, False)
                        my_solutions = solution.get_solutions_by_name_and_exercise(username['user'], exercise_id)
                        total_number_exercises = exercise.get_exercises_by_assignment(correct[0].assignment)
                        if len(my_solutions) == len(total_number_exercises):
                            right = 0
                            for el in my_solutions:
                                if el.correct == True:
                                    right = right + 1
                            if right == 0:
                                result.add_result_without_comment(correct[0].assignment, username['user'],0)
                            else: 
                                result.add_result_without_comment(correct[0].assignment, username['user'],(right/len(total_number_exercises))*100)
                elif language == 'C++':
                    path: str = 'dockerdata/dockerfiles/cpp/' + username['user']
                    try:
                        if not os.path.exists(path):
                            os.mkdir(path)
                            f = open(path + "/app.cpp", "w")
                            f.write(program.replace('>', '>\n'))
                            f.close()
                            subprocess.check_output("g++ " + path + "/app.cpp -o " + path + "/app",
                                                    stderr=subprocess.STDOUT, shell=True)
                            res = subprocess.check_output("./" + path + "/app", stderr=subprocess.STDOUT,
                                                        shell=True).decode('UTF-8')
                    except subprocess.CalledProcessError as e:
                        response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
                    finally:
                        shutil.rmtree(path)
                        if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                            solution.add_solution(exercise_id, program, username['user'],True)    
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, True)
                        else:
                            solution.add_solution(exercise_id, program, username['user'],False)
                            response = utils.check_integrity_solution(exercise_id, username['user'], res, correct[0].correct, False)
                        my_solutions = solution.get_solutions_by_name_and_exercise(username['user'], exercise_id)
                        total_number_exercises = exercise.get_exercises_by_assignment(correct[0].assignment)
                        if len(my_solutions) == len(total_number_exercises):
                            right = 0
                            for el in my_solutions:
                                if el.correct == True:
                                    right = right + 1
                            if right == 0:
                                result.add_result_without_comment(correct[0].assignment, username['user'],0)
                            else: 
                                result.add_result_without_comment(correct[0].assignment, username['user'],(right/len(total_number_exercises))*100)
    return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

# backend % docker run --name mariadbtest -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d docker.io/library/mariadb:10.5
# docker exec -it mariadbtest bash
