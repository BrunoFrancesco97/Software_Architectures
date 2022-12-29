from flask import Flask, jsonify,request
import json 
import result

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.get('/result/<id>/<user>')
def get_results(id,user):
    result_assignments = result.get_results_by_assignment_user(id,user)
    result_json = [result.obj_to_dict(item) for item in result_assignments]
    return jsonify({'result': result_json}), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5010)


