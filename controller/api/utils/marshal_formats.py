from flask_restful import fields

sponsor_output = {
    "id": fields.Integer,
    "name": fields.String,
    "industry": fields.String,
    "budget": fields.Float,
}

influencer_output = {
    "id": fields.Integer,
    "name": fields.String,
    "category": fields.String,
    "budget": fields.Float,
}

campaign_output = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "start_date": fields.Date,
    "end_date": fields.Date,
    "budget": fields.Float,
    "visibility": fields.Boolean,
    "goals": fields.String,
}

ad_request_output = {
    "id": fields.Integer,
    "campaign_id": fields.Integer, 
    "influencer_id": fields.Integer,
    "messages": fields.String,
    "requirements": fields.String,
    "payment_amount": fields.Float,
    "status": fields.Integer,
}
