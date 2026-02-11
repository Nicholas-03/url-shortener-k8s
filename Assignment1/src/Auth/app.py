from users import User
from utils import createToken, validateToken
from flask import Flask, request, jsonify
import sys
sys.path.append('..')
from config import AUTH_SERVICE_PORT

app = Flask(__name__)

@app.post("/users")
def createUser():
    data = request.get_json()
    name = data.get('username')
    pwd = data.get('password')

    if name in User.users:
        return jsonify("Duplicate"), 409

    User.createUser(name, pwd)
    return jsonify("User created"), 201

@app.put("/users/")
def updatePwd():
    data = request.get_json()
    name = data.get('username')
    oldPwd = data.get('old-password')
    newPwd = data.get('new-password')

    if name in User.users and User.users[name] == oldPwd:
        User.users[name] = newPwd
        return jsonify("Updated"), 200
    
    return jsonify("forbidden"), 403

@app.post("/users/login")
def loginUser():
    data = request.get_json()
    name = data.get('username')
    pwd = data.get('password')

    if name in User.users and User.users[name] == pwd:
        return jsonify({"token": createToken(name)}), 200

    return jsonify("forbidden"), 403

@app.post("/validate")
def validate():
    data = request.get_json()
    token = data.get('token')

    username = validateToken(token)
    if username is None or username not in User.users:
        return jsonify("forbidden"), 403
    else:
        return jsonify({'username': username}), 200

if __name__ == '__main__':
    app.run(debug=True, port=AUTH_SERVICE_PORT)