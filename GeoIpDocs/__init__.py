from flask import Blueprint

docs = Blueprint(
    name="docs",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="DocsStaticStorage"
)


from . import view