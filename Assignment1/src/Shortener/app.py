from url import Url
import os
from utils import *
from flask import Flask, request, jsonify
from config import URL_SHORTENER_PORT
from pathlib import Path

INSTANCE_PATH = str((Path(__file__).resolve().parent / "instance").resolve())
BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")

app = Flask(__name__, instance_path=INSTANCE_PATH)

# GET / - Returns a list of all existing keys
@app.get("/")
def getUrls():
    token = request.headers.get('Authorization')
    username = validateToken(token)

    if not username:
        return jsonify("forbidden"), 403

    keys = list(Url.getUrls(username))

    if len(keys) == 0:
        return jsonify({"value": None}), 200
    
    return jsonify({"value": keys}), 200

# GET /:id - Returns URL for a given key
@app.get("/<id>")
def returnUrl(id):
    if id in Url.urls:
        url = Url.urls[id]['url']
        return jsonify({"value": url}), 301
    else:
        return jsonify("Not Found"), 404

# POST / - Creates a new key for a provided URL
@app.post("/")
def addUrl():
    if not request.is_json:
        return jsonify("Error"), 400
    
    token = request.headers.get('Authorization')
    username = validateToken(token)

    if not username:
        return jsonify("forbidden"), 403
    
    data = request.get_json()
    url = data.get('value')

    if not is_valid_url(url):
        return jsonify("Error"), 400
    
    id = Url.addUrl(url, username)
    return jsonify({"id": id}), 201
    
# PUT /:id - Updates the destination URL for a key
@app.put("/<id>")
def update(id):
    token = request.headers.get('Authorization')
    username = validateToken(token)

    if not username:
        return jsonify("forbidden"), 403
    
    data = request.get_json(force=True)
    url = data.get('url')
    
    if id not in Url.urls:
        return jsonify("Not Found"), 404
    
    if Url.urls[id]['owner'] != username:
        return jsonify("forbidden"), 403
    
    if not is_valid_url(url):
        return jsonify("Error"), 400

    Url.urls[id]['url'] = url
    Url.updateDatabase()
    return "", 200

# DELETE /:id - Removes a specific URL
@app.delete("/<id>")
def deleteUrl(id):
    token = request.headers.get('Authorization')
    username = validateToken(token)

    if not username:
        return jsonify("forbidden"), 403

    if id in Url.urls and Url.urls[id]['owner'] == username:
        del Url.urls[id]
        Url.updateDatabase()
        return "", 204
    else:
        return jsonify("Not found"), 404

# DELETE / - Clears the repository
@app.delete("/")
def deleteNull():
    token = request.headers.get('Authorization')
    username = validateToken(token)

    if not username:
        return jsonify("forbidden"), 403

    Url.deleteAllUrls(username)
    return jsonify("Not Found"), 404

Url.loadData(app)

if __name__ == '__main__':
    app.run(host=BIND_HOST, port=URL_SHORTENER_PORT)