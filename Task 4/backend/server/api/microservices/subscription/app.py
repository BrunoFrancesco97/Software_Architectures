from flask import Flask, jsonify,request
import json 
import channel_sub
import channel 
import course_sub
import course 

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200

@app.get('/channel_subscription/<user>')
def get_channel_sub(user):
    channel_sub_list = channel_sub.select_channel_subs_by_user(user)
    channel_new = [channel_sub.obj_to_dict_complete(item) for item in channel_sub_list]
    return jsonify({'channels': channel_new}), 200


@app.post('/channel_subscription')
def add_channel_sub():
    name = request.json['name']
    user = request.json['username'] 
    channel_got = channel.get_channels_by_name(name)
    if channel_got is not None and len(channel_got) == 1:
        channel_sub.add_subscription(channel_got[0].id, user)
        return jsonify({'response': 'ok'}), 200
    return jsonify({'response': 'no'}),403

@app.delete('/channel_subscription')
def delete_channel_sub():
    name = request.json['name']
    user = request.json['username'] 
    channel_got = channel.get_channels_by_name(name)
    if channel_got is not None and len(channel_got) == 1:
        channel_sub.remove_subscription(user, channel_got[0].id)
        return jsonify({'response': 'ok'}), 200
    return jsonify({'response': 'no'}), 403


@app.get('/course_subscription/<user>')
def get_course_sub(user):
    course_sub_list = course_sub.select_course_subs_by_user(user)
    course_sub_list_new = [course_sub.obj_to_dict(item) for item in course_sub_list]
    return jsonify({'courses': course_sub_list_new}), 200


@app.post('/course_subscription')
def add_course_sub():
    name = request.json['name']
    user = request.json['username']
    course_got = course.select_course_by_name(name)
    if course_got is not None and len(course_got) == 1:
        course_sub.add_subscription(name, user)
        return jsonify({'response': 'ok'}), 200
    return jsonify({'response': 'no'}), 403

@app.delete('/course_subscription')
def delete_course_sub():
    name = request.json['name']
    user = request.json['username']   
    course_sub.remove_subscription(user, name)
    return jsonify({'response': 'ok'}), 200
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)