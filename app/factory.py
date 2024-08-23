import os

from flask import Flask, render_template
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS

from bson import ObjectId
from datetime import datetime

from flask_mail import Mail

from app.api.auth import auth_api_v1
from app.api.test import test_api_v1
from app.api.user import user_api_v1
from app.api.messages import message_api_v1


class MongoJsonEncoder(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


def create_app():
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )
    mail = Mail(app)

    CORS(app)

    app.json = MongoJsonEncoder(app)

    # Endpoints registration
    app.register_blueprint(test_api_v1)
    app.register_blueprint(auth_api_v1)
    app.register_blueprint(user_api_v1)
    app.register_blueprint(message_api_v1)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('index.html')

    return app
