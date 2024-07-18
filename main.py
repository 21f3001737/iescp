from config import LocalDevelopmentConfig
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from model.db import db
from flask_bootstrap import Bootstrap5
import secrets
from flask_wtf.csrf import CSRFProtect


def setup_app():
    app = Flask(__name__, template_folder="view")
    app.config.from_object(LocalDevelopmentConfig)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lux'
    app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        api = Api(app)
        CORS(app, resources={r"/*": {"origins": "*"}})
        bootstrap = Bootstrap5(app)
        csrf = CSRFProtect(app)
        return app, api, bootstrap

app, api, bootstrap = setup_app()

with app.app_context():
    from controller.base import *
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8099)
