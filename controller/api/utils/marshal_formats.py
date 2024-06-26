from flask_restful import fields

sponsor_output = {
    "id": fields.Integer,
    "name": fields.String,
    "industry": fields.String,
    "budget": fields.Float,
}

influencers_output = {
    "id": fields.Integer,
    "name": fields.String,
    "category": fields.String,
    "budget": fields.Float,
}
