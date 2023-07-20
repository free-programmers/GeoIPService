from flask import Blueprint

web = Blueprint(
    "web",
    __name__,
    static_folder="static",
    template_folder="templates"
)

import GeoIpWeb.views