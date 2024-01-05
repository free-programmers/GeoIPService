from . import app
from flask import url_for


@app.template_filter('StorageUrl')
def StorageUrl(path: str):
    """
        this template filter generate dynamic urls base of app.debug mode for serving files via flask or nginx
        if debug mode is set this filter redirect request to nginx
        otherwise return requests to flask serve view
    """
    if app.config.get("DEBUG"):
        return url_for("FlaskServeStorageFile", path=path)  # flask serve
    else:
        return f"/Storage/{path}"  # Nginx Serve Files




