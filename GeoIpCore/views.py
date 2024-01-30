# build in
import os.path

# framework
from flask import send_from_directory

# App
from . import app

if app.debug:  # only read this view if debug is on
    app.simpleLOGGER.warning("\tFlask Serving Static files.\n\tbecause app.debug is True")


    @app.get("/ServeStorageFile/<path:path>")
    def FlaskServeStorageFile(path):
        if os.path.exists(app.config.get("STORAGE_DIR") / path):
            return send_from_directory(app.config.get("STORAGE_DIR"), path)
        else:
            return f"File Not Found. at: {path}", 404
