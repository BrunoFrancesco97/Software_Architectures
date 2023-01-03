from flask import Flask, jsonify,request
import json 
import support

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200



@app.get('/message/<user>')
def get_received_messages(user):
    messages = support.select_messages_by_receiver(user)
    messages_new = [support.obj_to_dict(item) for item in messages]
    return jsonify({'messages': messages_new}), 200


@app.post('/message')
def send_message():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    user = data.get('username')
    receiver = data.get('receiver')  
    object_message = data.get('object')
    message = data.get('message')
    support.send_message(user, receiver, object_message, message)
    return jsonify({'send': 'ok'}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)