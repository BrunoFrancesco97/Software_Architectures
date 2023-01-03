from flask import Flask, jsonify,request
import utils
import crypto
import user 

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.post('/login')
def registration():
    try:
        email = request.json['email']
        password = request.json['password']
        name = request.json['name']
        surname = request.json['surname']
        role = request.json['role']
        username: str = utils.whitespaces_remover(email)
        password: str = utils.whitespaces_remover(password)
        if username is not None and password is not None and role is not None and len(username) > 0 and len(password) > 0:
            check = user.select_user_by_email(username)
            if len(check) == 0:
                (passwordHash, salt) = crypto.sha256_encode(password)
                user.add_user_complete(username, passwordHash, salt, name, surname, role)
                return jsonify({"registered":True}),200
        else:
            return jsonify({"registered":False}),400
    except Exception as e:
        print(str(e))
        return jsonify({"registered":False}),403
    else:
        return jsonify({"registered":False}),403


@app.get('/login/<token>')
def login(token):
    try:
        email = token.split(":")[0] 
        password = token.split(':')[1] 
        if email is not None and password is not None:
            username: str = utils.whitespaces_remover(email)
            password: str = utils.whitespaces_remover(password)
            if len(username) > 0 and len(password) > 0:
                user_DB = user.select_user_by_email(username)
                if user_DB is not None and len(user_DB) == 1:
                    (passwordHashedDB, salt) = user.get_password_salt(username)
                    if (passwordHashedDB, salt) is not None:
                        password_hash = crypto.sha256_encode_salt(password, salt)
                        if password_hash == passwordHashedDB:
                            return jsonify({'logged': True, "user":username,"role":user_DB[0].role}),200
    except Exception as e:
        print(e)
        return jsonify({'logged': False}),403
    else:
        return jsonify({'logged': False}),403


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5011)


