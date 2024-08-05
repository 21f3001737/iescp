from flask_restful import fields

sponsor_output = {
    "id": fields.Integer,
    "name": fields.String,
    "username": fields.String,
    "password": fields.String,
    "industry": fields.String,
    "budget": fields.Float,
    "flag": fields.Boolean
}

influencer_output = {
    "id": fields.Integer,
    "name": fields.String,
    "username": fields.String,
    "password": fields.String,
    "category": fields.String,
    "niche": fields.String,
    "followers": fields.Integer,
    "budget": fields.Float,
    "flag": fields.Boolean
}

campaign_output = {
    "id": fields.Integer,
    "sponsor_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "start_date": fields.DateTime,
    "end_date": fields.DateTime,
    "budget": fields.Float,
    "visibility": fields.Boolean,
    "goals": fields.String,
    "niche": fields.String,
    "flag": fields.Boolean
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
