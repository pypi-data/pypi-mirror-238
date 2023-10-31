import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        # expecting FLASK_LMS_HOST and FLASK_LMS_PORT
        app.config.from_prefixed_env()
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import player, library
    app.register_blueprint(player.bp)
    app.register_blueprint(library.bp)

    return app
