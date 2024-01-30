from . import app


@app.context_processor
def global_app_context():
    """This function register template context_processors"""

    ctx = {
        "SERVER_NAME": app.config.get("SERVER", "")
    }
    return ctx
