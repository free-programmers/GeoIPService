from . import auth
from . import form as AuthForm

from flask import render_template


@auth.route("/login/", methods=["GET"])
def login_get():
    form = AuthForm.LoginForm()
    return render_template("auth/login.html", form=form)


@auth.route("/register/", methods=["GET"])
def register_get():
    form = AuthForm.RegisterForm()
    return render_template("auth/register.html", form=form)


@auth.route("/process_activate_account/", methods=["GET"])
def process_activate_account():
    # token = token, lang = lang
    ...