from flask import Blueprint

web = Blueprint(
    name="web",
    import_name=__name__,
    static_folder="static/web",
    template_folder="templates",
    static_url_path="WebStaticStorage",
)

from . import views, model
