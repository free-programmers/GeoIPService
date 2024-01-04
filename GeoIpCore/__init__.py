from flask import Flask, session, url_for, redirect, request

from GeoIpConfig import Setting
from .extensions import db, ServerSession, ServerMigrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Setting)

    # init Extensions
    db.init_app(app=app)
    ServerSession.init_app(app)
    ServerMigrate.init_app(app=app, db=db)



    # read Apps
    from GeoIpApi import api
    app.register_blueprint(api, url_prefix="/api/v1/")

    from GeoIpWeb import web
    app.register_blueprint(web, url_prefix="/")

    return app




def userLocalSelector():
    """
        this function select user local base on session
    """
    try:
        return session.get("language", "fa")
    except:
        return "en"


app = create_app()


@app.before_request
def set_user_statue():
    """
    Set Some Useful utils on request before heads up to view

    properties:

        0.0 request.user_object
            this prob return Users Object:<Sqlalchemy Object> from database if user is authenticated!
            first user is_authenticated to ensure that user is logged in then
            get user object from db

        0.1 request.current_language
            this prob return user current language:<str> < this prob uses local_selector flask_babel >

        0.2 request.is_authenticated
            this prob return user is authenticated: <bool> or nor


    """
    request.current_language = userLocalSelector()
    request.is_authenticated = session.get("login", False)
    request.user_object = db.session.execute(
        db.select(User).filter_by(id=session.get("account-id", None))).scalar_one_or_none()


@app.route("/lang/set/<string:language>")
def setUserLanguage(language):
    """
        this view select a  language for user
    """
    location = (request.referrer or url_for('web.index_get'))

    if language not in Setting.LANGUAGES:
        return redirect(location)
    else:
        session["language"] = language
        return redirect(location)



import context_processor