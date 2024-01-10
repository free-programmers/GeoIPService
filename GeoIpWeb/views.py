# app
from . import web
from . import form as WebForm

# framework
from flask import render_template


@web.route("/", methods=["GET"])
def index_get() -> str:
    """Render Index Page"""
    return render_template("web/index.html")


@web.route("/terms/", methods=["GET"])
def term_get() -> str:
    """Render term of use privacy page to user"""
    return render_template("web/term-of-use.html")


@web.route("/contact-us/", methods=["GET"])
def contact_us_get() -> str:
    """Render term of use privacy page to user"""
    form = WebForm.ContactUsForm()
    return render_template("web/contact-us.html", form=form)
