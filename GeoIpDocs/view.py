import os.path

from . import docs
from GeoIpCore.extensions import ServerCache

from flask import current_app, render_template, abort


@docs.route("/<string:documentName>/")
@ServerCache.cached(timeout=1296000) # 30 day
def serve(documentName: str) -> str:
    """Serve Docs"""
    print("action")
    documentName += ".html"
    if os.path.exists(current_app.config.get("STORAGE_DIR") / "docs" / documentName):
        with open(current_app.config.get("STORAGE_DIR") / "docs" / documentName, mode="r", encoding="utf-8") as f:
            content = f.read()
            return render_template("docs/document.html", content=content, title=documentName.split(".")[0])
    else:
        abort(404)
