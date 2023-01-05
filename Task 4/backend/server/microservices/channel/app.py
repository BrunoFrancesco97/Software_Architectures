from flask import Flask, jsonify,request
import json 
import channel 
import channel_sub
import course 

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.get('/channel')
def get_channels():
    channels_got = channel.selectAll()
    channels_new = [channel.obj_to_dict(item) for item in channels_got]
    return jsonify({"channels": channels_new}), 200


@app.get('/channel/<channelname>/<name>')
def get_channel_courses(channelname,name):
    channel_got = channel.get_channels_by_name(channelname) 
    if channel_got is not None and len(channel_got) == 1:
        channel_subcr = channel_sub.select_channel_subs(name,channel_got[0].id)
        if channel_subcr is not None and len(channel_subcr) == 1:
            courses_got = course.select_course_by_channel(channel_got[0].id)
            courses_new = [course.obj_to_dict(item) for item in courses_got]
        else:
            return jsonify({'courses': []}), 401
        return jsonify(courses_new), 200
    return jsonify({'courses': []}), 403


@app.post('/channel')
def add_channel():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data.get('channel')
    channel.add_channel(name)
    return jsonify({'response': 'ok'}), 200
        
@app.delete('/channel/<name>')
def remove_channel(name):
    channel.remove_channel(name)
    return jsonify({'response': 'ok'}), 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)