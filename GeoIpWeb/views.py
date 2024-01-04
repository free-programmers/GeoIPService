# app
from . import web

# framework
from flask import render_template


@web.route("/", methods=["GET"])
def index_get() -> str:
    """Render Index Page"""
    return render_template("web/index.html")
