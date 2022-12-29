from flask import Flask, jsonify
import json 
import user 

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.get('/user/<name>')
def get_user(name):
    user_got = user.select_user_by_email(name)
    if len(user_got) == 1:
        userr = user_got[0]
        return jsonify({"user":user.obj_to_dict(userr)}), 200
    return jsonify({}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)