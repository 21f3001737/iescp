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
        name = args.get("name", str)
        industry = args.get("industry", str)
        budget = args.get("budget", float)

        if name is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Name is required", error_code= "SC1001")
        elif industry is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Industry is required", error_code= "SC1002")
        elif budget is None:
            raise CreationError(status_code = 400, object_type = "AdRequest", status_message="Budget is required", error_code= "SC1003")
        else:
            ad_request = AdRequests(name=name, industry = industry, budget = budget)
            db.session.add(ad_request)
            db.session.commit()
            return ad_request
        


        
        
    
        
 
