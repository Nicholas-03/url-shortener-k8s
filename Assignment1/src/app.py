from url import Url
from utils import is_valid_url
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# GET / - Returns a list of all existing keys
@app.get("/")
def getUrls():
    keys = list(Url.getUrls())

    if len(keys) == 0:
        return jsonify({"value": None}), 200
    
    return jsonify({"value": keys}), 200

# GET /:id - Returns URL for a given key
@app.get("/<id>")
def returnUrl(id):
    if id in Url.urls:
        url = Url.urls[id]
        return jsonify({"value": url}), 301
    else:
        return jsonify("Not Found"), 404

# POST / - Creates a new key for a provided URL
@app.post("/")
def addUrl():
    if not request.is_json:
        return jsonify("Error"), 400
    
    data = request.get_json()
    url = data.get('value')

    if not is_valid_url(url):
        return jsonify("Error"), 400
    
    id = Url.addUrl(url)
    return jsonify({"id": id}), 201
    
# PUT /:id - Updates the destination URL for a key
@app.put("/<id>")
def update(id):    
    data = request.get_json(force=True)
    url = data.get('url')
    
    if id not in Url.urls:
        return jsonify("Not Found"), 404
    
    if not is_valid_url(url):
        return jsonify("Error"), 400

    Url.urls[id] = url
    return "", 200

# DELETE /:id - Removes a specific URL
@app.delete("/<id>")
def deleteUrl(id):
    if id in Url.urls:
        del Url.urls[id]
        return "", 204
    else:
        return jsonify("Not found"), 404

# DELETE / - Clears the repository
@app.delete("/")
def deleteNull():
    Url.urls.clear()
    return jsonify("Not Found"), 404