from config import LocalDevelopmentConfig
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from model.db import db
from controller.api.sponsors_api import SponsorsAPI

def setup_app():
    app = Flask(__name__, template_folder="view")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app, api

app, api = setup_app()

with app.app_context():
    db.create_all()

api.add_resource(SponsorsAPI, "/api/sponsor/", "/api/sponsor/<sponsor_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
