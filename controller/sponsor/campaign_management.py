from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
        render_template
    )
from model.db import db, Sponsors, Campaigns, AdRequests, Influencers
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    validators, 
    PasswordField, 
    SubmitField, 
    RadioField, 
    IntegerField,
    DecimalField,
    DateField,
    BooleanField,
)
@app.route("/sponsor/campaign/delete/<campaign_id>")
def sponsor_delete_campaign(campaign_id):
    campaign = Campaigns.query.filter(Campaigns.id == campaign_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and campaign and campaign.sponsor_id == session["user"]["id"]:
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for("sponsor_dashboard"))
    else:
        return redirect(url_for("login"))
    
@app.route("/sponsor/campaign/edit/<campaign_id>")
def sponsor_edit_campaign(campaign_id):
    campaign = Campaigns.query.filter(Campaigns.id == campaign_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and campaign and campaign.sponsor_id == session["user"]["id"]:
        pass
    else:
        return redirect(url_for("login"))
    
