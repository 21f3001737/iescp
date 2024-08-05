from flask_restful import Resource, marshal_with
from model.db import db, Influencers
from controller.api.utils.marshal_formats import influencer_output
from controller.api.utils.validation import NotFoundError, CreationError
from controller.api.utils.request_parser import create_influencer_parser

class InfluencersAPI(Resource):
    def delete(self, influencer_id):
        influencer = db.session.query(Influencers).filter(Influencers.id == influencer_id).first()
        if influencer:
            db.session.delete(influencer)
            db.session.commit()
        else:
            raise NotFoundError(status_code=404, status_message="influencer not found")    

    @marshal_with(influencer_output)
    def get(self, influencer_id):
        influencer = db.session.query(Influencers).filter(Influencers.id == influencer_id).first()
        if influencer:
            return influencer
        else:
            raise NotFoundError(status_code=404, status_message="influencer not found")

    @marshal_with(influencer_output)
    def post(self):
        args = create_influencer_parser.parse_args()
        name = args.get("name", str)
        username = args.get("username", str)
        password = args.get("password", str)
        category = args.get("category", str)
        niche = args.get("niche", str)
        followers = args.get("followers", int)
        budget = args.get("budget", float)
        flag = args.get("flag", bool)

        if name is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Name is required", error_code= "IC1001")
        if username is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Username is required", error_code= "IC1002")
        elif category is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Category is required", error_code= "IC1003")
        elif niche is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Niche is required", error_code= "IC1004")
        elif followers is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Followers is required", error_code= "IC1005")
        elif budget is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Budget is required", error_code= "IC1006")
        elif flag is None:
            raise CreationError(status_code = 400, object_type = "influencer", status_message="Flag is required", error_code= "IC1007")
        else:
            influencer = Influencers(name=name, username= username, password = password, category = category, niche = niche, budget = budget, flag = flag, followers=followers)
            db.session.add(influencer)
            db.session.commit()
            return influencer
