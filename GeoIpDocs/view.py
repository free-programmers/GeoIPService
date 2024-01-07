import os.path

from . import docs
from GeoIpCore.extensions import ServerCache

from flask import current_app, render_template, abort


@docs.route("/<string:documentName>/")
# @ServerCache.cached(timeout=1296000)  # 30 day
def serve(documentName: str) -> str:
    """
    Serve Docs
    this view take a file name and search it in docs folder and if file exists read file and serve it to user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    this view cache the response
    """
    documentName += ".html"
    documentName = documentName.lower()
    if os.path.exists(current_app.config.get("STORAGE_DIR") / "docs" / documentName):
        with open(current_app.config.get("STORAGE_DIR") / "docs" / documentName, mode="r", encoding="utf-8") as f:
            content = f.read()
            documentName = documentName.split(".")[0].capitalize()
            return render_template("docs/document.html", content=content, title=documentName)
    else:
        abort(404)
