from flask import Blueprint


api = Blueprint("api", __name__)

import GeoIpApi.views
import GeoIpApi.model