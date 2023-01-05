from flask import Flask, jsonify,request
from werkzeug.utils import secure_filename
import json 
import course 
import channel
import files
import channel_sub
import course_sub 
import utils 

app = Flask(__name__)

UPLOAD_FOLDER = 'userdata/'

@app.get('/')
def works():
    return jsonify({"works":True}), 200

@app.put('/file/<name>')
def upload_file(name):
        course_name = request.form['course']
        channel_name = request.form['channel']
        if course_name is not None and channel_name is not None:
            # Check if I'm subscripted to the course I want to update the file
            course_subscription = course_sub.select_course_subs_by_user(name)  
            channel_got = channel.get_channels_by_name(channel_name)
            # Check if the course is linked to the channel (consistency of information)
            course_got = course.select_course_by_name(course_name)
            if channel_got is not None and len(channel_got) == 1:
                # Check if I'm subscribed to the channel the course is linked
                channel_subscription = channel_sub.select_channel_subs(name, channel_got[0].id) 
                if course_subscription is not None and channel_subscription is not None and len(course_subscription) == 1 and len(channel_subscription) == 1 and course_got is not None and len(course_got) == 1:  # If true then I've got the right permissions to upload it
                    files_got = request.files.getlist("file")
                    for file in files_got:
                        if file and utils.allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            if files.add_file(filename, course_name, channel_name, file):
                                return jsonify({'uploaded': 'ok'}), 200
                            else:
                                return jsonify({'uploaded': False}), 403
        else:
            return jsonify({'uploaded': 'no'}), 401
        return jsonify({'uploaded': 'no'}), 500


@app.delete('/file')
def delete_file():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    course_name = data.get('course')
    channel_name = data.get('channel')
    file_name = data.get('file')
    user = data.get('username')
    course_subscription = course_sub.select_course_subs_by_user(user)  # Check if I'm subscripted to the course I want to update the file
    channel_got = channel.get_channels_by_name(channel_name)
    course_got = course.select_course_by_name(course_name)  # Check if the course is linked to the channel (consistency of information)
    if channel_got is not None and len(channel_got) == 1:
        channel_subscription = channel_sub.select_channel_subs(user, channel_got[0].id)  # Check if I'm subscripted to the channel the course is linked
        if course_subscription is not None and channel_subscription is not None and len(course_subscription) == 1 and len(channel_subscription) == 1 and course_got is not None and len(course_got) == 1:  # If true then I've got the right permissions to upload it
            file_got = files.select_file(file_name, course_name)
            if file_got is not None and len(file_got) == 1:
                if files.remove_file(file_name, course_name, channel_name):
                    return jsonify({'deleted': 'ok'}), 200
                else:
                    return jsonify({'deleted': 'false'}), 404
    return jsonify({'deleted': 'no'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5012)


