from flask import Blueprint

installer = Blueprint(
    name="installer",
    import_name=__name__,
    template_folder="templates",
    static_folder="static"
)


import Installer.views