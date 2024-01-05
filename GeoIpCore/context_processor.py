from . import app
from flask import session, request


@app.context_processor
def app_context():



    ctx = {
        "SERVER_NAME": app.config.get("SERVER", "")

    }
    return ctx

