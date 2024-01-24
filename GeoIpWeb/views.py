# app
from . import web
from . import form as WebForm, model as WebModel
from GeoIpCore.extensions import ServerCaptcha2

# framework
from flask import render_template, flash, redirect, request


from flask_babel import lazy_gettext as _l





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


@web.route("/contact-us/", methods=["POST"])
def contact_us_post() -> str:
    """saving contact us messages"""
    form = WebForm.ContactUsForm()
    if not ServerCaptcha2.is_verify():
        flash(_l("invalid captcha"), "daner")
        form.form_errors.append(_l("invalid captcha"))
        return render_template("web/contact-us.html", form=form)

    if not form.validate():
        flash(_l("invalid request"), "daner")
        form.form_errors.append(_l("invalid request"))
        return render_template("web/contact-us.html", form=form)

    contactUS = WebModel.ContactUS()
    contactUS.Title = form.Title.data
    contactUS.Message = form.Message.data
    contactUS.Email = form.Email.data
    contactUS.SetPublicKey()
    contactUS.save()
    flash(_l("Thanks for your message, we will contact you as soon as possible"), "success")
    return redirect(request.referrer)


@web.route("/about-us/", methods=["GET"])
def about_us_get() -> str:
    """Render about us page"""
    return render_template("web/about-us.html")
