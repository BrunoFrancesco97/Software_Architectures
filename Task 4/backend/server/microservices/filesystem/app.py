from flask import Flask, jsonify,request
import json 
import os 
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = 'userdata/'

@app.get('/')
def works():
    return jsonify({"works":True}), 200

@app.put('/channel/<name>')
def add_channel(name):
    try:
        os.mkdir(UPLOAD_FOLDER + name) 
        return jsonify({"added":True}), 200
    except:
        return jsonify({"added":False}), 500

@app.delete('/channel/<name>')
def remove_channel(name):
    try:
        shutil.rmtree(UPLOAD_FOLDER + name)
        return jsonify({"added":True}), 200
    except:
        return jsonify({"added":False}), 500

@app.put('/course/<channel>/<name>')
def add_course(channel,name):
    try:
        os.mkdir(UPLOAD_FOLDER + channel + "/" + name)
        return jsonify({"added":True}), 200
    except:
        return jsonify({"added":False}), 500

@app.delete('/course/<channel>/<name>')
def remove_course(channel,name):
    try:
        shutil.rmtree(UPLOAD_FOLDER + channel + "/" + name)
        return jsonify({"added":True}), 200
    except:
        return jsonify({"added":False}), 500


@app.put('/file/<channel>/<course>/<file>')
def add_file(channel,course,file):
    try:
        if not os.path.exists(UPLOAD_FOLDER + channel + '/' + course + '/'+file): 
            file.save(os.path.join(UPLOAD_FOLDER + channel + '/' + course + '/', file))
            return jsonify({"added":True}), 200
        else:
            return jsonify({"added":False}), 200
    except:
        return jsonify({"added":False}), 500


@app.delete('/file/<channel>/<course>/<file>')
def remove_file(channel,course,file):
    try:
        if not os.path.exists(UPLOAD_FOLDER + channel + '/' + course + '/'+file): 
            os.remove(UPLOAD_FOLDER + channel + '/' + course + '/' + file) 
            return jsonify({"removed":True}), 200
        else:
            return jsonify({"removed":False}), 200
    except:
        return jsonify({"removed":False}), 500


if __name__ == '__main__':
    if not os.path.exists('userdata'):
        os.mkdir('userdata')
    app.run(host='0.0.0.0', debug=True, port=5100)


