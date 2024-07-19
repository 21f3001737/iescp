from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = None
Base = declarative_base()
db = SQLAlchemy()

class Sponsors(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Numeric, nullable=False)

class Influencers(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username= db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    budget = db.Column(db.Numeric, nullable=False)

class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.id"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Numeric, nullable=False)
    visibility = db.Column(db.Boolean, nullable=False)
    goals = db.Column(db.String, nullable=False)
    
class AdRequests(db.Model):
    __tablename__ = "ad_requests"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencers.id"), nullable=False)
    messages = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    


