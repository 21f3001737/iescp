from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from typing import List

engine = None
Base = declarative_base()
db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Sponsors(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique = True)
    password = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Numeric(precision=10,scale=2), nullable=False)
    campaigns: db.Mapped["Campaigns"] = db.relationship(back_populates="sponsor", cascade="all, delete")

class Influencers(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username= db.Column(db.String, nullable=False, unique = True)
    password = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Numeric(precision=10,scale=2), nullable=False)
    ad_requests: db.Mapped["AdRequests"] = db.relationship(back_populates="influencer", cascade="all, delete")

class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.id"))
    sponsor: db.Mapped["Sponsors"] = db.relationship(back_populates="campaigns")
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Numeric(precision=10,scale=2), nullable=False)
    visibility = db.Column(db.Boolean, nullable=False)
    goals = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    ad_requests: db.Mapped[List["AdRequests"]] = db.relationship(back_populates="campaign", cascade="all, delete")
    
class AdRequests(db.Model):
    __tablename__ = "ad_requests"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    campaign: db.Mapped["Campaigns"] = db.relationship(back_populates="ad_requests")
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencers.id"), nullable=False)
    influencer: db.Mapped["Influencers"] = db.relationship(back_populates="ad_requests")
    messages = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Numeric(precision=10,scale=2), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    


