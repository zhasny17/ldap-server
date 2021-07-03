from flask import Flask
from .blueprints import user

def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_mapping(**config)

    app.register_blueprint(user.bp)

    return app