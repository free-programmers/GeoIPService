from flask import Flask, session, url_for, redirect, request

from GeoIpConfig import Setting
from GeoipAuth.model import User

from .utils import celery_init_app, user_real_ip
from .logger import GetStdoutLogger
from .extensions import (db, babel, ServerSession, ServerMigrate,
                         ServerMail, ServerCache, ServerCaptcha2, ServerRequestLimiter)


def create_app(None) -> Flask:
    """Factory function for main flask app with all configs.
    this function creates an app and then it adds all blueprints
    and configs to it.
    """
  
    app = Flask(__name__)
    app.config.from_object(Setting)

    # init Extensions
    db.init_app(app=app)
    babel.init_app(app=app)
    celery_init_app(app=app)

    ServerSession.init_app(app)
    ServerMigrate.init_app(app=app, db=db)
    ServerMail.init_app(app=app)
    ServerCache.init_app(app=app)
    ServerCaptcha2.init_app(app=app)
    ServerRequestLimiter.init_app(app=app)

    # Register all Blueprints
  
    # from GeoipAdmin import admin
    # app.register_blueprint(admin, url_prefix="/admin/")

    # from GeoipAuth import auth
    # app.register_blueprint(auth, url_prefix="/auth/")

  
    from GeoIpApi import api
    app.register_blueprint(api, url_prefix="/api/v1/", subdomain="www")

    from GeoIpDocs import docs
    app.register_blueprint(docs, url_prefix="/",  subdomain='docs')

    from GeoIpWeb import web
    app.register_blueprint(web, url_prefix="/", subdomain="www")

    app.viewLOGGER = GetStdoutLogger(name="viewLOGGER")
    app.simpleLOGGER = GetStdoutLogger(name="simpleLOGGER", type="simple")

    return app


def userLocalSelector():
    """ This function selects users local base on  their session
        this is called every time the user send a request

        uses for getting users selected language
    """
    try:
        return session.get("language", "en")  # change with request.best...
    except:
        return "fa"


app = create_app()


@app.before_request
def middle_ware_center():
    """
    Set Some Useful utils on request before heads up to view

    properties:

        0.0 request.user_object
          this prob returns User  Object:<Sqlalchemy Object> from the database if user is authenticated
          otherwise this prob returns None!
           
        .. versionadded:: 1.0

        0.1 request.current_language
          this prob return users current language:<str> < this prob uses local_selector func -> flask_babel >
        .. versionadded:: 1.0

        0.2 request.is_authenticated
          this prob returns True if user is authenticated otherwise False
        .. versionadded:: 1.0

        0.3 request.real_ip
          this prob returns users actual public ip address 
        .. versionadded:: 1.0



    """
    request.user_object = db.session.execute(db.select(User)
                                             .filter_by(id=session.get("account-id", None)))
                                              .scalar_one_or_none()
  
    request.current_language = userLocalSelector()
    request.is_authenticated = session.get("login", False)
    
  request.real_ip = user_real_ip()


@app.route("/lang/set/<string:language>/")
def setUserLanguage(language: str) -> :
    """This view set a language for user in session"""
    location = (request.referrer or url_for('web.index_get'))

    if language not in Setting.LANGUAGES:
        return redirect(location)
    else:
        session["language"] = language
        return redirect(location)



from . import views
from . import context_processor
from . import template_filter
from . import errors
