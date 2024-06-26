from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = None
Base = declarative_base()
db = SQLAlchemy()

class Sponsors(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    industry = db.Column(db.String)
    budget = db.Column(db.Numeric)

class Influencers(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    budget = db.Column(db.Numeric)

class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric)
    visibility = db.Column(db.Boolean)
    goals = db.Column(db.String)
    
class AdRequests(db.Model):
    __tablename__ = "ad_requests"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencers.id"), nullable=False)
    messages = db.Column(db.String)
    requirements = db.Column(db.String)
    payment_amount = db.Column(db.Numeric)
    status = db.Column(db.Integer)

    


