import json
import base64
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, \
    unset_jwt_cookies
from datetime import timedelta
from flask_cors import CORS, cross_origin
import requests
from url import *

app = Flask(__name__)
cors = CORS(app, allow_headers=["Access-Control-Allow-Credentials"],supports_credentials=True, origins="localhost:8080") 

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_SECRET_KEY'] = 'vnjfueofkskf'  # TODO: IN APP SERIE QUESTA ANDREBBE PORTATA FUORI DA QUI, MAGARI IN UN FILE
app.config['JWT_COOKIE_SECURE'] = True 
app.config['JWT_COOKIE_SAMESITE'] = "None" 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
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


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL INFORMATION ABOUT THE USER WHO SENT THE REQUEST
"""

#FATTO
@app.get('/user')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_user():
    username = get_jwt_identity()
    if username is not None and len(username) > 0:
        response = requests.get((URL_USER+"/"+username['user']).strip())
        return response.content,response.status_code
    else:
        return jsonify({}), 401



"""
TYPE: GET
BODY: 
HEADER: 
"""

#FATTO
@app.get('/solution')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_open_question():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        id_assignment = data.get("assignment")
        if id_assignment is not None:
            response = requests.get((URL_SOLUTION+"/"+id_assignment).strip())
            return response.content,response.status_code
    return jsonify({}), 401


"""
TYPE: POST
BODY: 
HEADER: 
"""

#FATTO
@app.post('/solution')
@cross_origin(supports_credentials=True) 
@jwt_required()
def check_open_question():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        exercise_id = data.get('exercise')
        res = data.get('correct')
        msg = data.get('comment')
        if exercise_id is not None: 
            response = requests.post((URL_SOLUTION).strip(),data={"exercise_id":exercise_id,"res":res,"msg":msg, "username":username['user']})
            return response.content, response.status_code
    return jsonify({"added": "False"}), 401




"""
TYPE: GET
BODY: NONE
HEADER: AUTHORIZATION: Basic base64(email:password)
ENDPOINT USED IN ORDER TO DO A LOGIN GIVEN A MAIL AND A PASSWORD.
IT SETS A COOKIE IS LOGIN IS SUCCESSFUL
"""

#FATTO
@app.get('/login')
@cross_origin(supports_credentials=True) 
def login():
    try:
        token = base64.b64decode(request.headers.get('Authorization').split(' ')[1]).decode('UTF-8')
        response = requests.get((URL_LOGIN+"/"+token).strip())
        json_received = json.loads(response.content) 
        if json_received['logged'] == True:
            access_token = create_access_token(identity={'user': json_received['user'], 'role':json_received['role']})
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            return resp, 200            
    except Exception as e:
        print(e)
        return jsonify({'login': False}),500
    else:
        return jsonify({'login': False}),403


"""
TYPE: POST
BODY: json(email,password, name, surname, role)
ENDPOINT USED IN ORDER TO REGISTRATE A USER INTO THE PLATFORM
"""

#FATTO
@app.post('/login')
@cross_origin(supports_credentials=True)
def registration():
    try:
        data = json.loads(request.data.decode(encoding='UTF-8'))
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        role = data.get('role')
        if email is not None and password is not None and role is not None:
            response = requests.post((URL_LOGIN).strip(),json={"email":email,"password":password,"name":name,"surname":surname,"role":role},headers={'Content-type':'application/json'})
            return response.content,response.status_code
    except Exception as e:
        return jsonify({'registered': False}),500
    else:
        return jsonify({'registered': False}),403


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
ENDPOINT USED IN ORDER TO GET ALL CHANNELS
"""


#FATTO
@app.get('/channel')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_channels():
    response = requests.get((URL_CHANNEL).strip())
    return response.content,response.status_code


"""
TYPE: GET
BODY: NONE
URL: NAME OF THE CHANNEL
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
"""

#FATTO
@app.get('/channel/<name>')
@cross_origin(supports_credentials=True)  
@jwt_required()
def get_channel_courses(name):
    username = get_jwt_identity()
    response = requests.get((URL_CHANNEL+"/"+name+"/"+username['user']+"/"+username['role']).strip())
    return response.content,response.status_code


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED IN ORDER TO ADD A NEW CHANNEL, ONLY ADMINS AND STAFF MEMBERS CAN PERFORM THIS ACTION
"""

#FATTO
@app.post('/channel')
@cross_origin(supports_credentials=True) 
@jwt_required()
def add_channel():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        name = data.get('channel')  
        if name is not None:
            response = requests.post((URL_CHANNEL).strip(),json={"channel":name})
            return response.content,response.status_code
    return jsonify({'Add': 'no'}), 401


"""
TYPE: DELETE
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS IN ORDER TO REMOVE A CHANNEL
"""

#FATTO
@app.delete('/channel')
@cross_origin(supports_credentials=True) 
@jwt_required()
def remove_channel():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        name = data.get('channel')  # TODO: DOVREI SANITIZZARE NAME
        if name is not None:
            response = requests.delete((URL_CHANNEL+"/"+name).strip())
            return response.content,response.status_code
    return jsonify({'Remove': 'no'}), 401


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL COURSES
"""

#FATTO
@app.get('/course')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_courses():
    response = requests.get((URL_COURSE).strip())
    return response.content,response.status_code


"""
TYPE: GET
BODY: 
URL: NAME OF THE COURSE
ENDPOINT USED IN ORDER TO GET ALL FILES AND ASSIGNMENTS OF A SPECIFIC COURSE WHICH NAME IS SPECIFIED INSIDE THE ENDOPOINT URL
"""

#FATTO
@app.get('/course/<name>')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_course_stuff(name):
    username = get_jwt_identity()
    response = requests.get((URL_COURSE+"/"+name+"/"+username["user"]).strip())
    return response.content,response.status_code


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME), COURSE (COURSE NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO ADD A NEW COURSE RELATED TO A CHANNEL
"""

#FATTO
@app.post('/course')
@cross_origin(supports_credentials=True)
@jwt_required()
def add_course():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        channel_name = data.get('channel')
        course_name = data.get('course')
        if channel_name is not None and course_name is not None:
            response = requests.post((URL_COURSE).strip(),json={"channel":channel_name, "course":course_name})
            return response.content,response.status_code
    return jsonify({'Add': 'no'}), 401


"""
TYPE: DELETE
BODY: CHANNEL (CHANNEL NAME), COURSE (COURSE NAME)
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO REMOVE A NEW COURSE RELATED TO A CHANNEL
"""

#FATTO
@app.delete('/course')
@cross_origin(supports_credentials=True) 
@jwt_required()
def remove_course():
    username = get_jwt_identity()
    if username['role'] == 'staff' or username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        channel_name = data.get('channel')
        course_name = data.get('course')
        if channel_name is not None and course_name is not None:
            response = requests.delete((URL_COURSE+"/"+channel_name+"/"+course_name).strip())
            return response.content,response.status_code
    return jsonify({'Add': 'no'}), 401


"""
TYPE: GET
BODY: NONE
ENDPOINT THAT RETURNS ALL CHANNEL SUBSCRIPTIONS OF THE USER WHO COMMIT THE REQUEST
"""

#FATTO
@app.get('/channel_subscription')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_channel_sub():
    username = get_jwt_identity()
    response = requests.get((URL_CHANNEL_SUB+"/"+username["user"]).strip())
    return response.content, response.status_code


"""
TYPE: POST
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED BY A USER TO ADD A NEW CHANNEL SUBSCRIPTION
"""

#FATTO
@app.post('/channel_subscription')
@cross_origin(supports_credentials=True) 
@jwt_required()
def add_channel_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data.get('channel')  
    if name is not None:
        response = requests.post((URL_CHANNEL_SUB).strip(),json={"username":username['user'],"name":name},headers={'Content-type':'application/json'})
        return response.content,response.status_code
    return jsonify({'response': 'no'}), 403


"""
TYPE: DELETE
BODY: CHANNEL (CHANNEL NAME)
ENDPOINT USED BY A USER TO DELETE A NEW CHANNEL SUBSCRIPTION
"""

#FATTO
@app.delete('/channel_subscription')
@cross_origin(supports_credentials=True) 
@jwt_required()
def delete_channel_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data.get('channel') 
    if name is not None:
         response = requests.delete((URL_CHANNEL_SUB).strip(),json={"username":username['user'],"name":name},headers={'Content-type':'application/json'})
         return response.content,response.status_code
    return jsonify({'response': 'no'}), 403


"""
TYPE: GET
BODY: NONE
ENDPOINT USED BY A USER TO GET ALL ITS COURSE SUBSCRIPTIONS
"""

#FATTO
@app.get('/course_subscription')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_course_sub():
    username = get_jwt_identity()
    response = requests.get((URL_COURSE_SUB+"/"+username["user"]).strip())
    return response.content, response.status_code


"""
TYPE: POST
BODY: COURSE (COURSE NAME) 
ENDPOINT USED BY A USER TO ADD A NEW COURSE SUBSCRIPTION
"""

#FATTO
@app.post('/course_subscription')
@cross_origin(supports_credentials=True) 
@jwt_required()
def add_course_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data.get('course')
    if name is not None:
        response = requests.post((URL_COURSE_SUB).strip(),json={"username":username['user'],"name":name},headers={'Content-type':'application/json'})
        return response.content,response.status_code
    return jsonify({'response': 'no'}), 403


"""
TYPE: DELETE
BODY: COURSE (COURSE NAME)
ENDPOINT USED BY A USER TO REMOVE A NEW COURSE SUBSCRIPTION
"""

#FATTO
@app.delete('/course_subscription')
@cross_origin(supports_credentials=True) 
@jwt_required()
def delete_course_sub():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    course_name = data.get('course')  
    if course_name is not None:
        response = requests.delete((URL_COURSE_SUB).strip(),json={"username":username['user'],"name":course_name}, headers={'Content-type':'application/json'})
        return response.content,response.status_code
    return jsonify({'response': 'no'}), 403


"""
TYPE: PUT
BODY: COURSE (COURSE NAME), CHANNEL (CHANNEL NAME)
ENDPOINT USED BY A USER TO UPLOAD A FILES RELATED TO A COURSE AND CHANNEL
"""

#FATTO
@app.put('/file')
@cross_origin(supports_credentials=True)
@jwt_required()
def upload_file():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        response = requests.put(URL_FILE+"/"+username['user'],data=request.form, headers={'Content-Type':'multipart/form-data'},files=request.files.getlist("file"))
        return response.content, response.status_code
    else:
        return jsonify({'uploaded': 'no'}), 403


"""
TYPE: DELETE
BODY: COURSE (COURSE NAME), CHANNEL (CHANNEL NAME). FILE (FILENAME)
ENDPOINT USED BY A USER TO DELETE AN ALREADY UPLOADED FILE RELATED TO A COURSE AND CHANNEL
"""

#FATTO
@app.delete('/file')
@cross_origin(supports_credentials=True)
@jwt_required()
def delete_file():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        course_name = data.get('course')
        channel_name = data.get('channel')
        file_name = data.get('file')
        if course_name is not None and channel_name is not None:
            response = requests.delete(URL_FILE,data={"course_name":course_name,"channel_name":channel_name,"file_name":file_name,"username":username['user']})
            return response.content,response.status_code
    else:
        return jsonify({'deleted': 'no'}), 401
    return jsonify({'deleted': 'no'}), 403


"""
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL RECEIVED MESSAGES OF AN AUTHENTICATED USER
"""

#FATTO
@app.get('/message')
@cross_origin(supports_credentials=True) 
@jwt_required()
def get_received_messages():
    username = get_jwt_identity()
    response = requests.get((URL_MESSAGE+"/"+username['user']).strip())
    return response.content,response.status_code

"""
TYPE: POST
BODY: RECEIVER (RECEIVER EMAIL), OBJECT (OBJECT MESSAGE), MESSAGE (MESSAGE CONTENT)
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
"""

#FATTO
@app.post('/message')
@cross_origin(supports_credentials=True) 
@jwt_required()
def send_message():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    receiver = data.get('receiver')  
    object_message = data.get('object')
    message = data.get('message')
    if receiver is not None and object is not None and message is not None:
        response = requests.post((URL_MESSAGE).strip(),data={"username":username['user'],"receiver":receiver, "object_message":object_message, "message":message})
        return response.content,response.status_code
    return jsonify({'send': 'no'}), 403


"""
TYPE: POST
BODY: NAME (ASSIGNMENT_NAME), DEADLINE (TIMESTAMP OF DEADLINE), COURSE (COURSE ASSOCIATED TO THE ASSIGNMENT)
ENDPOINT USED IN ORDER TO CREATE A NEW ASSIGNMENT
"""

#FATTO
@app.post('/assignment')
@cross_origin(supports_credentials=True) 
@jwt_required()
def add_assignment():
    username = get_jwt_identity()
    if username['role'] == 'admin':
        data = json.loads(request.data.decode(encoding='UTF-8'))
        name = data.get('name')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        hour = data.get('hour')
        minutes = data.get('minutes')
        course_got = data.get('course')
        response = requests.post((URL_ASSIGNMENT).strip(),data={"name":name,"year":year, "month":month, "day":day, "hour":hour, "minutes":minutes,"course_got":course_got})
        return response.content, response.status_code
    return jsonify({'added': 'false'}), 401


"""
TYPE: DELETE
BODY: 
ENDPOINT USED IN ORDER TO DELETE A NEW ASSIGNMENT
"""

#FATTO
@app.delete('/assignment/<id>')
@cross_origin(supports_credentials=True) 
@jwt_required()
def remove_assignment(id):
    username = get_jwt_identity()
    if username['role'] == 'admin':
        response = requests.delete((URL_ASSIGNMENT+"/"+id).strip())
        return response.content, response.status_code
    return jsonify({'removed':False}),401


"""
TYPE: GET
BODY: ASSIGNMENT (ASSIGNMENT ID)
ENDPOINT USED IN ORDER TO GET ALL EXERCISES RELATED TO AN ASSIGNMENT
"""

#FATTO
@app.get('/exercise/<id>')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_exercises(id):
    username = get_jwt_identity()
    response = requests.get((URL_EXERCISE+"/"+id+"/"+username['user']).strip())
    return response.content, response.status_code

"""
URL: /exercise
TYPE: POST
BODY: json(quest,correct,assignment,type) OR json(quest,correct,assignment,type,wrong1,wrong2,wrong3)
ENDPOINT USED IN ORDER TO ADD A NEW EXERCISE
"""

#FATTO
@app.post('/exercise')
@cross_origin(supports_credentials=True)
@jwt_required()
def create_exercise():
    username = get_jwt_identity()
    data = json.loads(request.data.decode(encoding='UTF-8'))
    if username['role'] == 'admin':
        response = requests.post(URL_EXERCISE,data={"data":data})
        return response.content,response.status_code
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
    if username['role'] == 'user': 
        form : dict = request.form.to_dict()
        if request.form['type'] == 'develop':
            file = request.files
            if len(file) > 0:
                program = request.files['file'].read().decode('UTF-8')
            else:
                program : str = request.form['text']
            form['program'] = program
        form['user'] = username 
        language = request.form['language']
        if language is None or language.lower() not in ["java", "python", "c++", "c"]:
            return jsonify({"evaluated":False}),400
        response = requests.put(URL_EXERCISE,files={'data':(None, json.dumps(form),'application/json')})
        return response.content, response.status_code
    else:
        response = jsonify({}), 401
    return response


"""
TYPE: GET
BODY: json(exercise)  WHERE exercise=EXERCISE_ID
ENDPOINT USED IN ORDER TO GET TESTS OF AN EXERCISE
"""

#FATTO
@app.get('/test')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_test():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    exercise = data.get('exercise')
    if exercise is not None:
        response = requests.get((URL_TEST+"/"+exercise).strip())
        return response.content, response.status_code
    else:
         return jsonify({'added': False}), 403

"""
TYPE: POST
BODY: json(name,exercise,parameter,expected) or json(name,comment,exercise,parameter,expected) WHERE name=NAME_OF_THE_TEST, exercise=EXERCISE_ID, parameter = PARAMETER OF THE FUNCTION TO TEST, comment=DESCRIPTION_OF_THE_TEST, expected = EXPECTED VALUE 
ENDPOINT USED IN ORDER TO ADD A TEST FOR A EXERCISE
"""

#FATTO
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
        response = requests.post((URL_TEST).strip(),data={"exercise":exercise, "name":name, "parameter":parameter, "comment":comment,"expected":expected})
        return response.content, response.status_code
    else:
        return jsonify({'added': False}), 403



#FATTO
@app.get('/result/<id>')
@cross_origin(supports_credentials=True)
@jwt_required()
def get_results(id):
    username = get_jwt_identity()
    response = requests.get((URL_RESULT+"/"+id+"/"+username['user']).strip())
    return response.content, response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)

# backend % docker run --name mariadbtest -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d docker.io/library/mariadb:10.5
# docker exec -it mariadbtest bash
