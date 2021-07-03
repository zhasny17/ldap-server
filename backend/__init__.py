from flask import Flask, jsonify
from .blueprints import user, doc
from . import exceptions

def create_app(config=None):
    app = Flask(__name__, template_folder='doc')

    if config:
        app.config.from_mapping(**config)

    exceptions.error_treatment(app=app)

    app.register_blueprint(user.bp)
    app.register_blueprint(doc.bp, url_prefix='/doc')

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header['Access-Control-Allow-Methods'] = '*'
        header['Access-Control-Allow-Headers'] = '*'

        return response

    return app