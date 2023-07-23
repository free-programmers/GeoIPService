from flask import Blueprint



installer = Blueprint(
    "installer",
    __name__,
    static_folder="static",
    template_folder="templates"
)

import Installer.views