from flask import Flask, jsonify
from .blueprints import user
from . import exceptions

def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_mapping(**config)

    exceptions.error_treatment(app=app)

    app.register_blueprint(user.bp)

    return app