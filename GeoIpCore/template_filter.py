from flask import url_for

from . import app


@app.template_filter('StorageUrl')
def StorageUrl(path: str, external: bool = False):
    """ StorageUrl -> dynamic template linking
        this template filter generates dynamic urls based on app.debug, for determining serving files with flask or Nginx
        if debug is on this filter redirect request to nginx to be served.
        otherwise, redirects requests to flask to served <only in debug mode>
    """
    if app.config.get("DEBUG"):
        return url_for("FlaskServeStorageFile", path=path, _external=external)  # flask serve
    else:
        return f"{app.config.get('SERVER', '') if external else ''}/Storage/{path}"  # Nginx Serve Files
