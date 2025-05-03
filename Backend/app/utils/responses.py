from flask import jsonify

def respond(data, status_code=200):
    response = jsonify(data)
    response.status_code = status_code
    return response