# build in
from functools import wraps

# framework
from flask import session, request, redirect, url_for, flash

# apps
from GeoipAuth.model import User

# libs
from flask_babel import lazy_gettext as _l


def login_required(f):
    """Base Login required Decorator for users"""

    @wraps(f)
    def inner(*args, **kwargs):
        next = request.url_rule

        # check user login
        message = _l("برای دسترسی به صفحه مورد نیاز ابتدا وارد حساب کاربری خود شوید")
        if not session.get("login", False):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # get user id
        if not session.get("account-id"):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check user id
        try:
            user = User.query.get(session.get("account-id"))
            if not user:
                raise ValueError
        except Exception as e:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check password
        if user.Password != (session.get("password")):
            flash(message, "danger")
            print("herwe")
            return redirect(url_for("auth.login_get", next=next))

        if not user.Active:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        return f(*args, **kwargs)

    return inner


def only_reset_password(f):
    """"""

    @wraps(f)
    def inner(*args, **kwargs):

        if not session.get("mail", False):
            return redirect(url_for("auth.login_get"))

        # get user id
        if not session.get("allow-set-password"):
            return redirect(url_for("auth.login_get"))

        return f(*args, **kwargs)

    return inner
