from . import auth
from . import form as AuthForm


from flask import render_template




@auth.route("/login/", methods=["GET"])
def login_get():
    form = AuthForm.LoginForm()
    return render_template("auth/login.html", form=form)
