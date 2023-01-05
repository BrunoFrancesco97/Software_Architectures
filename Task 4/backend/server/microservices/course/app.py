from flask import Flask, jsonify,request
import json 
import course 
import course_sub
import assignment
import files 
import channel 

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.get('/course')
def get_courses():
    course_got = course.select_all()
    course_ap = []
    for item in course_got:
        course_ap.append(course.obj_to_dict(item))
    return jsonify({"courses": course_ap}), 200


@app.get('/course/<name>/<name_user>')
def get_course_stuff(name, name_user):
    if len(course_sub.select_course_subs(name_user, name)) == 1:
        ass_list = assignment.get_assignments_by_course(name)
        ass_done = assignment.get_assignments_by_course_done(name,name_user)
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
    
@app.post('/course')
def add_course():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    channel_name = data.get('channel')
    course_name = data.get('course')
    if channel_name is not None and course_name is not None:
        channel_got = channel.get_channels_by_name(channel_name)
        if channel_got is not None and len(channel_got) == 1:
            course.add_course(course_name, channel_got[0].id)
            return jsonify({'response': 'ok'}), 200
    return jsonify({'response': 'no'}), 400

@app.delete('/course/<channel_name>/<course_name>')
def remove_course(channel_name,course_name):
    course_got = course.select_course_by_name(course_name)
    if course_got is not None and len(course_got) == 1:
        course.remove_course(course_name, course_got[0].channel, channel_name)
        return jsonify({'response': 'ok'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5004)