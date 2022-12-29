from flask import Flask, jsonify,request
import json 
import course 
import assignment

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.post('/assignment')
def add_assignment():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    name = data.get('name')
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    hour = data.get('hour')
    minutes = data.get('minutes')
    course_got = data.get('course')
    if len(course.select_course_by_name(course_got)) == 1:
        resp = assignment.add_assignment(name, year, month, day, hour, minutes, course_got)
        if resp[0] == True:
            return jsonify({'added': assignment.obj_to_dict(resp[1])}), 200
        else:
            return jsonify({'added': 'false'}), 400
    else:
        return jsonify({'added': 'false'}), 400

@app.delete('/assignment/<id>')
def remove_assignment(id):
    assignment.remove_assignment(id)
    return jsonify({'removed':True}),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5007)

