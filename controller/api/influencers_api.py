from flask_restful import Resource, marshal_with
from model.db import db, Influencers
from controller.api.utils.marshal_formats import influencer_output
from controller.api.utils.validation import NotFoundError, CreationError
from controller.api.utils.request_parser import create_influencer_parser

class InfluencersAPI(Resource):
    def delete(self, influencer_id):
        influencer = db.session.query(influencers).filter(influencers.id == influencer_id).first()
        if influencer:
            db.session.delete(influencer)
            db.session.commit()
        else:
            raise NotFoundError(status_code=404, status_message="influencer not found")    

    @marshal_with(influencer_output)
    def get(self, influencer_id):
        influencer = db.session.query(influencers).filter(influencers.id == influencer_id).first()
        if influencer:
            return influencer
        else:
            raise NotFoundError(status_code=404, status_message="influencer not found")

    @marshal_with(influencer_output)
    def post(self, influencer_id):
        args = create_influencer_parser.parse_args()
        name = args.get("name", str)
        category = args.get("category", str)
        budget = args.get("budget", float)

        if name is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Name is required", error_code= "SC1001")
        elif category is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Category is required", error_code= "SC1002")
        elif budget is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Budget is required", error_code= "SC1003")
        else:
            influencer = Influencers(name=name, industry = industry, budget = budget)
            db.session.add(influencer)
            db.session.commit()
            return influencer
