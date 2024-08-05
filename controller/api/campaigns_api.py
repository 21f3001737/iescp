from flask_restful import Resource, marshal_with
from model.db import db, Campaigns
from controller.api.utils.marshal_formats import campaign_output
from controller.api.utils.validation import NotFoundError, CreationError
from controller.api.utils.request_parser import create_campaign_parser

class CampaignsAPI(Resource):
    def delete(self, campaign_id):
        campaign = db.session.query(Campaigns).filter(Campaigns.id == campaign_id).first()
        if campaign:
            db.session.delete(campaign)
            db.session.commit()
        else:
            raise NotFoundError(status_code=404, status_message="campaign not found")    

    @marshal_with(campaign_output)
    def get(self, campaign_id):
        campaign = db.session.query(Campaigns).filter(Campaigns.id == campaign_id).first()
        if campaign:
            return campaign
        else:
            raise NotFoundError(status_code=404, status_message="campaign not found")

    @marshal_with(campaign_output)
    def post(self):
        args = create_campaign_parser.parse_args()
        sponsor_id = args.get("sponsor_id", int)
        name = args.get("name", str)
        description = args.get("description",str)
        start_date = args.get("start_date",str)
        end_date = args.get("end_date",str)
        budget = args.get("budget",float)
        visibility = args.get("visibility",bool)
        goals = args.get("goals",str)
        niche = args.get("niche", str)
        flag = args.get("flag", bool)

        if sponsor_id is None:
            raise CreationError(status_code= 400, object_type= "campaign", status_message="sponsor_id is required", error_code="CC1000")
        if name is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="name is required", error_code="CC1001") 
        elif description is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="description is required", error_code="CC1002") 
        elif start_date is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="start_date is required", error_code="CC1003") 
        elif end_date is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="end_date is required", error_code="CC1004")
        elif budget is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="budget is required", error_code="CC1005")
        elif visibility is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="visibility is required", error_code="CC1006")
        elif goals is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="goals is required", error_code="CC1007")
        elif niche is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="niche is required", error_code="CC1008")
        elif flag is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="flag is required", error_code="CC1009")
        else:
            campaign = Campaigns(sponsor_id=sponsor_id, name=name,  description = description,  start_date = start_date,  end_date = end_date,  budget = budget,  visibility = visibility, goals = goals, niche = niche, flag = flag )
            db.session.add(campaign)
            db.session.commit()
            return campaign
