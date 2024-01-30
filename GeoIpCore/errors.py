# Hands errors

from . import app

from flask import jsonify

@app.errorhandler(429)
def to_many_request(e):
    """ to many request -> view limiter """
    return jsonify({"status": "failed", "message":"to many request, 60 request per minute is allowed"}), 429


@app.errorhandler(404)
def not_found_error(e):
    """ page not found error """
    return jsonify({"status": "failed", "message":"page not found"}), 404


@app.errorhandler(500)
def server_error(e):
    """ server error """
    return jsonify({"status": "failed", "message":"server error "}), 500
