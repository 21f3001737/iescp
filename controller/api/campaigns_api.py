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
    def post(self, campaign_id):
        args = create_campaign_parser.parse_args()
        name = args.get("name", str)
        description = args.get("description",str)
        start_date = args.get("start_date",str)
        end_date = args.get("end_date",str)
        budget = args.get("budget",float)
        visibility = args.get("visibility",bool)
        goals = args.get("goals",str)

        if name is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="name is required", error ="CC1001") 
        elif description is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="description is required", error ="CC1002") 
        elif start_date is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="start_date is required", error ="CC1003") 
        elif end_date is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="end_date is required", error ="CC1004")
        elif budget is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="budget is required", error ="CC1005")
        elif visibility is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="visibility is required", error ="CC1006")
        elif goals is None:
            raise CreationError(status_code = 400, object_type = "campaign", status_message="goals is required", error ="CC1007")
        else:
            campaign = Campaigns(name=name, name = name,  description = description,  start_date = start_date,  end_date = end_date,  budget = budget,  visibility = visibility, goals = goals )
            db.session.add(campaign)
            db.session.commit()
            return campaign
