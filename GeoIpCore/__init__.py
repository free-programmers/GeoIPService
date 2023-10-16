from flask import Flask, redirect, url_for

from GeoIpConfig import config
from GeoIpCore.extensions import db, cache, migrate, \
        csrf, captchaVersion2, limiter, SessionServer


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # init Extensions
    db.init_app(app=app)
    cache.init_app(app)
    migrate.init_app(app=app, db=db)
    csrf.init_app(app)
    captchaVersion2.init_app(app)
    limiter.init_app(app)
    SessionServer.init_app(app)

    from GeoIpApi import api
    app.register_blueprint(api, url_prefix="/api/v1/")

    from GeoIpWeb import web
    app.register_blueprint(web, url_prefix="/")




    return app


app = create_app()


# read Base Views
import GeoIpCore.views
