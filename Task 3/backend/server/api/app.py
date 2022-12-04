import json
import base64
import os

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, set_access_cookies, \
    unset_jwt_cookies
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_cors import CORS, cross_origin
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
import tests

# https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/

app = Flask(__name__)
cors = CORS(app, allow_headers=["Access-Control-Allow-Credentials"],supports_credentials=True, origins="localhost:8080")

UPLOAD_FOLDER = 'userdata/'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config[
    'JWT_SECRET_KEY'] = 'vnjfueofkskf'  # TODO: IN APP SERIE QUESTA ANDREBBE PORTATA FUORI DA QUI, MAGARI IN UN FILE
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = "None"
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

jwt = JWTManager(app)

"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO SHOW ALL POSSIBLE ENDPOINTS A CLIENT CAN INTERROGATE.
IT RETURNS A LIST OF AVAILABLE ENDPOINT NAMES
"""


@app.get('/')
@cross_origin()
def show_endpoints():
    data = ['login', 'logout', 'channel', 'course', 'channel_subscription', 'course_subscription', 'file', 'message',
            'assignment', 'exercise', 'solution','test','user']
    return jsonify({'endpoints': data}), 200



@app.get('/user')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_user():
    username = get_jwt_identity()
    user_got = user.select_user_by_email(username['user'])
    if len(user_got) == 1:
        userr = user_got[0]
        return jsonify({"user":user.obj_to_dict(userr)}), 200
    return jsonify({}), 401



"""
TYPE: GET
BODY: 
HEADER: 
"""


@app.get('/solution')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_open_question():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        id_assignment = data.get("assignment")
        exe_list = exercise.get_exercise_by_type_and_assignment('open', id_assignment)
        open_q = []
        for item in exe_list:
            unreviewed = solution.get_unreviewed_solution(item.id)
            for elem in unreviewed:
                open_q.append(solution.obj_to_dict_quest(elem, item.quest))
        return jsonify({"solution": open_q}), 200
    return jsonify({}), 401


"""
TYPE: POST
BODY: 
HEADER: 
"""


@app.post('/solution')
@cross_origin(supports_credentials=True)
@jwt_required()
def check_open_question():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        exercise_id = data.get('exercise')
        res = data.get('correct')
        current_ass = exercise.get_exercise_by_id(exercise_id)
        msg = data.get('comment')
        if current_ass is not None and len(current_ass) == 1:
            solution.check_solution(exercise_id, username['user'], (res=='true'))
            n_exe = exercise.get_exercises_by_assignment(current_ass[0].assignment)
            count_sol = 0
            count_correct = 0
            result_json = []
            for item in n_exe:
                db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                if len(db_sol) == 1:
                    count_sol += 1
                    if db_sol[0].correct is True:
                        count_correct += 1
            if len(n_exe) == count_sol:
                if count_correct == 0:
                    result.add_result_with_comment(current_ass[0].assignment, username["user"], 0, msg)
                    result_list = utils.get_result_assignment(username['user'],current_ass[0].assignment)
                    result_json = [result.obj_to_dict(item) for item in result_list]
                else:
                    result.add_result_with_comment(current_ass[0].assignment, username["user"],
                                                   int((count_correct / len(n_exe)) * 100), msg)
                    result_list = utils.get_result_assignment(username['user'],current_ass[0].assignment)
                    result_json = [result.obj_to_dict(item) for item in result_list]
            return jsonify({"results": result_json}), 200
    return jsonify({"added": "False"}), 401




"""
TYPE: GET
BODY: NONE
HEADER: AUTHORIZATION: Basic base64(email:password)
ENDPOINT USED IN ORDER TO DO A LOGIN GIVEN A MAIL AND A PASSWORD.
IT SETS A COOKIE IS LOGIN IS SUCCESSFUL
"""


# LOGIN
@app.get('/login')
@cross_origin(supports_credentials=True)
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
                            #resp.set_cookie('access_token_cookie',access_token, path='/', samesite="None", secure=True, domain='127.0.0.1')
                            return resp, 200
    except Exception as e:
        print(e)
        return utils.forbidden_response()
    else:
        return utils.forbidden_response()


"""
TYPE: POST
BODY: json(email,password, name, surname, role)
ENDPOINT USED IN ORDER TO REGISTRATE A USER INTO THE PLATFORM
"""


@app.post('/login')
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
@jwt_required()
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL COURSES
"""


@app.get('/course')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_courses():
    course_got = course.select_all()
    course_ap = []
    for item in course_got:
        course_ap.append(course.obj_to_dict(item))
    return jsonify({"courses": course_ap}), 200


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL CHANNELS
"""


@app.get('/channel')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_channels():
    channels_got = channel.selectAll()
    channels_new = [channel.obj_to_dict(item) for item in channels_got]
    return jsonify({"channels": channels_new}), 200


"""
TYPE: GET
BODY: NONE
URL: NAME OF THE CHANNEL
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
"""


@app.get('/channel/<name>')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_channel_courses(name):
    username = get_jwt_identity()
    channel_got = channel.get_channels_by_name(name)  # TODO: DOVREI SANITIZZARE NAME
    if channel_got is not None and len(channel_got) == 1:
        channel_subcr = channel_sub.select_channel_subs(username['user'],channel_got[0].id)
        if channel_subcr is not None and len(channel_subcr) == 1:
            courses_got = course.select_course_by_channel(channel_got[0].id)
            courses_new = [course.obj_to_dict(item) for item in courses_got]
        else:
            return jsonify({'courses': []}), 401
        return jsonify(courses_new), 200
    return jsonify({'courses': []}), 403


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED IN ORDER TO ADD A NEW CHANNEL, ONLY ADMINS AND STAFF MEMBERS CAN PERFORM THIS ACTION
"""


@app.post('/channel')
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
@jwt_required()
def get_course_stuff(name):
    username = get_jwt_identity()
    name_user = username["user"]
    if len(course_sub.select_course_subs(name_user, name)) == 1:
        ass_list = assignment.get_assignments_by_course(name)
        ass_done = assignment.get_assignments_by_course_done(name)
        file_list = files.select_files_by_course(name)
        ass_ret = []
        file_ret = []
        ass_done_new = [assignment.obj_to_dict(item) for item in ass_done]
        for el in ass_list:
            for el2 in ass_done:
                if el.name == el2.name:
                    ass_list.remove(el)
        for item in ass_list:
            ass_ret.append(assignment.obj_to_dict(item))
        for item in file_list:
            file_ret.append(files.obj_to_dict(item))
        return jsonify({"assignments_remaining": ass_ret, "files": file_ret, "assignment_done":ass_done_new}), 200
    return jsonify({}), 401


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME), COURSE (COURSE NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO ADD A NEW COURSE RELATED TO A CHANNEL
"""


@app.post('/course')
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
@jwt_required()
def upload_file():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        course_name = request.form['course']
        channel_name = request.form['channel']
        if course_name is not None and channel_name is not None:
            # Check if I'm subscripted to the course I want to update the file
            course_subscription = course_sub.select_course_subs_by_user(username['user'])  
            channel_got = channel.get_channels_by_name(channel_name)
            # Check if the course is linked to the channel (consistency of information)
            course_got = course.select_course_by_name(course_name)
            if channel_got is not None and len(channel_got) == 1:
                # Check if I'm subscribed to the channel the course is linked
                channel_subscription = channel_sub.select_channel_subs(username['user'], channel_got[0].id) 
                if course_subscription is not None and channel_subscription is not None and len(course_subscription) == 1 and len(channel_subscription) == 1 and course_got is not None and len(course_got) == 1:  # If true then I've got the right permissions to upload it
                    files_got = request.files.getlist("file")
                    for file in files_got:
                        if file and utils.allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            if files.add_file(filename, course_name, channel_name, file):
                                return jsonify({'uploaded': 'ok'}), 200
                            else:
                                return jsonify({'uploaded': 'false'}), 403
    else:
        return jsonify({'uploaded': 'no'}), 401
    return jsonify({'uploaded': 'no'}), 403


"""
TYPE: DELETE
BODY: COURSE (COURSE NAME), CHANNEL (CHANNEL NAME). FILE (FILENAME)
ENDPOINT USED BY A USER TO DELETE AN ALREADY UPLOADED FILE RELATED TO A COURSE AND CHANNEL
"""


@app.delete('/file')
@cross_origin(supports_credentials=True)
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
                username['user'])  # Check if I'm subscripted to the course I want to update the file
            channel_got = channel.get_channels_by_name(channel_name)
            course_got = course.select_course_by_name(
                course_name)  # Check if the course is linked to the channel (consistency of information)
            if channel_got is not None and len(channel_got) == 1:
                channel_subscription = channel_sub.select_channel_subs(username['user'], channel_got[
                    0].id)  # Check if I'm subscripted to the channel the course is linked
                if course_subscription is not None and channel_subscription is not None and len(
                        course_subscription) == 1 and \
                        len(channel_subscription) == 1 and course_got is not None and len(
                    course_got) == 1:  # If true then I've got the right permissions to upload it
                    file_got = files.select_file(file_name, course_name)
                    if file_got is not None and len(file_got) == 1:
                        if files.remove_file(file_name, course_name, channel_name):
                            return jsonify({'deleted': 'ok'}), 200
                        else:
                            return jsonify({'deleted': 'false'}), 404
    else:
        return jsonify({'deleted': 'no'}), 401
    return jsonify({'deleted': 'no'}), 403


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL RECEIVED MESSAGES OF AN AUTHENTICATED USER
"""


@app.get('/message')
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
        minutes = data['minutes']
        course_got = data['course']
        if len(course.select_course_by_name(course_got)) == 1:
            resp = assignment.add_assignment(name, year, month, day, hour, minutes, course_got)
            if resp[0] == True:
                return jsonify({'added': assignment.obj_to_dict(resp[1])}), 200
            else:
                return jsonify({'added': 'false'}), 400
        else:
            return jsonify({'added': 'false'}), 400
    return jsonify({'added': 'false'}), 401


"""
TYPE: DELETE
BODY: 
ENDPOINT USED IN ORDER TO DELETE A NEW ASSIGNMENT
"""


@app.delete('/assignment/<id>')
@cross_origin(supports_credentials=True)
@jwt_required()
def remove_assignment(id):
    username = get_jwt_identity()
    if username['role'] == 'admin':
        assignment.remove_assignment(id)
        return jsonify({'removed':True}),200
    return jsonify({'removed':False}),401


"""
TYPE: GET
BODY: ASSIGNMENT (ASSIGNMENT ID)
ENDPOINT USED IN ORDER TO GET ALL EXERCISES RELATED TO AN ASSIGNMENT
"""


@app.get('/exercise/<id>')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_exercises(id):
    username = get_jwt_identity()
    assignment_got = assignment.get_assignments_by_id(id)
    if len(assignment_got) == 1:
        sub = course_sub.select_course_subs(username['user'], assignment_got[0].course)
        if len(sub) == 1:  # I'm subscribed to that course thus I must be able to see the exercises of an assignment
            exercises = exercise.get_exercises_by_assignment(id)
            exercises_new = [exercise.obj_to_dict(item) for item in exercises]
            return jsonify({'exercises': exercises_new}), 200
        else:
            return jsonify({'exercises': []}), 401
    return jsonify({'exercises': []}), 400


"""
URL: /exercise
TYPE: POST
BODY: json(quest,correct,assignment,type) OR json(quest,correct,assignment,type,wrong1,wrong2,wrong3)
ENDPOINT USED IN ORDER TO ADD A NEW EXERCISE
"""


@app.post('/exercise')
@cross_origin(supports_credentials=True)
@jwt_required()
def create_exercise():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        quest = data['quest']
        correct = data.get('correct')
        assignment_el = data['assignment']
        type_el = data['type']
        if type_el == 'multiple' or type_el == 'open' or type_el == 'develop' or type_el == 'quiz':
            if 'wrong1' in data.keys() and 'wrong2' in data.keys() and 'wrong3' in data.keys():
                exercise.add_exercise_complete(quest, correct, data['wrong1'], data['wrong2'], data['wrong3'],
                                               assignment_el, type_el)
            else:
                resp = exercise.add_exercise_uncomplete(quest, correct, assignment_el, type_el)
                if resp[0] == True:
                    return jsonify({'added': exercise.obj_to_dict(resp[1])}), 200
                else:
                    return jsonify({'added': 'false'}), 400
        else:
            return jsonify({'added': 'false'}), 400
    return jsonify({'added': 'false'}), 401


"""
TYPE: PUT
BODY: FORM DATA(FILE OR TEXT, LANGUAGE, EXERCISE ID)
ENDPOINT USED IN ORDER TO UPLOAD AS USER AN ASSIGNMENT GIVEN
"""


@app.put('/exercise')
@cross_origin(supports_credentials=True)
@jwt_required()
def send_exercise_develop():
    username = get_jwt_identity()
    response = jsonify({'ok': 'no'}), 400
    SIMILARITY_CONSTRAINT = 0.82
    if username['role'] == 'admin': #TODO: USER 
        form = request.form.to_dict()
        print(form)
        type = request.form['type']
        result_json = []
        if type == "develop":
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
                    if language.upper() == 'PYTHON':
                        path: str = 'dockerdata/dockerfiles/python/' + username['user']
                        res = ""
                        res_list = []
                        tests_to_perform = []
                        error = ""
                        try:
                            if not os.path.exists(path):
                                os.mkdir(path)
                                f = open(path + "/app.py", "w")
                                f.write(program)
                                f.close()
                                tests_to_perform = tests.get_tests_by_exercise(exercise_id)
                                if len(tests_to_perform) == 0:
                                    res = subprocess.check_output("python3 " + path + "/app.py", stderr=subprocess.STDOUT, 
                                                              shell=True).decode('UTF-8')
                                else:
                                    for test in tests_to_perform:
                                        resu = subprocess.check_output("python3 " + path + "/app.py "+test.given_value, stderr=subprocess.STDOUT, 
                                                              shell=True).decode('UTF-8')
                                        if utils.similar(resu.replace('\r','').strip(), test.expected) > SIMILARITY_CONSTRAINT:
                                            res_list.append((True,resu.replace('\r','').strip(),test.expected, test.name))
                                        else:
                                            res_list.append((False,resu.replace('\r','').strip(),test.expected, test.name))
                        except subprocess.CalledProcessError as e:
                            error = e.output.decode('UTF-8')[e.output.decode('UTF-8').find('app.py'):]
                            ' '.join(error.split())
                        finally:
                            shutil.rmtree(path)
                            res = res.replace('\r','').strip()
                            if len(tests_to_perform) == 0:
                                if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                                    solution.add_solution(exercise_id, program, username['user'], True, True)
                                else:
                                    solution.add_solution(exercise_id, program, username['user'], False, True)                                    
                            else:
                                if error == "":
                                    flag_passed = True 
                                    for element in res_list:
                                        if element[0] == False:
                                            flag_passed = False
                                else:
                                    flag_passed = False
                                solution.add_solution(exercise_id, program, username['user'], flag_passed, True)
                            similar = utils.check_integrity_solution(exercise_id, username['user'])
                            n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
                            count_sol = 0
                            count_correct = 0
                            for item in n_exe:
                                db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                                if len(db_sol) == 1:
                                    count_sol += 1
                                    if db_sol[0].correct is True:
                                        count_correct += 1
                            if len(n_exe) == count_sol:
                                if count_correct == 0:
                                    result.add_result_without_comment(correct[0].assignment, username["user"], 0)
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                                else:
                                    result.add_result_without_comment(correct[0].assignment, username["user"],
                                                                    int((count_correct / len(n_exe)) * 100))
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                            if len(tests_to_perform) == 0:
                                response = jsonify({"results": result_json,"given": res,"expected":correct[0].correct, "correct":db_sol[0].correct, "similar_responses":similar, "error":error}), 200
                            else:
                                response = jsonify({"results": result_json,"tests":res_list, "similar_responses":similar,"error":error}), 200  
                    elif language.upper() == 'C':
                        path: str = 'dockerdata/dockerfiles/c/' + username['user']
                        res = ""
                        res_list = []
                        tests_to_perform = []
                        error = ""
                        try:
                            if not os.path.exists(path):
                                os.mkdir(path)
                                f = open(path + "/app.c", "w")
                                f.write(program.replace('>', '>\n'))
                                f.close()
                                subprocess.check_output("gcc -lstdc++ " + path + "/app.c -o " + path + "/app",
                                                        stderr=subprocess.STDOUT, shell=True)
                                tests_to_perform = tests.get_tests_by_exercise(exercise_id)
                                if len(tests_to_perform) == 0:
                                    res = subprocess.check_output("./" + path + "/app", stderr=subprocess.STDOUT,
                                                              shell=True).decode('UTF-8')
                                else:
                                    for test in tests_to_perform:
                                        resu = subprocess.check_output("./ " + path + "/app "+test.given_value, stderr=subprocess.STDOUT,
                                                              shell=True).decode('UTF-8') 
                                        if utils.similar(resu.replace('\r','').strip(), test.expected) > SIMILARITY_CONSTRAINT:
                                            res_list.append((True,resu.replace('\r','').strip(),test.expected, test.name))
                                        else:
                                            res_list.append((False,resu.replace('\r','').strip(),test.expected, test.name))
                        except subprocess.CalledProcessError as e:
                            #response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
                            error = str(e.output)
                        finally:
                            shutil.rmtree(path)
                            res = res.replace('\r','').strip()
                            if len(tests_to_perform) == 0:
                                if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                                    solution.add_solution(exercise_id, program, username['user'], True, True)
                                else:
                                    solution.add_solution(exercise_id, program, username['user'], False, True)                                    
                            else:
                                if error == "":
                                    flag_passed = True 
                                    for element in res_list:
                                        if element[0] == False:
                                            flag_passed = False
                                else:
                                    flag_passed = False
                                solution.add_solution(exercise_id, program, username['user'], flag_passed, True)
                            similar = utils.check_integrity_solution(exercise_id, username['user'])
                            n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
                            count_sol = 0
                            count_correct = 0
                            for item in n_exe:
                                db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                                if len(db_sol) == 1:
                                    count_sol += 1
                                    if db_sol[0].correct is True:
                                        count_correct += 1
                            if len(n_exe) == count_sol:
                                if count_correct == 0:
                                    result.add_result_without_comment(correct[0].assignment, username["user"], 0)
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                                else:
                                    result.add_result_without_comment(correct[0].assignment, username["user"],
                                                                    int((count_correct / len(n_exe)) * 100))
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                            if len(tests_to_perform) == 0:
                                response = jsonify({"results": result_json,"given": res,"expected":correct[0].correct, "correct":db_sol[0].correct, "similar_responses":similar, "error":error}), 200
                            else:
                                response = jsonify({"results": result_json,"tests":res_list, "similar_responses":similar,"error":error}), 200  
                    elif language.upper() == 'JAVA':
                        path: str = 'dockerdata/dockerfiles/java/' + username['user']
                        res = ""
                        res_list = []
                        tests_to_perform = []
                        error = ""
                        try:
                            if not os.path.exists(path):
                                os.mkdir(path)
                                f = open(path + "/app.java", "w")
                                f.write(program.replace('\"', '"'))
                                f.close()
                                tests_to_perform = tests.get_tests_by_exercise(exercise_id)
                                if len(tests_to_perform) == 0:
                                    res = subprocess.check_output("java " + path + "/app.java", stderr=subprocess.STDOUT,
                                                              shell=True).decode('UTF-8')
                                else:
                                    for test in tests_to_perform:
                                        resu = subprocess.check_output("java " + path + "/app.java "+test.given_value, stderr=subprocess.STDOUT, #TODO: CAMBIARE IN PYTHON3
                                                              shell=True).decode('UTF-8') 
                                        if utils.similar(resu.replace('\r','').strip(), test.expected) > SIMILARITY_CONSTRAINT:
                                            res_list.append((True,resu.replace('\r','').strip(),test.expected, test.name))
                                        else:
                                            res_list.append((False,resu.replace('\r','').strip(),test.expected, test.name))
                        except subprocess.CalledProcessError as e:
                            print(e.output)
                            error = str(e.output.decode('UTF-8') )
                        finally:
                            shutil.rmtree(path)
                            res = res.replace('\r','').strip()
                            if len(tests_to_perform) == 0:
                                if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                                    solution.add_solution(exercise_id, program, username['user'], True, True)
                                else:
                                    solution.add_solution(exercise_id, program, username['user'], False, True)                                    
                            else:
                                if error == "":
                                    flag_passed = True 
                                    for element in res_list:
                                        if element[0] == False:
                                            flag_passed = False
                                else:
                                    flag_passed = False  
                                solution.add_solution(exercise_id, program, username['user'], flag_passed, True)
                            similar = utils.check_integrity_solution(exercise_id, username['user'])
                            n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
                            count_sol = 0
                            count_correct = 0
                            for item in n_exe:
                                db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                                if len(db_sol) == 1:
                                    count_sol += 1
                                    if db_sol[0].correct is True:
                                        count_correct += 1
                            if len(n_exe) == count_sol:
                                if count_correct == 0:
                                    result.add_result_without_comment(correct[0].assignment, username["user"], 0)
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                                else:
                                    result.add_result_without_comment(correct[0].assignment, username["user"],
                                                                    int((count_correct / len(n_exe)) * 100))
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                            if len(tests_to_perform) == 0:
                                response = jsonify({"results": result_json,"given": res,"expected":correct[0].correct, "correct":db_sol[0].correct, "similar_responses":similar, "error":error}), 200
                                ' '.join(response.split())
                            else:
                                response = jsonify({"results": result_json,"tests":res_list, "similar_responses":similar, "error":error}), 200  
                    elif language.upper() == 'C++':
                        path: str = 'dockerdata/dockerfiles/cpp/' + username['user']
                        res = ""
                        res_list = []
                        tests_to_perform = []
                        error = ""
                        try:
                            if not os.path.exists(path):
                                os.mkdir(path)
                                f = open(path + "/app.cpp", "w")
                                f.write(program.replace('>', '>\n'))
                                f.close()
                                subprocess.check_output("g++ " + path + "/app.cpp -o " + path + "/app",
                                                        stderr=subprocess.STDOUT, shell=True)
                                tests_to_perform = tests.get_tests_by_exercise(exercise_id)
                                if len(tests_to_perform) == 0:
                                    res = subprocess.check_output("./" + path + "/app", stderr=subprocess.STDOUT,
                                                              shell=True).decode('UTF-8')
                                else:
                                    for test in tests_to_perform:
                                        resu = subprocess.check_output("./" + path + "/app "+test.given_value, stderr=subprocess.STDOUT, #TODO: CAMBIARE IN PYTHON3
                                                              shell=True).decode('UTF-8') 
                                        if utils.similar(resu.replace('\r','').strip(), test.expected) > SIMILARITY_CONSTRAINT:
                                            res_list.append((True,resu.replace('\r','').strip(),test.expected, test.name))
                                        else:
                                            res_list.append((False,resu.replace('\r','').strip(),test.expected, test.name))
                        except subprocess.CalledProcessError as e:
                            #response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
                            error = str(e.output)
                        finally:
                            shutil.rmtree(path)
                            res = res.replace('\r','').strip()
                            if len(tests_to_perform) == 0:
                                if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
                                    solution.add_solution(exercise_id, program, username['user'], True, True)
                                else:
                                    solution.add_solution(exercise_id, program, username['user'], False, True)                                    
                            else:
                                if error == "":
                                    flag_passed = True 
                                    for element in res_list:
                                        if element[0] == False:
                                            flag_passed = False
                                else:
                                    flag_passed = False  
                                solution.add_solution(exercise_id, program, username['user'], flag_passed, True)
                            similar = utils.check_integrity_solution(exercise_id, username['user'])
                            n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
                            count_sol = 0
                            count_correct = 0
                            for item in n_exe:
                                db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                                if len(db_sol) == 1:
                                    count_sol += 1
                                    if db_sol[0].correct is True:
                                        count_correct += 1
                            if len(n_exe) == count_sol:
                                if count_correct == 0:
                                    result.add_result_without_comment(correct[0].assignment, username["user"], 0)
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                                else:
                                    result.add_result_without_comment(correct[0].assignment, username["user"],
                                                                    int((count_correct / len(n_exe)) * 100))
                                    result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                                    result_json = [result.obj_to_dict(item) for item in result_list]
                            if len(tests_to_perform) == 0:
                                response = jsonify({"results": result_json,"given": res,"expected":correct[0].correct, "correct":db_sol[0].correct, "similar_responses":similar, "error":error}), 200
                                ' '.join(response.split())
                            else:
                                response = jsonify({"results": result_json,"tests":res_list, "similar_responses":similar, "error":error}), 200  
        elif type == "quiz":
            answer = request.form['text']
            exe = request.form['exercise']
            exe_db = exercise.get_exercise_by_id(exe)
            if exe_db is not None and len(exe_db) == 1:
                if answer == exe_db[0].correct:
                    solution.add_solution(exe, answer, username["user"], True, True)
                else:
                    solution.add_solution(exe, answer, username["user"], False, True)
                n_exe = exercise.get_exercises_by_assignment(exe_db[0].assignment)
                count_sol = 0
                count_correct = 0
                for item in n_exe:
                    db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                    if len(db_sol) == 1:
                        count_sol += 1
                        if db_sol[0].correct is True:
                            count_correct += 1
                if len(n_exe) == count_sol:
                    if count_correct == 0:
                        result.add_result_without_comment(exe_db[0].assignment, username["user"], 0)
                        result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                        result_json = [result.obj_to_dict(item) for item in result_list]
                    else:
                        result.add_result_without_comment(exe_db[0].assignment, username["user"],
                                                          int((count_correct / len(n_exe)) * 100))
                        result_list = utils.get_result_assignment(username['user'],correct[0].assignment)
                        result_json = [result.obj_to_dict(item) for item in result_list]
                response = jsonify({"results": result_json,"given": answer,"expected":exe_db[0].correct}), 200
            else:
                response = jsonify({}), 401
        elif type == "open":
            answer = request.form['text']
            exe = request.form['exercise']
            exe_db = exercise.get_exercise_by_id(exe)
            if exe_db is not None and len(exe_db) == 1:
                solution.add_solution_open(exe, answer, username["user"], False)
                n_exe = exercise.get_exercises_by_assignment(exe_db[0].assignment)
                count_sol = 0
                for item in n_exe:
                    db_sol = solution.get_solutions_by_name_and_exercise(username["user"], item.id, True)
                    if len(db_sol) == 1:
                        count_sol += 1
                response = jsonify({"added": "True"}), 200
            else:
                response = jsonify({}), 401
        else:
            response = jsonify({}), 400
    else:
        response = jsonify({}), 401
    return response




"""
TYPE: GET
BODY: json(exercise)  WHERE exercise=EXERCISE_ID
ENDPOINT USED IN ORDER TO GET TESTS OF AN EXERCISE
"""


@app.get('/test')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_test():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    exercise = data.get('exercise')
    if exercise is not None:
        tests_got = tests.get_tests_by_exercise(exercise)
        tests_json = [tests.obj_to_dict(item) for item in tests_got] 
        return jsonify({'tests': tests_json}), 200 
    else:
         return jsonify({'added': False}), 403

"""
TYPE: POST
BODY: json(name,exercise,parameter,expected) or json(name,comment,exercise,parameter,expected) WHERE name=NAME_OF_THE_TEST, exercise=EXERCISE_ID, parameter = PARAMETER OF THE FUNCTION TO TEST, comment=DESCRIPTION_OF_THE_TEST, expected = EXPECTED VALUE 
ENDPOINT USED IN ORDER TO ADD A TEST FOR A EXERCISE
"""


@app.post('/test')
@cross_origin(supports_credentials=True)
@jwt_required()
def add_test():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    exercise = data.get('exercise')
    name = data.get('name')
    parameter = data.get('parameter')
    comment = data.get('comment')
    expected = data.get('expected')
    if exercise is not None and name is not None and parameter is not None and expected is not None:
        if comment is not None:
            if tests.add_test_complete(name,comment, exercise,parameter,expected) == True:
                return jsonify({'added': True }), 200
            else:
                return jsonify({'added': False}), 403   
        else:
            if tests.add_test_uncomplete(name,exercise,parameter,expected) == True:
                return jsonify({'added': True}), 200
            else:
                return jsonify({'added': False}), 403 
    else:
        return jsonify({'added': False}), 403




@app.get('/result/<id>')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_results(id):
    username = get_jwt_identity()
    result_assignments = result.get_results_by_assignment_user(id,username['user'])
    result_json = [result.obj_to_dict(item) for item in result_assignments]
    return jsonify({'result': result_json}), 200


if __name__ == '__main__':
    if not os.path.exists('dockerdata'):
        os.mkdir('dockerdata')
        os.mkdir('dockerdata/dockerfiles')
        os.mkdir('dockerdata/dockerfiles/c')
        os.mkdir('dockerdata/dockerfiles/cpp')
        os.mkdir('dockerdata/dockerfiles/java')
        os.mkdir('dockerdata/dockerfiles/python')
    if not os.path.exists('userdata'):
        os.mkdir('userdata')
    app.run(host='0.0.0.0', debug=True, port=5000)

# backend % docker run --name mariadbtest -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d docker.io/library/mariadb:10.5
# docker exec -it mariadbtest bash
