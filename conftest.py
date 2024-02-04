import pytest
from GeoIpCore import create_app
from flask import Flask


@pytest.fixture()
def app():
    app:Flask = create_app()
    app.debug = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"



    yield app