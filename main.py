from config import LocalDevelopmentConfig
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from model.db import db
from flask_bootstrap import Bootstrap5
import secrets
from flask_wtf.csrf import CSRFProtect
from model.dummy_data import add_dummy_data, add_dummy_admin


def setup_app():
    app = Flask(__name__, template_folder="view")
    app.config.from_object(LocalDevelopmentConfig)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lux'
    secret = secrets.token_urlsafe(32)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        add_dummy_admin()
        add_dummy_data()
        api = Api(app)
        app.secret_key = secret
        CORS(app, resources={r"/*": {"origins": "*"}})
        bootstrap = Bootstrap5(app)
        csrf = CSRFProtect(app)
        return app, api, bootstrap

app, api, bootstrap = setup_app()


with app.app_context():
    from controller.api.influencers_api import InfluencersAPI
    from controller.api.ad_request_api import AdRequestsAPI
    from controller.api.campaigns_api import CampaignsAPI
    from controller.api.sponsors_api import SponsorsAPI
    api.add_resource(InfluencersAPI, "/api/influencer", "/api/influencer/<influencer_id>")
    api.add_resource(SponsorsAPI, "/api/sponsor", "/api/sponsor/<sponsor_id>")
    api.add_resource(CampaignsAPI, "/api/campaign", "/api/campaign/<campaign_id>")
    api.add_resource(AdRequestsAPI, "/api/ad_request", "/api/ad_request/<ad_request_id>")
    from controller import *
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8099)
