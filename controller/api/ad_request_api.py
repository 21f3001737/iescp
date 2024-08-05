from flask_restful import Resource, marshal_with
from model.db import db, AdRequests
from controller.api.utils.marshal_formats import ad_request_output
from controller.api.utils.validation import NotFoundError, CreationError
from controller.api.utils.request_parser import create_ad_request_parser

class AdRequestsAPI(Resource):
    def delete(self, ad_request_id):
        ad_request = db.session.query(AdRequests).filter(AdRequests.id == ad_request_id).first()
        if ad_request:
            db.session.delete(ad_request)
            db.session.commit()
        else:
            raise NotFoundError(status_code=404, status_message="AdRequest not found")    

    @marshal_with(ad_request_output)
    def get(self, ad_request_id):
        ad_request = db.session.query(AdRequests).filter(AdRequests.id == ad_request_id).first()
        if ad_request:
            return ad_request
        else:
            raise NotFoundError(status_code=404, status_message="AdRequest not found")

    @marshal_with(ad_request_output)
    def post(self, ad_request_id):
        args = create_ad_request_parser.parse_args()
        campaign_id = args.get("campaign_id", int)
        influencer_id = args.get("influencer_id", int)
        messages = args.get("messages", str)
        requirements = args.get("requirements", str)
        payment_amount = args.get("payment_amount", float)
        status = args.get("status", int)

        if campaign_id is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Campaign ID is required", error_code= "ADC1001")
        elif influencer_id is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Influencer ID is required", error_code= "ADC1002")
        elif messages is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Messages is required", error_code= "ADC1003")
        elif requirements is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Requirements is required", error_code= "ADC1004")
        elif payment_amount is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Payment Amount is required", error_code= "ADC1005")
        elif status is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Status is required", error_code= "ADC1006")
        else:
            ad_request = AdRequests(campaign_id = campaign_id, influencer_id = influencer_id, messages = messages, requirements = requirements, payment_amount = payment_amount, status = status)
            db.session.add(ad_request)
            db.session.commit()
            return ad_request
        


        
        
    
        
 
