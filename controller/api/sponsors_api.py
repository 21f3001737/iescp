from flask_restful import Resource, marshal_with
from model.db import db, Sponsors
from controller.api.utils.marshal_formats import sponsor_output
from controller.api.utils.validation import NotFoundError, CreationError
from controller.api.utils.request_parser import create_sponsor_parser

class SponsorsAPI(Resource):
    def delete(self, sponsor_id):
        sponsor = db.session.query(Sponsors).filter(Sponsors.id == sponsor_id).first()
        if sponsor:
            db.session.delete(sponsor)
            db.session.commit()
        else:
            raise NotFoundError(status_code=404, status_message="Sponsor not found")    

    @marshal_with(sponsor_output)
    def get(self, sponsor_id):
        sponsor = db.session.query(Sponsors).filter(Sponsors.id == sponsor_id).first()
        if sponsor:
            return sponsor
        else:
            raise NotFoundError(status_code=404, status_message="Sponsor not found")

    @marshal_with(sponsor_output)
    def post(self, sponsor_id):
        args = create_sponsor_parser.parse_args()
        name = args.get("name", str)
        industry = args.get("industry", str)
        budget = args.get("budget", float)

        if name is None:
            raise CreationError(status_code = 400, object_type = "Sponsor", status_message="Name is required", error_code= "SC1001")
        elif industry is None:
            raise CreationError(status_code = 400, object_type = "Sponsor", status_message="Industry is required", error_code= "SC1002")
        elif budget is None:
            raise CreationError(status_code = 400, object_type = "Sponsor", status_message="Budget is required", error_code= "SC1003")
        else:
            sponsor = Sponsors(name=name, industry = industry, budget = budget)
            db.session.add(sponsor)
            db.session.commit()
            return sponsor
        


        
        
    
        
            
