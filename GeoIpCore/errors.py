from . import app
from flask import jsonify

@app.errorhandler(429)
def to_many_request(e):
    return jsonify({"status": "failed", "message":"to many request, 60 request per minute is Allowed"}), 429

@app.errorhandler(404)
def not_found_error(e):
    return jsonify({"status": "failed", "message":"Page not found"}), 404
