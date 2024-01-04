# build in
import os.path

# App
from . import app

# framework
from flask import send_from_directory

if app.debug: # only read this view if debug is on
    app.logger.warning("Development Serve File View is Up")
    @app.get("/ServeStorageFile/<path:path>")
    def FlaskServeStorageFile(path):
        if os.path.exists(app.config.get("STORAGE_DIR") / path):
            return send_from_directory(app.config.get("STORAGE_DIR"), path)
        else:
            return f"File Not Found. at: {path}", 404