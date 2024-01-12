from . import auth
from . import form as AuthForm

from flask import render_template, session, request, flash
from flask_babel import lazy_gettext as _l

from GeoIpCore.extensions import ServerCaptcha2, db
from GeoipAuth.model import User



@auth.route("/login/", methods=["GET"])
def login_get():
    form = AuthForm.LoginForm()
    return render_template("auth/login.html", form=form)


@auth.route("/register/", methods=["GET"])
def register_get():
    form = AuthForm.RegisterForm()
    return render_template("auth/register.html", form=form)


@auth.route("/register/", methods=["POST"])
def register_post():
    form = AuthForm.RegisterForm()

    if not ServerCaptcha2.is_verify():
        flash(_l('invalid captcha.'), "danger")
        form.Submit.errors.append(_l('captcha error'))
        return render_template("auth/register.html", form=form)

    if not form.validate():
        flash(_l('Some values seem to be missing', "danger"), "danger")
        return render_template("auth/register.html", form=form)

    # db redis_db
    # TODO:if more than one user register with same info at the same time


    # check username or email is duplicated db
    user = User()

    if not user.setUsername(form.Username.data):
        flash(_l("username is taken by another user"), "danger")
        return render_template("auth/register.html", form=form)

    if not user.setEmail(form.EmailAddress.data):
        flash(_l("email address is taken by another user"), "danger")
        return render_template("auth/register.html", form=form)

    user.setPassword(form.Password.data)
    user.SetPublicKey()
    if not user.save():
        flash(_l("An error occurred, try again later"), "danger")
        return render_template("auth/register.html", form=form)





@auth.route("/process_activate_account/", methods=["GET"])
def process_activate_account():
    # token = token, lang = lang
    ...