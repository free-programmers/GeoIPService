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





def login_manager_required(role:int):
    """ 
    create custom login_required decorator base on user role


    login_required = login_manger_required(role:int=3)

    
    @app.get("/only/role/3")
    @login_required
    def ... ():
        ...
    
    """
    def login_required(f):
        """Base Login required Decorator for users"""

        @wraps(f)
        def inner(*args, **kwargs):
            next = request.url_rule
            message = _l("برای دسترسی به صفحه مورد نیاز ابتدا وارد حساب کاربری خود شوید")

            nonlocal role
            role = role or request.user_role_id or session.get('role') or None
            if not role:
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # check user login
            if not session.get("is-login", False):
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # get user id
            if not session.get("account-id"):
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # check user id
            try:
                user = db.session.get(User, session.get("account-id"))
                if not user:
                    raise ValueError
                if user.RoleID != role:
                    message="access denied"
                    raise ValueError
            except Exception as e:
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))


            # check password
            if user.Password != (session.get("password")):
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            if not user.Active:
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            return f(*args, **kwargs)
        return inner

    return login_required
