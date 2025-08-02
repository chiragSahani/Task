from flask import Flask
from .config import Config
from . import database
from . import routes
from . import errors

def create_app(config_class=Config, config_override=None):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if config_override:
        app.config.update(config_override)

    database.init_app(app)
    errors.init_app(app)

    app.register_blueprint(routes.bp)

    return app
