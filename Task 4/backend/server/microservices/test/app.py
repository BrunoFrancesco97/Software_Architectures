from flask import Flask, jsonify,request
import json 
import tests

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.get('/test/<exercise>')
def get_test(exercise):
    if exercise is not None:
        tests_got = tests.get_tests_by_exercise(exercise)
        tests_json = [tests.obj_to_dict(item) for item in tests_got] 
        return jsonify({'tests': tests_json}), 200 
    else:
         return jsonify({'added': False}), 403

@app.post('/test')
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5009)


