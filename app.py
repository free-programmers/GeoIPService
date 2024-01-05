import os
import json
from GeoIpCore import app
from flask import current_app
from threading import Thread
from GeoIpCore.extensions import db
from GeoIpApi.model import IPV4,IPV6, CountryInfo


if __name__ == "__main__":
    app.run(
        port=8080,
        debug=True,
    )
